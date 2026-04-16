"""
rpn.py - Calculadora RPN (Reverse Polish Notation)
Soporta operaciones básicas, funciones matemáticas, trigonometría,
comandos de pila, constantes, memorias y manejo de errores.
nano rpn.py"""

import math
import sys

# ── Operadores binarios soportados: suma, resta, multiplicación, división ────
# ── Funciones unarias: raíz, logaritmos, exponencial, trigonometría, signo ───
# ── Comandos de pila: dup (duplicar), swap (intercambiar), drop, clear ────────
# ── Constantes: p=pi, e=Euler, j=phi (número áureo) ─────────────────────────
# ── Memorias: 10 registros '00'-'09' accesibles con STO y RCL ────────────────

# ── Constantes disponibles como tokens ──────────────────────────────────────
CONSTANTS = {
    "p": math.pi,  # pi
    "e": math.e,  # número de Euler
    "j": (1 + math.sqrt(5)) / 2,  # phi (número áureo)
}

# ── Conversión de grados a radianes y viceversa ──────────────────────────────
DEG = math.pi / 180


class RPNError(Exception):
    """Excepción propia para errores de la calculadora RPN."""


def _require(stack: list, n: int) -> None:
    """Verifica que la pila tenga al menos n elementos."""
    if len(stack) < n:
        raise RPNError(
            f"Pila insuficiente: se necesitan {n} elemento(s), hay {len(stack)}"
        )


def _apply_binary(stack: list, op: str) -> None:
    """Aplica una operación binaria (+, -, *, /) a los dos topes de la pila."""
    _require(stack, 2)
    # En RPN: se apila a luego b, y se opera a op b
    b, a = stack.pop(), stack.pop()  # 'a op b' en notación RPN
    if op == "+":
        stack.append(a + b)
    elif op == "-":
        stack.append(a - b)
    elif op == "*":
        stack.append(a * b)
    elif op == "/":
        if b == 0:
            raise RPNError("División por cero")
        stack.append(a / b)


def _apply_unary(stack: list, op: str) -> None:
    """Aplica una función unaria al tope de la pila."""
    _require(stack, 1)
    x = stack.pop()
    try:
        if op == "sqrt":
            # Raíz cuadrada
            if x < 0:
                raise RPNError("sqrt de número negativo")
            stack.append(math.sqrt(x))
        elif op == "log":
            # Logaritmo base 10
            if x <= 0:
                raise RPNError("log de número no positivo")
            stack.append(math.log10(x))
        elif op == "ln":
            # Logaritmo natural
            if x <= 0:
                raise RPNError("ln de número no positivo")
            stack.append(math.log(x))
        elif op == "ex":
            # e elevado a x
            stack.append(math.exp(x))
        elif op == "10x":
            # 10 elevado a x
            stack.append(10**x)
        elif op == "1/x":
            # Inverso multiplicativo
            if x == 0:
                raise RPNError("Inverso de cero indefinido")
            stack.append(1 / x)
        elif op == "chs":
            # Cambio de signo (Change Sign)
            stack.append(-x)
        elif op == "sin":
            # Seno: convierte grados a radianes antes del cálculo
            stack.append(math.sin(x * DEG))
        elif op == "cos":
            # Coseno: entrada en grados
            stack.append(math.cos(x * DEG))
        elif op == "tg":
            # Tangente: entrada en grados
            stack.append(math.tan(x * DEG))
        elif op == "asin":
            # Arcoseno: resultado convertido a grados
            stack.append(math.asin(x) / DEG)
        elif op == "acos":
            # Arcocoseno: resultado en grados
            stack.append(math.acos(x) / DEG)
        elif op == "atg":
            # Arcotangente: resultado en grados
            stack.append(math.atan(x) / DEG)
        else:
            stack.append(x)  # no debería llegar aquí
    except ValueError as exc:
        raise RPNError(f"Error matemático en '{op}': {exc}") from exc


def _apply_yx(stack: list) -> None:
    """Eleva y (segundo elemento) a la x (tope): y^x."""
    _require(stack, 2)
    x, y = stack.pop(), stack.pop()  # x es el exponente, y la base
    try:
        stack.append(y**x)
    except (ValueError, ZeroDivisionError) as exc:
        raise RPNError(f"Error en yx: {exc}") from exc


