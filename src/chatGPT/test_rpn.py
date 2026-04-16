"""
test_rpn.py - Tests unitarios para rpn.py
Cobertura objetivo: >= 90%
"""

import math
import unittest

from rpn import RPNError, evaluate


class TestBasicOperations(unittest.TestCase):
    """Tests para operaciones aritméticas básicas."""

    def test_addition(self):
        self.assertEqual(evaluate("3 4 +"), 7)

    def test_subtraction(self):
        self.assertEqual(evaluate("10 3 -"), 7)

    def test_multiplication(self):
        self.assertEqual(evaluate("3 4 *"), 12)

    def test_division(self):
        self.assertAlmostEqual(evaluate("10 2 /"), 5.0)

    def test_float_operands(self):
        self.assertAlmostEqual(evaluate("2.5 1.5 +"), 4.0)

    def test_negative_numbers(self):
        self.assertEqual(evaluate("-3 4 +"), 1)

    def test_complex_expression_1(self):
        """5 1 2 + 4 * + 3 - → 14"""
        self.assertEqual(evaluate("5 1 2 + 4 * + 3 -"), 14)

    def test_complex_expression_2(self):
        """2 3 4 * + → 14"""
        self.assertEqual(evaluate("2 3 4 * +"), 14)


class TestErrorHandling(unittest.TestCase):
    """Tests para manejo de errores."""

    def test_division_by_zero(self):
        with self.assertRaises(RPNError) as ctx:
            evaluate("3 0 /")
        self.assertIn("cero", str(ctx.exception).lower())

    def test_invalid_token(self):
        with self.assertRaises(RPNError) as ctx:
            evaluate("3 foo +")
        self.assertIn("inválido", str(ctx.exception).lower())

    def test_insufficient_stack_binary(self):
        with self.assertRaises(RPNError):
            evaluate("3 +")

    def test_insufficient_stack_unary(self):
        with self.assertRaises(RPNError):
            evaluate("sqrt")

    def test_too_many_values_on_stack(self):
        with self.assertRaises(RPNError):
            evaluate("3 4")

    def test_empty_stack_result(self):
        with self.assertRaises(RPNError):
            evaluate("")

    def test_sqrt_negative(self):
        with self.assertRaises(RPNError):
            evaluate("-4 sqrt")

    def test_log_nonpositive(self):
        with self.assertRaises(RPNError):
            evaluate("0 log")

    def test_ln_nonpositive(self):
        with self.assertRaises(RPNError):
            evaluate("-1 ln")

    def test_inverse_zero(self):
        with self.assertRaises(RPNError):
            evaluate("0 1/x")

    def test_sto_missing_register(self):
        with self.assertRaises(RPNError):
            evaluate("5 sto")

    def test_sto_invalid_register(self):
        with self.assertRaises(RPNError):
            evaluate("5 sto 99")

    def test_rcl_missing_register(self):
        with self.assertRaises(RPNError):
            evaluate("rcl")

    def test_rcl_invalid_register(self):
        with self.assertRaises(RPNError):
            evaluate("rcl 99")

    def test_sto_insufficient_stack(self):
        with self.assertRaises(RPNError):
            evaluate("sto 00")

    def test_yx_error(self):
        """0 elevado a negativo debe lanzar RPNError."""
        with self.assertRaises(RPNError):
            evaluate("0 -1 yx")


class TestStackCommands(unittest.TestCase):
    """Tests para comandos de pila."""

    def test_dup(self):
        self.assertEqual(evaluate("5 dup +"), 10)

    def test_swap(self):
        self.assertEqual(evaluate("3 7 swap -"), 4)   # 7 - 3

    def test_drop(self):
        self.assertEqual(evaluate("5 3 drop"), 5)

    def test_clear(self):
        with self.assertRaises(RPNError):
            evaluate("1 2 3 clear")  # pila vacía al final

    def test_dup_insufficient(self):
        with self.assertRaises(RPNError):
            evaluate("dup")

    def test_swap_insufficient(self):
        with self.assertRaises(RPNError):
            evaluate("3 swap")

    def test_drop_insufficient(self):
        with self.assertRaises(RPNError):
            evaluate("drop")


class TestConstants(unittest.TestCase):
    """Tests para constantes predefinidas."""

    def test_pi(self):
        self.assertAlmostEqual(evaluate("p"), math.pi)

    def test_euler(self):
        self.assertAlmostEqual(evaluate("e"), math.e)

    def test_phi(self):
        expected = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(evaluate("j"), expected)


class TestMathFunctions(unittest.TestCase):
    """Tests para funciones matemáticas."""

    def test_sqrt(self):
        self.assertAlmostEqual(evaluate("9 sqrt"), 3.0)

    def test_log(self):
        self.assertAlmostEqual(evaluate("100 log"), 2.0)

    def test_ln(self):
        self.assertAlmostEqual(evaluate("e ln"), 1.0)

    def test_ex(self):
        self.assertAlmostEqual(evaluate("1 ex"), math.e)

    def test_10x(self):
        self.assertAlmostEqual(evaluate("2 10x"), 100.0)

    def test_1_over_x(self):
        self.assertAlmostEqual(evaluate("4 1/x"), 0.25)

    def test_chs(self):
        self.assertEqual(evaluate("5 chs"), -5)

    def test_yx(self):
        self.assertAlmostEqual(evaluate("2 10 yx"), 1024.0)

    def test_yx_insufficient_stack(self):
        with self.assertRaises(RPNError):
            evaluate("2 yx")


class TestTrigonometry(unittest.TestCase):
    """Tests para funciones trigonométricas (en grados)."""

    def test_sin_90(self):
        self.assertAlmostEqual(evaluate("90 sin"), 1.0)

    def test_cos_0(self):
        self.assertAlmostEqual(evaluate("0 cos"), 1.0)

    def test_tg_45(self):
        self.assertAlmostEqual(evaluate("45 tg"), 1.0)

    def test_asin(self):
        self.assertAlmostEqual(evaluate("1 asin"), 90.0)

    def test_acos(self):
        self.assertAlmostEqual(evaluate("1 acos"), 0.0)

    def test_atg(self):
        self.assertAlmostEqual(evaluate("1 atg"), 45.0)


class TestMemory(unittest.TestCase):
    """Tests para comandos STO/RCL."""

    def test_sto_rcl(self):
        """Guarda 42 en memoria 03, descarta el original y recupera con RCL."""
        self.assertEqual(evaluate("42 sto 03 drop rcl 03"), 42)

    def test_sto_does_not_consume(self):
        """STO no debe consumir el valor de la pila."""
        self.assertEqual(evaluate("7 sto 01"), 7)

    def test_rcl_default_zero(self):
        """Las memorias arrancan en 0."""
        self.assertEqual(evaluate("0 rcl 05 +"), 0)

    def test_sto_single_digit_register(self):
        """Registro '5' se interpreta como '05'."""
        self.assertEqual(evaluate("99 sto 5 drop rcl 5"), 99)


class TestCaseInsensitive(unittest.TestCase):
    """Los tokens deben ser insensibles a mayúsculas."""

    def test_uppercase_ops(self):
        self.assertAlmostEqual(evaluate("9 SQRT"), 3.0)

    def test_mixed_case(self):
        self.assertAlmostEqual(evaluate("45 TG"), 1.0)


if __name__ == "__main__":
    unittest.main()