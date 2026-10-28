import pytest

from grading import average, get_grade, is_honors, is_passed


def test_grade_excellent():
    assert get_grade(95) == "5"


def test_grade_good():
    assert get_grade(80) == "4"


def test_grade_satisfactory():
    assert get_grade(70) == "3"


def test_grade_fail():
    assert get_grade(10) == "2"


def test_negative_score_is_invalid():
    with pytest.raises(ValueError):
        get_grade(-5)


def test_is_passed():
    assert is_passed(80)


def test_average():
    assert average([80, 90]) == 85


def test_average_empty():
    with pytest.raises(ValueError):
        average([])


def test_average_empty_message():
    with pytest.raises(ValueError, match=r"^scores must not be empty$"):
        average([])


@pytest.mark.parametrize(
    "scores, expected",
    [
        ([90, 90], True),  # средний ровно 90 — отличник
        ([89, 89], False),  # средний ниже порога
        ([100], True),
        ([100, 79], False),  # средний 89,5 — не отличник
        ([90, 90, 90], True),
        ([89, 90], False),  # средний 89,5
    ],
)
def test_is_honors(scores, expected):
    assert is_honors(scores) is expected


def test_is_honors_empty():
    with pytest.raises(ValueError, match=r"^scores must not be empty$"):
        is_honors([])


@pytest.mark.parametrize(
    "score, expected",
    [
        (90, "5"),  # нижняя граница пятёрки
        (89, "4"),  # на балл ниже
        (75, "4"),  # нижняя граница четвёрки
        (74, "3"),
        (60, "3"),  # нижняя граница тройки
        (59, "2"),
        (0, "2"),  # крайнее допустимое значение
        (100, "5"),  # верхнее допустимое значение
    ],
)
def test_grade_boundaries(score, expected):
    assert get_grade(score) == expected


@pytest.mark.parametrize("score", [-1, 101, -100, 1000])
def test_score_out_of_range(score):
    with pytest.raises(ValueError, match=r"^score must be between 0 and 100$"):
        get_grade(score)


@pytest.mark.parametrize(
    "score, threshold, expected",
    [
        (60, 60, True),  # ровно порог — сдано
        (59, 60, False),
        (75, 75, True),
        (74, 75, False),
        (90, 90, True),
        (89, 90, False),
        (61, 61, True),  # свой порог, ровно на границе
        (60, 61, False),
    ],
)
def test_is_passed_boundaries(score, threshold, expected):
    assert is_passed(score, threshold) is expected


def test_is_passed_default_threshold():
    assert is_passed(60) is True
    assert is_passed(59) is False


def test_is_passed_custom_threshold():
    assert is_passed(90, 90) is True
    assert is_passed(89, 90) is False
