"""Bloque 28 · Longest Common Subsequence

Encontrá movimientos comunes entre dos sets de ataques.
"""

def lcs_length(seq1, seq2):
    """Retorna la longitud de la subsecuencia común más larga."""
    # TODO: armá la tabla dp de (m+1) × (n+1), compará los caracteres de
    #   ambas secuencias y retorná la celda final dp[m][n]
    return 0


def lcs_sequence(seq1, seq2):
    """Retorna la subsecuencia común más larga real."""
    # TODO: completá la DP, reconstruí la secuencia con backtrack y
    #   retorná los movimientos comunes en orden
    return []


# COMPARAR MOVESSETS DE POKÉMONS
print("=== ANÁLISIS DE MOVESSETS ===\n")

teammoves = ["Thunderbolt", "Volt Tackle", "Iron Tail", "Quick Attack"]
optimal_moveset = ["Thunderbolt", "Discharge", "Volt Tackle", "Electro Ball"]

print(f"Tu equipo actual:   {', '.join(teammoves)}")
print(f"Moveset óptimo:     {', '.join(optimal_moveset)}")

longitud = lcs_length(teammoves, optimal_moveset)
comunes = lcs_sequence(teammoves, optimal_moveset)

print(f"\nLongitud LCS: {longitud}")
print(f"Movimientos compartidos: {', '.join(comunes)}")

# Comparar otros equipos
print("\n--- Comparaciones adicionales ---\n")

p1_moves = ["Llamarada", "Plaza Solar", "Garra Dragon", "Arañazo"]
p2_moves = ["Llamarada", "Plasma Ígneo", "Garra Dragón", "Rayo"]

l1 = lcs_length(p1_moves, p2_moves)
c1 = lcs_sequence(p1_moves, p2_moves)
print(f"Pokémon A:     {', '.join(p1_moves)}")
print(f"Pokémon B:     {', '.join(p2_moves)}")
print(f"Compartidos:   {', '.join(c1)} ({l1} en común)\n")

p3_moves = ["Hidrobomba", "Piscada", "Burbuja", "Maremoto"]
p4_moves = ["Hidrobomba", "Cascada", "Piscada", "Giro Agua"]

l2 = lcs_length(p3_moves, p4_moves)
c2 = lcs_sequence(p3_moves, p4_moves)
print(f"Pokémon C:     {', '.join(p3_moves)}")
print(f"Pokémon D:     {', '.join(p4_moves)}")
print(f"Compartidos:   {', '.join(c2)} ({l2} en común)")
