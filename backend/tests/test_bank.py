import json
from pathlib import Path

import pytest

from engine.bank import QuestionLoader


def test_sample_bank_loads_70_questions(loader: QuestionLoader, sample_bank_path: Path):
    assert len(loader.load(sample_bank_path)) == 70


def test_invalid_question_error_names_id(loader: QuestionLoader, tmp_path):
    bank = tmp_path / "bank.json"
    bank.write_text(
        json.dumps([{"id": "ast-bad", "level": 1, "topic": "astrofisica", "text": "?",
                     "options": ["a", "b"], "correct_index": 0, "explanation": "",
                     "status": "draft"}]),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="ast-bad"):
        loader.load(bank)


def test_missing_field_error_names_id(loader: QuestionLoader, tmp_path):
    bank = tmp_path / "bank.json"
    bank.write_text(json.dumps([{"id": "ast-short", "level": 1}]), encoding="utf-8")
    with pytest.raises(ValueError, match="ast-short"):
        loader.load(bank)
