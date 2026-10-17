from dataclasses import dataclass

TOPICS = ("astrofisica", "fisica", "matematicas")
MIN_OPTIONS = 2
MAX_OPTIONS = 4
MIN_LEVEL = 1
MAX_LEVEL = 10


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
    def validate(self, question: Question) -> None:
        if question.status != "reviewed":
            raise ValueError(f"{question.id}: status must be 'reviewed', got '{question.status}'")
        if question.topic not in TOPICS:
            raise ValueError(f"{question.id}: unknown topic '{question.topic}'")
        if not MIN_LEVEL <= question.level <= MAX_LEVEL:
            raise ValueError(f"{question.id}: level {question.level} out of range")
        if not MIN_OPTIONS <= len(question.options) <= MAX_OPTIONS:
            raise ValueError(f"{question.id}: must have {MIN_OPTIONS} to {MAX_OPTIONS} options")
        if not 0 <= question.correct_index < len(question.options):
            raise ValueError(f"{question.id}: correct_index {question.correct_index} out of range")
