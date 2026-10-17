from pathlib import Path

import pytest

from engine.bank import QuestionLoader
from engine.info import InfoCatalog
from engine.question import QuestionValidator

SAMPLE_BANK = Path(__file__).parents[1] / "bank" / "astrofisica.json"
INFO_FILE = Path(__file__).parents[1] / "messages" / "info.json"


@pytest.fixture
def sample_bank_path() -> Path:
    return SAMPLE_BANK


@pytest.fixture
def catalog() -> InfoCatalog:
    return InfoCatalog(INFO_FILE)


@pytest.fixture
def validator(catalog: InfoCatalog) -> QuestionValidator:
    return QuestionValidator(catalog)


@pytest.fixture
def loader(validator: QuestionValidator, catalog: InfoCatalog) -> QuestionLoader:
    return QuestionLoader(validator, catalog)


@pytest.fixture
def sample_questions(loader: QuestionLoader, sample_bank_path: Path):
    return loader.load(sample_bank_path)
