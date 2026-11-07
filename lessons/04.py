"""Bloque 04 · Números y operaciones matemáticas

Calculá estadísticas de combate con operadores aritméticos.
"""

# RETO 1 — Suma de HP (base + boost):
hp_base = 80
bono_hp = 20
hp_total = None            # TODO: sumá hp_base + bono_hp

# RETO 2 — Restar daño recibido:
hp_actual = 100
daño_recibido = 35
hp_despues = None          # TODO: restale el daño recibido

# RETO 3 — Multiplicar ATK por multiplicador (ej: ventaja tipo):
atk = 70
multiplicador = 1.5
atk_efectivo = None        # TODO: multiplicá el ataque

# RETO 4 — División entera // :
niveles_totales = 42
entrenadores = 5
por_entrenador = None      # TODO: usá la división entera

# RETO 5 — Módulo % (distribuir Pokémons en equipos de 6):
pokemons = 25
tamaño_equipo = 6
sobran = None              # TODO: usá el módulo

# RETO 6 — Potencia ** (velocidad x velocidad):
fuerza = 3
exponente = 4
resultado = None           # TODO: usá la potencia

# Verificá:
print(f"HP total: {hp_total}")           # Esperado: 100
print(f"HP después del daño: {hp_despues}")  # Esperado: 65
print(f"ATK efectivo (x1.5): {atk_efectivo}")  # Esperado: 105.0
print(f"42 niveles ÷ 5 entrenadores: {por_entrenador}")  # Esperado: 8
print(f"25 Pokémons en equipos de 6 → sobran {sobran}")  # Esperado: 1
print(f"3⁴ = {resultado}")               # Esperado: 81
