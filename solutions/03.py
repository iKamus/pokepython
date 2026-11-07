"""Bloque 03 · Strings — Manipulando texto — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Nombre en mayúsculas con .upper():
pokemon = "pIkachu"
nombre_mayus = pokemon.upper()

# RETO 2 — Nombre en minúsculas con .lower():
nombre_minus = pokemon.lower()

# RETO 3 — Capitalizar con .title():
nombre_cap = pokemon.title()

# RETO 4 — Contar caracteres con len():
#   (consigna: la palabra es "hidrobomba", de 10 letras)
movimiento = "hidrobomba"
cant_caracteres = len(movimiento)  # "hidrobomba" tiene 10 letras

# RETO 5 — Reemplazar con .replace("_", " "):
nombre_huesped = "pi_kachu"
nombre_normal = nombre_huesped.replace("_", " ")  # "pi_kachu" → "pi kachu"

# RETO 6 — Verificar contenido con 'in':
contiene_chu = "chu" in pokemon

# RETO 7 — Eliminar espacios con .strip():
espacios = "  Raichu  "
sin_espacios = espacios.strip()

# Verificá tus respuestas imprimiendo:
print(f"{pokemon} -> {nombre_mayus}")
print(f"{pokemon} -> {nombre_minus}")
print(f"{pokemon} -> {nombre_cap}")
print(f"{movimiento} tiene {cant_caracteres} letras")
print(f"'{nombre_huesped}' -> '{nombre_normal}'")
print(f"¿'{pokemon}' contiene 'chu'? {contiene_chu}")
print(f"'{espacios}'.strip() -> '{sin_espacios}'")

# Verificación:
assert cant_caracteres == 10          # hidrobomba tiene 10 letras
assert nombre_normal == "pi kachu"    # "pi_kachu" → "pi kachu"
