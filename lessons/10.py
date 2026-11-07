"""Bloque 10 · Bucles while y break/continue

Controlá el flujo con while y break/continue para simulaciones por turnos.
"""

# RETO 1 — while básico: contar turnos de batalla:
turno = 0
print("")  # TODO: con while turno < 5 imprimí "Turno 1: ¡A combatir!" … hasta 5

# RETO 2 — while con condición de victoria (HP enemigo):
hp_enemigo = 100
print("\n--- Combate ---")
print("")  # TODO: restá 25 por vuelta imprimiendo el HP hasta llegar a 0
           #   y terminá con print("¡Victoria!")

# RETO 3 — break cuando HP llega a 0:
hp = 100
giros = 0
resultados = []
print("")  # TODO: while True: restá 15 de hp, registrá "vivo"/"derrotado" en
           #   resultados, imprimí cada giro y salí con break cuando hp <= 0

# RETO 4 — continue en bucle for (saltar Pokémon debilitados):
equipo = [
    {"nombre": "Pikachu", "hp": 30},
    {"nombre": "Snorlax", "hp": 0},
    {"nombre": "Charizard", "hp": 85},
]

para_evadir = ["Snorlax"]
print("")  # TODO: recorré equipo con for y usá continue para saltar los que
           #   tengan hp == 0; imprimí a los que quedan en combate
