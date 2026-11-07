"""Bloque 28 · Longest Common Subsequence — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

def lcs_length(seq1, seq2):
    """Retorna la longitud de la subsecuencia común más larga."""
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def lcs_sequence(seq1, seq2):
    """Retorna la subsecuencia común más larga real."""
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i-1] == seq2[j-1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Reconstruir la secuencia con backtrack
    # seq1i1 → seq1[i-1]: notación corta de la comparación
    common = []
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i-1] == seq2[j-1]:
            common.append(seq1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return common[::-1]


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
