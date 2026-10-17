import json
from pathlib import Path

import pytest

from engine.bank import load_bank

SAMPLE_BANK = Path(__file__).parents[1] / "bank" / "astrofisica.json"


def test_sample_bank_loads_70_questions():
    assert len(load_bank(SAMPLE_BANK)) == 70


def test_invalid_question_error_names_id(tmp_path):
    bank = tmp_path / "bank.json"
    bank.write_text(
        json.dumps([{"id": "ast-bad", "level": 1, "topic": "astrofisica", "text": "?",
                     "options": ["a", "b"], "correct_index": 0, "explanation": "",
                     "status": "draft"}]),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="ast-bad"):
        load_bank(bank)


def test_missing_field_error_names_id(tmp_path):
    bank = tmp_path / "bank.json"
    bank.write_text(json.dumps([{"id": "ast-short", "level": 1}]), encoding="utf-8")
    with pytest.raises(ValueError, match="ast-short"):
        load_bank(bank)
