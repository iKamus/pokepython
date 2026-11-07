"""Bloque 29 · Batalla Pokémon Completa — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

import json
import random
from datetime import datetime

# ════════════ CLASES BASE ════════════

class Pokemon:
    TIPOS_SUPER = {
        "electrico": ["agua", "volador"],
        "fuego": ["planta", "hielo", "acero", "bicho"],
        "agua": ["fuego", "roca", "tierra"],
        "planta": ["agua", "roca", "tierra"],
        "lucha": ["normal", "hielo", "roca", "siniestro", "acero"],
        "veneno": ["planta", "hada"],
        "tierra": ["electrico", "fuego", "roca", "veneno", "acero"],
        "volador": ["planta", "lucha", "bicho"],
        "bicho": ["planta", "psiquico", "siniestro"],
        "roca": ["fuego", "volador", "bicho", "tierra"],
        "hielo": ["planta", "tierra", "volador", "dragon"],
        "dragon": ["dragon"],
        "siniestro": ["psiquico", "fantasma"],
        "hada": ["lucha", "siniestro", "dragon"]
    }
    
    def __init__(self, nombre, tipo, nivel=5):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        self.hp_max = nivel * 20
        self.hp = self.hp_max
        self.movimientos = [self._movimiento_base()]
        self.exp = 0
    
    def _movimiento_base(self):
        return "Placaje"
    
    @property
    def vivo(self):
        return self.hp > 0
    
    @property
    def porcentaje_hp(self):
        return round(self.hp / self.hp_max * 100, 1) if self.hp_max else 0
    
    def __str__(self):
        emoji = "💀" if not self.vivo else "🟢"
        hp_bar = f"{self.hp}/{self.hp_max}"
        return f"{emoji} {self.nombre:<15} Nv.{self.nivel} {self.tipo:<10} [{hp_bar}] HP:{self.porcentaje_hp}%"
    
    def aprender(self, mov):
        if mov not in self.movimientos:
            self.movimientos.append(mov)
    
    def ganar_exp(self, exp):
        self.exp += exp
        niveles_ganados = self.exp // 100
        for _ in range(niveles_ganados):
            self.subir_nivel()
    
    def subir_nivel(self):
        self.nivel += 1
        self.hp_max = self.nivel * 20
        self.hp = min(self.hp + 20, self.hp_max)
        print(f"  ⬆️ ¡{self.nombre} subió a Nv.{self.nivel}!")
    
    def recibir_dano(self, dano):
        self.hp = max(0, self.hp - dano)
    
    def curar(self, cantidad=20):
        self.hp = min(self.hp + cantidad, self.hp_max)


class Electrico(Pokemon):
    MOVIMIENTOS = ["Chispazo", "Rayo", "Thunderbolt", "Volt Tackle", "Cola Férrea"]
    
    def __init__(self, nombre, voltaje=100000):
        super().__init__(nombre, "electrico")
        self.voltaje = voltaje
        self.movimientos.extend(self.MOVIMIENTOS[:3])
    
    def atacar(self, objetivo):
        mult = 2.0 if objetivo.tipo in self.TIPOS_SUPER.get("electrico", []) else 1.0
        mult = 0.5 if objetivo.tipo == "planta" else mult
        dano = max(1, int((self.nivel * 8 * self.voltaje / 10000) * mult))
        objetivo.recibir_dano(dano)
        mov = self.movimientos[min(len(self.movimientos)-1, self.nivel // 5)]
        print(f"  ⚡ {self.nombre} usa {mov}! (-{dano}HP)")


class Fuego(Pokemon):
    MOVIMIENTOS = ["Llamarada", "Arañazo", "Rayo Solar", "Garra Dragón", "Envite Ígneo"]
    
    def __init__(self, nombre, poder_llama=85):
        super().__init__(nombre, "fuego")
        self.poder_llama = poder_llama
        self.movimientos.extend(self.MOVIMIENTOS[:3])
    
    def atacar(self, objetivo):
        mult = 2.0 if objetivo.tipo in self.TIPOS_SUPER.get("fuego", []) else 1.0
        mult = 0.5 if objetivo.tipo == "agua" else mult
        dano = max(1, int(self.poder_llama * (self.nivel / 10) * mult))
        objetivo.recibir_dano(dano)
        mov = self.movimientos[min(len(self.movimientos)-1, self.nivel // 5)]
        print(f"  🔥 {self.nombre} usa {mov}! (-{dano}HP)")


class Agua(Pokemon):
    MOVIMIENTOS = ["Hidrobomba", "Acua Jet", "Burbuja", "Surf", "Cascada"]
    
    def __init__(self, nombre, velocidad=30):
        super().__init__(nombre, "agua")
        self.velocidad = velocidad
        self.movimientos.extend(self.MOVIMIENTOS[:3])
    
    def atacar(self, objetivo):
        mult = 2.0 if objetivo.tipo in self.TIPOS_SUPER.get("agua", []) else 1.0
        mult = 0.5 if objetivo.tipo == "planta" else mult
        dano = max(1, int(self.nivel * 7 * mult))
        objetivo.recibir_dano(dano)
        mov = self.movimientos[min(len(self.movimientos)-1, self.nivel // 5)]
        print(f"  💧 {self.nombre} usa {mov}! (-{dano}HP)")


# ════════════ MOTOR DE BATALLA ════════════

def batalla(pokemon1, pokemon2):
    print("\n" + "=" * 60)
    print(f"   ⚔️  ¡BATALLA! {pokemon1.nombre} vs {pokemon2.nombre}")
    print("=" * 60)
    
    turno = 1
    while pokemon1.vivo and pokemon2.vivo and turno <= 30:
        print(f"\n--- Turno {turno} ---")
        
        # Polimorfismo: todos tienen .atacar() pero se comporta distinto
        p1_v = getattr(pokemon1, 'velocidad', 50)
        p2_v = getattr(pokemon2, 'velocidad', 50)
        primero = pokemon1 if p1_v >= p2_v else pokemon2
        segundo = pokemon2 if primero is pokemon1 else pokemon1
        
        print(f"  ► {primero.nombre} ataca...")
        primero.atacar(segundo)
        
        if segundo.vivo:
            print(f"  ► {segundo.nombre} contraataca...")
            segundo.atacar(primero)
        
        print(f"\n  {pokemon1}")
        print(f"  {pokemon2}")
        turno += 1
    
    ganador = pokemon1 if not pokemon2.vivo else pokemon2
    perdedor = pokemon2 if ganador is pokemon1 else pokemon1
    print(f"\n{'=' * 60}")
    print(f"  🏆 ¡{ganador.nombre} GANA LA BATALLA!")
    print(f"  💀 {perdedor.nombre} fue derrotado.")
    print(f"{'=' * 60}")
    return ganador


# ════════════ GUARDAR/CARGAR CON JSON ════════════

def guardar_partida(ganador, nombre_entrenador="Entrenador"):
    partida = {
        "fecha": str(datetime.now()),
        "entrenador": nombre_entrenador,
        "pokemon": {k: v for k, v in ganador.__dict__.items() if k != "movimientos"},
        "tipo_clase": type(ganador).__name__,
        "movimientos": ganador.movimientos
    }
    with open("./battle_save.json", "w", encoding="utf-8") as f:
        json.dump(partida, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Partida guardada en battle_save.json")


# ════════════ EJECUCIÓN PRINCIPAL ════════════

print("╔══════════════════════════════════════════════╗")
print("║     🎮 BATALLA POKÉMON EN PYTHON 🎮          ║")
print("║  POO · Herencia · Polimorfismo · Grafos      ║")
print("╚══════════════════════════════════════════════╝\n")

# Crear equipo de tipos variados (herencia de clases)
pika    = Electrico("Pikachu", 50000)
charz   = Fuego("Charizard", 120)
blast   = Agua("Blastoise", 40)

print("EQUIPOS ENTRANDES:")
for pok in [pika, charz, blast]:
    print(f"  {pok}")

print("\n" + "-" * 60)
print("\n¡Las batallas comienzan!\n")

batalla(pika, charz)       # electrico vs fuego
print("\n" + "-" * 60)
batalla(charz, blast)      # fuego vs agua

# Guardar resultado
if blast.vivo:
    guardar_partida(blast, "Entrenador")
elif charz.vivo:
    guardar_partida(charz, "Entrenador")
else:
    guardar_partida(pika, "Entrenador")
