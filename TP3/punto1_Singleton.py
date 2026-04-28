#Provea una clase que dado un número entero cualquiera retorne el factorial del
#mismo, debe asegurarse que todas las clases que lo invoquen utilicen la misma
#instancia de clase.

import sys

class Factorial: # clase singleton para calcular factoriales
    _instance = None # variable de clase para almacenar la instancia única

    def __new__(cls): #definición del método __new__ para controlar la creación de instancias
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def calculate(self, n): # método para calcular el factorial de un número entero n
        if n == 0:
            return 1
        else:
            return n * self.calculate(n-1)

# ejemplo de uso
if __name__ == "__main__": # bloque de código para probar la clase Factorial
    factorial = Factorial()
    print(factorial.calculate(5))  # Output: 120