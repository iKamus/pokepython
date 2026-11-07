"""Bloque 05 · Booleanos y condicionales — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — ¿Pokémon vencido? (hp <= 0):
hp = 0
derrotado = hp <= 0
print(f"¿Derrotado? {derrotado}")  # True

# RETO 2 — ¿Pokémon fuerte? (nivel >= 50):
nivel = 55
es_fuerte = nivel >= 50
print(f"¿Fuerte? {es_fuerte}")  # True

# RETO 3 — Tipo advantage con if/elif/else:
tipo_mov = "agua"
tipo_def = "fuego"

if tipo_mov == "fuego" and tipo_def == "planta":
    print("¡Súper efectivo! x2")
elif tipo_mov == tipo_def:
    print("Neutral. x1")
else:
    print("No muy efectivo... x0.5")

# RETO 4 — Combinar booleanos con and/or:
en_batalla = True
hp = 25
puede_atacar = en_batalla and hp > 0
print(f"¿Puede atacar? {puede_atacar}")  # True

# RETO 5 — Verificar super efectivo (diccionario de matchups):
super_efectivo = {
    "fuego": ["planta", "hielo", "acero"],
    "agua": ["fuego", "roca", "tierra"],
    "electrico": ["agua", "volador"]
}
mov = "electrico"
defensor = "agua"
si_efectivo = defensor in super_efectivo.get(mov, [])
print(f"¿{mov} vs {defensor} es efectivo? {si_efectivo}")  # True
