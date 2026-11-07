"""Bloque 16 · Clases básicas — Clase Pokémon

Creá una clase con atributos, métodos y __str__ para representar un Pokémon.
"""

# RETO 1 — Clase Pokemon básica:
class Pokemon:
    TIPOS_SUPER = {
        "electrico": ["agua", "volador"],
        "fuego": ["planta", "hielo", "acero"],
        "agua": ["fuego", "roca", "tierra"]
    }
    
    def __init__(self, nombre, tipo, nivel=5):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp_max = nivel * 20
        self.hp = self.hp_max
        self.movimientos = ["Placaje"]
    
    def __str__(self):
        return f"{self.nombre} Nv.{self.nivel} {self.tipo} HP:{self.hp}/{self.hp_max}"
    
    # RETO 2 — Aprender nuevo movimiento:
    def aprender(self, mov):
        # TODO: si mov no está en self.movimientos, agregalo con .append()
        pass
    
    # RETO 3 — Recibir daño:
    def recibir_dano(self, dano):
        # TODO: restá dano a self.hp sin bajar de 0 (usá max)
        pass
    
    # RETO 4 — Curar:
    def curar(self, cantidad=20):
        # TODO: sumá cantidad a self.hp sin pasarte de self.hp_max (usá min)
        pass
    
    # RETO 5 — Verificar ventaja de tipo:
    def ventaja_vs(self, otro):
        # TODO: compará self.tipo con los tipos efectivos de TIPOS_SUPER y
        #   devolvé "x2 SUPER EFECTIVO!", "x1 neutral" o "x0.5 no muy efectivo"
        return None

# CREAR INSTANCIAS:
pikachu = Pokemon("Pikachu", "electrico", 25)
charizard = Pokemon("Charizard", "fuego", 36)

# PROBAR MÉTODOS:
print(pikachu)               # Pikachu Nv.25 electrico HP:500/500
print(charizard)             # Charizard Nv.36 fuego HP:720/720

print("\n--- Entrenamiento ---")
pikachu.aprender("Thunderbolt")
pikachu.aprender("Volt Tackle")
print(f"Movimientos: {pikachu.movimientos}")

print("\n--- Batalla ---")
pikachu.recibir_dano(100)
charizard.curar(50)
print(f"\nVentaja: {pikachu.ventaja_vs(charizard)}")
