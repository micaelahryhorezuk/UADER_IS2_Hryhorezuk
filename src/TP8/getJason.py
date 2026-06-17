#!/usr/bin/env python3
"""
getJason.py - Sistema automatizado de pagos con selección balanceada de cuentas.

Descripción:
    Implementa un sistema de pagos que selecciona automáticamente la cuenta
    bancaria desde la cual realizar cada pago, usando enrutamiento balanceado
    entre dos cuentas. Integra los siguientes patrones de diseño:

    - Singleton             : GetJason garantiza una única instancia de acceso
                              al archivo JSON de configuración (sitedata.json).
    - Cadena de Responsabilidad: ManejadorCuenta intenta procesar el pago; si no
                              cuenta con saldo suficiente, delega al siguiente
                              manejador en la cadena.
    - Iterator              : IteradorPagos recorre los pagos realizados en orden
                              cronológico.

Cuentas iniciales:
    token1 → saldo inicial $1000.-
    token2 → saldo inicial $2000.-

Uso:
    python3 getJason.py [archivo_json] [-v]

Argumentos:
    archivo_json  Ruta al JSON con tokens bancarios (default: sitedata.json).
    -v            Muestra la versión del programa.

Versión: 1.2
copyright UADERFCyT-IS2©2024 todos los derechos reservados.
"""

# pylint: disable=invalid-name   # nombre de módulo requerido por la consigna
import json
import sys

VERSION = "1.2"

# Parámetros de simulación
SALDO_TOKEN1 = 1000.0
SALDO_TOKEN2 = 2000.0
MONTO_PAGO = 500.0
NUM_PEDIDOS = 8
ARCHIVO_JSON_DEFAULT = "sitedata.json"


# ---------------------------------------------------------------------------
# Patrón Singleton
# ---------------------------------------------------------------------------

