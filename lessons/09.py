"""Bloque 09 · Tuplas y slicing

Usá tuplas para datos que no cambian y slicing para extraer porciones.
"""

# RETO 1 — Tupla de stats base de Pikachu (HP, Atk, Def, SpA, SpD, Spe):
stats = (35, 55, 40, 50, 65, 90)

# RETO 2 — Acceder a estadística por índice:
print(f"HP: {stats[0]}, Speed: {stats[-1]}")  # HP: 35, Speed: 90

# RETO 3 — Slicing: primeros 3 stats
primeros_3 = stats[:3]
print(f"Primeros 3 stats: {primeros_3}")  # (35, 55, 40)

# RETO 4 — Último stat con índice negativo
velocidad = stats[-1]
print(f"Speed: {velocidad}")  # 90

# RETO 5 — Invertir todos los stats
invertidos = stats[::-1]
print(f"Invertidos: {invertidos}")  # (90, 65, 50, 40, 55, 35)

# RETO 6 — Desempaquetar en variables separadas
hp, atk, def_val, sp_atk, sp_def, spe = stats
print(f"\nDesempaquetado:")
print(f"  HP={hp}, ATK={atk}, DEF={def_val}")
print(f"  SpA={sp_atk}, SpD={sp_def}, Spe={spe}")

# RETO 7 — Slice con paso (solo pares):
numeros = list(range(20))
pares = numeros[::2]
print(f"\nPares de 0 a 19: {pares}")  # [0, 2, 4, ..., 18]
