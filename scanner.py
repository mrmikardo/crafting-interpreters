from dataclasses import dataclass, field

from error import error
from tokens import Token, TokenType

RESERVED_WORDS_MAP = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUN,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


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

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _scan_identifier(self) -> None:
        while self._peek().isalnum():
            self._advance()

        # Determine if this is an identifier or a reserved word and set
        # the token type accordingly.
        text = self.source[self.start : self.current]
        token_type = RESERVED_WORDS_MAP.get(text, TokenType.IDENTIFIER)

        self._add_token(token_type)

    def _scan_string(self) -> None:
        while self._peek() != '"' and not self.is_at_end:
            if self._peek() == "\n":
                self.line += 1
            self._advance()

        # Encountered EOF whilst parsing a string => string is
        # unterminated.
        if self.is_at_end:
            error(self.line, "Unerminated string.")

        # Consume the closing ".
        self._advance()

        # Trim the surrounding quotation marks and add a token with the
        # literal value.
        value = self.source[self.start + 1 : self.current - 1]
        self._add_token(TokenType.STRING, value)

    def _scan_number(self) -> None:
        while self._peek().isdigit():
            self._advance()

        # Check for fractional part.
        if self._peek() == "." and self._peek_next().isdigit():
            # Consume the ".".
            self._advance()
            # Continuing consuming any digit characters after the
            # decimal place.
            while self._peek().isdigit():
                self._advance()

        self._add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

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
            case '"':
                self._scan_string()
                return
            case _:
                # First, handle number literals.
                if c.isdigit():
                    self._scan_number()
                # Then handle reserved words and identifiers.
                elif c.isalpha():
                    self._scan_identifier()
                else:
                    # Handle unrecognised characters last.
                    error(self.line, "Unexpected character.")

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end:
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
