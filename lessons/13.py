"""Bloque 13 · collections — defaultdict y Counter

Analizá datos de combate con módulos de collections.
"""
from collections import Counter, defaultdict

# RETO 1 — Contar frecuencias de tipos en tu equipo:
tipos_equipo = ["electrico", "fuego", "agua", "electrico", "planta", "fuego"]
cuenta_tipos = None  # TODO: Counter(tipos_equipo)
print("")  # TODO: mostrá cuenta_tipos y most_common

# RETO 2 — defaultdict para agrupar Pokémon por tipo:
pokemons = ["pikachu", "raichu", "charizard", "arcanine"]
tipos_map = {"pikachu": "electrico", "raichu": "electrico",
             "charizard": "fuego", "arcanine": "fuego"}
grupo = None  # TODO: defaultdict(list) y agrupá
print("")  # TODO: mostrá grupos

# RETO 3 — defaultdict(int) para sumar daños recibidos:
daño_total = None  # TODO: defaultdict(int) y acumulá
turnos = [
    ("Pikachu", 15), ("Charizard", 20), ("Pikachu", 8),
    ("Blastoise", 12), ("Charizard", 5)
]
print("")  # TODO: mostrá daño por Pokémon
