"""Bloque 06 · Funciones y scope — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Daño con multiplicador por defecto:
def calcular_daño(base, multiplicador=1.5):
    return base * multiplicador

print(f"calcular_daño(40) = {calcular_daño(40)}")  # 60.0

# RETO 2 — Curación con tope:
def curar(hp, cantidad, tope=100):
    if hp + cantidad > tope:
        return tope
    return hp + cantidad

print(f"curar(80, 30) = {curar(80, 30)}")  # 100

# RETO 3 — Efectividad de tipos:
def efectividad(tipo_ataque, tipo_defensor):
    if tipo_ataque == "agua" and tipo_defensor == "fuego":
        return 2.0
    if tipo_ataque == "fuego" and tipo_defensor == "agua":
        return 0.5
    return 1.0

print(f"efectividad('agua', 'fuego') = {efectividad('agua', 'fuego')}")  # 2.0

# RETO 4 — Sumar daño:
def sumar_daño(a, b):
    return a + b

print(f"sumar_daño(40, 35) = {sumar_daño(40, 35)}")  # 75

# RETO 5 — Saludar sin devolver:
def saludar_entrenador(nombre):
    print(f"¡Hola, {nombre}! Preparate para la batalla.")

saludar_entrenador("Ash")

# RETO 6 — Contador global de turnos:
turnos_batalla = 0
def incrementar_turno():
    global turnos_batalla
    turnos_batalla += 1

incrementar_turno()
incrementar_turno()
print(f"Turnos de batalla: {turnos_batalla}")  # 2

# RETO 7 — Variable local:
valor = 10
def valor_local():
    valor = 5
    return valor

print(f"Valor interno: {valor_local()}")  # 5
print(f"Valor global: {valor}")  # 10
