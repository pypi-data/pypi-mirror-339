"""
The `Result` type and its components.
"""


class Ok:
    """
    The variant containing a success value.
    """


class Err:
    """
    The variant containing an error value.
    """


class Result[T, E]:
    """
    A type that is either a success value or an error value, never both.
    """

    def __init__(self, adt: tuple[Ok, T] | tuple[Err, E]) -> None:
        self.inner = adt
        """
        The inner value.

        ## Examples

        ```python
        val = Result((Ok(), 5))

        match val.inner:
            case (Ok(), x):
                assert x == 5
            case (Err(), _):
                raise AssertionError("unreachable")
        ```
        """

    def __repr__(self) -> str:
        match self.inner:
            case (Ok(), x):
                return f"Ok({repr(x)})"
            case (Err(), x):
                return f"Err({repr(x)})"

    def __str__(self) -> str:
        match self.inner:
            case (Ok(), x):
                return str(x)
            case (Err(), x):
                return str(x)
