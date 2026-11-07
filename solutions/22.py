"""Bloque 22 · Big O Notation — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

import time

# RETO 1 — Búsqueda secuencial O(n):
def buscar_secuencial(lista, objetivo):
    """Recorre toda la lista hasta encontrar el objetivo."""
    for i, item in enumerate(lista):
        if item == objetivo:
            return i
    return -1

pokemons = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu", "Eevee"]
print(f"Pikachu está en posición: {buscar_secuencial(pokemons, 'Pikachu')}")  # 3
print(f"Mewtwo está en posición: {buscar_secuencial(pokemons, 'Mewtwo')}")    # -1

# RETO 2 — Acceso directo O(1):
def get_primero(equipo):
    """Accede directamente al primer elemento."""
    return equipo[0]

print(f"Primer pokemon: {get_primero(pokemons)}")  # Bulbasaur

# RETO 3 — Suma lineal O(n):
def sumar_hp(equipo):
    """Suma HP de todo el equipo."""
    total = 0
    for poke in equipo:
        total += poke["hp"]
    return total

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
    for i in range(len(pokemons)):
        for j in range(i + 1, len(pokemons)):
            comparaciones += 1
            print(f"  {pokemons[i]} vs {pokemons[j]}")
    return comparaciones

nombres = ["A", "B", "C"]
total = comparar_parejas(nombres)
print(f"\nComparaciones totales ({len(nombres)} pokémons): {total}")  # C(3,2)=3

# Verificación con la fórmula de pares (n-1 vecinos por cada uno):
n = len(nombres)
esperado = n * (n-1) / 2
assert total == esperado  # C(3,2)=3 → n * (n-1) / 2 comparaciones

# RETO 5 — Medir tiempo real:
tamanios = [100, 1000, 10000]
for tam in tamanios:
    lista = list(range(tam))
    
    start = time.time()
    buscar_secuencial(lista, tam - 1)
    duracion = time.time() - start
    
    print(f"Búsqueda en {tam:>6} items: {duracion*1000:.3f}ms")
