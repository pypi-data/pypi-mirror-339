"""
The `Either` type and its components.
"""


class Left:
    """
    The "left" variant containing a value.
    """


class Right:
    """
    The "right" variant containing a value.
    """


class Either[L, R]:
    """
    A type that is either a left or a right value, never both.
    """

    def __init__(self, adt: tuple[Left, L] | tuple[Right, R]) -> None:
        self.inner = adt
        """
        The inner value.

        ## Examples

        ```python
        val = Either((Left(), 5))

        match val.inner:
            case (Left(), x):
                assert x == 5
            case (Right(), _):
                raise AssertionError("unreachable")
        ```
        """

    def __repr__(self) -> str:
        match self.inner:
            case (Left(), x):
                return f"Left({repr(x)})"
            case (Right(), x):
                return f"Right({repr(x)})"

    def __str__(self) -> str:
        match self.inner:
            case (Left(), x):
                return str(x)
            case (Right(), x):
                return str(x)
