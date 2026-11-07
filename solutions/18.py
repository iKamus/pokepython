"""Bloque 18 · Propiedades (@property) — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

class Pokemon:
    def __init__(self, nombre, tipo, nivel=1):
        self.nombre = nombre
        self.tipo = tipo
        self._nivel = nivel
        self._hp_max = nivel * 20
        self._hp = self._hp_max
    
    @property
    def nivel(self):
        """Getter: retorna el nivel actual."""
        return self._nivel
    
    @nivel.setter
    def nivel(self, valor):
        """Setter: solo acepta niveles entre 1 y 100."""
        if 1 <= valor <= 100:
            self._nivel = valor
            self._hp_max = valor * 20
            print(f"📈 {self.nombre} alcanzó nivel {valor}!")
        else:
            print("⚠️ Nivel inválido (debe ser 1-100)")
    
    @property
    def hp(self):
        """Getter: retorna el HP actual."""
        return self._hp
    
    @hp.setter
    def hp(self, valor):
        """Setter: limita HP entre 0 y max."""
        if 0 <= valor <= self._hp_max:
            self._hp = valor
        else:
            raise ValueError(f"HP debe estar entre 0 y {self._hp_max}")
    
    @property
    def vivo(self):
        """Propiedad de solo lectura: ¿el Pokémon sigue en pie?"""
        return self._hp > 0
    
    @property
    def porcentaje_hp(self):
        """¿Cuánto HP queda en porcentaje?"""
        return round(self._hp / self._hp_max * 100, 1)
    
    def recibir_daño(self, daño):
        nuevo_hp = max(0, self._hp - daño)
        self.hp = nuevo_hp
        print(f"💥 {self.nombre}: {daño} daño. HP: {nuevo_hp}/{self._hp_max}")
    
    def curar(self, cantidad=20):
        self.hp = min(self._hp + cantidad, self._hp_max)
        print(f"❤️ {self.nombre}: +{cantidad}HP. HP: {self.hp}/{self._hp_max}")


# PROBAR
pikachu = Pokemon("Pikachu", "electrico", 25)

print(f"Nivel: {pikachu.nivel}")       # 25
print(f"HP: {pikachu.hp}")              # 500
print(f"Vivo: {pikachu.vivo}")          # True
print(f"Porcentaje: {pikachu.porcentaje_hp}%")  # 100.0

print("\n--- Batalla ---")
pikachu.recibir_daño(200)
print(f"HP ahora: {pikachu.hp}")         # 300
print(f"% HP: {pikachu.porcentaje_hp}%") # 60.0

pikachu.curar(100)
print(f"Después de curar: {pikachu.hp}") # 400

# Intentar setear valores inválidos:
try:
    pikachu.hp = 9999    # Error!
except ValueError as e:
    print(f"❌ {e}")

print("\n--- Evolución ---")
pikachu.nivel = 50     # Validado: ok
print(f"Nivel: {pikachu.nivel}")   # 50
print(f"HP Max: {pikachu._hp_max}")  # 1000
print(f"HP: {pikachu.hp}")         # 1000 (se ajusta al max)
