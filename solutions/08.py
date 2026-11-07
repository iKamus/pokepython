"""Bloque 08 · Listas y bucles — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Lista de primeros 6 starters:
tus_starters = ["Pikachu", "Charmander", "Squirtle", "Bulbasaur", "Jigglypuff", "Meowth"]

# RETO 2 — Recorrer con for, imprimir cada uno:
for pokemon in tus_starters:
    print(f"🔹 {pokemon}")

# RETO 3 — Agregar un compañero adicional con .append():
tus_starters.append("Eevee")
print(f"\nAhora tenés {len(tus_starters)} pokémons en tu lista.")

# RETO 4 — Eliminar el último con .pop():
utilizado = tus_starters.pop()
print(f"{utilizado} se fue a descansar. Quedan: {len(tus_starters)} pokémons")

# RETO 5 — Insertar en posición 0 con .insert(0, valor):
tus_starters.insert(0, "Mewtwo")
print(f"Nuevo líder del equipo: {tus_starters[0]}")

# RETO 6 — enumerate para mostrar con número:
print("\nTu equipo ordenado:")
for i, pokemon in enumerate(tus_starters):
    print(f"  #{i+1}: {pokemon}")

# RETO 7 — Slicing de la lista:
primeros_3 = tus_starters[:3]
ultimos_2 = tus_starters[-2:]
print(f"\nPrimeros 3: {primeros_3}")
print(f"Últimos 2: {ultimos_2}")
