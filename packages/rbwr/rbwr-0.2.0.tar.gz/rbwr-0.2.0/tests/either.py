from rbwr import Either
from rbwr.either import Left, Right


def test_inner_left():
    val = Either[int, None]((Left(), 5))

    match val.inner:
        case (Left(), x):
            assert x == 5
        case (Right(), _):
            raise AssertionError("should be left")


def test_inner_right():
    val = Either[None, int]((Right(), 5))

    match val.inner:
        case (Left(), _):
            raise AssertionError("should be right")
        case (Right(), x):
            assert x == 5


def test_repr_left():
    val = Either[int, None]((Left(), 5))

    assert repr(val) == "Left(5)"


def test_repr_right():
    val = Either[None, int]((Right(), 5))

    assert repr(val) == "Right(5)"


def test_str_left():
    val = Either[int, None]((Left(), 5))

    assert str(val) == "5"


def test_str_right():
    val = Either[None, int]((Right(), 5))

    assert str(val) == "5"
