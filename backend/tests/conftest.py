from pathlib import Path

import pytest

from engine.bank import QuestionLoader
from engine.question import QuestionValidator

SAMPLE_BANK = Path(__file__).parents[1] / "bank" / "astrofisica.json"


@pytest.fixture
def sample_bank_path() -> Path:
    return SAMPLE_BANK


@pytest.fixture
def validator() -> QuestionValidator:
    return QuestionValidator()


@pytest.fixture
def loader(validator: QuestionValidator) -> QuestionLoader:
    return QuestionLoader(validator)


@pytest.fixture
def sample_questions(loader: QuestionLoader, sample_bank_path: Path):
    return loader.load(sample_bank_path)
