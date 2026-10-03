import sys

# Lifted from sysexits.h
EX_USAGE = 64


# Scanner class
class Scanner:
    def __init__(self, source: str) -> None:
        self.source = source

    def scan_tokens(self) -> list[str]:
        return []


def run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token)


def run_file(path: str) -> None:
    with open(path, "r") as f:
        run("".join(f.readlines()))


def run_prompt() -> None:
    while True:
        line = input("> ")
        if not line:
            break
        run(line)


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
