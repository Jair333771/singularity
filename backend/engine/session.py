from dataclasses import dataclass, field

from engine.question import Question


@dataclass
class SessionState:
    current_level: int = 1
    pending_ids: list[str] = field(default_factory=list)
    status: str = "in_progress"


def new_session(questions: list[Question]) -> SessionState:
    level_one = [q.id for q in questions if q.level == 1 and q.status == "reviewed"]
    return SessionState(current_level=1, pending_ids=level_one, status="in_progress")
