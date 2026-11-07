"""Bloque 14 · json — Guardar y cargar equipo

Persistí datos de entrenador con el módulo json.
"""
import json

# RETO 1 — Crear datos de entrenador:
entrenador = {
    "nombre": "Red",
    "nivel": 8,
    "insignias": 8,
    "equipo": ["Pikachu", "Charizard", "Blastoise", "Venusaur", "Eevee", "Alakazam"],
    "pociones": 10,
    "revivir": 2
}

# RETO 2 — Convertir a JSON string:
texto_json = None  # TODO: serializá entrenador con json.dumps(..., indent=2, ensure_ascii=False)
print("JSON serializado:")
print("")  # TODO: imprimí texto_json

# RETO 3 — Parsear JSON de vuelta (simular carga de archivo):
datos_leidos = None  # TODO: parseá texto_json con json.loads(...)
print("")  # TODO: imprimí equipo, primer pokemon y pociones desde datos_leidos

# RETO 4 — Escribir a archivo y leer (simulado):
archivo = "./entrenador_save.json"
# TODO: escribí entrenador con json.dump(..., f, indent=2, ensure_ascii=False)
#   y leelo de vuelta con json.load(f); imprimí nombre y nivel del guardado
