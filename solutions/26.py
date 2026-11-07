"""Bloque 26 · Memoización — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

from functools import lru_cache

# RETO 1 — Fibonacci con memoización manual:
def fib_memo(n, cache=None):
    """Calcula fibonacci con caché manual."""
    if cache is None:
        cache = {}
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]

print("Fibonacci (memoizado):")
for i in range(15):
    print(f"  fib({i}) = {fib_memo(i)}")


# RETO 2 — @lru_cache decorator (auto-memoización):
@lru_cache(maxsize=None)
def win_probability(attacker_hp, defender_hp, turnos_restantes):
    """Simula probabilidad de victoria en batalla."""
    if turnos_restantes <= 0:
        return 1.0 if attacker_hp > 0 else 0.0
    
    # Atacante ataca primero (70% chance de daño significativo)
    atk_dano = int(attacker_hp * 0.15)
    new_def_hp = max(0, defender_hp - atk_dano)
    
    def_atk_dano = int(defender_hp * 0.10)
    new_att_hp = max(0, attacker_hp - def_atk_dano)
    
    prob_ataca = 0.7 * win_probability(new_def_hp, defender_hp, turnos_restantes - 1)
    prob_defiende = 0.3 * win_probability(attacker_hp, new_def_hp, turnos_restantes - 1)
    
    return prob_ataca + prob_defiende

# Usar (recuerda que es una simulación simple)
p1_hp = 100
p2_hp = 80
prob = min(1.0, win_probability(p1_hp, p2_hp, 5))
print(f"\nProbabilidad de victoria (P1={p1_hp}HP vs P2={p2_hp}HP, 5 turnos): {prob:.2%}")


# RETO 3 — DP Bottom-Up: Camino más corto entre tipos
def mejor_camino_tipos(tipos_inicio, tipo_final, conexiones):
    """Encuentra el camino más largo de advantage entre dos tipos."""
    queue = [(tipos_inicio, [tipos_inicio])]
    visited = set()  # evita re-visitar nodos (ciclos)
    mejor_path = []
    
    while queue:
        actual, path = queue.pop(0)
        if len(path) > len(mejor_path):
            mejor_path = path
        if actual == tipo_final:
            break
        if actual not in visited:
            visited.add(actual)
            for vecino in conexiones.get(actual, []):
                queue.append((vecino, path + [vecino]))
    
    return mejor_path


conexiones = {
    "fuego": ["planta", "hielo"],
    "agua": ["fuego"],
    "electrico": ["agua", "volador"],
    "planta": ["agua"],
    "volador": ["planta", "lucha"],
    "lucha": ["normal"]
}

path = mejor_camino_tipos("electrico", "normal", conexiones)
print(f"\nCamino desde electrico hasta normal:")
print(" → ".join(path))
