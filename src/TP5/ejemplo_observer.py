# Ejemplo práctico de aplicación de patrón observer
#*------------------------------------------------------------------------
#* Ingeniería de Software II
#* Patrones de Creación
#* Observer
#* UADER - Ingeniería de Software II
#* Dr. Pedro E. Colla
#*------------------------------------------------------------------------
"""
Observer es útil cuando un cambio en un objeto debe disparar acciones en otros objetos sin acoplarlos directamente.
Casos típicos:
	interfaces gráficas,
	sistemas de eventos,
	monitoreo,
	logs y auditoría,
	notificaciones,
	actualización de dashboards,
	arquitecturas publish/subscribe.


Observer desacopla al emisor del evento de los objetos que reaccionan al evento.
Un objeto cambia, y todos los interesados (objetos subscriptos) son notificados automáticamente.
"""
from abc import ABC, abstractmethod


class Observador(ABC):
    """Interfaz común para todos los observadores."""

    @abstractmethod
    def actualizar(self, servidor: str, estado: str) -> None:
        pass


class MonitorServidor:
    """
    Sujeto observado.

    Mantiene una lista de observadores y los notifica cuando cambia su estado.
    """

    def __init__(self, nombre: str) -> None:
        self.nombre = nombre
        self._estado = "desconocido"
        self._observadores: list[Observador] = []

    def agregar_observador(self, observador: Observador) -> None:
        self._observadores.append(observador)

    def remover_observador(self, observador: Observador) -> None:
        self._observadores.remove(observador)

    def cambiar_estado(self, nuevo_estado: str) -> None:
        if nuevo_estado == self._estado:
            return

        self._estado = nuevo_estado
        self._notificar()

    def _notificar(self) -> None:
        for observador in self._observadores:
            observador.actualizar(self.nombre, self._estado)


class AlertaConsola(Observador):
    """Observador concreto: muestra alertas en consola."""

    def actualizar(self, servidor: str, estado: str) -> None:
        print(f"[CONSOLA] Servidor {servidor} cambió a estado: {estado}")


class AlertaEmail(Observador):
    """Observador concreto: simula el envío de email."""

    def __init__(self, destinatario: str) -> None:
        self.destinatario = destinatario

    def actualizar(self, servidor: str, estado: str) -> None:
        print(
            f"[EMAIL] Para {self.destinatario}: "
            f"Servidor {servidor} cambió a estado {estado}"
        )


class RegistroLog(Observador):
    """Observador concreto: registra el evento."""

    def actualizar(self, servidor: str, estado: str) -> None:
        print(f"[LOG] Evento registrado: {servidor} -> {estado}")


def main() -> None:
    servidor = MonitorServidor("api-produccion-01")

    consola = AlertaConsola()
    email = AlertaEmail("admin@example.com")
    log = RegistroLog()

    servidor.agregar_observador(consola)
    servidor.agregar_observador(email)
    servidor.agregar_observador(log)

    print("=== Primer cambio de estado ===")
    servidor.cambiar_estado("operativo")

    print("\n=== Segundo cambio de estado ===")
    servidor.cambiar_estado("degradado")

    print("\n=== Se remueve alerta por email ===")
    servidor.remover_observador(email)

    print("\n=== Tercer cambio de estado ===")
    servidor.cambiar_estado("caído")


if __name__ == "__main__":
    main()
