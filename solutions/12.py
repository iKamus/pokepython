"""Bloque 12 · Comprensión de listas y diccionarios — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Lista de nombres en mayúsculas:
pokemons = ["pikachu", "charizard", "blastiose", "venusaur"]
nombres_mayu = [p.upper() for p in pokemons]
print(nombres_mayu)  # ['PIKACHU', 'CHARIZARD', 'BLASTIOSE', 'VENUSAUR']

# RETO 2 — Filtrar Pokémons largos (más de 8 letras):
longos = [p for p in pokemons if len(p) > 8]
print(f"Largos: {longos}")  # ['charizard', 'blastiose']

# RETO 3 — Mapear a diccionario {nombre: nivel}
nombres = ["pika", "char", "blasto", "venus"]
niveles = [25, 36, 42, 38]
por_nombre = {nom: niv for nom, niv in zip(nombres, niveles)}
print(por_nombre)  # {'pika': 25, 'char': 36, ...}

# RETO 4 — Comprensión con condición dentro (electrico = divisible por 5):
pares = [x for x in range(1, 21)]
div_5 = [x for x in pares if x % 5 == 0]
print(f"Divisibles por 5: {div_5}")  # [5, 10, 15, 20]
print("Promedio de divisibles: {:.2f}".format(sum(div_5) / len(div_5)))  # 12.50
# tabla de restos: 5  0, 10  0, 15  0, 20  0 — todos % 5 == 0
# Acceso anidado en forma escapada:

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
