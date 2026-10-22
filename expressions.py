from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

from tokens import Token

if TYPE_CHECKING:
    from statement import Stmt


# TODO: pull this into its own file.
# TODO: split Visitor classes for expressions and statements.
class Visitor[R](ABC):
    """
    Base class of all visitor classes.
    """

    @abstractmethod
    def visit_binary_expr(self, expr: "Binary") -> R: ...

    @abstractmethod
    def visit_grouping_expr(self, expr: object) -> R: ...

    @abstractmethod
    def visit_literal_expr(self, expr: "Literal") -> R: ...

    @abstractmethod
    def visit_unary_expr(self, expr: "Unary") -> R: ...

    @abstractmethod
    def visit_expression_stmt(self, stmt: "Stmt") -> R: ...

    @abstractmethod
    def visit_print_stmt(self, stmt: "Stmt") -> R: ...


class Expr(ABC):
    """
    Base class of all expressions.
    """

    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


# Concrete expressions


@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary_expr(self)


@dataclass
class Grouping(Expr):
    expression: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping_expr(self)


@dataclass
class Literal(Expr):
    value: object | None

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal_expr(self)


@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary_expr(self)


# Visitor classes


class AstPrinter(Visitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def _parenthesize(self, name: str, exprs: list[Expr]) -> str:
        out = f"({name}"
        for expr in exprs:
            out += f" {expr.accept(self)}"
        out += ")"
        return out

    def visit_binary_expr(self, expr: Binary) -> str:
        return self._parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self._parenthesize("group", [expr.expression])

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self._parenthesize(expr.operator.lexeme, [expr.right])
