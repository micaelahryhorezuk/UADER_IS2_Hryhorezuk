#implemente una clase que permita a un número cualquiera imprimir su valor,
#luego agregarle sucesivamente.
#a. Sumarle 2.
#b. Multiplicarle por 2.
#c. Dividirlo por 3.
"""
TP4 - Ejercicio 4: Patrón Decorator
Componente base: Numero
Decoradores:     SumarDos, MultiplicarPorDos, DividirPorTres
"""

from abc import ABC, abstractmethod


# COMPONENTE BASE
class NumeroBase(ABC):
    @abstractmethod
    def obtener(self) -> float:
        pass

    def imprimir(self):
        print(f"  Valor: {self.obtener()}")


class Numero(NumeroBase):
    def __init__(self, valor: float):
        self._valor = valor

    def obtener(self) -> float:
        return self._valor


# DECORADOR ABSTRACTO 
class DecoradorNumero(NumeroBase):
    def __init__(self, envuelto: NumeroBase):
        self._envuelto = envuelto

    def obtener(self) -> float:
        return self._envuelto.obtener()


# DECORADORES CONCRETOS
class SumarDos(DecoradorNumero):
    def obtener(self) -> float:
        return self._envuelto.obtener() + 2


class MultiplicarPorDos(DecoradorNumero):
    def obtener(self) -> float:
        return self._envuelto.obtener() * 2


class DividirPorTres(DecoradorNumero):
    def obtener(self) -> float:
        return self._envuelto.obtener() / 3


# 
# Demo
# 
if __name__ == "__main__":
    base = Numero(6)

    print("=" * 45)
    print(f"Número base (sin decoradores):")
    base.imprimir()

    print("\nSolo +2:")
    SumarDos(base).imprimir()

    print("\nSolo ×2:")
    MultiplicarPorDos(base).imprimir()

    print("\nSolo ÷3:")
    DividirPorTres(base).imprimir()

    print("\n--- Composición anidada ---")

    # +2 luego ×2 luego ÷3  →  ((6+2)*2)/3 = 16/3 ≈ 5.33
    comp1 = DividirPorTres(MultiplicarPorDos(SumarDos(base)))
    print(f"((6 + 2) × 2) ÷ 3 =")
    comp1.imprimir()

    # ×2 luego +2 luego ÷3  →  ((6*2)+2)/3 = 14/3 ≈ 4.67
    comp2 = DividirPorTres(SumarDos(MultiplicarPorDos(base)))
    print(f"\n((6 × 2) + 2) ÷ 3 =")
    comp2.imprimir()

    # Todos anidados al revés: ÷3 luego ×2 luego +2
    comp3 = SumarDos(MultiplicarPorDos(DividirPorTres(base)))
    print(f"\n((6 ÷ 3) × 2) + 2 =")
    comp3.imprimir()
    print("=" * 45)