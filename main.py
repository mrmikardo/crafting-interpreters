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

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

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

    def _string(self) -> None:
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        if self._is_at_end():
            errors.error(self.line, "Unterminated string.")

        # Capture the closing '"'
        self._advance()

        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        if self._peek() == "." and self._peek_next().isdigit():
            self._advance()
            while self._peek().isdigit():
                self._advance()

        value = float(self.source[self.start : self.current])
        self._add_token(TokenType.NUMBER, value)

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
        elif char == "=":
            if self._match("="):
                self._add_token(TokenType.EQUAL_EQUAL)
            else:
                self._add_token(TokenType.EQUAL)
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
        elif char == "/":
            if self._match("/"):
                # We are dealing with a comment => advance through it, don't tokenize.
                while self._peek() != "\n" and not self._is_at_end():
                    self._advance()
            else:
                self._add_token(TokenType.SLASH)
        elif char == "\n":
            self.line += 1
        elif char in [" ", "\t", "\r"]:
            return None  # Ignore whitespace
        # Handle literals
        elif char == '"':
            self._string()
        elif char.isdigit():
            self._number()
        else:
            errors.error(self.line, "Unexpected character")

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            # We are at the beginning of the next lexeme => scan it.
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
