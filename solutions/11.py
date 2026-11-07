"""Bloque 11 · Diccionarios — La Pokédex — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Crear diccionario de Charizard:
charizard = {
    "nombre": "Charizard",
    "tipo": "fuego",
    "nivel": 36,
    "hp_max": 390,
}

# RETO 2 — Acceder y modificar atributos:
print(f"{charizard['nombre']} es tipo {charizard['tipo']}")
charizard["habilidad"] = "Mar Llamas"

# RETO 3 — Agregar nueva clave (lista de habilidades):
charizard["movimientos"] = ["Llamarada", "Rayo Solar", "Arañazo"]
charizard["habilidades"] = ["Mar Llamas", "Intimidación"]

# Texto escapado de la ficha (comillas dobles con \):
print("Ficha como texto: {\"nombre\": \"Charizard\"}")
print("Claves usadas: [\"tipo\"] y [\"habilidades\"]")

# RETO 4 — Iterar con items():
print("\nDetalles de Charizard:")
for clave, valor in charizard.items():
    print(f"  {clave}: {valor}")

# RETO 5 — get() con valor por defecto:
movimiento_especial = charizard.get("ataque_especial", "Placaje")
print(f"\nAtaque especial: {movimiento_especial}")  # Placaje (no existe, usa el valor por defecto)

# RETO 6 — Pokédex completa con varios Pokémon:
pokedex = {
    25: {"nombre": "Pikachu", "tipo": "electrico"},
    6: {"nombre": "Charizard", "tipo": "fuego"},
    9: {"nombre": "Blastoise", "tipo": "agua"},
    1: {"nombre": "Venusaur", "tipo": "planta"},
}

# RETO 7 — Set de tipos únicos:
tipos_usados = set(pokedex[num]["tipo"] for num in pokedex)
print(f"\nTipos encontrados: {tipos_usados}")
print(f"Cantidad de tipos distintos: {len(tipos_usados)}")
