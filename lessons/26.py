"""Bloque 26 · Memoización

Usá memoización para no recalcular probabilidades repetidamente.
"""

from functools import lru_cache

# RETO 1 — Caché manual: XP acumulada por nivel
def xp_con_cache(nivel, cache=None):
    """XP acumulada para llegar al nivel, guardando lo ya calculado en cache."""
    # TODO: si cache es None creá un dict; si nivel ya está en cache, devolvelo;
    #   caso base nivel <= 1 devuelve 0;
    #   guardá el resultado en cache[nivel] antes de devolverlo
    return None

print(f"XP al nivel 10: {xp_con_cache(10)}")           # 5400
print(f"XP al nivel 10 otra vez: {xp_con_cache(10)}")  # sale del cache


# RETO 2 — @lru_cache decorator (auto-memoización):
@lru_cache(maxsize=None)
def win_probability(attacker_hp, defender_hp, turnos_restantes):
    """Simula probabilidad de victoria en batalla, turno a turno."""
    # TODO: caso base turnos_restantes <= 0 -> 1.0 si attacker_hp > 0, si no 0.0;
    #   cada turno: el atacante pega 15% (70% de las veces) y el defensor 10%;
    #   devolvé 0.7 * win_probability(nuevo defensor) + 0.3 * win_probability(nuevo atacante)
    return None

print(f"Probabilidad de victoria: {win_probability(100, 80, 5)}")


# RETO 3 — Búsqueda del mejor camino entre tipos (sin repetir estados):
def mejor_camino_tipos(tipo_inicio, tipo_final, conexiones):
    """Busca el camino más largo de ventajas entre dos tipos conectados."""
    # TODO: usá una cola con (tipo_actual, camino), registrá los tipos visitados
    #   para no dar vueltas y quedate con el camino más largo
    return []


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
