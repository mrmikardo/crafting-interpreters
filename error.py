import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from interpreter import RuntimeError
    from tokens import Token

HAD_ERROR = False
HAD_RUNTIME_ERROR = False


def _report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)


def error(line: int, message: str) -> None:
    global HAD_ERROR

    _report(line, "", message)
    HAD_ERROR = True


def token_error(token: "Token", message: str) -> None:
    from tokens import TokenType

    if token.type == TokenType.EOF:
        _report(token.line, " at end", message)
    else:
        _report(token.line, f" at '{token.lexeme}'", message)


def runtime_error(error: "RuntimeError"):
    global HAD_RUNTIME_ERROR

    print(f"{error!s} [line {error.token.line}]", file=sys.stderr)

    HAD_RUNTIME_ERROR = True
