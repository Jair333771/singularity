"""Estado de sesión y resultado de una respuesta."""

from dataclasses import dataclass, field

__all__ = [
    "GAME_COMPLETED",
    "IN_PROGRESS",
    "LEVEL_COMPLETED",
    "AnswerResult",
    "SessionState",
]

IN_PROGRESS = "in_progress"
LEVEL_COMPLETED = "level_completed"
GAME_COMPLETED = "game_completed"


@dataclass
class SessionState:
    current_level: int = 1
    pending_ids: list[str] = field(default_factory=list)
    status: str = IN_PROGRESS


@dataclass
class AnswerResult:
    correct: bool
    explanation: str
    next_state: SessionState
