"""Bloque 06 · Funciones y scope — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Función que retorna el doble de un número:
def doble(n):
    return n * 2

print(f"doble(21) = {doble(21)}")  # 42
assert doble(21) == 42

# RETO 2 — Dos parámetros con default:
def area_rectangulo(base, altura=1):
    return base * altura

print(f"area_rectangulo(4) = {area_rectangulo(4)}")     # 4
print(f"area_rectangulo(4, 3) = {area_rectangulo(4, 3)}")  # 12

# RETO 3 — Parámetro obligatorio + opcional por nombre:
def nombre_completo(nombre, apellido=""):
    if apellido:
        return f"{nombre} {apellido}"
    return nombre

print(f"nombre_completo('Red') = '{nombre_completo('Red')}'")           # Red
print(f"nombre_completo('Red', 'Blue') = '{nombre_completo('Red', 'Blue')}'")  # Red Blue

print(nombre_completo("Ada", "Lovelace"))  # Ada Lovelace

# RETO 4 — Sumar dos valores:
def sumar(a, b):
    return a + b

print(f"sumar(7, 8) = {sumar(7, 8)}")  # 15
assert sumar(7, 8) == 15

# RETO 5 — Imprimir sin devolver nada (return implícito None):
def saludar(nombre):
    print(f"Hola, {nombre}! Bienvenido al mundo Pokémon.")

saludar("Ash")  # Hola, Ash! Bienvenido...

# RETO 6 — Modificar variable global con global:
globales_counter = 0
def incrementar():
    global globales_counter
    globales_counter += 1

incrementar()
incrementar()
print(f"Contador global: {globales_counter}")  # 2

# RETO 7 — Variable local no afecta global:
valor = 10
def valor_local():
    valor = 5  # Solo local
    return valor

print(f"Valor interno: {valor_local()}")   # 5
print(f"Valor global: {valor}")             # 10 (sin cambios)
