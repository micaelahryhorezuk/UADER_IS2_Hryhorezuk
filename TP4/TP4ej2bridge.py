#Para un producto láminas de acero de 0.5” de espesor y 1,5 metros de ancho
#dispone de dos trenes laminadores, uno que genera planchas de 5 mts y otro
#de 10 mts. Genere una clase que represente a las láminas en forma genérica al
#cual se le pueda indicar que a que tren laminador se enviará a producir. (Use el
#patrón bridge en la solución).
"""
TP4 - Ejercicio 2: Patrón Bridge
Abstracción: LaminaAcero
Implementación: TrenLaminador (TrenLaminador5m, TrenLaminador10m)
"""

from abc import ABC, abstractmethod


# IMPLEMENTACIÓN (lado del "bridge") 
class TrenLaminador(ABC):
    """Interfaz de implementación."""

    @abstractmethod
    def producir(self, espesor: float, ancho: float):
        pass


class TrenLaminador5m(TrenLaminador):
    def producir(self, espesor: float, ancho: float):
        print(f"  [Tren 5m]  Produciendo plancha de {espesor}\" x {ancho}m x 5m")


class TrenLaminador10m(TrenLaminador):
    def producir(self, espesor: float, ancho: float):
        print(f"  [Tren 10m] Produciendo plancha de {espesor}\" x {ancho}m x 10m")


#ABSTRACCIÓN
class LaminaAcero:
    """
    Representa una lámina de acero genérica.
    El 'bridge' conecta esta clase con el tren laminador elegido.
    """

    def __init__(self, espesor: float, ancho: float, tren: TrenLaminador):
        self.espesor = espesor   # pulgadas
        self.ancho = ancho       # metros
        self._tren = tren

    def set_tren(self, tren: TrenLaminador):
        """Permite cambiar el tren en tiempo de ejecución."""
        self._tren = tren

    def producir(self):
        print(f"Lámina de acero ({self.espesor}\" espesor, {self.ancho}m ancho):")
        self._tren.producir(self.espesor, self.ancho)


# 
# Demo
# 
if __name__ == "__main__":
    tren5  = TrenLaminador5m()
    tren10 = TrenLaminador10m()

    lamina = LaminaAcero(espesor=0.5, ancho=1.5, tren=tren5)

    print("=" * 45)
    print("Producción con Tren 5m:")
    lamina.producir()

    print("\nCambiando al Tren 10m en tiempo de ejecución:")
    lamina.set_tren(tren10)
    lamina.producir()
    print("=" * 45)