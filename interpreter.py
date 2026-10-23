from typing import TYPE_CHECKING, cast

from error import error
from expressions import Visitor
from statement import Expression, Print
from tokens import Token, TokenType

if TYPE_CHECKING:
    from expressions import Binary, Expr, Grouping, Literal, Unary
    from statement import Stmt


class RuntimeError(Exception):
    token: Token

    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token


class Environment:
    values: dict

    def define(self, name: str, value: object) -> None:
        self.values[name] = value

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")


class Interpreter(Visitor[object]):
    _environment: Environment

    def __init__(self) -> None:
        self._environment = Environment()

    def _assert_number_operand(self, operator: Token, operand: object) -> None:
        if isinstance(operand, int):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def _assert_number_operands(
        self, operator: Token, left: object, right: object
    ) -> None:
        if isinstance(left, float) and isinstance(right, float):
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

    def _stringify(self, obj: object) -> str:
        if obj is None:
            return "nil"

        if isinstance(obj, int):
            text = str(obj)
            if text.endswith(".0"):
                text = text[0 : len(text) - 2]
            return text

        return str(obj)

    def _truthy(self, obj: object) -> bool:
        """
        False and nil are falsey; everything else is truthy.
        """
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def _execute(self, statement: "Stmt") -> None:
        statement.accept(self)

    def interpret(self, statements: list["Stmt"]) -> None:
        """
        Entrypoint for the Interpreter class.
        """
        try:
            for statement in statements:
                self._execute(statement)
        except RuntimeError as e:
            error(0, str(e))

    # Visitor methods

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
        left = self._evaluate(expr.left)
        right = self._evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self._assert_number_operands(expr.operator, left, right)
                return int(left) - int(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
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

    # Statements

    def visit_expression_stmt(self, stmt: Expression) -> None:
        self._evaluate(stmt.expr)

    def visit_print_stmt(self, stmt: Print) -> None:
        value = self._evaluate(stmt.expr)
        print(str(value))
