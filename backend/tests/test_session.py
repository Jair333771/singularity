import random
from pathlib import Path

from engine.bank import load_bank
from engine.session import new_session, select_next_id

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


def test_selected_id_is_pending():
    state = new_session(load_bank(SAMPLE_BANK))
    assert select_next_id(state, random.Random(1)) in state.pending_ids


def test_same_seed_gives_same_sequence():
    state = new_session(load_bank(SAMPLE_BANK))
    first = random.Random(42)
    second = random.Random(42)
    sequence_a = [select_next_id(state, first) for _ in range(10)]
    sequence_b = [select_next_id(state, second) for _ in range(10)]
    assert sequence_a == sequence_b
