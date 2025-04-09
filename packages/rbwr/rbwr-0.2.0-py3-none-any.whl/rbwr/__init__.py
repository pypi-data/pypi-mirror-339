"""
Rather be writing Rust.

A small Python library providing sum types that play well with existing
typechecking PEPs and should work out-of-the-box with any good typechecker, such
as Pyright.
"""

from . import either as either, option as option, result as result
from .either import Either as Either
from .option import Option as Option
from .result import Result as Result