def _apply_stack_cmd(stack: list, cmd: str) -> None:
    """Ejecuta comandos de manipulación de pila: dup, swap, drop, clear."""
   # dup: duplica el tope; swap: intercambia los dos topes
    # drop: descarta el tope; clear: vacía la pila
    if cmd == "dup":
        _require(stack, 1)
        stack.append(stack[-1])
    elif cmd == "swap":
        _require(stack, 2)
        stack[-1], stack[-2] = stack[-2], stack[-1]
    elif cmd == "drop":
        _require(stack, 1)
        stack.pop()
    elif cmd == "clear":
        stack.clear()


def evaluate(expression: str) -> float:
    """
    Evalúa una expresión RPN y devuelve el resultado.
    Lanza RPNError si la expresión es inválida.
    """
    stack: list[float] = []  # pila principal de operandos
    # Memorias: 10 registros nombrados '00' a '09'
    memory: dict[str, float] = {f"{i:02d}": 0.0 for i in range(10)}

    # Conjuntos de tokens reconocidos
    # Operadores que consumen dos operandos
    binary_ops = {"+", "-", "*", "/"}
    unary_ops = {
        "sqrt",
        "log",
        "ln",
        "ex",
        "10x",
        "1/x",
        "chs",
        "sin",
        "cos",
        "tg",
        "asin",
        "acos",
        "atg",
    }
    # Comandos de manipulación de pila sin operación aritmética
    stack_cmds = {"dup", "swap", "drop", "clear"}

    # Tokenizar: dividir la expresión por espacios
    tokens = expression.split()
    i = 0  # índice de posición en la lista de tokens
    while i < len(tokens):
        token = tokens[i].lower()

        # ── Número: se intenta convertir a float; si falla, es otro token ────
        try:
            stack.append(float(token))
            i += 1
            continue
        except ValueError:
            pass

        # ── Constante ───────────────────────────────────────────────────────
        if token in CONSTANTS:
            stack.append(CONSTANTS[token])

        # ── Operación binaria ────────────────────────────────────────────────
        elif token in binary_ops:
            _apply_binary(stack, token)

        # ── Función unaria ───────────────────────────────────────────────────
        elif token in unary_ops:
            _apply_unary(stack, token)

        # ── yx (potencia) ────────────────────────────────────────────────────
        elif token == "yx":
            _apply_yx(stack)

        # ── Comandos de pila ─────────────────────────────────────────────────
        elif token in stack_cmds:
            _apply_stack_cmd(stack, token)

        # ── STO nn: almacena tope en memoria nn ──────────────────────────────
        elif token == "sto":
            i += 1
            if i >= len(tokens):
                raise RPNError("STO requiere un número de memoria (00-09)")
            reg = tokens[i].zfill(2)
            if reg not in memory:
                raise RPNError(f"Memoria inválida: '{tokens[i]}' (use 00-09)")
            _require(stack, 1)
            memory[reg] = stack[-1]  # STO no consume el valor

        # ── RCL nn: recupera valor de memoria nn ─────────────────────────────
        elif token == "rcl":
            i += 1
            if i >= len(tokens):
                raise RPNError("RCL requiere un número de memoria (00-09)")
            reg = tokens[i].zfill(2)
            if reg not in memory:
                raise RPNError(f"Memoria inválida: '{tokens[i]}' (use 00-09)")
            stack.append(memory[reg])

        # ── Token desconocido ────────────────────────────────────────────────
        else:
            raise RPNError(f"Token inválido: '{token}'")

        i += 1

    # ── Validación final ─────────────────────────────────────────────────────
    if len(stack) != 1:
        raise RPNError(
            f"La expresión debe dejar exactamente 1 valor en la pila, "
            f"quedaron {len(stack)}: {stack}"
        )
    return stack[0]


def main() -> None:
    """Punto de entrada: acepta expresión por argumento o modo interactivo."""
    if len(sys.argv) > 1:
        # Modo argumento: expresión pasada directamente
        expression = " ".join(sys.argv[1:])
        try:
            result = evaluate(expression)
            print(int(result) if result == int(result) else result)
        except RPNError as err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        # Modo interactivo: loop hasta que el usuario escriba exit o quit
        print("Calculadora RPN — escribí 'exit' para salir")
        while True:
            try:
                expression = input("RPN> ").strip()
                if expression.lower() in ("exit", "quit"):
                    break
                if not expression:
                    continue
                result = evaluate(expression)
                print(int(result) if result == int(result) else result)
            except RPNError as err:
                print(f"Error: {err}", file=sys.stderr)


if __name__ == "__main__":
    main()



