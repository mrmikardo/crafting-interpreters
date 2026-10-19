from typing import TYPE_CHECKING, cast

from expressions import Visitor
from tokens import Token, TokenType

if TYPE_CHECKING:
    from expressions import Binary, Expr, Grouping, Literal, Unary


class RuntimeError(Exception):
    token: Token

    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token


class Interpreter(Visitor[object]):
    def _assert_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, int):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def _assert_number_operands(
        self, operator: Token, left: object, right: object
    ) -> None:
        if isinstance(left, int) and isinstance(right, int):
            return
        raise RuntimeError(operator, "Operands must be a number.")

    def _evaluate(self, expr: "Expr") -> object:
        return expr.accept(self)

    def _is_equal(self, a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            # b is not None
            return False
        return a.__eq__(b)

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
                self._assert_number_operand(expr.operator, right)
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
                self._assert_number_operands(expr.operator, left, right)
                return int(left) - int(right)
            case TokenType.PLUS:
                if isinstance(left, int) and isinstance(right, int):
                    return int(left) + int(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                else:
                    raise RuntimeError(
                        expr.operator, "Operands must be two numbers or two strings."
                    )
            case TokenType.SLASH:
                self._assert_number_operands(expr.operator, left, right)
                return int(left) / int(right)
            case TokenType.STAR:
                self._assert_number_operands(expr.operator, left, right)
                return int(left) * int(right)
            case TokenType.GREATER:
                self._assert_number_operands(expr.operator, left, right)
                return int(left) > int(right)
            case TokenType.GREATER_EQUAL:
                self._assert_number_operands(expr.operator, left, right)
                return int(left) >= int(right)
            case TokenType.LESS:
                self._assert_number_operands(expr.operator, left, right)
                return int(left) < int(right)
            case TokenType.LESS_EQUAL:
                self._assert_number_operands(expr.operator, left, right)
                return int(left) <= int(right)
            case TokenType.BANG_EQUAL:
                return not self._is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self._is_equal(left, right)

        # Unreachable
        return None
