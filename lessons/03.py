"""Bloque 03 · Strings — Manipulando texto

Usá métodos de string para transformar nombres y movimientos Pokémon.
"""

# RETO 1 — Nombre en mayúsculas con .upper():
pokemon = "pIkachu"
nombre_mayus = None      # TODO: pasá pokemon a mayúsculas

# RETO 2 — Nombre en minúsculas con .lower():
nombre_minus = None      # TODO: pasá pokemon a minúsculas

# RETO 3 — Capitalizar con .title():
nombre_cap = None        # TODO: capitalizá pokemon

# RETO 4 — Contar caracteres con len():
movimiento = "hidrobomba"
cant_caracteres = None    # TODO: contá las letras de movimiento

# RETO 5 — Reemplazar con .replace("_", " "):
nombre_huesped = "pi_kachu"
nombre_normal = None     # TODO: cambiá el guion bajo por un espacio

# RETO 6 — Verificar contenido con 'in':
contiene_chu = None      # TODO: averiguá si pokemon contiene "chu"

# RETO 7 — Eliminar espacios con .strip():
espacios = "  Raichu  "
sin_espacios = None      # TODO: quitá los espacios de los costados

# Verificá tus respuestas imprimiendo:
print(f"{pokemon} -> {nombre_mayus}")
print(f"{pokemon} -> {nombre_minus}")
print(f"{pokemon} -> {nombre_cap}")
print(f"{movimiento} tiene {cant_caracteres} letras")
print(f"'{nombre_huesped}' -> '{nombre_normal}'")
print(f"¿'{pokemon}' contiene 'chu'? {contiene_chu}")
print(f"'{espacios}' -> '{sin_espacios}'")
