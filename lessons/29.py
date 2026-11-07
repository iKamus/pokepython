"""Bloque 29 · Batalla Pokémon Completa

JUEGO DE BATALLAS POKÉMON — Integrando todo lo aprendido.

POO + herencia + polimorfismo + estructuras de datos + algoritmos + DP.
Este proyecto sintetiza TODO lo del curso en un juego funcional por consola.
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
    MOVIMIENTOS = ["Chispazo", "Rayo", "Thunderbolt", "Volt Tackle", "ColaFerrovia"]
    
    def __init__(self, nombre, voltaje=100000):
        super().__init__(nombre, "electrico")
        self.voltaje = voltaje
        self.movimientos.extend(self.MOVIMIENTOS[:3])
    
    def atacar(self, objetivo):
        # TODO: daño = nivel × 8 × voltaje / 10000 × multiplicador de tipo
        #   (agua x2, planta x1/2); aplicá con recibir_dano() e imprimí
        #   "⚡ {nombre} usa {movimiento}! (-{daño}HP)"
        pass


class Fuego(Pokemon):
    MOVIMIENTOS = ["Llamarada", "Arañazo", "Plaza Solar", "GarraDragon", "PlasmaIgneo"]
    
    def __init__(self, nombre, poder_llama=85):
        super().__init__(nombre, "fuego")
        self.poder_llama = poder_llama
        self.movimientos.extend(self.MOVIMIENTOS[:3])
    
    def atacar(self, objetivo):
        # TODO: daño = poder_llama × (nivel / 10) × multiplicador de tipo
        #   (fuego x2, agua x1/2); aplicá con recibir_dano() e imprimí
        #   "🔥 {nombre} usa {movimiento}! (-{daño}HP)"
        pass


class Agua(Pokemon):
    MOVIMIENTOS = ["Hidrobomba", "Piscada", "Burbuja", "Maremoto", "Cascada"]
    
    def __init__(self, nombre, velocidad=30):
        super().__init__(nombre, "agua")
        self.velocidad = velocidad
        self.movimientos.extend(self.MOVIMIENTOS[:3])
    
    def atacar(self, objetivo):
        # TODO: daño = nivel × 7 × multiplicador de tipo (agua x2, planta x1/2);
        #   aplicá con recibir_dano() e imprimí "💧 {nombre} usa {movimiento}!"
        pass


# ════════════ MOTOR DE BATALLA ════════════

def batalla(pokemon1, pokemon2):
    print("\n" + "=" * 60)
    print(f"   ⚔️  ¡BATALLA! {pokemon1.nombre} vs {pokemon2.nombre}")
    print("=" * 60)
    
    turno = 1
    # TODO: simulá el combate con un while (máx. 30 turnos): elegí quién
    #   ataca primero por velocidad, alterná .atacar() entre ambos e
    #   imprimí el estado de cada Pokémon en cada turno
    
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
