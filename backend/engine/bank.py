import json
from pathlib import Path

from engine.info import Info, InfoCatalog
from engine.question import Question, QuestionValidator


class QuestionLoader:
    def __init__(self, validator: QuestionValidator, catalog: InfoCatalog) -> None:
        self._validator = validator
        self._catalog = catalog

    def load(self, path: Path) -> list[Question]:
        with open(path, encoding="utf-8") as file:
            raw_questions = json.load(file)
        questions = []
        for raw in raw_questions:
            try:
                question = Question(**raw)
            except TypeError as error:
                message = self._catalog.text(Info.QUESTION_FIELDS_INVALID, id=raw.get("id", "?"), detail=error)
                raise ValueError(message) from error
            self._validator.validate(question)
            questions.append(question)
        return questions
