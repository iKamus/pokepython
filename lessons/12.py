"""Bloque 12 · Comprensión de listas y diccionarios

Transformá colecciones de Pokémons con list comprehensions elegantes.
"""

# RETO 1 — Lista de nombres en mayúsculas:
pokemons = ["pikachu", "charizard", "blastoise", "venusaur"]
nombres_mayu = [p.upper() for p in pokemons]
print(nombres_mayu)  # ['PIKACHU', 'CHARIZARD', 'BLASTOISE', 'VENUSAUR']

# RETO 2 — Filtrar Pokémons largos (más de 8 letras):
longos = [p for p in pokemons if len(p) > 8]
print(f"Largos: {longos}")  # ['charizard', 'blastoise']

# RETO 3 — Mapear a diccionario {nombre: nivel}
nombres = ["pika", "char", "blasto", "venus"]
niveles = [25, 36, 42, 38]
por_nombre = {nom: niv for nom, niv in zip(nombres, niveles)}
print(por_nombre)  # {'pika': 25, 'char': 36, ...}

# RETO 4 — Comprensión con condición dentro (electrico = divisible por 5):
pares = [x for x in range(1, 21)]
div_5 = []  # TODO: filtrá los divisibles por 5 con una comprensión condicional
print(f"Divisibles por 5: {div_5}")  # [5, 10, 15, 20]

# RETO 5 — Nested loop comprehension
colores = ["rojo", "azul"]
estados = ["activo", "inactivo"]
combinaciones = [(c, e) for c in colores for e in estados]
print(combinaciones)
# [('rojo', 'activo'), ('rojo', 'inactivo'), ('azul', 'activo'), ('azul', 'inactivo')]

# RETO 6 — Extraer stats de lista de pokémons:
equipo = [
    {"nombre": "Pikachu", "stats": {"hp": 35, "attack": 55}},
    {"nombre": "Charizard", "stats": {"hp": 78, "attack": 84}},
]
nombres_stats = [{"nombre": p["nombre"], "atk": p["stats"]["attack"]} for p in equipo]
for e in nombres_stats:
    print(f"{e['nombre']}: ATK={e['atk']}")
