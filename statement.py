from abc import ABC, abstractmethod
from dataclasses import dataclass

from expressions import Expr, Visitor


class Stmt(ABC):
    """
    Base class of all statements.
    """

    @abstractmethod
    def accept[R](self, visitor: Visitor[R]) -> R: ...


# Concrete statements


@dataclass
class Expression(Stmt):
    expr: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_expression_stmt(self)


@dataclass
class Print(Stmt):
    expr: Expr

    def accept[R](self, visitor: Visitor[R]) -> R:
        return visitor.visit_print_stmt(self)
