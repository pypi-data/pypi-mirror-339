from rbwr import Option
from rbwr.option import Some


def test_inner_some():
    val = Option[int]((Some(), 5))

    match val.inner:
        case (Some(), x):
            assert x == 5
        case None:
            raise AssertionError("should be some")


def test_inner_none():
    val = Option[int](None)

    match val.inner:
        case (Some(), _):
            raise AssertionError("should be none")
        case None:
            pass


def test_repr_some():
    val = Option[int]((Some(), 5))

    assert repr(val) == "Some(5)"


def test_repr_none():
    val = Option[int](None)

    assert repr(val) == "None"


def test_str_some():
    val = Option[int]((Some(), 5))

    assert str(val) == "5"


def test_str_none():
    val = Option[int](None)

    assert str(val) == "None"
