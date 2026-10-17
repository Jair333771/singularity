import random
from dataclasses import replace

import pytest

from app.domain.question import Question
from app.domain.session import SessionState
from app.infrastructure.messages import InfoCatalog
from app.services.session_engine import SessionEngine


def test_new_session_starts_at_level_one(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    state = SessionEngine(random.Random(), catalog).start(sample_questions)
    assert state.current_level == 1
    assert state.status == "in_progress"


def test_new_session_pending_ids_are_level_one_questions(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    state = SessionEngine(random.Random(), catalog).start(sample_questions)
    expected = [q.id for q in sample_questions if q.level == 1]
    assert state.pending_ids == expected
    assert len(state.pending_ids) == 7


def test_selected_id_is_pending(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    state = engine.start(sample_questions)
    assert engine.next_id(state) in state.pending_ids


def test_same_seed_gives_same_sequence(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    state = SessionEngine(random.Random(), catalog).start(sample_questions)
    engine_a = SessionEngine(random.Random(42), catalog)
    engine_b = SessionEngine(random.Random(42), catalog)
    sequence_a = [engine_a.next_id(state) for _ in range(10)]
    sequence_b = [engine_b.next_id(state) for _ in range(10)]
    assert sequence_a == sequence_b


def test_correct_answer_removes_id_from_pending(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    state = engine.start(sample_questions)
    question = next(q for q in sample_questions if q.id == state.pending_ids[0])
    result = engine.answer(state, question, question.correct_index)
    assert result.correct is True
    assert question.id not in result.next_state.pending_ids
    assert result.explanation == question.explanation


def test_wrong_answer_keeps_id_pending(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    state = engine.start(sample_questions)
    question = next(q for q in sample_questions if q.id == state.pending_ids[0])
    wrong_index = (question.correct_index + 1) % len(question.options)
    result = engine.answer(state, question, wrong_index)
    assert result.correct is False
    assert question.id in result.next_state.pending_ids
    assert result.explanation == question.explanation


def answer_all_correctly(
    engine: SessionEngine, state: SessionState, questions: list[Question]
) -> SessionState:
    by_id = {q.id: q for q in questions}
    while state.status == "in_progress":
        question = by_id[state.pending_ids[0]]
        state = engine.answer(state, question, question.correct_index).next_state
    return state


def test_level_stays_in_progress_while_pending_ids_remain(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    state = engine.start(sample_questions)
    for _ in range(6):
        question = next(q for q in sample_questions if q.id == state.pending_ids[0])
        state = engine.answer(state, question, question.correct_index).next_state
    assert len(state.pending_ids) == 1
    assert state.status == "in_progress"


def test_emptying_pending_ids_completes_level(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    state = answer_all_correctly(
        engine, engine.start(sample_questions), sample_questions
    )
    assert state.pending_ids == []
    assert state.status == "level_completed"
    assert state.current_level == 1


def test_advance_loads_next_level(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    completed = answer_all_correctly(
        engine, engine.start(sample_questions), sample_questions
    )
    state = engine.advance(completed, sample_questions)
    assert state.current_level == 2
    assert state.status == "in_progress"
    assert state.pending_ids == [q.id for q in sample_questions if q.level == 2]


def test_advance_rejected_while_level_in_progress(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    state = engine.start(sample_questions)
    with pytest.raises(ValueError, match="level 1: not completed"):
        engine.advance(state, sample_questions)


def test_short_level_blocks_session_start(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    short_bank = [q for q in sample_questions if q.id != "ast-003"]
    with pytest.raises(
        ValueError, match="level 1: expected 7 reviewed questions, found 6"
    ):
        SessionEngine(random.Random(1), catalog).start(short_bank)


def test_extra_question_blocks_session_start(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    extra = replace(next(q for q in sample_questions if q.level == 4), id="ast-extra")
    with pytest.raises(
        ValueError, match="level 4: expected 7 reviewed questions, found 8"
    ):
        SessionEngine(random.Random(1), catalog).start([*sample_questions, extra])


def test_full_game_completes_all_ten_levels(
    sample_questions: list[Question], catalog: InfoCatalog
) -> None:
    engine = SessionEngine(random.Random(1), catalog)
    state = engine.start(sample_questions)
    for level in range(1, 11):
        assert state.current_level == level
        state = answer_all_correctly(engine, state, sample_questions)
        if level < 10:
            assert state.status == "level_completed"
            state = engine.advance(state, sample_questions)
    assert state.status == "game_completed"
