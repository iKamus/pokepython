"""Bloque 13 · collections — defaultdict y Counter — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""
from collections import Counter, defaultdict

# RETO 1 — Contar frecuencias de tipos en tu equipo:
tipos_equipo = ["electrico", "fuego", "agua", "electrico", "planta", "fuego"]
cuenta_tipos = Counter(tipos_equipo)
print(f"Tipos: {cuenta_tipos}")
# Counter({'electrico': 2, 'fuego': 2, 'agua': 1, 'planta': 1})
print(f"Más común: {cuenta_tipos.most_common(2)}")
print(f"Ranking completo: {cuenta_tipos.most_common()}")

# RETO 2 — defaultdict para agrupar Pokémon por tipo:
pokemons = ["pikachu", "raichu", "charizard", "arcanine"]
tipos_map = {"pikachu": "electrico", "raichu": "electrico",
             "charizard": "fuego", "arcanine": "fuego"}
grupo = defaultdict(list)
for p in pokemons:
    grupo[tipos_map[p]].append(p)
for tipo, lista in grupo.items():
    print(f"{tipo}: {lista}")
# electrico: ['pikachu', 'raichu']
# fuego: ['charizard', 'arcanine']

# RETO 3 — defaultdict(int) para sumar daños recibidos:
daño_total = defaultdict(int)
turnos = [
    ("Pikachu", 15), ("Charizard", 20), ("Pikachu", 8),
    ("Blastoise", 12), ("Charizard", 5)
]
for pokemon, daño in turnos:
    daño_total[pokemon] += daño
print("\nDaño recibido por Pokémon:")
for pk, total in sorted(daño_total.items()):
    print(f"  {pk}: {total} damage")
