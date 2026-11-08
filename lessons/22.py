"""Bloque 22 · Big O Notation

¿Qué tan rápido es tu código cuando crece el equipo?
"""

import time

# RETO 1 — Búsqueda secuencial O(n):
def buscar_secuencial(lista, objetivo):
    """Recorre toda la lista hasta encontrar el objetivo."""
    # TODO: recorré la lista y devolvé el índice o -1
    return None  # TODO

pokemons = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee"]
print("")  # TODO: mostrá la posición
print("")  # TODO

# RETO 2 — Acceso directo O(1):
def get_primero(equipo):
    """Accede directamente al primer elemento."""
    return None  # TODO: equipo[0]

print("")  # TODO

# RETO 3 — Suma lineal O(n):
def sumar_hp(equipo):
    """Suma HP de todo el equipo."""
    total = 0
    # TODO: sumá poke["hp"] de cada uno
    return None  # TODO

equipo = [
    {"nombre": "Pikachu", "hp": 35},
    {"nombre": "Charmander", "hp": 39},
    {"nombre": "Squirtle", "hp": 44},
]
print(f"\nHP total del equipo: {sumar_hp(equipo)}")  # 118

# RETO 4 — Comparación de todas las parejas O(n²):
def comparar_parejas(pokemons):
    """Compara cada Pokémon contra todos los demás."""
    comparaciones = 0
    # TODO: bucles anidados contando comparaciones
    return None  # TODO

nombres = ["A", "B", "C"]
total = comparar_parejas(nombres)
print(f"\nComparaciones totales ({len(nombres)} pokémons): {total}")  # C(3,2)=3

# RETO 5 — Medir tiempo real:
tamanos = [100, 1000, 10000]
for tam in tamanos:
    lista = list(range(tam))
    print("")  # TODO: medí el tiempo de búsqueda
