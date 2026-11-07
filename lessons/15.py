"""Bloque 15 · try/except — Errores controlados

Prevén crashes y manejá errores elegantes como un experto.
"""

# RETO 1 — División segura con try/except:
def dividir(a, b):
    # TODO: envolvé a / b en try/except ZeroDivisionError, con finally
    #   imprimiendo "(intento de división procesado)"
    return None

print(dividir(10, 3))     # 3.33...
print(dividir(10, 0))     # Error message

# RETO 2 — Acceso seguro a Pokédex:
pokdex = {25: "Pikachu", 6: "Charizard", 9: "Blastoise"}

def obtener_pokemon(id_pokemon):
    # TODO: intentá pokdex[id_pokemon] y capturá KeyError con mensaje claro
    return None

print(obtener_pokemon(25))     # Pikachu
print(obtener_pokemon(151))    # Error message

# RETO 3 — Parsear nivel desde texto:
def parseaar_nivel(texto):
    # TODO: convertí a int dentro de try/except ValueError y validá 1-100
    return None

print(parseaar_nivel("42"))     # 42
print(parseaar_nivel("abc"))    # Error message
print(parseaar_nivel("150"))    # Fuera de rango

# RETO 4 — Excepción genérica para operaciones aritméticas:
def intentar_operacion(a, b, oper):
    # TODO: resolvé +, -, *, / dentro de try y capturá Exception con
    #   "Operación '{oper}' no reconocida" para operadores desconocidos
    return None

print(intentar_operacion(10, 3, "+"))  # 13
print(intentar_operacion(10, 0, "/"))  # Zero division error
