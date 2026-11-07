"""Bloque 21 · Polimorfismo — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

class Pokemon:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo
        self.hp_max = 100
        self.hp = self.hp_max
    
    def atacar(self, objetivo):
        """Override en cada subclass."""
        pass


class Electrico(Pokemon):
    MOVIMIENTOS = ["Chispazo", "Rayo", "Impactrueno"]
    
    def atacar(self, objetivo):
        efectivo = objetivo.tipo == "agua"
        dano = 20 if efectivo else 10
        objetivo.hp = max(0, objetivo.hp - dano)
        mov = self.MOVIMIENTOS[min(len(self.MOVIMIENTOS)-1, self.nivel//5)] if hasattr(self,'nivel') else "Chispazo"
        print(f"⚡ {self.nombre} usa {mov}! (-{dano}HP)")
        return efectivo


class Fuego(Pokemon):
    MOVIMIENTOS = ["Llamarada", "Rayo Solar", "Arañazo"]
    
    def atacar(self, objetivo):
        # objetivotipo: si self.tipo == objetivo.tipo → daño neutral
        if self.tipo == objetivo.tipo:
            efectivo = False
            dano = 10
        else:
            efectivo = objetivo.tipo == "planta"
            dano = 20 if efectivo else 10
        objetivo.hp = max(0, objetivo.hp - dano)
        mov = self.MOVIMIENTOS[min(len(self.MOVIMIENTOS)-1, getattr(self,'nivel',0)//5)] if hasattr(self,'nivel') else "Llamarada"
        print(f"🔥 {self.nombre} usa {mov}! (-{dano}HP)")
        return efectivo


class Planta(Pokemon):
    MOVIMIENTOS = ["Látigo Cepa", "Hoja Afilada", "Gigadrenado"]
    
    def atacar(self, objetivo):
        efectivo = objetivo.tipo == "agua"
        dano = 20 if efectivo else 10
        objetivo.hp = max(0, objetivo.hp - dano)
        mov = self.MOVIMIENTOS[min(len(self.MOVIMIENTOS)-1, getattr(self,'nivel',0)//5)] if hasattr(self,'nivel') else "Hoja Afilada"
        print(f"🌿 {self.nombre} usa {mov}! (-{dano}HP)")
        return efectivo


class Agua(Pokemon):
    MOVIMIENTOS = ["Hidrobomba", "Acua Jet", "Burbuja"]
    
    def atacar(self, objetivo):
        efectivo = objetivo.tipo == "fuego"
        dano = 20 if efectivo else 10
        objetivo.hp = max(0, objetivo.hp - dano)
        mov = self.MOVIMIENTOS[min(len(self.MOVIMIENTOS)-1, getattr(self,'nivel',0)//5)] if hasattr(self,'nivel') else "Hidrobomba"
        print(f"💧 {self.nombre} usa {mov}! (-{dano}HP)")
        return efectivo


# BATALLA POLIMÓRFICA
def iniciar_combate(eq1, eq2):
    p1 = eq1[0]
    p2 = eq2[0]
    print(f"⚔️ ¡{p1.nombre} ({p1.tipo}) vs {p2.nombre} ({p2.tipo})!")
    print("=" * 40)
    
    turno = 1
    while p1.hp > 0 and p2.hp > 0:
        print(f"\n--- Turno {turno} ---")
        
        # Polimorfismo: ambos tienen .atacar() pero se comportan diferente
        p1_efectivo = p1.atacar(p2)
        
        if p2.hp > 0:
            p2_efectivo = p2.atacar(p1)
        
        print(f"   HP: {p1.nombre}={p1.hp}/{p1.hp_max} | {p2.nombre}={p2.hp}/{p2.hp_max}")
        turno += 1
        
        if turno > 20:  # Safety limit
            print("¡Empate por agotamiento de turnos!")
            break
    
    ganador = p1 if p2.hp <= 0 else p2
    print(f"\n🏆 ¡{ganador.nombre} gana la batalla!")


# BATALLAS EJEMPLO:
print("\n" + "=" * 50)
print("BATALLA 1: Electrico vs Agua (super efectivo!)")
print("=" * 50)
iniciar_combate([Electrico("Pikachu", "electrico")], 
                [Agua("Squirtle", "agua")])

print("\n" + "=" * 50)
print("BATALLA 2: Fuego vs Planta (super efectivo!)")
print("=" * 50)
iniciar_combate([Fuego("Charmander", "fuego")], 
                [Planta("Bulbasaur", "planta")])

print("\n" + "=" * 50)
print("BATALLA 3: Neutral — Agua vs Fuego")
print("=" * 50)
iniciar_combate([Agua("Blastoise", "agua")], 
                [Fuego("Charizard", "fuego")])

print("\n" + "=" * 50)
print("BATALLA 4: Espejo — Fuego vs Fuego (mismo tipo → neutral)")
print("=" * 50)
iniciar_combate([Fuego("Charizard", "fuego")],
                [Fuego("Charmander", "fuego")])
