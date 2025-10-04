import abc
import typing


if typing.TYPE_CHECKING:
    from scanner.tokens import Token

R = typing.TypeVar("R")


class Visitor(abc.ABC, typing.Generic[R]):
    @abc.abstractmethod
    def visit_unary_expr(self, expr: "Unary") -> R:
        pass

    @abc.abstractmethod
    def visit_binary_expr(self, expr: "Binary") -> R:
        pass

    @abc.abstractmethod
    def visit_literal_expr(self, expr: "Literal") -> R:
        pass

    @abc.abstractmethod
    def visit_grouping_expr(self, expr: "Grouping") -> R:
        pass


class AstPrinter(Visitor[str]):
    def _parenthesize(self, name: str, exprs: list["Expr"]) -> str:
        out = f"({name}"
        for expr in exprs:
            out += " "
            out += expr.accept(self)
        out += ")"
        return out

    def print(self, expr: "Expr") -> str:
        return expr.accept(self)

    def visit_unary_expr(self, expr: "Unary") -> str:
        return self._parenthesize(expr.operator.lexeme, [expr.right])

    def visit_binary_expr(self, expr: "Binary") -> str:
        return self._parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visit_literal_expr(self, expr: "Literal") -> str:
        if not expr.value:
            return "nil"
        return str(expr.value)

    def visit_grouping_expr(self, expr: "Grouping") -> str:
        return self._parenthesize("grouping", [expr.expr])


class Expr(abc.ABC):
    @abc.abstractmethod
    def accept(self, visitor: Visitor[R]) -> R:
        pass  # Do nothing


class Unary(Expr):
    operator: "Token"
    right: Expr

    def __init__(self, operator: "Token", right: Expr) -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_unary_expr(self)


class Binary(Expr):
    operator: "Token"
    left: Expr
    right: Expr

    def __init__(self, operator: "Token", left: Expr, right: Expr) -> None:
        self.operator = operator
        self.left = left
        self.right = right

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_binary_expr(self)


class Literal(Expr):
    value: typing.Any

    def __init__(self, value: typing.Any) -> None:
        self.value = value

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_literal_expr(self)


class Grouping(Expr):
    expr: Expr

    def __init__(self, expr: Expr) -> None:
        self.expr = expr

    def accept(self, visitor: Visitor[R]) -> R:
        return visitor.visit_grouping_expr(self)
