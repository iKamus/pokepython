"""Bloque 23 · Fundamentos de Recursión

Funciones que se llaman a sí mismas para simular evolución Pokémon.
"""

# RETO 1 — XP acumulada hasta un nivel (caso base + paso recursivo):
def xp_total(nivel):
    """XP que junta un Pokémon para llegar a ese nivel: 100 por nivel, acumulada."""
    # TODO: caso base nivel <= 1 devuelve 0;
    #   paso recursivo: nivel * 100 + xp_total(nivel - 1)
    return None

print(f"XP al nivel 5: {xp_total(5)}")     # 1400

# RETO 2 — Daño total de un combo (suma recursiva de una lista):
def dano_total(combo):
    """Suma el daño de cada golpe del combo, recursivamente."""
    # TODO: caso base combo vacío devuelve 0;
    #   paso recursivo: combo[0] + dano_total(combo[1:])
    return None

golpes = [12, 8, 20, 5]
print(f"Daño total del combo: {dano_total(golpes)}")   # 45

# RETO 3 — Potencia recursiva (el ataque se multiplica por sí mismo):
def potencia(base, nivel):
    """Calcula base ** nivel de forma recursiva."""
    # TODO: caso base nivel == 0 devuelve 1;
    #   paso recursivo: base * potencia(base, nivel - 1)
    return None

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
    # TODO: recursá sobre EVOLUTION_CHAINS armando la cadena completa;
    #   caso base: el nombre no está en el diccionario
    return []


# Demo de evoluciones
starters = ["bulbasaur", "charmander", "squirtle", "pikachu"]
print("\n--- Cadenas Evolutivas ---")
for starter in starters:
    cadena = evolucion(starter)
    print(f"{starter.title()} → {' → '.join(cadena)}")
