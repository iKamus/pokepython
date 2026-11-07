"""Bloque 16 · Clases básicas — Clase Pokémon — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
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
        if mov not in self.movimientos:
            self.movimientos.append(mov)
            print(f"📚 {self.nombre} aprendió {mov}!")
    
    # RETO 3 — Recibir daño:
    def recibir_dano(self, dano):
        self.hp = max(0, self.hp - dano)
        print(f"💥 {self.nombre} recibió {dano} daño. HP: {self.hp}")
    
    # RETO 4 — Curar:
    def curar(self, cantidad=20):
        self.hp = min(self.hp + cantidad, self.hp_max)
        print(f"❤️ {self.nombre} recuperó {cantidad}HP. HP: {self.hp}")
    
    # RETO 5 — Verificar ventaja de tipo:
    def ventaja_vs(self, otro):
        efectivos = self.TIPOS_SUPER.get(self.tipo, [])
        if otro.tipo in efectivos:
            return "x2 SUPER EFECTIVO!"
        elif self.tipo == otro.tipo:
            return "x1 neutral"
        else:
            return "x0.5 no muy efectivo"

# CREAR INSTANCIAS:
pikachu = Pokemon("Pikachu", "electrico", 25)
charizard = Pokemon("Charizard", "fuego", 36)

# PROBAR MÉTODOS:
print(pikachu)               # Pikachu Nv.25 electrico HP:500/500
print(charizard)             # Charizard Nv.36 fuego HP:720/720

print("\n--- Entrenamiento ---")
pikachu.aprender("Rayo")
pikachu.aprender("Placaje Eléctrico")
print(f"Movimientos: {pikachu.movimientos}")

print("\n--- Batalla ---")
pikachu.recibir_dano(100)
charizard.curar(50)
print(f"\nVentaja: {pikachu.ventaja_vs(charizard)}")
