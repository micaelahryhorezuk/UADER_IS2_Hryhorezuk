#Extienda el ejemplo visto en el taller en clase de forma que se pueda utilizar
#para construir aviones en lugar de vehículos. Para simplificar suponga que un
#avión tiene un “body”, 2 turbinas, 2 alas y un tren de aterrizaje.

from __future__ import annotations
from abc import ABC, abstractmethod
class Avion:
    def __init__(self):
        self.body = None
        self.turbinas = []
        self.alas = []
        self.tren_aterrizaje = None

    def __str__(self):
        return f"Avion con body: {self.body}, turbinas: {self.turbinas}, alas: {self.alas}, tren de aterrizaje: {self.tren_aterrizaje}"
class AvionBuilder(ABC):
    @abstractmethod
    def build_body(self):
        pass

    @abstractmethod
    def build_turbinas(self):
        pass

    @abstractmethod
    def build_alas(self):
        pass

    @abstractmethod
    def build_tren_aterrizaje(self):
        pass

    @abstractmethod
    def get_avion(self) -> Avion:
        pass
class AvionConcretoBuilder(AvionBuilder):   
    def __init__(self):
        self.avion = Avion()

    def build_body(self):
        self.avion.body = "Body de avión"

    def build_turbinas(self):
        self.avion.turbinas = ["Turbina 1", "Turbina 2"]

    def build_alas(self):
        self.avion.alas = ["Ala 1", "Ala 2"]

    def build_tren_aterrizaje(self):
        self.avion.tren_aterrizaje = "Tren de aterrizaje"

    def get_avion(self) -> Avion:
        return self.avion
class Director:
    def __init__(self, builder: AvionBuilder):
        self._builder = builder

    def construct_avion(self):
        self._builder.build_body()
        self._builder.build_turbinas()
        self._builder.build_alas()
        self._builder.build_tren_aterrizaje()
        return self._builder.get_avion()
# Ejemplo de uso
if __name__ == "__main__":
    builder = AvionConcretoBuilder()
    director = Director(builder)
    avion = director.construct_avion()
    print(avion)