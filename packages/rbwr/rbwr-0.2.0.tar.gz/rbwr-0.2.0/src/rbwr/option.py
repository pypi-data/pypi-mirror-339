"""
The `Option` type and its components.

This is similar to `T | None` except that this type can be nested within itself.
"""


class Some:
    """
    The variant containing a value.
    """


class Option[T]:
    """
    A type that is either some value or a lack of a value.
    """

    def __init__(self, adt: tuple[Some, T] | None) -> None:
        self.inner = adt
        """
        The inner value.

        ## Examples

        ```python
        val = Option((Some(), 5))

        match val.inner:
            case (Some(), x):
                assert x == 5
            case None:
                raise AssertionError("unreachable")
        ```
        """

    def __repr__(self) -> str:
        match self.inner:
            case (Some(), x):
                return f"Some({repr(x)})"
            case None:
                return str(None)

    def __str__(self) -> str:
        match self.inner:
            case (Some(), x):
                return str(x)
            case None:
                return str(None)