class SingletonMeta(type):  # pylint: disable=too-few-public-methods
    """Metaclase que implementa el patrón Singleton."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class GetJason(metaclass=SingletonMeta):  # pylint: disable=too-few-public-methods
    """
    Singleton para recuperar claves desde un archivo JSON de configuración.

    Garantiza que solo exista una instancia de lectura del archivo durante
    toda la ejecución del programa.
    """

    def __init__(self, archivo_json: str):
        """
        Inicializa la instancia cargando el archivo JSON en memoria.

        Args:
            archivo_json: Ruta al archivo JSON de configuración.

        Raises:
            FileNotFoundError   : Si el archivo no existe.
            json.JSONDecodeError: Si el contenido no es JSON válido.
        """
        self.datos = self._cargar(archivo_json)

    def _cargar(self, archivo_json: str) -> dict:
        """
        Lee y parsea el archivo JSON.

        Args:
            archivo_json: Ruta al archivo JSON.

        Returns:
            Diccionario con el contenido del archivo.
        """
        with open(archivo_json, 'r', encoding='utf-8') as myfile:
            return json.loads(myfile.read())

    def obtener(self, clave: str) -> str:
        """
        Recupera el valor asociado a una clave del JSON.

        Args:
            clave: Nombre de la clave a recuperar.

        Returns:
            Valor (str) asociado a la clave.

        Raises:
            KeyError: Si la clave no existe en el JSON.
        """
        return str(self.datos[clave])


# ---------------------------------------------------------------------------
# Registro de pago
# ---------------------------------------------------------------------------

class RegistroPago:  # pylint: disable=too-few-public-methods
    """Registro inmutable de un pago realizado exitosamente."""

    def __init__(
        self,
        num_pedido: int,
        token: str,
        clave: str,
        monto: float,
    ):
        """
        Crea un registro de pago.

        Args:
            num_pedido: Número identificador del pedido.
            token     : Nombre del token (banco) utilizado.
            clave     : Clave de seguridad del banco.
            monto     : Monto del pago realizado.
        """
        self.num_pedido = num_pedido
        self.token = token
        self.clave = clave
        self.monto = monto

    def __str__(self) -> str:
        return (
            f"Pedido #{self.num_pedido:>3}: "
            f"token={self.token}, "
            f"clave={self.clave}, "
            f"monto=${self.monto:.2f}"
        )


# ---------------------------------------------------------------------------
# Patrón Iterator
# ---------------------------------------------------------------------------

class IteradorPagos:
    """
    Iterador sobre la colección de pagos realizados (patrón Iterator).

    Permite recorrer en orden cronológico todos los registros de pago
    sin exponer la estructura interna de la colección.
    """

    def __init__(self, pagos: list):
        """
        Inicializa el iterador con la lista de pagos.

        Args:
            pagos: Lista de objetos RegistroPago en orden cronológico.
        """
        self._pagos = pagos
        self._indice = 0

    def __iter__(self):
        """Retorna el propio objeto iterador."""
        return self

    def __next__(self) -> RegistroPago:
        """
        Retorna el siguiente pago en la secuencia.

        Returns:
            Próximo RegistroPago de la colección.

        Raises:
            StopIteration: Al agotarse la colección.
        """
        if self._indice >= len(self._pagos):
            raise StopIteration
        pago = self._pagos[self._indice]
        self._indice += 1
        return pago


# ---------------------------------------------------------------------------
# Patrón Cadena de Responsabilidad
# ---------------------------------------------------------------------------

class ManejadorCuenta:
    """
    Manejador de cuenta bancaria (patrón Cadena de Responsabilidad).

    Intenta procesar el pago descontando del saldo disponible. Si el saldo
    es insuficiente, delega la solicitud al siguiente manejador en la cadena.
    """

    def __init__(self, token: str, saldo_inicial: float, lector_json: GetJason):
        """
        Inicializa la cuenta bancaria.

        Args:
            token        : Nombre del token identificador del banco.
            saldo_inicial: Saldo inicial de la cuenta.
            lector_json  : Instancia de GetJason para obtener la clave del token.
        """
        self.token = token
        self.clave = lector_json.obtener(token)
        self.saldo = saldo_inicial
        self._siguiente = None

    def set_siguiente(self, siguiente) -> None:
        """
        Establece el siguiente manejador en la cadena.

        Args:
            siguiente: Próximo ManejadorCuenta a intentar si este no puede procesar.
                       Usar None para indicar el fin de la cadena.
        """
        self._siguiente = siguiente

    def procesar(self, num_pedido: int, monto: float):
        """
        Intenta procesar el pago; si no puede, delega al siguiente manejador.

        Args:
            num_pedido: Número identificador del pedido.
            monto     : Monto a debitar de la cuenta.

        Returns:
            RegistroPago si el pago fue procesado, None si ningún manejador pudo.
        """
        if self.saldo >= monto:
            self.saldo -= monto
            registro = RegistroPago(num_pedido, self.token, self.clave, monto)
            print(registro)
            return registro

        if self._siguiente is not None:
            return self._siguiente.procesar(num_pedido, monto)

        print(
            f"Pedido #{num_pedido:>3}: Sin fondos suficientes "
            f"en ninguna cuenta bancaria."
        )
        return None


# ---------------------------------------------------------------------------
# Procesador de pagos (coordina los patrones)
# ---------------------------------------------------------------------------

class ProcesadorPagos:
    """
    Coordina el sistema de pagos balanceado entre dos cuentas bancarias.

    Aplica enrutamiento alternado: cada pedido se dirige primero a la cuenta
    contraria a la utilizada en el pedido anterior. Si esa cuenta no tiene
    saldo suficiente, la cadena de responsabilidad continúa con la otra.
    """

    def __init__(self, archivo_json: str):
        """
        Inicializa el procesador cargando las dos cuentas bancarias.

        Args:
            archivo_json: Ruta al archivo JSON con los tokens bancarios.
        """
        lector = GetJason(archivo_json)
        self._cuenta1 = ManejadorCuenta("token1", SALDO_TOKEN1, lector)
        self._cuenta2 = ManejadorCuenta("token2", SALDO_TOKEN2, lector)
        self._historial = []
        self._turno = 0  # 0 → intenta cuenta1 primero; 1 → intenta cuenta2 primero

    def pagar(self, num_pedido: int, monto: float) -> bool:
        """
        Procesa un pedido de pago con enrutamiento balanceado.

        Configura la cadena según el turno actual y alterna para el siguiente
        pedido. La cadena garantiza que si la cuenta principal no tiene saldo,
        se intente con la secundaria.

        Args:
            num_pedido: Número identificador del pedido.
            monto     : Monto del pago a realizar.

        Returns:
            True si el pago fue procesado exitosamente, False en caso contrario.
        """
        if self._turno == 0:
            self._cuenta1.set_siguiente(self._cuenta2)
            self._cuenta2.set_siguiente(None)
            inicio = self._cuenta1
        else:
            self._cuenta2.set_siguiente(self._cuenta1)
            self._cuenta1.set_siguiente(None)
            inicio = self._cuenta2

        self._turno = (self._turno + 1) % 2

        registro = inicio.procesar(num_pedido, monto)
        if registro is not None:
            self._historial.append(registro)
        return registro is not None

    def listar(self) -> None:
        """
        Muestra todos los pagos realizados en orden cronológico.

        Utiliza el patrón Iterator (IteradorPagos) para recorrer el historial.
        """
        print("\n=== Listado cronológico de pagos realizados ===")
        iterador = IteradorPagos(self._historial)
        for pago in iterador:
            print(f"  {pago}")
        print(f"\nTotal pagos realizados : {len(self._historial)}")
        print(
            f"Saldo final - token1: ${self._cuenta1.saldo:.2f}, "
            f"token2: ${self._cuenta2.saldo:.2f}"
        )


# ---------------------------------------------------------------------------
# Punto de entrada
# ---------------------------------------------------------------------------

def main():
    """Punto de entrada: procesa argumentos y ejecuta la simulación de pagos."""

    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        print(f"getJason versión {VERSION}")
        sys.exit(0)

    archivo_json = sys.argv[1] if len(sys.argv) >= 2 else ARCHIVO_JSON_DEFAULT

    try:
        procesador = ProcesadorPagos(archivo_json)
        print(f"=== Sistema de Pagos Automatizados v{VERSION} ===")
        print(
            f"Saldo inicial - token1: ${SALDO_TOKEN1:.2f}, "
            f"token2: ${SALDO_TOKEN2:.2f}\n"
        )

        for num in range(1, NUM_PEDIDOS + 1):
            procesador.pagar(num, MONTO_PAGO)

        procesador.listar()

    except FileNotFoundError:
        print(
            f"Error: no se encontró el archivo '{archivo_json}'.",
            file=sys.stderr,
        )
        sys.exit(1)
    except json.JSONDecodeError as exc:
        print(
            f"Error: el archivo '{archivo_json}' no es JSON válido. {exc}",
            file=sys.stderr,
        )
        sys.exit(1)
    except KeyError as exc:
        print(
            f"Error: la clave {exc} no existe en '{archivo_json}'.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
