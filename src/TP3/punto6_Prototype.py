#Dado una clase que implemente el patrón “prototipo” verifique que una clase
#generada a partir de ella permite por su parte obtener también copias de si misma.
import copy 
from abc import ABC, abstractmethod
class Prototipo(ABC):
    @abstractmethod
    def clonar(self):
        pass
class PrototipoConcreto(Prototipo):
    def __init__(self, valor):
        self.valor = valor

    def clonar(self):
        return copy.deepcopy(self)
    def __str__(self):
        return f"PrototipoConcreto con valor: {self.valor}"
def main():
    prototipo1 = PrototipoConcreto(10)
    print(prototipo1)  # Output: PrototipoConcreto con valor: 10

    prototipo2 = prototipo1.clonar()
    print(prototipo2)  # Output: PrototipoConcreto con valor: 10

    # Modificar el valor del prototipo2 para verificar que es una copia independiente
    prototipo2.valor = 20
    print(prototipo1)  # Output: PrototipoConcreto con valor: 10
    print(prototipo2)  # Output: PrototipoConcreto con valor: 20
if __name__ == "__main__":
    main()  