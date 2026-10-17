"""Modelo de pregunta y validación de sus campos."""

from dataclasses import dataclass
from typing import NoReturn

from app.domain.errors import DomainError
from app.domain.messages import Info, MessageCatalog

__all__ = ["MAX_LEVEL", "QUESTIONS_PER_LEVEL", "Question", "QuestionValidator"]

REVIEWED = "reviewed"
TOPICS = ("astrofisica", "fisica", "matematicas")
MIN_OPTIONS = 2
MAX_OPTIONS = 4
MIN_LEVEL = 1
MAX_LEVEL = 10
QUESTIONS_PER_LEVEL = 7


@dataclass
class Question:
    id: str
    level: int
    topic: str
    text: str
    options: list[str]
    correct_index: int
    explanation: str
    status: str


class QuestionValidator:
    """Valida que una pregunta sea usable por el motor."""

    def __init__(self, catalog: MessageCatalog) -> None:
        self._catalog = catalog

    def validate(self, question: Question) -> None:
        """Lanza DomainError con el id de la pregunta si algún campo es inválido."""
        if question.status != REVIEWED:
            self._reject(
                Info.QUESTION_STATUS_NOT_REVIEWED,
                id=question.id,
                status=question.status,
            )
        if question.topic not in TOPICS:
            self._reject(
                Info.QUESTION_TOPIC_UNKNOWN, id=question.id, topic=question.topic
            )
        if not MIN_LEVEL <= question.level <= MAX_LEVEL:
            self._reject(
                Info.QUESTION_LEVEL_OUT_OF_RANGE, id=question.id, level=question.level
            )
        if not MIN_OPTIONS <= len(question.options) <= MAX_OPTIONS:
            self._reject(
                Info.QUESTION_OPTIONS_COUNT,
                id=question.id,
                min=MIN_OPTIONS,
                max=MAX_OPTIONS,
            )
        if not 0 <= question.correct_index < len(question.options):
            self._reject(
                Info.QUESTION_CORRECT_INDEX_OUT_OF_RANGE,
                id=question.id,
                index=question.correct_index,
            )

    def _reject(self, info: Info, **params: object) -> NoReturn:
        raise DomainError(self._catalog.text(info, **params))
