"""Bloque 07 · Instalación y ejecución — SOLUCIÓN

Solución completa de la lección: verificamos el entorno y ejecutamos las operaciones básicas.
"""

import sys

# RETO 1 — Confirmar que el script corre en tu entorno:
print(f"Python {sys.version.split()[0]} instalado en {sys.executable}")
print("Script ejecutado")

# RETO 2 — Tu primera función:
def doble(n):
    return n * 2

print(f"doble(5) = {doble(5)}")    # Esperado: 10
print(f"doble(21) = {doble(21)}")  # Esperado: 42
assert doble(21) == 42

# RETO 3 — División entera y potencia:
print(f"10 // 3 = {10 // 3}")  # Esperado: 3
print(f"2 ** 8 = {2 ** 8}")    # Esperado: 256
assert 2 ** 8 == 256

# RETO 4 — Concatenación con +:
parte1 = "py"
parte2 = "thon"
print(parte1 + parte2)         # Esperado: python
