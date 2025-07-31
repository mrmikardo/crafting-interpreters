import sys


had_error = False


def _report(line: int, where: str, message: str) -> None:
    sys.stderr.write("[line " + str(line) + "] Error" + where + ": " + message)


def error(line: int, message: str) -> None:
    global had_error
    had_error = True
    _report(line, "", message)
