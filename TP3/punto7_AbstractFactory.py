#Imagine una situación donde pueda ser de utilidad el patrón “abstract factory”.
# Sistema de Notificaciones: Una app necesita notificar al usuario, pero según 
# la plataforma usa Email o SMS. Cada plataforma tiene su propio formato de mensaje y su propio enviador,no podés mezclarlos.


from abc import ABC, abstractmethod

# Productos abstractos 
class Mensaje(ABC):
    @abstractmethod
    def formatear(self, texto: str) -> str:
        pass

class Enviador(ABC):
    @abstractmethod
    def enviar(self, destino: str, contenido: str):
        pass


# Familia Email 
class MensajeEmail(Mensaje):
    def formatear(self, texto: str) -> str:
        return f"Asunto: Notificación\n\nEstimado usuario,\n{texto}\n\nSaludos."

class EnviadorEmail(Enviador):
    def enviar(self, destino: str, contenido: str):
        print(f"Enviando email a {destino}:\n{contenido}\n")


#Familia SMS 
class MensajeSMS(Mensaje):
    def formatear(self, texto: str) -> str:
        # SMS tiene límite de caracteres, va corto
        return f"[NOTIF] {texto[:50]}"

class EnviadorSMS(Enviador):
    def enviar(self, destino: str, contenido: str):
        print(f" Enviando SMS a {destino}: {contenido}\n")


#  Abstract Factory 
class NotificacionFactory(ABC):
    @abstractmethod
    def crear_mensaje(self) -> Mensaje:
        pass

    @abstractmethod
    def crear_enviador(self) -> Enviador:
        pass


# Factories concretas 
class EmailFactory(NotificacionFactory):
    def crear_mensaje(self) -> Mensaje:
        return MensajeEmail()

    def crear_enviador(self) -> Enviador:
        return EnviadorEmail()


class SMSFactory(NotificacionFactory):
    def crear_mensaje(self) -> Mensaje:
        return MensajeSMS()

    def crear_enviador(self) -> Enviador:
        return EnviadorSMS()


#  Cliente 
class SistemaNotificaciones:
    """
    No sabe si usa Email o SMS.
    Solo trabaja con la factory abstracta.
    """

    def __init__(self, factory: NotificacionFactory):
        self.mensaje  = factory.crear_mensaje()
        self.enviador = factory.crear_enviador()

    def notificar(self, destino: str, texto: str):
        contenido = self.mensaje.formatear(texto)
        self.enviador.enviar(destino, contenido)


# Prueba 
if __name__ == "__main__":
    texto = "Su pedido ha sido confirmado exitosamente."

    print("=== Notificación por Email ===")
    sistema = SistemaNotificaciones(EmailFactory())
    sistema.notificar("usuario@mail.com", texto)

    print("=== Notificación por SMS ===")
    sistema = SistemaNotificaciones(SMSFactory())
    sistema.notificar("+5493442000000", texto)