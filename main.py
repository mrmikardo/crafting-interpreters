import sys

from error import HAD_ERROR
from scanner import Scanner

# Lifted from sysexits.h
EX_USAGE = 64
EX_DATAERR = 65


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def run_file(path: str) -> None:
    with open(path, "r") as f:
        run("".join(f.readlines()))

    if HAD_ERROR:
        sys.exit(EX_DATAERR)


def run_prompt() -> None:
    global HAD_ERROR

    while True:
        line = input("> ")
        if not line:
            break
        run(line)
        HAD_ERROR = False


def main() -> None:
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        sys.exit(EX_USAGE)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()


if __name__ == "__main__":
    main()
