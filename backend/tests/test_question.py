import pytest

from engine.question import Question, validate_question


def make_question(**overrides):
    fields = dict(
        id="ast-001",
        level=1,
        topic="astrofisica",
        text="Cuál es la estrella más cercana al Sol?",
        options=["Sirio", "Próxima Centauri", "Vega"],
        correct_index=1,
        explanation="Próxima Centauri está a unos 4,2 años luz.",
        status="reviewed",
    )
    fields.update(overrides)
    return Question(**fields)


def test_valid_question_passes():
    validate_question(make_question())


def test_draft_status_is_rejected():
    with pytest.raises(ValueError, match="ast-001"):
        validate_question(make_question(status="draft"))


def test_correct_index_out_of_range_is_rejected():
    with pytest.raises(ValueError, match="ast-001"):
        validate_question(make_question(correct_index=3))


def test_fewer_than_two_options_is_rejected():
    with pytest.raises(ValueError, match="ast-001"):
        validate_question(make_question(options=["Sirio"], correct_index=0))


def test_more_than_four_options_is_rejected():
    with pytest.raises(ValueError, match="ast-001"):
        validate_question(make_question(options=["a", "b", "c", "d", "e"], correct_index=0))


def test_unknown_topic_is_rejected():
    with pytest.raises(ValueError, match="ast-001"):
        validate_question(make_question(topic="quimica"))


def test_level_out_of_range_is_rejected():
    with pytest.raises(ValueError, match="ast-001"):
        validate_question(make_question(level=11))
