#!/usr/bin/env python3

import sys
from typing import Any

import errors
from tokens import Token, TokenType


class Scanner:

    source: str
    tokens: list[Token]

    # Variables to keep track of scanning process
    start: int = 0
    current: int = 0
    line: int = 1

    def __init__(self, source: str) -> None:
        self.source = source
        self.tokens = []

    def _advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def _match(self, expected: str) -> bool:
        if self._is_at_end():
            return False
        if self.source[self.current] == expected:
            self.current += 1
            return True
        return False

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _add_token(self, type: TokenType, literal: Any | None = None) -> None:
        self.tokens.append(
            Token(
                lexeme=self.source[self.start : self.current],
                type=type,
                literal=literal,
                line=self.line,
            )
        )

    def _scan_token(self) -> None:
        char = self._advance()
        if char == "(":
            self._add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self._add_token(TokenType.RIGHT_PAREN)
        elif char == "{":
            self._add_token(TokenType.LEFT_BRACE)
        elif char == "}":
            self._add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self._add_token(TokenType.COMMA)
        elif char == ".":
            self._add_token(TokenType.DOT)
        elif char == "-":
            self._add_token(TokenType.MINUS)
        elif char == "+":
            self._add_token(TokenType.PLUS)
        elif char == "*":
            self._add_token(TokenType.STAR)
        elif char == ";":
            self._add_token(TokenType.SEMICOLON)
        elif char == "!":
            if self._match("="):
                self._add_token(TokenType.BANG_EQUAL)
            else:
                self._add_token(TokenType.BANG)
        elif char == ">":
            if self._match("="):
                self._add_token(TokenType.GREATER_EQUAL)
            else:
                self._add_token(TokenType.GREATER)
        elif char == "<":
            if self._match("="):
                self._add_token(TokenType.LESS_EQUAL)
            else:
                self._add_token(TokenType.LESS)
        else:
            errors.error(self.line, "Unexpected character")

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self._scan_token()
        self.tokens.append(
            Token(lexeme="", type=TokenType.EOF, literal=None, line=self.line)
        )
        return self.tokens


def _run(source: str) -> None:
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(f"Token: {token}")


def run_file(filename: str) -> None:
    with open(filename) as f:
        _run(f.read())
        if errors.had_error:
            sys.exit(65)


def run_prompt() -> None:
    while True:
        try:
            line = input("> ")
            _run(line)
            errors.had_error = False
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
