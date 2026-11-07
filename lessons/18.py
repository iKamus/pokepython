"""Bloque 18 · Propiedades (@property)

Usá propiedades para controlar cómo se leen y modifican los atributos.
"""

class Pokemon:
    def __init__(self, nombre, tipo, nivel=1):
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel           # TODO: volvé esto una @property con setter que valide 1-100
        self._hp_max = nivel * 20
        self.hp = self._hp_max       # TODO: @property + setter que limite HP entre 0 y _hp_max
        self.vivo = True             # TODO: @property de solo lectura: ¿sigue en pie?
        self.porcentaje_hp = 100.0   # TODO: @property calculada: hp / hp_max * 100

    def recibir_daño(self, daño):
        # TODO: aplicá el daño usando el setter de hp
        pass

    def curar(self, cantidad=20):
        # TODO: curá usando el setter de hp (sin pasarte del máximo)
        pass


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
