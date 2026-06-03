#!/usr/bin/env python3
"""
getJason.py - Recuperador de claves desde archivo JSON de configuración.

Descripción:
    Lee un archivo JSON y recupera el valor asociado a una clave indicada.
    Implementado con el patrón de diseño Singleton para garantizar una única
    instancia de acceso al archivo de configuración.

Uso:
    python3 getJason.py <archivo_json> [clave|-v]

Argumentos:
    archivo_json  Ruta al archivo JSON que contiene las claves (requerido).
    clave         Nombre de la clave a recuperar (opcional, default: "token1").
    -v            Muestra la versión del programa.

Ejemplos:
    python3 getJason.py sitedata.json              recupera token1 (default)
    python3 getJason.py sitedata.json token1       recupera token1
    python3 getJason.py sitedata.json token2       recupera token2
    python3 getJason.py -v                         muestra la versión

copyright UADERFCyT-IS2©2024 todos los derechos reservados.
"""

import json
import sys

VERSION = "1.1"

class SingletonMeta(type): #pylint: disable=too-few-public-methods
    """Metaclase que implementa el patrón Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class GetJason(metaclass=SingletonMeta): #pylint: disable=too-few-public-methods
    """
    Clase Singleton para recuperar claves desde un archivo JSON.

    Garantiza una única instancia de acceso al archivo de configuración
    durante toda la ejecución del programa.
    """

    def __init__(self, archivo_json: str):
        """
        Inicializa la instancia cargando el archivo JSON en memoria.

        Args:
            archivo_json: Ruta al archivo JSON de configuración.

        Raises:
            FileNotFoundError   : Si el archivo no existe.
            json.JSONDecodeError: Si el archivo no es JSON válido.
        """
        self.archivo_json = archivo_json
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
            data = myfile.read()
        return json.loads(data)

    def obtener(self, clave: str) -> str:
        """
        Recupera el valor asociado a una clave del JSON.

        Args:
            clave: Nombre de la clave a recuperar.

        Returns:
            El valor (str) asociado a la clave.

        Raises:
            KeyError: Si la clave no existe en el JSON.
        """
        return str(self.datos[clave])


def main():
    """Punto de entrada principal. Procesa argumentos y ejecuta la consulta."""

    # Manejo del argumento -v (versión)
    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        print(f"getJason versión {VERSION}")
        sys.exit(0)

    # Validación de argumentos
    if len(sys.argv) < 2:
        print(
            "Uso: python3 getJason.py <archivo_json> [clave|-v]\n"
            "     clave por defecto: token1",
            file=sys.stderr
        )
        sys.exit(1)

    archivo_json = sys.argv[1]
    clave = sys.argv[2] if len(sys.argv) >= 3 else 'token1'

    # Ejecución con errores controlados — el programa nunca termina
    # con una excepción del sistema
    try:
        lector = GetJason(archivo_json)
        print(lector.obtener(clave))
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{archivo_json}'.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: el archivo '{archivo_json}' no es JSON válido. {e}", file=sys.stderr)
        sys.exit(1)
    except KeyError:
        print(f"Error: la clave '{clave}' no existe en '{archivo_json}'.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()  