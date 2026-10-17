import random
from dataclasses import dataclass, field, replace

from engine.question import MAX_LEVEL, Question


@dataclass
class SessionState:
    current_level: int = 1
    pending_ids: list[str] = field(default_factory=list)
    status: str = "in_progress"


@dataclass
class AnswerResult:
    correct: bool
    explanation: str
    next_state: SessionState


class SessionEngine:
    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def start(self, questions: list[Question]) -> SessionState:
        return SessionState(current_level=1, pending_ids=self._reviewed_ids(questions, 1), status="in_progress")

    def advance(self, state: SessionState, questions: list[Question]) -> SessionState:
        if state.status != "level_completed":
            raise ValueError(f"level {state.current_level}: not completed")
        level = state.current_level + 1
        return SessionState(current_level=level, pending_ids=self._reviewed_ids(questions, level), status="in_progress")

    def next_id(self, state: SessionState) -> str:
        return self._rng.choice(state.pending_ids)

    def answer(self, state: SessionState, question: Question, chosen_index: int) -> AnswerResult:
        if question.id not in state.pending_ids:
            raise ValueError(f"{question.id}: not pending in current level")
        correct = chosen_index == question.correct_index
        pending_ids = list(state.pending_ids)
        if correct:
            pending_ids.remove(question.id)
        status = state.status
        if not pending_ids:
            status = "game_completed" if state.current_level == MAX_LEVEL else "level_completed"
        next_state = replace(state, pending_ids=pending_ids, status=status)
        return AnswerResult(correct=correct, explanation=question.explanation, next_state=next_state)

    def _reviewed_ids(self, questions: list[Question], level: int) -> list[str]:
        return [q.id for q in questions if q.level == level and q.status == "reviewed"]
