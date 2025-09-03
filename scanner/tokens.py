import dataclasses
import enum
from utils import utils


class TokenType(enum.Enum):

    # Single-character tokens
    LEFT_PAREN = "left_paren"
    RIGHT_PAREN = "right_paren"
    LEFT_BRACE = "left_brace"
    RIGHT_BRACE = "right_brace"
    COMMA = "comma"
    DOT = "dot"
    MINUS = "minus"
    PLUS = "plus"
    STAR = "star"
    SEMICOLON = "semicolon"
    SLASH = "slash"

    # One- or two-character tokens
    BANG = "bang"
    BANG_EQUAL = "bang_equal"
    EQUAL = "equal"
    EQUAL_EQUAL = "equal_equal"
    GREATER = "greater"
    GREATER_EQUAL = "greater_equal"
    LESS = "less"
    LESS_EQUAL = "less_equal"

    # Literals
    IDENTIFIER = "identifier"
    STRING = "string"
    NUMBER = "number"

    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    EOF = "eof"


@dataclasses.dataclass
class Token:
    lexeme: str
    type: TokenType
    literal: str | None
    line: int

    def __str__(self):
        return (
            utils.green(utils.bold("~~ Token ~~\n"))
            + f"\t{utils.yellow(utils.underline('Type'))}: {self.type.value}\n"
            + f"\t{utils.yellow(utils.underline('Lexeme'))}: {self.lexeme}\n"
            + f"\t{utils.yellow(utils.underline('Literal'))} {(str(self.literal) or '')}\n"
        )


IDENTIFIERS = {
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
