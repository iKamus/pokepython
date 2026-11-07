"""Bloque 06 · Funciones y scope

Creá funciones reutilizables para calcular daño, curar y verificar condiciones.
"""

# RETO 1 — calcular_dano(base, multiplicador=1.5): retorna base * multiplicador
def calcular_dano(base, multiplicador=1.5):
    # TODO: retorná base * multiplicador
    pass

print(f"calcular_dano(40) = {calcular_dano(40)}")   # 60.0

# RETO 2 — curar(hp, cantidad, tope=100): cura sin superar el tope
def curar(hp, cantidad, tope=100):
    # TODO: retorná el mínimo entre hp + cantidad y tope
    pass

print(f"curar(80, 30) = {curar(80, 30)}")  # 100

# RETO 3 — efectividad(tipo_ataque, tipo_defensor): devuelve el multiplicador
def efectividad(tipo_ataque, tipo_defensor):
    # TODO: devolvé 2.0 si agua vs fuego, 0.5 si fuego vs agua, 1.0 en otro caso
    pass

print(f"efectividad('agua', 'fuego') = {efectividad('agua', 'fuego')}")  # 2.0

# RETO 4 — sumar_dano(a, b): retorna la suma
def sumar_dano(a, b):
    # TODO: retorná a + b
    pass

print(f"sumar_dano(40, 35) = {sumar_dano(40, 35)}")  # 75

# RETO 5 — saludar_entrenador(nombre): imprime saludo, no devuelve nada
def saludar_entrenador(nombre):
    # TODO: imprimí el saludo de batalla
    pass

saludar_entrenador("Ash")

# RETO 6 — incrementar_turno(): suma 1 al contador global turnos_batalla
turnos_batalla = 0
def incrementar_turno():
    # TODO: usá global y sumá 1
    pass

incrementar_turno()
incrementar_turno()
print(f"Turnos de batalla: {turnos_batalla}")  # 2

# RETO 7 — valor_local(): variable local no afecta global
valor = 10
def valor_local():
    # TODO: asigná 5 a valor (solo local) y retornalo
    pass

print(f"Valor interno: {valor_local()}")  # 5
print(f"Valor global: {valor}")  # 10
