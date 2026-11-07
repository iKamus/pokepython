"""Bloque 21 · Polimorfismo

Tratá subclases distintas como si fueran iguales. Cada Pokémon tiene .atacar().
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
        # TODO: si el tipo del objetivo da ventaja, el daño es 20; si no, 10.
        #   Descontá de objetivo.hp y retorná si fue efectivo
        pass


class Fuego(Pokemon):
    MOVIMIENTOS = ["Llamarada", "Rayo Solar", "Arañazo"]
    
    def atacar(self, objetivo):
        # TODO: ventaja contra planta (20) o neutral (10); descontá de
        #   objetivo.hp e imprimí el movimiento usado; retorná si fue efectivo
        pass


class Planta(Pokemon):
    MOVIMIENTOS = ["Látigo Cepa", "Hoja Afilada", "Gigadrenado"]
    
    def atacar(self, objetivo):
        # TODO: ventaja contra agua (20) o neutral (10); descontá de
        #   objetivo.hp e imprimí el movimiento usado; retorná si fue efectivo
        pass


class Agua(Pokemon):
    MOVIMIENTOS = ["Hidrobomba", "Acua Jet", "Burbuja"]
    
    def atacar(self, objetivo):
        # TODO: ventaja contra fuego (20) o neutral (10); descontá de
        #   objetivo.hp e imprimí el movimiento usado; retorná si fue efectivo
        pass


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
