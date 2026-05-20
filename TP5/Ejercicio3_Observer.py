#Implemente una clase bajo el patrón observer donde una serie de clases están
#subscriptas, cada clase espera que su propio ID (una secuencia arbitraria de 4
#caracteres) sea expuesta y emitirá un mensaje cuando el ID emitido y el propio
#coinciden. Implemente 4 clases de tal manera que cada una tenga un ID
#especifico. Emita 8 ID asegurándose que al menos cuatro de ellos coincidan con
#ID para el que tenga una clase implementada.

from abc import ABC, abstractmethod


class Observador(ABC):
    @abstractmethod
    def actualizar(self, id_emitido: str) -> None:
        pass


class EmisorID:             
    """Sujeto: emite IDs y notifica a todos los observadores subscriptos."""

    def __init__(self):
        self._observadores: list[Observador] = []   #Lista de observadores subscriptos

    def agregar_observador(self, observador: Observador) -> None:
        self._observadores.append(observador)

    def emitir(self, id_emitido: str) -> None: #Emite un ID y notifica a todos los observadores, indicando si fue consumido o no
        print(f"\n[EMISOR] Emitiendo ID: {id_emitido}")
        consumido = False
        for observador in self._observadores: #Notifica a cada observador y verifica si alguno lo consume
            if observador.actualizar(id_emitido):
                consumido = True
        if not consumido:
            print(f"  -> ID '{id_emitido}' no fue consumido por ninguna clase.")

#cada clase usa un ID específico y verifica si el ID emitido coincide con el suyo para decidir si lo consume o no.
# Si el ID coincide, imprime un mensaje indicando que fue consumido; de lo contrario, devuelve False para indicar que no fue consumido.
class ClaseA(Observador):
    ID = "AA01"

    def actualizar(self, id_emitido: str) -> bool:
        if id_emitido == self.ID:
            print(f"  [ClaseA] ID '{id_emitido}' coincide con mi ID '{self.ID}'. ¡Consumido!")
            return True
        return False


class ClaseB(Observador):
    ID = "BB02"

    def actualizar(self, id_emitido: str) -> bool:
        if id_emitido == self.ID:
            print(f"  [ClaseB] ID '{id_emitido}' coincide con mi ID '{self.ID}'. ¡Consumido!")
            return True
        return False


class ClaseC(Observador):
    ID = "CC03"

    def actualizar(self, id_emitido: str) -> bool:
        if id_emitido == self.ID:
            print(f"  [ClaseC] ID '{id_emitido}' coincide con mi ID '{self.ID}'. ¡Consumido!")
            return True
        return False


class ClaseD(Observador):
    ID = "DD04"

    def actualizar(self, id_emitido: str) -> bool:
        if id_emitido == self.ID:
            print(f"  [ClaseD] ID '{id_emitido}' coincide con mi ID '{self.ID}'. ¡Consumido!")
            return True
        return False

#En esta parte se crea una instancia del emisor, se agregan los observadores (clases A, B, C y D) y se emiten 8 IDs, 
# de los cuales 4 coinciden con los IDs de las clases implementadas y 4 no, demostrando el funcionamiento del patrón 
# observer.
if __name__ == "__main__":
    emisor = EmisorID()
    emisor.agregar_observador(ClaseA())
    emisor.agregar_observador(ClaseB())
    emisor.agregar_observador(ClaseC())
    emisor.agregar_observador(ClaseD())

    # 8 IDs emitidos: 4 coinciden, 4 no
    ids = ["AA01", "BB02", "CC03", "DD04", "XY99", "ZZ00", "1234", "ABCD"]
    for id_emitido in ids:
        emisor.emitir(id_emitido)
