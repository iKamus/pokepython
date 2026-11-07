"""Bloque 24 · Merge Sort

Algoritmo divide y vencerás para ordenar Pokémons en O(n log n).
"""

def merge_sort(arr, key=None):
    """Ordena una lista usando el algoritmo Merge Sort."""
    # TODO: caso base (lista de longitud <= 1), partí en dos mitades y
    #   combiná merge_sort(izquierda) y merge_sort(derecha) con merge()
    return arr


def merge(left, right, key=None):
    """Fusiona dos listas ya ordenadas en una sola ordenada."""
    # TODO: recorré ambas listas comparando con key(...), agregá siempre el
    #   menor y concatená los restos al final
    return left + right


# DATOS DE POKÉMONS CON STATS
pokemons = [
    {"nombre": "Pikachu", "speed": 90, "attack": 80},
    {"nombre": "Snorlax", "speed": 30, "attack": 110},
    {"nombre": "Charizard", "speed": 100, "attack": 84},
    {"nombre": "Blastoise", "speed": 78, "attack": 83},
    {"nombre": "Venusaur", "speed": 80, "attack": 82},
    {"nombre": "Eevee", "speed": 55, "attack": 55},
]

# RETO 1 — Ordenar por velocidad:
ordenado_speed = merge_sort(pokemons, key=lambda p: p["speed"])
print("Ordenados por velocidad:")
for p in ordenado_speed:
    print(f"  {p['nombre']:>12} — Speed: {p['speed']}")

# RETO 2 — Ordenar por ataque:
ordenado_attack = merge_sort(pokemons, key=lambda p: p["attack"])
print("\nOrdenados por ATK:")
for p in ordenado_attack:
    print(f"  {p['nombre']:>12} — ATK: {p['attack']}")

# RETO 3 — Ordenar por HP total (hp + atk + spd):
pokemons_with_hp = [
    {"nombre": p["nombre"], 
     "hp": 35 + p["speed"] + p["attack"],
     "speed": p["speed"],
     "attack": p["attack"]}
    for p in pokemons
]

total_stats = list(reversed(merge_sort(pokemons_with_hp, key=lambda p: p["hp"])))
print("\nOrdenados por HP total:")
for p in total_stats:
    print(f"  {p['nombre']:>12} — Total: {p['hp']}")
