"""
Utils for printing output in colour 🌈
"""

from enum import Enum
from typing import Protocol


class Stringable(Protocol):
    def __str__(self) -> str:
        ...


class FormatCode(Enum):
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def _apply_format_code(colour: FormatCode, text: Stringable) -> str:
    if not isinstance(text, str):
        text = str(text)
    return colour.value + text + FormatCode.END.value


def green(text: Stringable) -> str:
    return _apply_format_code(FormatCode.GREEN, text)


def yellow(text: Stringable) -> str:
    return _apply_format_code(FormatCode.YELLOW, text)


def red(text: Stringable) -> str:
    return _apply_format_code(FormatCode.RED, text)


def bold(text: Stringable) -> str:
    return _apply_format_code(FormatCode.BOLD, text)


def underline(text: Stringable) -> str:
    return _apply_format_code(FormatCode.UNDERLINE, text)
