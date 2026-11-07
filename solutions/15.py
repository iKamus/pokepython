"""Bloque 15 · try/except — Errores controlados — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — División segura con try/except:
def dividir(a, b):
    try:
        resultado = a / b
        return f"{a} ÷ {b} = {resultado}"
    except ZeroDivisionError:
        return "❌ No podés dividir por cero!"
    finally:
        print("   (intento de división procesado)")

print(dividir(10, 3))     # 3.33...
print(dividir(10, 0))     # Error message

# RETO 2 — Acceso seguro a Pokédex:
pokdex = {25: "Pikachu", 6: "Charizard", 9: "Blastoise"}

def obtener_pokemon(id_pokemon):
    try:
        return pokdex[id_pokemon]
    except KeyError:
        return f"❌ ID {id_pokemon} no encontrado en la Pokédex."

print(obtener_pokemon(25))     # Pikachu
print(obtener_pokemon(151))    # Error message

# RETO 3 — Parsear nivel desde texto:
def parseaar_nivel(texto):
    try:
        nivel = int(texto)
        if 1 <= nivel <= 100:
            return nivel
        return "Nivel fuera de rango (1-100)"
    except ValueError:
        return "❌ Debes pasar un número válido."

print(parseaar_nivel("42"))     # 42
print(parseaar_nivel("abc"))    # Error message
print(parseaar_nivel("150"))    # Fuera de rango

# RETO 4 — Excepción genérica para operaciones aritméticas:
def intentar_operacion(a, b, oper):
    try:
        if oper == "+": return a + b
        if oper == "-": return a - b
        if oper == "*": return a * b
        if oper == "/": return a / b
        raise ValueError(f"Operación '{oper}' no reconocida")
    except Exception as e:
        return f"❌ Error: {e}"

print(intentar_operacion(10, 3, "+"))  # 13
print(intentar_operacion(10, 0, "/"))  # Zero division error
