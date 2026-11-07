"""Bloque 26 · Memoización — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

from functools import lru_cache

# RETO 1 — Caché manual: XP acumulada por nivel
def xp_con_cache(nivel, cache=None):
    """XP acumulada para llegar al nivel, guardando lo ya calculado en cache."""
    if cache is None:
        cache = {}
    if nivel in cache:
        return cache[nivel]
    if nivel <= 1:
        return 0
    cache[nivel] = nivel * 100 + xp_con_cache(nivel - 1, cache)
    return cache[nivel]

print(f"XP al nivel 10: {xp_con_cache(10)}")           # 5400
print(f"XP al nivel 10 otra vez: {xp_con_cache(10)}")  # sale del cache


# RETO 2 — @lru_cache decorator (auto-memoización):
@lru_cache(maxsize=None)
def win_probability(attacker_hp, defender_hp, turnos_restantes):
    """Simula probabilidad de victoria en batalla, turno a turno."""
    if turnos_restantes <= 0:
        return 1.0 if attacker_hp > 0 else 0.0

    # El atacante golpea primero (70% de las veces, daño del 15% de su HP)
    atk_daño = int(attacker_hp * 0.15)
    new_def_hp = max(0, defender_hp - atk_daño)

    # El defensor responde (30% de las veces, daño del 10%)
    def_atk_daño = int(defender_hp * 0.10)
    new_att_hp = max(0, attacker_hp - def_atk_daño)

    prob_ataca = 0.7 * win_probability(new_def_hp, defender_hp, turnos_restantes - 1)
    prob_defiende = 0.3 * win_probability(attacker_hp, new_def_hp, turnos_restantes - 1)
    return min(1.0, prob_ataca + prob_defiende)

print(f"Probabilidad de victoria: {win_probability(100, 80, 5)}")


# RETO 3 — Búsqueda del mejor camino entre tipos (sin repetir estados):
def mejor_camino_tipos(tipo_inicio, tipo_final, conexiones):
    """Busca el camino más largo de ventajas entre dos tipos conectados."""
    queue = [(tipo_inicio, [tipo_inicio])]
    visitados = set()
    mejor_path = []

    while queue:
        actual, path = queue.pop(0)
        if len(path) > len(mejor_path):
            mejor_path = path
        if actual == tipo_final:
            break
        if actual not in visitados:
            visitados.add(actual)
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

print("Camino desde electrico hasta normal:")
print(" → ".join(mejor_camino_tipos("electrico", "normal", conexiones)))
