"""Bloque 27 · Knapsack Problem — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

def knapsack(capacidad, pesos, valores, n):
    """Resuelve mochila 0/1 con programación dinámica."""
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacidad + 1):
            if pesos[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - pesos[i - 1]] + valores[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacidad]


def knapsack_trace(capacidad, pesos, valores, nombres, n):
    """Retorna valor máximo Y qué items fueron seleccionados."""
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacidad + 1):
            if pesos[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w],
                               dp[i - 1][w - pesos[i - 1]] + valores[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    
    # Backtrack: reconstruir qué items se eligieron
    selected = []
    w = capacidad
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= pesos[i - 1]
    
    return dp[n][capacidad], selected[::-1]


# === ITEMS DE PREPARACIÓN ===
items = [
    {"nombre": "Poción",      "peso": 1, "valor": 20},
    {"nombre": "Super Poción","peso": 1, "valor": 50},
    {"nombre": "Hiper Poción","peso": 2, "valor": 80},
    {"nombre": "Revivir",     "peso": 2, "valor": 100},
    {"nombre": "Elixir",      "peso": 1, "valor": 35},
    {"nombre": "Antídoto",    "peso": 1, "valor": 15},
    {"nombre": "Bomba Humo",  "peso": 3, "valor": 90}
]

nombres = [i["nombre"] for i in items]
pesos   = [i["peso"]   for i in items]
valores = [i["valor"]  for i in items]
cap_max = 5

print(f"=== MOCHILA ÓPTIMA (capacidad {cap_max}) ===\n")

for item in items:
    print(f"  {item['nombre']:>15} | peso={item['peso']} | valor={item['valor']}")

max_v = knapsack(cap_max, pesos, valores, len(items))
print(f"\nValor máximo sin seleccionar: {max_v}")

max_v, idxs = knapsack_trace(cap_max, pesos, valores, nombres, len(items))
total_peso = sum(pesos[i] for i in idxs)

print(f"\n🎒 SELECCIÓN ÓPTIMA:")
for i in idxs:
    print(f"  ✓ {items[i]['nombre']:>15} (p:{pesos[i]}, v:{valores[i]})")
print(f"\nPeso total: {total_peso}/{cap_max}  |  Valor total: {max_v}")
