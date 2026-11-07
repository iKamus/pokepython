"""Bloque 23 · Fundamentos de Recursión — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

# RETO 1 — Factorial recursivo (caso base + paso recursivo):
def factorial(n):
    """Calcula n! = n * (n-1) * ... * 1"""
    if n <= 1:
        return 1      # CASO BASE
    return n * factorial(n - 1)  # PASO RECUSIVO

print(f"5! = {factorial(5)}")     # 120
print(f"10! = {factorial(10)}")   # 3628800

# RETO 2 — Suma recursiva de una lista:
def suma_recursiva(lista):
    """Suma todos los elementos de la lista recursivamente."""
    if not lista:           # CASO BASE: lista vacía
        return 0
    return lista[0] + suma_recursiva(lista[1:])  # PASO: primer elemento + resto

numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"\nSuma de {numeros} = {suma_recursiva(numeros)}")  # 55

# RETO 3 — Potencia recursiva:
def potencia(base, exp):
    """Calcula base^exp de forma recursiva."""
    if exp == 0:            # CASO BASE
        return 1
    if exp == 1:            # CASO BASE
        return base
    return base * potencia(base, exp - 1)  # PASO

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
    if chain is None:
        chain = []
    
    formas = EVOLUTION_CHAINS.get(name, [])
    nueva_chain = chain + [name]
    
    if not formas:
        return nueva_chain  # CASO BASE: fin de la cadena
    
    # Para cada posible siguiente evolución, recursar y tomar la primera
    for next_form in formas:
        sub_cadena = evolucion(next_form, nueva_chain)
        if len(sub_cadena) > len(nueva_chain):
            return sub_cadena
    
    return nueva_chain


# Demo de evoluciones
starters = ["bulbasaur", "charmander", "squirtle", "pikachu"]
print("\n--- Cadenas Evolutivas ---")
for starter in starters:
    cadena = evolucion(starter)
    print(f"{starter.title()} → {' → '.join(cadena)}")