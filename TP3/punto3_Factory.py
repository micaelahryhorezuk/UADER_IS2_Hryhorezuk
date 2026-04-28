#Genere una clase donde se instancie una comida rápida “hamburguesa” que
#pueda ser entregada en mostrador, retirada por el cliente o enviada por
#delivery. A los efectos prácticos bastará que la clase imprima el método de
#entrega.

from abc import ABC, abstractmethod #importación de módulos necesarios para definir clases abstractas y métodos abstractos

class Hamburguesa(ABC): # clase abstracta para representar una hamburguesa con un método de entrega
    def __init__(self, metodo_entrega): 
        self.metodo_entrega = metodo_entrega

    @abstractmethod # definición del método abstracto entregar que debe ser implementado por las clases concretas que hereden de Hamburguesa
    def entregar(self):
        pass

class HamburguesaMostrador(Hamburguesa):  # clase concreta que representa una hamburguesa entregada en mostrador, hereda de Hamburguesa e implementa el método entregar
    def entregar(self):
        print(f"La hamburguesa será entregada en mostrador")

class HamburguesaRetirada(Hamburguesa): # clase concreta que representa una hamburguesa retirada por el cliente, hereda de Hamburguesa e implementa el método entregar
    def entregar(self):
        print(f"La hamburguesa será retirada por el cliente")

class HamburguesaDelivery(Hamburguesa): # clase concreta que representa una hamburguesa enviada por delivery, hereda de Hamburguesa e implementa el método entregar
    def entregar(self):
        print(f"La hamburguesa será enviada por delivery")

class HamburguesaFactory: # clase factory para crear instancias de hamburguesas según el método de entrega especificado
    @staticmethod
    def crear_hamburguesa(metodo_entrega):  # método estático para crear una hamburguesa según el método de entrega recibido como argumento
        if metodo_entrega == "mostrador":
            return HamburguesaMostrador(metodo_entrega)
        elif metodo_entrega == "retirada":
            return HamburguesaRetirada(metodo_entrega)
        elif metodo_entrega == "delivery":
            return HamburguesaDelivery(metodo_entrega)
        else:
            raise ValueError("Método de entrega no válido")     
# Ejemplo de uso
if __name__ == "__main__": # bloque de código para probar la clase HamburguesaFactory y las clases concretas de hamburguesas
    metodo_entrega = "delivery"
    hamburguesa = HamburguesaFactory.crear_hamburguesa(metodo_entrega)
    hamburguesa.entregar()  