"""Motor de sesión: selección de preguntas, registro de respuestas y avance de nivel."""

import random
from dataclasses import replace

from app.domain.errors import DomainError
from app.domain.messages import Info, MessageCatalog
from app.domain.question import MAX_LEVEL, QUESTIONS_PER_LEVEL, REVIEWED, Question
from app.domain.session import (
    GAME_COMPLETED,
    IN_PROGRESS,
    LEVEL_COMPLETED,
    AnswerResult,
    SessionState,
)

__all__ = ["SessionEngine"]


class SessionEngine:
    """Motor sin estado propio: recibe y devuelve SessionState."""

    def __init__(self, rng: random.Random, catalog: MessageCatalog) -> None:
        self._rng = rng
        self._catalog = catalog

    def start(self, questions: list[Question]) -> SessionState:
        """Valida la cobertura de los 10 niveles y devuelve el estado del nivel 1."""
        for level in range(1, MAX_LEVEL + 1):
            found = len(self._reviewed_ids(questions, level))
            if found != QUESTIONS_PER_LEVEL:
                raise DomainError(
                    self._catalog.text(
                        Info.LEVEL_COVERAGE_MISMATCH,
                        level=level,
                        expected=QUESTIONS_PER_LEVEL,
                        found=found,
                    )
                )
        return SessionState(
            current_level=1,
            pending_ids=self._reviewed_ids(questions, 1),
            status=IN_PROGRESS,
        )

    def advance(self, state: SessionState, questions: list[Question]) -> SessionState:
        """Pasa al siguiente nivel; solo válido con el nivel actual completado."""
        if state.status != LEVEL_COMPLETED:
            raise DomainError(
                self._catalog.text(Info.LEVEL_NOT_COMPLETED, level=state.current_level)
            )
        level = state.current_level + 1
        return SessionState(
            current_level=level,
            pending_ids=self._reviewed_ids(questions, level),
            status=IN_PROGRESS,
        )

    def next_id(self, state: SessionState) -> str:
        """Elige al azar una id pendiente del nivel actual."""
        return self._rng.choice(state.pending_ids)

    def answer(
        self, state: SessionState, question: Question, chosen_index: int
    ) -> AnswerResult:
        """Registra la respuesta; solo una correcta quita la id de pendientes."""
        if question.id not in state.pending_ids:
            raise DomainError(
                self._catalog.text(Info.QUESTION_NOT_PENDING, id=question.id)
            )
        correct = chosen_index == question.correct_index
        pending_ids = list(state.pending_ids)
        if correct:
            pending_ids.remove(question.id)
        status = state.status
        if not pending_ids:
            status = self._completion_status(state.current_level)
        next_state = replace(state, pending_ids=pending_ids, status=status)
        return AnswerResult(
            correct=correct,
            explanation=question.explanation,
            next_state=next_state,
        )

    def _completion_status(self, level: int) -> str:
        return GAME_COMPLETED if level == MAX_LEVEL else LEVEL_COMPLETED

    def _reviewed_ids(self, questions: list[Question], level: int) -> list[str]:
        return [q.id for q in questions if q.level == level and q.status == REVIEWED]
