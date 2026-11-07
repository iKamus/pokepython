"""Bloque 04 · Números y operaciones matemáticas — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Suma de HP (base + boost):
hp_base = 80
ehill_boost = 20
hp_total = hp_base + ehill_boost

# RETO 2 — Restar daño recibido:
hp_actual = 100
daño_recibido = 35
hp_despues = hp_actual - daño_recibido

# RETO 3 — Multiplicar ATK por multiplicador (ej: ventaja tipo):
atk = 70
multiplicador = 1.5
atk_efectivo = atk * multiplicador

# RETO 4 — División entera // :
niveles_totales = 42
entrenadores = 5
por_entrenador = niveles_totales // entrenadores

# RETO 5 — Módulo % (distribuir Pokémons en equipos de 6):
pokemons = 25
equipe_size = 6
sobran = pokemons % equipe_size

# RETO 6 — Potencia ** (velocidad x velocidad):
fuerza = 3
exponente = 4
resultado = fuerza ** exponente

# Verificá:
print(f"HP total: {hp_total}")           # Esperado: 100
print(f"HP después del daño: {hp_despues}")  # Esperado: 65
print(f"ATK efectivo (x1.5): {atk_efectivo}")  # Esperado: 105.0
print(f"42 niveles ÷ 5 entrenadores: {por_entrenador}")  # Esperado: 8
print(f"25 Pokémons en equipos de 6 → sobran {sobran}")  # Esperado: 1
print(f"3⁴ = {resultado}")               # Esperado: 81

# Verificación:
assert hp_total == 100
assert hp_despues == 65
assert atk_efectivo == 105.0
assert por_entrenador == 8
assert sobran == 1
assert resultado == 81
