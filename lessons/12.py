"""Bloque 12 · Comprensión de listas y diccionarios

Transformá colecciones de Pokémons con list comprehensions elegantes.
"""

# RETO 1 — Lista de nombres en mayúsculas:
pokemons = ["pikachu", "charizard", "blastoise", "venusaur"]
nombres_mayu = None  # TODO: [p.upper() for p in pokemons]
print("")  # TODO: mostrá nombres_mayu

# RETO 2 — Filtrar Pokémons largos (más de 8 letras):
largos = None  # TODO: [p for p in pokemons if len(p) > 8]
print("")  # TODO: mostrá largos

# RETO 3 — Mapear a diccionario {nombre: nivel}
nombres = ["pika", "char", "blasto", "venus"]
niveles = [25, 36, 42, 38]
por_nombre = None  # TODO: {nom: niv for nom, niv in zip(nombres, niveles)}
print("")  # TODO: mostrá por_nombre

# RETO 4 — Comprensión con condición dentro (electrico = divisible por 5):
pares = [x for x in range(1, 21)]
div_5 = None  # TODO: filtrá los divisibles por 5 con una comprensión condicional
print("")  # TODO: mostrá div_5

# RETO 5 — Nested loop comprehension
colores = ["rojo", "azul"]
estados = ["activo", "inactivo"]
combinaciones = None  # TODO: [(c, e) for c in colores for e in estados]
print("")  # TODO: mostrá combinaciones

# RETO 6 — Extraer stats de lista de pokémons:
equipo = [
    {"nombre": "Pikachu", "stats": {"hp": 35, "attack": 55}},
    {"nombre": "Charizard", "stats": {"hp": 78, "attack": 84}},
]
nombres_stats = None  # TODO: extraé nombre y atk con comprensión
print("")  # TODO: mostrá cada nombre y ATK
