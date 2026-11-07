"""Bloque 19 · Decoradores @classmethod y @staticmethod — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

class Pokemon:
    TIPOS_SUPER = {
        "electrico": ["agua", "volador"],
        "fuego": ["planta", "hielo", "acero"],
        "agua": ["fuego", "roca", "tierra"],
        "planta": ["agua", "roca", "tierra"]
    }
    
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = 5
        self.hp_max = 100
    
    # RETO 1 — @classmethod: Factory que crea un Pokémon huevo:
    @classmethod
    def huevo(cls, tipo):
        """Crea un Pokémon 'huevo' del tipo especificado."""
        return cls(f"Huevo-{tipo}", tipo)
    
    # RETO 2 — @staticmethod: Consulta de ventaja de tipo sin instancia:
    @staticmethod
    def ventaja(tipo_mov, tipo_def):
        """Verifica si tipo_mov tiene ventaja sobre tipo_def."""
        efectivos = Pokemon.TIPOS_SUPER.get(tipo_mov, [])
        return tipo_def in efectivos
    
    # RETO 3 — @property: fortalezas del tipo (solo lectura):
    @property
    def fortalezas(self):
        """Tipos contra los que este Pokémon es súper efectivo."""
        return Pokemon.TIPOS_SUPER.get(self.tipo, [])

    # Método de instancia normal:
    def atacar(self, target):
        efectivo = self.ventaja(self.tipo, target.tipo)
        dano = 20 if efectivo else 10
        print(f"→ {self.nombre} ({self.tipo}) vs {target.nombre} ({target.tipo}): {'x2' if efectivo else 'x1'}")


# USO DE @classmethod
print("Creando huevos:")
huevo_elec = Pokemon.huevo("electrico")
huego_fuego = Pokemon.huevo("fuego")
print(f"{huevo_elec.nombre} es tipo {huevo_elec.tipo}")
print(f"{huego_fuego.nombre} es tipo {huego_fuego.tipo}")

# USO DE @staticmethod
print("\nConsultas estáticas:")
print(f"electrico vs agua -> efectivo: {Pokemon.ventaja('electrico', 'agua')}")  # True
print(f"fuego vs planta -> efectivo: {Pokemon.ventaja('fuego', 'planta')}")      # True
print(f"agua vs fuego -> efectivo: {Pokemon.ventaja('agua', 'fuego')}")           # True
print(f"normal vs electrico -> efectivo: {Pokemon.ventaja('normal', 'electrico')}")  # False

# BATALLA CON MÉTODO DE INSTANCIA
print("\n--- Batalla ---")
pika = Pokemon("Pikachu", "electrico")
squirtle = Pokemon("Squirtle", "agua")
charmander = Pokemon("Charmander", "fuego")

pika.atacar(squirtle)   # x2 super efectivo!
squirtle.atacar(charmander)  # x2 super efectivo!
charmander.atacar(pika)     # x1 neutral
