#Genere una clase donde se instancie una comida rápida “hamburguesa” que
#pueda ser entregada en mostrador, retirada por el cliente o enviada por
#delivery. A los efectos prácticos bastará que la clase imprima el método de
#entrega.

from abc import ABC, abstractmethod

class Hamburguesa(ABC):
    def __init__(self, metodo_entrega):
        self.metodo_entrega = metodo_entrega

    @abstractmethod
    def entregar(self):
        pass

class HamburguesaMostrador(Hamburguesa):
    def entregar(self):
        print(f"La hamburguesa será entregada en mostrador")

class HamburguesaRetirada(Hamburguesa):
    def entregar(self):
        print(f"La hamburguesa será retirada por el cliente")

class HamburguesaDelivery(Hamburguesa):
    def entregar(self):
        print(f"La hamburguesa será enviada por delivery")

class HamburguesaFactory:
    @staticmethod
    def crear_hamburguesa(metodo_entrega):
        if metodo_entrega == "mostrador":
            return HamburguesaMostrador(metodo_entrega)
        elif metodo_entrega == "retirada":
            return HamburguesaRetirada(metodo_entrega)
        elif metodo_entrega == "delivery":
            return HamburguesaDelivery(metodo_entrega)
        else:
            raise ValueError("Método de entrega no válido")     
# Ejemplo de uso
if __name__ == "__main__":
    metodo_entrega = "delivery"
    hamburguesa = HamburguesaFactory.crear_hamburguesa(metodo_entrega)
    hamburguesa.entregar()  