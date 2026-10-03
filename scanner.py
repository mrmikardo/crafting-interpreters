from dataclasses import dataclass, field

from error import error
from tokens import Token, TokenType


@dataclass
class Scanner:
    # Source and output
    source: str
    tokens: list[Token] = field(default_factory=list)

    # Control flags
    start = 0  # First character in the lexeme being scanned
    current = 0  # Character currently being considered
    line = 1

    def _add_token(self, type: TokenType, literal: object | None = None) -> None:
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def _advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def _match(self, expected: str) -> bool:
        if self.is_at_end:
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def _peek(self) -> str:
        if self.is_at_end:
            return "\0"
        return self.source[self.current]

    @property
    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_token(self) -> None:
        c = self._advance()
        match c:
            case "(":
                self._add_token(TokenType.LEFT_PAREN)
                return
            case ")":
                self._add_token(TokenType.RIGHT_PAREN)
                return
            case "{":
                self._add_token(TokenType.LEFT_BRACE)
                return
            case "}":
                self._add_token(TokenType.RIGHT_BRACE)
                return
            case ",":
                self._add_token(TokenType.COMMA)
                return
            case ".":
                self._add_token(TokenType.DOT)
                return
            case "-":
                self._add_token(TokenType.MINUS)
                return
            case "+":
                self._add_token(TokenType.PLUS)
                return
            case ";":
                self._add_token(TokenType.SEMICOLON)
                return
            case "/":
                self._add_token(TokenType.SLASH)
                return
            case "*":
                self._add_token(TokenType.STAR)
                return
            case "!":
                self._add_token(
                    TokenType.BANG_EQUAL if self._match("=") else TokenType.BANG
                )
                return
            case "=":
                self._add_token(
                    TokenType.EQUAL_EQUAL if self._match("=") else TokenType.EQUAL
                )
                return
            case "<":
                self._add_token(
                    TokenType.LESS_EQUAL if self._match("=") else TokenType.LESS
                )
                return
            case ">":
                self._add_token(
                    TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
                )
                return
            case "/":
                # Start of a comment: consume until the end of the line
                # (without tokenising).
                if self._match("/"):
                    while self._peek() != "\n" and not self.is_at_end:
                        self._advance()
                else:
                    self._add_token(TokenType.SLASH)
                return
            case " ":
                return
            case "\r":
                return
            case "\t":
                return
            case "\n":
                self.line += 1
                return
            case _:
                error(self.line, "Unexpected character.")

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end:
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
