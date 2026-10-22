from dataclasses import dataclass
from typing import TYPE_CHECKING

from error import token_error
from expressions import Binary, Expr, Grouping, Literal, Unary
from statement import Expression, Print
from tokens import Token, TokenType

if TYPE_CHECKING:
    from expressions import Stmt


class ParseError(Exception):
    pass


@dataclass
class Parser:
    tokens: list[Token]
    current: int = 0

    def _advance(self) -> Token:
        if not self._is_at_end:
            self.current += 1
        return self._previous()

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end:
            return False
        return self._peek().type == token_type

    def _consume(self, token_type: TokenType, error_msg: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), error_msg)

    def _error(self, token: Token, error_msg: str) -> ParseError:
        token_error(token, error_msg)
        return ParseError()

    @property
    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _match(self, token_types: list[TokenType]) -> bool:
        for token_type in token_types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _synchronize(self) -> None:
        """
        Synchronize the parser state after an error has been hit.

        Synchronizing simply means we walk through the stream of tokens
        until we match a token which denotes a statement boundary.
        """
        self._advance()
        while not self._is_at_end:
            if self._previous().type == TokenType.SEMICOLON:
                return
            match self._peek().type:
                case TokenType.CLASS:
                    return
                case TokenType.FOR:
                    return
                case TokenType.FUN:
                    return
                case TokenType.IF:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.WHILE:
                    return
            self._advance()

    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()
        while self._match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            # _match advances current, so we need to check the previous
            # token to extract the operator.
            operator = self._previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> Expr:
        expr = self.term()
        while self._match(
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ]
        ):
            operator = self._previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self) -> Expr:
        expr = self.factor()
        while self._match([TokenType.MINUS, TokenType.PLUS]):
            operator = self._previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self) -> Expr:
        expr = self.unary()
        while self._match([TokenType.SLASH, TokenType.STAR]):
            operator = self._previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self) -> Expr:
        if self._match([TokenType.BANG, TokenType.MINUS]):
            operator = self._previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> Expr:
        if self._match([TokenType.FALSE]):
            return Literal(False)
        if self._match([TokenType.TRUE]):
            return Literal(True)
        if self._match([TokenType.NIL]):
            return Literal(None)

        if self._match([TokenType.STRING, TokenType.NUMBER]):
            return Literal(self._previous().literal)

        if self._match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        # If none of the cases have matched so far, we are sitting on a
        # token which cannot start an expression.
        raise self._error(self._peek(), "Expect expression.")

    # Statements

    def expression_statement(self) -> Expression:
        value = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(value)

    def print_statement(self) -> Print:
        value = self.expression()
        self._consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def statement(self) -> "Stmt":
        if self._match([TokenType.PRINT]):
            return self.print_statement()
        return self.expression_statement()

    def parse(self) -> list["Stmt"]:
        """
        Main entrypoint for the parser.
        """
        statements = []

        while not self._is_at_end:
            statements.append(self.statement())

        return statements
