from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional

from ..schemas.models import BotIntent, Message


@dataclass
class ClassificationResult:
    intent_id: Optional[str]
    confidence: float


class SimpleNLPEngine:
    """Classificador de intents baseado em correspondência de palavras-chave."""

    def __init__(self, intents: Iterable[BotIntent]):
        self._intents = list(intents)

    def classify(self, message: Message) -> ClassificationResult:
        body_lower = message.body.lower()
        best_score = 0.0
        best_intent: Optional[BotIntent] = None
        for intent in self._intents:
            score = sum(1 for sample in intent.samples if sample.lower() in body_lower)
            normalized = score / max(len(intent.samples), 1)
            if normalized > best_score:
                best_score = normalized
                best_intent = intent
        if best_intent and best_score >= best_intent.confidence_threshold:
            return ClassificationResult(intent_id=best_intent.id, confidence=best_score)
        return ClassificationResult(intent_id=None, confidence=best_score)


class BotOrchestrator:
    """Coordenador de automação para determinar fallback e próximos passos."""

    def __init__(self, intents: Iterable[BotIntent]):
        self.engine = SimpleNLPEngine(intents)

    def handle_message(self, message: Message) -> dict:
        classification = self.engine.classify(message)
        should_fallback = classification.intent_id is None or classification.confidence < 0.5
        return {
            "intent_id": classification.intent_id,
            "confidence": classification.confidence,
            "fallback_to_human": should_fallback,
        }
