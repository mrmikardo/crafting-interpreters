from typing import TYPE_CHECKING, cast

from expressions import Visitor
from tokens import TokenType

if TYPE_CHECKING:
    from expressions import Binary, Expr, Grouping, Literal, Unary


class Interpreter(Visitor[object]):
    def _evaluate(self, expr: "Expr") -> object:
        return expr.accept(self)

    def _truthy(self, obj: object) -> bool:
        """
        False and nil are falsey; everything else is truthy.
        """
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def visit_literal_expr(self, expr: "Literal") -> object:
        return expr.value

    def visit_grouping_expr(self, expr: "Grouping") -> object:
        return self._evaluate(expr)

    def visit_unary_expr(self, expr: "Unary") -> object:
        right = self._evaluate(expr)

        match expr.operator.type:
            case TokenType.MINUS:
                return -cast(int, right)
            case TokenType.BANG:
                return not self._truthy(right)

        # Unreachable
        return None

    def visit_binary_expr(self, expr: "Binary") -> object:
        left = cast(int, self._evaluate(expr.left))
        right = cast(int, self._evaluate(expr.right))

        match expr.operator.type:
            case TokenType.MINUS:
                return int(left) - int(right)
            case TokenType.PLUS:
                if isinstance(left, int) and isinstance(right, int):
                    return int(left) + int(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
            case TokenType.SLASH:
                return int(left) / int(right)
            case TokenType.STAR:
                return int(left) * int(right)

        # Unreachable
        return None
