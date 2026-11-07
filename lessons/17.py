"""Bloque 17 · Métodos especiales

Completá cada TODO para que Movimiento se comporte de forma natural.
Al terminar, corré ▶ Correr o Ctrl+Enter.
"""

class Movimiento:
    def __init__(self, nombre, potencia, pp=20):
        self.nombre = nombre
        self.potencia = potencia
        self.pp = pp

    # RETO 1 — __str__: representación legible con print():
    #   print(mov) -> Thunderbolt (potencia:90) [20PP]
    # TODO: implementá el método especial para que print(mov) muestre
    #   "Thunderbolt (potencia:90) [20PP]"

    # RETO 2 — __lt__: comparar por potencia con el operador <:
    #   Movimiento("Rayo",40) < Movimiento("Thunderbolt",90) -> True
    def __lt__(self, otro):
        # TODO: retorná True si este movimiento tiene MENOS potencia que otro
        return False

    # RETO 3 — __eq__: igualdad por nombre del movimiento:
    #   Movimiento("Rayo",40) == Movimiento("Rayo",40) -> True
    def __eq__(self, otro):
        # TODO: verificá que otro sea Movimiento y compará por nombre
        return False

    # RETO 4 — Usar el movimiento gasta PP:
    def usar(self):
        # TODO: si self.pp > 0 restá 1 a self.pp y retorná self.potencia; si no, retorná None
        return None

# DEMOSTRACIÓN — completá los TODOs y volvé a correr:
thunderbolt = Movimiento("Thunderbolt", 90)
rayo = Movimiento("Rayo", 40)
otro_rayo = Movimiento("Rayo", 40)

print(thunderbolt)
print(rayo < thunderbolt)
print(rayo == otro_rayo)

thunderbolt.usar()
thunderbolt.usar()
print(f"PP restantes: {thunderbolt.pp}")
