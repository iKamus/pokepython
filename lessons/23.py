"""Bloque 23 · Fundamentos de Recursión

Funciones que se llaman a sí mismas para simular evolución Pokémon.
"""

# RETO 1 — Factorial recursivo (caso base + paso recursivo):
def factorial(n):
    """Calcula n! = n * (n-1) * ... * 1"""
    # TODO: caso base con n <= 1 y paso recursivo n * factorial(n - 1)
    return None

print(f"5! = {factorial(5)}")     # 120
print(f"10! = {factorial(10)}")   # 3628800

# RETO 2 — Suma recursiva de una lista:
def suma_recursiva(lista):
    """Suma todos los elementos de la lista recursivamente."""
    # TODO: caso base con lista vacía y paso lista[0] + suma_recursiva(lista[1:])
    return None

numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"\nSuma de {numeros} = {suma_recursiva(numeros)}")  # 55

# RETO 3 — Potencia recursiva:
def potencia(base, exp):
    """Calcula base^exp de forma recursiva."""
    # TODO: caso base con exp == 0 (o 1) y paso base * potencia(base, exp - 1)
    return None

print(f"\n2^10 = {potencia(2, 10)}")   # 1024
print(f"3^4 = {potencia(3, 4)}")       # 81

# RETO 4 — Cadena de evolución (recursión con diccionario):
EVOLUTION_CHAINS = {
    "bulbasaur": ["ivysaur", "venusaur"],
    "charmander": ["charmeleon", "charizard"],
    "squirtle": ["wartortle", "blastoise"],
    "pikachu": ["raichu"],
    "eevee": ["flareon", "jolteon", "vaporeon"],
}

def evolucion(name, chain=None):
    """Devuelve toda la cadena evolutiva desde el nombre dado."""
    # TODO: recursá sobre EVOLUTION_CHAINS armando la cadena completa;
    #   caso base: el nombre no está en el diccionario
    return []


# Demo de evoluciones
starters = ["bulbasaur", "charmander", "squirtle", "pikachu"]
print("\n--- Cadenas Evolutivas ---")
for starter in starters:
    cadena = evolucion(starter)
    print(f"{starter.title()} → {' → '.join(cadena)}")
