#!/usr/bin/env python3
"""
getJason.py - Recuperador de claves desde archivo JSON de configuración.

Descripción:
    Lee un archivo JSON y recupera el valor asociado a una clave indicada.
    Diseñado para obtener API tokens de microservicios bancarios almacenados
    en sitedata.json, pero funciona con cualquier archivo JSON de clave/valor.

Uso:
    python3 getJason.py <archivo_json> [clave]

Argumentos:
    archivo_json  Ruta al archivo JSON que contiene las claves (requerido).
    clave         Nombre de la clave a recuperar (opcional, default: "token1").

Ejemplos:
    python3 getJason.py sitedata.json              recupera token1 (default)
    python3 getJason.py sitedata.json token1       recupera token1
    python3 getJason.py sitedata.json token2       recupera token2

Retorna:
    El valor asociado a la clave, impreso en stdout.
    Termina con código de salida 1 ante errores, con mensaje en stderr.

Versión 2.0 - Mayo 2025
Cambios respecto al original:
    - Corregido defecto: clave hardcodeada a 'token1', argv[2] nunca era leído.
    - Implementado argumento opcional [clave] con default 'token1'.
    - Agregado manejo de errores para archivo inexistente, clave inválida y JSON malformado.
    - Documentación completa agregada.
"""

import json
import sys

if len(sys.argv) < 2:
    print("Uso: python3 getJason.py <archivo_json> [clave]", file=sys.stderr)
    sys.exit(1)

archivo_json = sys.argv[1]
clave = sys.argv[2] if len(sys.argv) >= 3 else 'token1'

try:
    with open(archivo_json, 'r') as myfile:
        data = myfile.read()
    obj = json.loads(data)
    print(str(obj[clave]))
except FileNotFoundError:
    print(f"Error: no se encontró el archivo '{archivo_json}'.", file=sys.stderr)
    sys.exit(1)
except KeyError:
    print(f"Error: la clave '{clave}' no existe en '{archivo_json}'.", file=sys.stderr)
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error: el archivo '{archivo_json}' no es JSON válido. {e}", file=sys.stderr)
    sys.exit(1)