"""Bloque 27 · Knapsack Problem

Seleccioná los mejores items para tu equipo con límite de peso.
"""

def knapsack(capacidad, pesos, valores, n):
    """Resuelve el problema de mochila 0/1 con programación dinámica."""
    # TODO: armá la tabla DP y devolvé dp[n][capacidad]
    return None  # TODO


def knapsack_trace(capacidad, pesos, valores, nombres, n):
    """Retorna el valor máximo Y los items seleccionados."""
    # TODO: armá la tabla DP y reconstruí la selección
    return None  # TODO


# ITEMS DE PREPARACIÓN PARA BATALLA
items = [
    {"nombre": "Poción", "peso": 1, "valor": 20},
    {"nombre": "Super Poción", "peso": 1, "valor": 50},
    {"nombre": "Hiper Poción", "peso": 2, "valor": 80},
    {"nombre": "Revivir", "peso": 2, "valor": 100},
    {"nombre": "Elixir", "peso": 1, "valor": 35},
    {"nombre": "Antídoto", "peso": 1, "valor": 15},
    {"nombre": "Bomba de Humo", "peso": 3, "valor": 90}
]

nombres = [i["nombre"] for i in items]
pesos = [i["peso"] for i in items]
valores = [i["valor"] for i in items]
max_capacidad = 5

print(f"=== MOCHILA BÁSICA ===\n")
print("Items disponibles:")
for i, item in enumerate(items):
    print(f"  {item['nombre']:>15} | peso: {pesos[i]} | valor: {valores[i]}")

# RETO 1 — Calcular valor máximo sin seleccionar items:
max_valor = knapsack(max_capacidad, pesos, valores, len(items))
print(f"\nValor máximo con capacidad {max_capacidad}: {max_valor}")

# RETO 2 — Saber QUÉ items seleccionar:
max_valor, indices = knapsack_trace(max_capacidad, pesos, valores, nombres, len(items))
items_seleccionados = [items[i]["nombre"] for i in indices]
peso_total = sum(pesos[i] for i in indices)

print(f"\n🎒 Selección óptima:")
for idx in indices:
    print(f"  ✓ {items[idx]['nombre']:>15} (peso: {pesos[idx]}, valor: {valores[idx]})")
print(f"\nPeso total: {peso_total}/{max_capacidad}")
print(f"Valor total: {max_valor}")
