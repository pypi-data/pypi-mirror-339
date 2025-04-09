from rbwr import Result
from rbwr.result import Err, Ok


def test_inner_ok():
    val = Result[int, None]((Ok(), 5))

    match val.inner:
        case (Ok(), x):
            assert x == 5
        case (Err(), _):
            raise AssertionError("should be ok")


def test_inner_err():
    val = Result[None, int]((Err(), 5))

    match val.inner:
        case (Ok(), _):
            raise AssertionError("should be err")
        case (Err(), x):
            assert x == 5


def test_repr_ok():
    val = Result[int, None]((Ok(), 5))

    assert repr(val) == "Ok(5)"


def test_repr_err():
    val = Result[None, int]((Err(), 5))

    assert repr(val) == "Err(5)"


def test_str_ok():
    val = Result[int, None]((Ok(), 5))

    assert str(val) == "5"


def test_str_err():
    val = Result[None, int]((Err(), 5))

    assert str(val) == "5"
