#Provea una clase que dado un número entero cualquiera retorne el factorial del
#mismo, debe asegurarse que todas las clases que lo invoquen utilicen la misma
#instancia de clase.

import sys

class Factorial:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def calculate(self, n):
        if n == 0:
            return 1
        else:
            return n * self.calculate(n-1)

# ejemplo de uso
if __name__ == "__main__":
    factorial = Factorial()
    print(factorial.calculate(5))  # Output: 120