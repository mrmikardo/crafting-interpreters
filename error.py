import sys

HAD_ERROR = False


def _report(line: int, where: str, message: str) -> None:
    print(f"[line {line}] Error {where}: {message}", file=sys.stderr)


def error(line: int, message: str) -> None:
    global HAD_ERROR

    _report(line, "", message)
    HAD_ERROR = True
