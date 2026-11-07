"""Bloque 10 · Bucles while y break/continue — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — while básico: contar turnos de batalla
turno = 0
while turno < 5:
    turno += 1
    print(f"Turno {turno}: ¡A combatir!")

# RETO 2 — while con condición de victoria (HP enemigo)
hp_enemigo = 100
print("\n--- Combate ---")
while hp_enemigo > 0:
    daño = 25
    hp_enemigo -= daño
    print(f"Enemigo tiene {hp_enemigo}HP restantes")
print("¡Victoria!")

# RETO 3 — break cuando HP llega a 0
hp = 100
giros = 0
resultados = []
while True:
    giros += 1
    hp -= 15
    resultado = "vivo" if hp > 0 else "derrotado"
    resultados.append(resultado)
    print(f"Giro {giros}: {resultado} (HP={max(0,hp)})")
    if hp <= 0:
        break
print(f"Duró {giros} giros")

# RETO 4 — continue en bucle for (saltar Pokémon debilitados)
equipo = ["Pikachu", "Snorlax", "Charizard"]
hps = [30, 0, 85]

para_evadir = ["Snorlax"]
for nombre, hp in zip(equipo, hps):
    if hp == 0:
        print(f"⏭ Saltando {nombre} (debilitado)")
        continue
    print(f"→ {nombre} en combate ({hp}HP)")
