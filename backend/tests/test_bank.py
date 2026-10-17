import pytest

from app.infrastructure.question_bank import QuestionLoader


def test_sample_bank_loads_70_questions(loader: QuestionLoader, raw_bank: list) -> None:
    assert len(loader.load(raw_bank)) == 70


def test_invalid_question_error_names_id(loader: QuestionLoader) -> None:
    raw = [
        {
            "id": "ast-bad",
            "level": 1,
            "topic": "astrofisica",
            "text": "?",
            "options": ["a", "b"],
            "correct_index": 0,
            "explanation": "",
            "status": "draft",
        }
    ]
    with pytest.raises(ValueError, match="ast-bad"):
        loader.load(raw)


def test_missing_field_error_names_id(loader: QuestionLoader) -> None:
    with pytest.raises(ValueError, match="ast-short"):
        loader.load([{"id": "ast-short", "level": 1}])
