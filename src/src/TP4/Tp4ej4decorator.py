#Implemente una clase que permita a un número cualquiera imprimir su valor,
#luego agregarle sucesivamente.
#a. Sumarle 2.
#b. Multiplicarle por 2.
#c. Dividirlo por 3.
#Mostrar los resultados de la clase sin agregados y con la invocación anidada a
#las clases con las diferentes operaciones. Use un patrón decorator para implementar.



#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones Estructurales
#* Decorator - TP4 Ejercicio 4
#*------------------------------------------------------------------------

from abc import ABC, abstractmethod


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


class DecoradorNumero(NumeroBase):
    def __init__(self, envuelto: NumeroBase):
        self._envuelto = envuelto

    def obtener(self) -> float:
        return self._envuelto.obtener()


class SumarDos(DecoradorNumero):
    def obtener(self) -> float:
        return self._envuelto.obtener() + 2


class MultiplicarPorDos(DecoradorNumero):
    def obtener(self) -> float:
        return self._envuelto.obtener() * 2


class DividirPorTres(DecoradorNumero):
    def obtener(self) -> float:
        return self._envuelto.obtener() / 3


if __name__ == "__main__":
    base = Numero(6)

    print("=" * 45)
    print("Número base (sin decoradores):")
    base.imprimir()

    print("\nSolo +2:")
    SumarDos(base).imprimir()

    print("\nSolo x2:")
    MultiplicarPorDos(base).imprimir()

    print("\nSolo /3:")
    DividirPorTres(base).imprimir()

    print("\n--- Composición anidada ---")

    comp1 = DividirPorTres(MultiplicarPorDos(SumarDos(base)))
    print("((6 + 2) x 2) / 3 =")
    comp1.imprimir()

    comp2 = DividirPorTres(SumarDos(MultiplicarPorDos(base)))
    print("\n((6 x 2) + 2) / 3 =")
    comp2.imprimir()

    comp3 = SumarDos(MultiplicarPorDos(DividirPorTres(base)))
    print("\n((6 / 3) x 2) + 2 =")
    comp3.imprimir()
    print("=" * 45)
