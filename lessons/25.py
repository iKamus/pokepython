"""Bloque 25 · Grafos de Tipos

Modelá las relaciones de tipos como un grafo dirigido.
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
        # TODO: construí el grafo y el inverso
        pass
    
    def quien_gana(self, mov_tipo, def_tipo):
        """Retorna el multiplicador de daño."""
        # TODO: 2.0 si es super efectivo, si no 1.0
        return None  # TODO
    
    def mejor_ataque(self, defensor_tipo):
        """¿Qué tipo de movimiento sería más efectivo?"""
        # TODO: buscá los tipos que superan al defensor
        return None  # TODO
    
    def vulnerable_a_list(self, tipo):
        """¿Quiénes son fuertes contra este tipo?"""
        return []  # TODO
    
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
print("")  # TODO

# ¿Quién gana eléctrico vs agua?
resultado = tm.quien_gana("electrico", "agua")
print(f"\nElectrico vs Agua: {resultado}x {'(super efectivo!)' if resultado > 1 else '(neutral)'}")

# ¿Quién es fuerte contra dragon?
fuertes_contra_dragon = tm.vulnerable_a_list("dragon")
print(f"\nFuertes contra DRAGON: {', '.join(fuertes_contra_dragon)}")
