#Cree una clase bajo el patrón cadena de responsabilidad donde los números del
#1 al 100 sean pasados a las clases subscriptas en secuencia, aquella que
#identifique la necesidad de consumir el número lo hará y caso contrario lo
#pasará al siguiente en la cadena. Implemente una clase que consuma números
#primos y otra números pares. Puede ocurrir que un número no sea consumido
#por ninguna clase en cuyo caso se marcará como no consumido.

from abc import ABC, abstractmethod
class Handler(ABC):   #Clase abstracta que define la interfaz para manejar las solicitudes
    def __init__(self, successor=None):
        self._successor = successor

    @abstractmethod
    def handle(self, number): #Método abstracto que debe ser implementado por las clases concretas para manejar la solicitud
        pass    #pass es una declaración vacía que se utiliza como marcador de posición para el código que aún no se ha implementado.


class PrimeHandler(Handler):   #Clase concreta que maneja números primos
    def handle(self, number):
        if self.is_prime(number):
            print(f"{number} es un número primo.")
        elif self._successor:
            self._successor.handle(number)
        else:
            print(f"{number} no fue consumido por ninguna clase.")

    def is_prime(self, number): #Función para verificar si un número es primo
        if number <= 1:
            return False
        for i in range(2, int(number**0.5) + 1):
            if number % i == 0:
                return False
        return True

class EvenHandler(Handler):    #Clase concreta que maneja números pares
    def handle(self, number):
        if number % 2 == 0:
            print(f"{number} es un número par.")
        elif self._successor:  #Si el número no es par, se pasa al siguiente manejador en la cadena
            self._successor.handle(number)
        else:
            print(f"{number} no fue consumido por ninguna clase.")

if __name__ == "__main__":
    # Cadena: primero PrimeHandler, luego EvenHandler
    chain = PrimeHandler(successor=EvenHandler())

    for number in range(1, 101): #Itera a través de los números del 1 al 100 y los pasa a la cadena de responsabilidad
        chain.handle(number)
