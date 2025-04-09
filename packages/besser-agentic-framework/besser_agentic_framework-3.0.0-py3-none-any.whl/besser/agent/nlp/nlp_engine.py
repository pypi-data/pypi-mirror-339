import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Hide Tensorflow logs

from typing import Any, TYPE_CHECKING

from besser.agent import nlp
from besser.agent.core.property import Property
from besser.agent.core.session import Session
from besser.agent.exceptions.logger import logger
from besser.agent.nlp.intent_classifier.intent_classifier import IntentClassifier
from besser.agent.nlp.intent_classifier.intent_classifier_configuration import LLMIntentClassifierConfiguration, \
    SimpleIntentClassifierConfiguration
from besser.agent.nlp.intent_classifier.intent_classifier_prediction import IntentClassifierPrediction, \
    fallback_intent_prediction
from besser.agent.nlp.intent_classifier.llm_intent_classifier import LLMIntentClassifier
from besser.agent.nlp.intent_classifier.simple_intent_classifier_pytorch import SimpleIntentClassifierTorch
from besser.agent.nlp.intent_classifier.simple_intent_classifier_tensorflow import SimpleIntentClassifierTF
from besser.agent.nlp.llm.llm import LLM
from besser.agent.nlp.ner.ner import NER
from besser.agent.nlp.ner.simple_ner import SimpleNER
from besser.agent.nlp.preprocessing.pipelines import lang_map
from besser.agent.nlp.rag.rag import RAG
from besser.agent.nlp.speech2text.hf_speech2text import HFSpeech2Text
from besser.agent.nlp.speech2text.api_speech2text import APISpeech2Text
from besser.agent.nlp.speech2text.speech2text import Speech2Text

if TYPE_CHECKING:
    from besser.agent.core.agent import Agent
    from besser.agent.core.state import State


class NLPEngine:
    """The NLP Engine of an agent.

    It is in charge of running different Natural Language Processing tasks required by the agent.

    Args:
        agent (Agent): the agent the NLPEngine belongs to

    Attributes:
        _agent (Agent): The agent the NLPEngine belongs to
        _llms (dict[str, LLM]): The LLMs of the NLPEngine. Keys are the names and values are the LLMs themselves.
        _intent_classifiers (dict[State, IntentClassifier]): The collection of Intent Classifiers of the NLPEngine.
            There is one for each agent state (only states with transitions triggered by intent matching)
        _ner (NER or None): The NER (Named Entity Recognition) system of the NLPEngine
        _speech2text (Speech2Text or None): The Speech-to-Text System of the NLPEngine
    """

    def __init__(self, agent: 'Agent'):
        self._agent: 'Agent' = agent
        self._llms: dict[str, LLM] = {}
        self._intent_classifiers: dict['State', IntentClassifier] = {}
        self._ner: NER or None = None
        self._speech2text: Speech2Text or None = None
        self._rag: RAG = None

    @property
    def ner(self):
        """NER: NLPEngine NER component."""
        return self._ner

    def initialize(self) -> None:
        """Initialize the NLPEngine."""
        if self.get_property(nlp.NLP_LANGUAGE) in lang_map.values():
            # Set the language to ISO 639-1 format (e.g., 'english' => 'en')
            self._agent.set_property(
                nlp.NLP_LANGUAGE,
                list(lang_map.keys())[list(lang_map.values()).index(self.get_property(nlp.NLP_LANGUAGE))]
            )
        for llm_name, llm in self._llms.items():
            self._llms[llm_name].initialize()
        for state in self._agent.states:
            if state not in self._intent_classifiers and state.intents:
                if isinstance(state.ic_config, SimpleIntentClassifierConfiguration):
                    if state.ic_config.framework == 'pytorch':
                        self._intent_classifiers[state] = SimpleIntentClassifierTorch(self, state)
                    elif state.ic_config.framework == 'tensorflow':
                        self._intent_classifiers[state] = SimpleIntentClassifierTF(self, state)
                elif isinstance(state.ic_config, LLMIntentClassifierConfiguration):
                    self._intent_classifiers[state] = LLMIntentClassifier(self, state)
        # TODO: Only instantiate the NER if asked (maybe an agent does not need NER), via agent properties
        self._ner = SimpleNER(self, self._agent)
        if self.get_property(nlp.NLP_STT_HF_MODEL):
            self._speech2text = HFSpeech2Text(self)
        elif self.get_property(nlp.NLP_STT_SR_ENGINE):
            self._speech2text = APISpeech2Text(self)

    def get_property(self, prop: Property) -> Any:
        """Get a NLP property's value from the NLPEngine's agent.

        Args:
            prop (Property): the property to get its value

        Returns:
            Any: the property value, or None if the property is not an NLP property
        """
        if prop.section != nlp.SECTION_NLP:
            return None
        return self._agent.get_property(prop)

    def train(self) -> None:
        """Train the NLP components of the NLPEngine."""
        self._ner.train()
        logger.info(f"NER successfully trained.")
        for state, intent_classifier in self._intent_classifiers.items():
            if not state.intents:
                logger.info(f"Intent classifier in {state.name} not trained (no intents found).")
            else:
                intent_classifier.train()
                logger.info(f"Intent classifier in {state.name} successfully trained.")

    def predict_intent(self, session: Session) -> IntentClassifierPrediction:
        """Predict the intent of a user message.

        Args:
            session (Session): the user session

        Returns:
            IntentClassifierPrediction: the intent prediction
        """
        message: str = session.event.message
        fallback_intent = fallback_intent_prediction(message)
        if not session.current_state.intents:
            return fallback_intent
        intent_classifier = self._intent_classifiers[session.current_state]
        # TODO: check if state is different to run prediction
        intent_classifier_predictions: list[IntentClassifierPrediction] = intent_classifier.predict(message)
        best_intent_prediction = self.get_best_intent_prediction(intent_classifier_predictions)
        if best_intent_prediction is None:
            best_intent_prediction = fallback_intent
        best_intent_prediction.state = session.current_state.name
        return best_intent_prediction

    def get_best_intent_prediction(
            self,
            intent_classifier_predictions: list[IntentClassifierPrediction]
    ) -> IntentClassifierPrediction or None:
        """Get the best intent prediction out of a list of intent predictions. If none of the predictions is well
        enough to be considered, return nothing.

        Args:
            intent_classifier_predictions (list[IntentClassifierPrediction]):

        Returns:
            IntentClassifierPrediction or None: the best intent prediction or None if no intent prediction is well
                enough
        """
        best_intent_prediction: IntentClassifierPrediction
        if not intent_classifier_predictions:
            return None
        best_intent_prediction = intent_classifier_predictions[0]
        for intent_prediction in intent_classifier_predictions[1:]:
            if intent_prediction.score > best_intent_prediction.score:
                best_intent_prediction = intent_prediction
        intent_threshold: float = self.get_property(nlp.NLP_INTENT_THRESHOLD)
        if best_intent_prediction.score < intent_threshold:
            return None
        return best_intent_prediction

    def speech2text(self, speech: bytes):
        """Transcribe a voice audio into its corresponding text representation.

        Args:
            speech (bytes): the recorded voice that wants to be transcribed

        Returns:
            str: the speech transcription
        """
        text = self._speech2text.speech2text(speech)
        logger.info(f"[Speech2Text] Transcribed audio message: '{text}'")
        return text
