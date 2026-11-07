"""Bloque 25 · Grafos de Tipos — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""

class TypeMatchup:
    """Grafo de ventajas de tipo Pokémon."""
    
    SUPER_EFECTIVO = {
        "electrico": {"agua", "volador"},
        "fuego": {"planta", "hielo", "acero", "bicho"},
        "agua": {"fuego", "roca", "tierra"},
        "planta": {"agua", "roca", "tierra"},
        "lucha": {"normal", "hielo", "roca", "siniestro", "acero"},
        "veneno": {"planta", "hada"},
        "tierra": {"electrico", "fuego", "roca", "veneno", "acero"},
        "volador": {"planta", "lucha", "bicho"},
        "bicho": {"planta", "psiquico", "siniestro"},
        "roca": {"fuego", "volador", "bicho", "tierra"},
        "hielo": {"planta", "tierra", "volador", "dragon"},
        "dragon": {"dragon"},
        "siniestro": {"psiquico", "fantasma"},
        "hada": {"lucha", "siniestro", "dragon"}
    }
    
    def __init__(self):
        self.super_efectivo = self.SUPER_EFECTIVO
        self.grafo = {}
        self._construir()
    
    def _construir(self):
        """Construye el grafo de adyacencia."""
        for ofensivo in self.SUPER_EFECTIVO:
            if ofensivo not in self.grafo:
                self.grafo[ofensivo] = set()
        
        # Grafo inverso: quién supera a este tipo?
        self.vulnerable_a = {}
        for ofensivo, defensivos in self.SUPER_EFECTIVO.items():
            for defensivo in defensivos:
                self.vulnerable_a.setdefault(defensivo, []).append(ofensivo)
    
    def quien_gana(self, mov_tipo, def_tipo):
        """Retorna el multiplicador de daño."""
        if def_tipo in self.super_efectivo.get(mov_tipo, set()):
            return 2.0
        return 1.0
    
    def mejor_ataque(self, defensor_tipo):
        """¿Qué tipo de movimiento sería más efectivo?"""
        mejores = []
        max_mult = 0
        for ofensivo, defensivos in self.super_efectivo.items():
            if defensor_tipo in defensivos:
                mejores.append((ofensivo, 2.0))
                max_mult = 2.0
        
        return mejores or [("normal", 1.0)]  # sin ventajas → ["normal"]
    
    def vulnerable_a_list(self, tipo):
        """¿Quiénes son fuertes contra este tipo?"""
        return self.vulnerable_a.get(tipo, [])
    
    def mostrar_tabla(self):
        """Imprime toda la tabla de matchups."""
        print("Tabla de ventajas de tipo:\n")
        for ofensivo, defensivos in sorted(self.super_efectivo.items()):
            print(f"  {ofensivo:15} → {', '.join(sorted(defensivos))}")


# CREAR Y USAR
tm = TypeMatchup()

print("=== TABLA DE TIPOS ===\n")
tm.mostrar_tabla()

print("\n\n=== CONSULTAS ===\n")
# ¿Qué ataca fuerte al Charizard (fuego)?
mejores_vs_fuego = tm.mejor_ataque("fuego")
print(f"Mejores ataques contra FUEGO:")
for t, m in mejores_vs_fuego:
    print(f"  {t} ({m}x)")

# ¿Quién gana eléctrico vs agua?
resultado = tm.quien_gana("electrico", "agua")
print(f"\nElectrico vs Agua: {resultado}x {'(super efectivo!)' if resultado > 1 else '(neutral)'}")

# ¿Quién es fuerte contra dragon?
fuertes_contra_dragon = tm.vulnerable_a_list("dragon")
print(f"\nFuertes contra DRAGON: {', '.join(fuertes_contra_dragon)}")

# Sin ventajas, la lista de mejores vuelve con el tipo por defecto:
print("Por defecto: [\"normal\"]")
