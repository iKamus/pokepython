"""Bloque 23 · Fundamentos de Recursión — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — XP acumulada hasta un nivel:
def xp_total(nivel):
    """XP que junta un Pokémon para llegar a ese nivel: 100 por nivel, acumulada."""
    if nivel <= 1:                      # CASO BASE
        return 0
    return nivel * 100 + xp_total(nivel - 1)   # PASO RECURSIVO

print(f"XP al nivel 5: {xp_total(5)}")     # 1400

# RETO 2 — Daño total de un combo:
def daño_total(combo):
    """Suma el daño de cada golpe del combo, recursivamente."""
    if not combo:                                   # CASO BASE: sin golpes
        return 0
    return combo[0] + daño_total(combo[1:])         # PASO: primer golpe + resto

golpes = [12, 8, 20, 5]
print(f"Daño total del combo: {daño_total(golpes)}")   # 45

# RETO 3 — Potencia recursiva:
def potencia(base, nivel):
    """Calcula base ** nivel de forma recursiva."""
    if nivel == 0:                          # CASO BASE
        return 1
    return base * potencia(base, nivel - 1)  # PASO

print(f"Ataque base 2 a nivel 3: {potencia(2, 3)}")   # 8
print(f"Ataque base 3 a nivel 4: {potencia(3, 4)}")   # 81

# RETO 4 — Cadena de evolución (recursión con diccionario):
EVOLUTION_CHAINS = {
    "bulbasaur": ["ivysaur", "venusaur"],
    "charmander": ["charmeleon", "charizard"],
    "squirtle": ["wartortle", "blastoise"],
    "pikachu": ["raichu"],
    "eevee": ["flareon", "jolteon", "vaporeon"],
}

def evolucion(name, chain=None):
    """Devuelve toda la cadena evolutiva desde el nombre dado."""
    if chain is None:
        chain = []

    formas = EVOLUTION_CHAINS.get(name, [])
    nueva_chain = chain + [name]

    if not formas:
        return nueva_chain  # CASO BASE: fin de la cadena

    # Para cada posible siguiente evolución, recursar y tomar la primera
    for next_form in formas:
        sub_cadena = evolucion(next_form, nueva_chain)
        if len(sub_cadena) > len(nueva_chain):
            return sub_cadena

    return nueva_chain


# Demo de evoluciones
starters = ["bulbasaur", "charmander", "squirtle", "pikachu"]
print("\n--- Cadenas Evolutivas ---")
for starter in starters:
    cadena = evolucion(starter)
    print(f"{starter.title()} → {' → '.join(cadena)}")
