#Represente la lista de piezas componentes de un ensamblado con sus
#relaciones jerárquicas. Empiece con un producto principal formado por tres
#sub-conjuntos los que a su vez tendrán cuatro piezas cada uno. Genere clases
#que representen esa configuración y la muestren. Luego agregue un subconjunto opcional adicional también formado por cuatro piezas. 
#(Use el patróncomposite).
"""
TP4 - Ejercicio 3: Patrón Composite
Componente base: ComponenteEnsamblado
Hoja:            Pieza
Compuesto:       Subconjunto / ProductoPrincipal
"""

from abc import ABC, abstractmethod


# COMPONENTE BASE 
class ComponenteEnsamblado(ABC):
    @abstractmethod
    def mostrar(self, nivel: int = 0):
        pass


#HOJA 
class Pieza(ComponenteEnsamblado):
    def __init__(self, nombre: str):
        self.nombre = nombre

    def mostrar(self, nivel: int = 0):
        print("  " * nivel + f"[Pieza] {self.nombre}")


# COMPUESTO 
class Subconjunto(ComponenteEnsamblado):
    def __init__(self, nombre: str, opcional: bool = False):
        self.nombre = nombre
        self.opcional = opcional
        self._hijos: list[ComponenteEnsamblado] = []

    def agregar(self, componente: ComponenteEnsamblado):
        self._hijos.append(componente)
        return self   # para encadenado fluido

    def mostrar(self, nivel: int = 0):
        etiqueta = " (opcional)" if self.opcional else ""
        print("  " * nivel + f"[Subconjunto] {self.nombre}{etiqueta}")
        for hijo in self._hijos:
            hijo.mostrar(nivel + 1)


class ProductoPrincipal(ComponenteEnsamblado):
    def __init__(self, nombre: str):
        self.nombre = nombre
        self._subconjuntos: list[ComponenteEnsamblado] = []

    def agregar(self, sub: ComponenteEnsamblado):
        self._subconjuntos.append(sub)
        return self

    def mostrar(self, nivel: int = 0):
        print("  " * nivel + f"[Producto] {self.nombre}")
        for sub in self._subconjuntos:
            sub.mostrar(nivel + 1)


# 
# Demo
# 
if __name__ == "__main__":
    # Tres subconjuntos base, 4 piezas cada uno
    sub1 = Subconjunto("Subconjunto A")
    for i in range(1, 5):
        sub1.agregar(Pieza(f"Pieza A{i}"))

    sub2 = Subconjunto("Subconjunto B")
    for i in range(1, 5):
        sub2.agregar(Pieza(f"Pieza B{i}"))

    sub3 = Subconjunto("Subconjunto C")
    for i in range(1, 5):
        sub3.agregar(Pieza(f"Pieza C{i}"))

    producto = ProductoPrincipal("Producto Principal")
    producto.agregar(sub1).agregar(sub2).agregar(sub3)

    print("=" * 45)
    print("Ensamblado base (3 subconjuntos):")
    print("=" * 45)
    producto.mostrar()

    # Subconjunto opcional adicional
    sub_opt = Subconjunto("Subconjunto D (extra)", opcional=True)
    for i in range(1, 5):
        sub_opt.agregar(Pieza(f"Pieza D{i}"))

    producto.agregar(sub_opt)

    print("\n" + "=" * 45)
    print("Ensamblado con subconjunto opcional agregado:")
    print("=" * 45)
    producto.mostrar()