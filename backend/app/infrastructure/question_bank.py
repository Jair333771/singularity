"""Construcción de preguntas validadas desde su forma cruda."""

from typing import Any

from app.domain.errors import DomainError
from app.domain.messages import Info, MessageCatalog
from app.domain.question import Question, QuestionValidator

__all__ = ["QuestionLoader"]


class QuestionLoader:
    """Convierte un banco crudo en preguntas y solo devuelve las validadas."""

    def __init__(self, validator: QuestionValidator, catalog: MessageCatalog) -> None:
        self._validator = validator
        self._catalog = catalog

    def load(self, raw_questions: list[dict[str, Any]]) -> list[Question]:
        """Lanza DomainError con el id de la primera pregunta inválida."""
        questions: list[Question] = []
        for raw in raw_questions:
            try:
                question = Question(**raw)
            except TypeError as error:
                message = self._catalog.text(
                    Info.QUESTION_FIELDS_INVALID,
                    id=raw.get("id", "?"),
                    detail=error,
                )
                raise DomainError(message) from error
            self._validator.validate(question)
            questions.append(question)
        return questions
