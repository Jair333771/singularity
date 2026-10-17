from typing import Any

import pytest

from app.domain.question import Question, QuestionValidator
from app.infrastructure.messages import InfoCatalog
from app.infrastructure.question_bank import QuestionLoader
from app.utils import bank, messages


@pytest.fixture
def raw_bank() -> list[dict[str, Any]]:
    return bank.astrofisica


@pytest.fixture
def catalog() -> InfoCatalog:
    return InfoCatalog(messages.info)


@pytest.fixture
def validator(catalog: InfoCatalog) -> QuestionValidator:
    return QuestionValidator(catalog)


@pytest.fixture
def loader(validator: QuestionValidator, catalog: InfoCatalog) -> QuestionLoader:
    return QuestionLoader(validator, catalog)


@pytest.fixture
def sample_questions(
    loader: QuestionLoader, raw_bank: list[dict[str, Any]]
) -> list[Question]:
    return loader.load(raw_bank)
