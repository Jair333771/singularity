import json
from pathlib import Path

from engine.question import Question, QuestionValidator


class QuestionLoader:
    def __init__(self, validator: QuestionValidator) -> None:
        self._validator = validator

    def load(self, path: Path) -> list[Question]:
        with open(path, encoding="utf-8") as file:
            raw_questions = json.load(file)
        questions = []
        for raw in raw_questions:
            try:
                question = Question(**raw)
            except TypeError as error:
                raise ValueError(f"{raw.get('id', '?')}: {error}") from error
            self._validator.validate(question)
            questions.append(question)
        return questions
