"""Identificadores de mensajes y contrato del catálogo que los resuelve."""

from enum import Enum
from typing import Protocol

__all__ = ["Info", "MessageCatalog"]


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


class MessageCatalog(Protocol):
    """Resuelve un Info a texto con sus parámetros sustituidos."""

    def text(self, info: Info, **params: object) -> str: ...
