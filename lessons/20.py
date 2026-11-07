"""Bloque 20 · Herencia — Subclases

Creá subclases que hereden y extiendan el comportamiento base.
"""

class Pokemon:
    def __init__(self, nombre, tipo, nivel=1):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp_max = nivel * 20
        self.hp = self.hp_max
        self.movimientos = ["Placaje"]
    
    def __str__(self):
        return f"{self.nombre} {self.tipo} Nv.{self.nivel} HP:{self.hp}/{self.hp_max}"
    
    def aprender(self, mov):
        if mov not in self.movimientos:
            self.movimientos.append(mov)
    
    def atacar(self, objetivo):
        dano = self.nivel * 5
        objetivo.recibir_dano(dano)
    
    def recibir_dano(self, dano):
        self.hp = max(0, self.hp - dano)
    
    def curar(self, cantidad=20):
        self.hp = min(self.hp + cantidad, self.hp_max)


# --- Subclases con HERENCIA ---

class Electrico(Pokemon):
    MOVIMIENTOS_ELEC = ["Chispazo", "Rayo", "Thunderbolt", "Cola Férrea", "Volt Tackle"]
    
    def __init__(self, nombre, voltaje=100000):
        super().__init__(nombre, "electrico")
        self.voltaje = voltaje
    
    def aprender(self, mov):
        # TODO: aceptá solo movimientos de MOVIMIENTOS_ELEC y delegá en la
        #   superclase para agregarlo; si no, avisá que no es eléctrico
        pass
    
    def atacar(self, objetivo):
        # TODO: convertí el voltaje en daño (voltaje // 10000), aplicá ventaja
        #   contra agua/planta, descontá con recibir_dano() e imprimí el movimiento
        pass


class Fuego(Pokemon):
    MOVIMIENTOS_FUEGO = ["Llamarada", "Rayo Solar", "Arañazo", "Garra Dragón"]
    
    def __init__(self, nombre, poder_llama=85):
        super().__init__(nombre, "fuego")
        self.poder_llama = poder_llama
    
    def aprender(self, mov):
        # TODO: aceptá solo movimientos de MOVIMIENTOS_FUEGO y delegá en la
        #   superclase; si no, avisá que no es fuego
        pass
    
    def atacar(self, objetivo):
        # TODO: usá poder_llama como daño base, aplicá ventaja contra
        #   planta/agua, descontá con recibir_dano() e imprimí el movimiento
        pass


class Agua(Pokemon):
    MOVIMIENTOS_AGUA = ["Hidrobomba", "Burbuja", "Acua Jet", "Surf"]
    
    def __init__(self, nombre, velocidad_nado=30):
        super().__init__(nombre, "agua")
        self.velocidad_nado = velocidad_nado
    
    def aprender(self, mov):
        # TODO: aceptá solo movimientos de MOVIMIENTOS_AGUA y delegá en la
        #   superclase; si no, avisá que no es agua
        pass
    
    def atacar(self, objetivo):
        # TODO: daño base 20, aplicá ventaja contra fuego/planta, descontá
        #   con recibir_dano() e imprimí el movimiento
        pass


# CREAR EQUIPO DE TIPOS DIFERENTES
pikachu = Electrico("Pikachu", 50000)
charmander = Fuego("Charmander", 60)
squirtle = Agua("Squirtle", 25)

print(pikachu)
print(charmander)
print(squirtle)

# VERIFICAR HERENCIA
print(f"\n¿Pikachu es Pokemon? {isinstance(pikachu, Pokemon)}")
print(f"Tipo: {pikachu.tipo}")

# PROBAR APRENDIZAJE LIMITADO POR TIPO
print("\n--- Entrenamiento ---")
pikachu.aprender("Thunderbolt")      # OK
pikachu.aprender("Llamarada")         # NO - no es eléctrico
charmander.aprender("Hidrobomba")     # NO - no es fuego
squirtle.aprender("Burbuja")          # OK

# BATALLA
print("\n--- Batalla ---")
print(pikachu)
print(charmander)
print(squirtle)
print()

pikachu.atacar(charmander)     # x2 contra planta pero char es fuego -> normal
charmander.atacar(squirtle)    # x0.5 contra agua
squirtle.atacar(pikachu)       # x2 contra electrico!

print()
print(pikachu)
print(charmander)
print(squirtle)
