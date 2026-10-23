#!/usr/bin/env python

import sys

from error import HAD_ERROR, HAD_RUNTIME_ERROR
from interpreter import Interpreter
from parser import Parser
from scanner import Scanner

# Lifted from sysexits.h
EX_USAGE = 64
EX_DATAERR = 65
EX_SOFTWARE = 70


def run(source: str, interpreter: Interpreter) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    parser = Parser(tokens)
    expression = parser.parse()
    assert expression, "Something went wrong"

    if HAD_ERROR:
        return

    interpreter.interpret(expression)


def run_file(path: str) -> None:
    interpreter = Interpreter()

    with open(path, "r") as f:
        run("".join(f.readlines()), interpreter)

    if HAD_ERROR:
        sys.exit(EX_DATAERR)

    if HAD_RUNTIME_ERROR:
        sys.exit(EX_SOFTWARE)


def run_prompt() -> None:
    global HAD_ERROR

    interpreter = Interpreter()

    while True:
        line = input("> ")
        if not line:
            break
        run(line, interpreter)
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
