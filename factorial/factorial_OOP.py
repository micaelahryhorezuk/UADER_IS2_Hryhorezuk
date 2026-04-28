#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial_OOP.py                                                        *
#* calcula el factorial usando POO                                         *
#*-------------------------------------------------------------------------*

import sys

class Factorial:

    def __init__(self):
        pass

    def calcular(self, num):
        if num < 0:
            print("Factorial de un número negativo no existe")
            return 0
        elif num == 0:
            return 1
        else:
            fact = 1
            while num > 1:
                fact *= num
                num -= 1
            return fact

    def run(self, min, max):
        for num in range(min, max + 1):
            resultado = self.calcular(num)
            print(f"Factorial {num}! es {resultado}")


# Programa principal
if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Debe informar dos números: min y max")
        sys.exit()

    minimo = int(sys.argv[1])
    maximo = int(sys.argv[2])

    f = Factorial()
    f.run(minimo, maximo)