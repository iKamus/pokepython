"""Bloque 07 · Instalación y ejecución — SOLUCIÓN

Solución completa de la lección: verificamos el entorno y ejecutamos las operaciones básicas.
"""

import sys

# RETO 1 — Confirmar que el script corre en tu entorno:
print(f"Python {sys.version.split()[0]} instalado en {sys.executable}")
print("Script ejecutado")

# RETO 2 — Tu primera función:
def experiencia(nivel):
    return nivel * 100

print(f"experiencia(5) = {experiencia(5)}")    # Esperado: 500
print(f"experiencia(21) = {experiencia(21)}")  # Esperado: 2100

# RETO 3 — División entera y potencia:
print(f"100 // 3 = {100 // 3}")  # Esperado: 33
print(f"2 ** 8 = {2 ** 8}")    # Esperado: 256

# RETO 4 — Concatenación con +:
parte1 = "Pika"
parte2 = "chu"
print(parte1 + parte2)         # Esperado: Pikachu
