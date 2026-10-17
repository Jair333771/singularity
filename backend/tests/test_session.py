import random

from engine.session import SessionEngine


def test_new_session_starts_at_level_one(sample_questions):
    state = SessionEngine(random.Random()).start(sample_questions)
    assert state.current_level == 1
    assert state.status == "in_progress"


def test_new_session_pending_ids_are_level_one_questions(sample_questions):
    state = SessionEngine(random.Random()).start(sample_questions)
    expected = [q.id for q in sample_questions if q.level == 1]
    assert state.pending_ids == expected
    assert len(state.pending_ids) == 7


def test_selected_id_is_pending(sample_questions):
    engine = SessionEngine(random.Random(1))
    state = engine.start(sample_questions)
    assert engine.next_id(state) in state.pending_ids


def test_same_seed_gives_same_sequence(sample_questions):
    state = SessionEngine(random.Random()).start(sample_questions)
    engine_a = SessionEngine(random.Random(42))
    engine_b = SessionEngine(random.Random(42))
    sequence_a = [engine_a.next_id(state) for _ in range(10)]
    sequence_b = [engine_b.next_id(state) for _ in range(10)]
    assert sequence_a == sequence_b


def test_correct_answer_removes_id_from_pending(sample_questions):
    engine = SessionEngine(random.Random(1))
    state = engine.start(sample_questions)
    question = next(q for q in sample_questions if q.id == state.pending_ids[0])
    result = engine.answer(state, question, question.correct_index)
    assert result.correct is True
    assert question.id not in result.next_state.pending_ids
    assert result.explanation == question.explanation


def test_wrong_answer_keeps_id_pending(sample_questions):
    engine = SessionEngine(random.Random(1))
    state = engine.start(sample_questions)
    question = next(q for q in sample_questions if q.id == state.pending_ids[0])
    wrong_index = (question.correct_index + 1) % len(question.options)
    result = engine.answer(state, question, wrong_index)
    assert result.correct is False
    assert question.id in result.next_state.pending_ids
    assert result.explanation == question.explanation
