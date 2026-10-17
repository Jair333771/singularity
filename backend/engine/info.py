import json
from enum import Enum
from pathlib import Path


class Info(Enum):
    QUESTION_FIELDS_INVALID = "QUESTION_FIELDS_INVALID"
    QUESTION_STATUS_NOT_REVIEWED = "QUESTION_STATUS_NOT_REVIEWED"
    QUESTION_TOPIC_UNKNOWN = "QUESTION_TOPIC_UNKNOWN"
    QUESTION_LEVEL_OUT_OF_RANGE = "QUESTION_LEVEL_OUT_OF_RANGE"
    QUESTION_OPTIONS_COUNT = "QUESTION_OPTIONS_COUNT"
    QUESTION_CORRECT_INDEX_OUT_OF_RANGE = "QUESTION_CORRECT_INDEX_OUT_OF_RANGE"
    QUESTION_NOT_PENDING = "QUESTION_NOT_PENDING"
    LEVEL_NOT_COMPLETED = "LEVEL_NOT_COMPLETED"
    LEVEL_COVERAGE_MISMATCH = "LEVEL_COVERAGE_MISMATCH"


class InfoCatalog:
    def __init__(self, path: Path) -> None:
        raw = json.loads(path.read_text(encoding="utf-8"))
        self._messages = {Info[key]: text for key, text in raw.items()}
        missing = [info.name for info in Info if info not in self._messages]
        if missing:
            raise ValueError(f"info file missing keys: {', '.join(missing)}")

    def text(self, info: Info, **params: object) -> str:
        return self._messages[info].format(**params)
