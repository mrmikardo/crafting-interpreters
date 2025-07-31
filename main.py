#!/usr/bin/env python3

import sys
from dataclasses import dataclass


@dataclass
class Token:
    lexeme: str


class Scanner:

    source: str

    def __init__(self, source: str) -> None:
        self.source = source

    def scan_tokens(self) -> list[Token]:
        return []


def _run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(f"Token: {token}")


def run_file(filename: str) -> None:
    with open(filename) as f:
        _run(f.read())


def run_prompt() -> None:
    while True:
        try:
            line = input("> ")
            _run(line)
        except (EOFError, KeyboardInterrupt):
            break


def main():
    if len(sys.argv) > 2:
        print("Usage: python main.py <filename>")
        sys.exit(64)
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        run_file(filename)
    else:
        run_prompt()


if __name__ == "__main__":
    main()
