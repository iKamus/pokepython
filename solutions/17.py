"""Bloque 17 · Métodos especiales — SOLUCIÓN

Solución completa de la lección: métodos dunder para print(), comparaciones e igualdad.
"""

class Movimiento:
    def __init__(self, nombre, potencia, pp=20):
        self.nombre = nombre
        self.potencia = potencia
        self.pp = pp

    # RETO 1 — __str__: representación legible con print():
    def __str__(self):
        return f"{self.nombre} (potencia:{self.potencia}) [{self.pp}PP]"

    # RETO 2 — __lt__: comparar por potencia con el operador <:
    def __lt__(self, otro):
        return self.potencia < otro.potencia

    # RETO 3 — __eq__: igualdad por nombre del movimiento:
    def __eq__(self, otro):
        if not isinstance(otro, Movimiento):
            return False
        return self.nombre == otro.nombre

    # RETO 4 — Usar el movimiento gasta PP:
    def usar(self):
        if self.pp > 0:
            self.pp -= 1
            return self.potencia
        return None

# DEMOSTRACIÓN:
thunderbolt = Movimiento("Thunderbolt", 90)
rayo = Movimiento("Rayo", 40)
otro_rayo = Movimiento("Rayo", 40)

print(thunderbolt)                          # __str__ → Thunderbolt (potencia:90) [20PP]
print(f"¿Rayo < Thunderbolt? {rayo < thunderbolt}")   # __lt__ → True
print(f"¿Rayo == Rayo? {rayo == otro_rayo}")          # __eq__ → True

thunderbolt.usar()
thunderbolt.usar()
print(f"PP restantes: {thunderbolt.pp}")    # self.pp → 18
