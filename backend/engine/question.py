from dataclasses import dataclass

from engine.info import Info, InfoCatalog

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
    def __init__(self, catalog: InfoCatalog) -> None:
        self._catalog = catalog

    def validate(self, question: Question) -> None:
        if question.status != "reviewed":
            raise ValueError(self._catalog.text(Info.QUESTION_STATUS_NOT_REVIEWED, id=question.id, status=question.status))
        if question.topic not in TOPICS:
            raise ValueError(self._catalog.text(Info.QUESTION_TOPIC_UNKNOWN, id=question.id, topic=question.topic))
        if not MIN_LEVEL <= question.level <= MAX_LEVEL:
            raise ValueError(self._catalog.text(Info.QUESTION_LEVEL_OUT_OF_RANGE, id=question.id, level=question.level))
        if not MIN_OPTIONS <= len(question.options) <= MAX_OPTIONS:
            raise ValueError(self._catalog.text(Info.QUESTION_OPTIONS_COUNT, id=question.id, min=MIN_OPTIONS, max=MAX_OPTIONS))
        if not 0 <= question.correct_index < len(question.options):
            raise ValueError(self._catalog.text(Info.QUESTION_CORRECT_INDEX_OUT_OF_RANGE, id=question.id, index=question.correct_index))
