import random
from dataclasses import dataclass, field, replace

from engine.question import Question


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
        level_one = [q.id for q in questions if q.level == 1 and q.status == "reviewed"]
        return SessionState(current_level=1, pending_ids=level_one, status="in_progress")

    def next_id(self, state: SessionState) -> str:
        return self._rng.choice(state.pending_ids)

    def answer(self, state: SessionState, question: Question, chosen_index: int) -> AnswerResult:
        if question.id not in state.pending_ids:
            raise ValueError(f"{question.id}: not pending in current level")
        correct = chosen_index == question.correct_index
        pending_ids = list(state.pending_ids)
        if correct:
            pending_ids.remove(question.id)
        next_state = replace(state, pending_ids=pending_ids)
        return AnswerResult(correct=correct, explanation=question.explanation, next_state=next_state)
