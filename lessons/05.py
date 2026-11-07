"""Bloque 05 · Booleanos y condicionales

Tomá decisiones en código comparando tipos y estados de batalla.
"""

# RETO 1 — ¿Pokémon vencido? (hp <= 0):
hp = 0
derrotado = None  # TODO: asigná el resultado de la comparación hp <= 0
print(f"¿Derrotado? {derrotado}")  # True

# RETO 2 — ¿Pokémon fuerte? (nivel >= 50):
nivel = 55
es_fuerte = None  # TODO: asigná el resultado de la comparación nivel >= 50
print(f"¿Fuerte? {es_fuerte}")  # True

# RETO 3 — Tipo advantage con if/elif/else:
tipo_mov = "agua"
tipo_def = "fuego"

# TODO: completá el if/elif/else que imprime según el enfrentamiento:
#   "¡Súper efectivo! x2" / "Neutral. x1" / "No muy efectivo... x0.5"

# RETO 4 — Combinar booleanos con and/or:
en_batalla = None  # TODO: poné True acá
hp = 25
puede_atacar = None  # TODO: resultado de en_batalla and hp > 0
print(f"¿Puede atacar? {puede_atacar}")  # True

# RETO 5 — Verificar super efectivo (diccionario de matchups):
super_efectivo = {
    "fuego": ["planta", "hielo", "acero"],
    "agua": ["fuego", "roca", "tierra"],
    "electrico": ["agua", "volador"]
}
mov = "electrico"
defensor = "agua"
si_efectivo = None  # TODO: usá `in` sobre super_efectivo.get(mov, [])
print(f"¿{mov} vs {defensor} es efectivo? {si_efectivo}")  # True
