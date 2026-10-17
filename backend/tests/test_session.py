from pathlib import Path

from engine.bank import load_bank
from engine.session import new_session

SAMPLE_BANK = Path(__file__).parents[1] / "bank" / "astrofisica.json"


def test_new_session_starts_at_level_one():
    state = new_session(load_bank(SAMPLE_BANK))
    assert state.current_level == 1
    assert state.status == "in_progress"


def test_new_session_pending_ids_are_level_one_questions():
    questions = load_bank(SAMPLE_BANK)
    state = new_session(questions)
    expected = [q.id for q in questions if q.level == 1]
    assert state.pending_ids == expected
    assert len(state.pending_ids) == 7
