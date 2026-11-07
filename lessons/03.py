"""Bloque 03 · Strings — Manipulando texto

Usá métodos de string para transformar nombres y movimientos Pokémon.
"""

# RETO 1 — Nombre en mayúsculas con .upper():
pokemon = "pIkachu"
nombre_mayus = pokemon.upper()

# RETO 2 — Nombre en minúsculas con .lower():
nombre_minus = pokemon.lower()

# RETO 3 — Capitalizar con .title():
nombre_cap = pokemon.title()

# RETO 4 — Contar caracteres con len():
movimiento = "hidrobomba"
cant_caracteres = len(movimiento)

# RETO 5 — Reemplazar con .replace("_", " "):
nombre_huesped = "pi_kachu"
nombre_normal = nombre_huesped.replace("_", " ")

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
