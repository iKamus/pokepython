"""Bloque 14 · json — Guardar y cargar equipo — SOLUCIÓN

Solución completa de la lección, lista para ejecutar.
"""
import json

# RETO 1 — Crear datos de entrenador:
entrenador = {
    "nombre": "Red",
    "nivel": 8,
    "insignias": 8,
    "equipo": ["Pikachu", "Charizard", "Blastoise", "Venusaur", "Eevee", "Alakazam"],
    "pociones": 10,
    "revivires": 2
}

# RETO 2 — Convertir a JSON string:
texto_json = json.dumps(entrenador, indent=2, ensure_ascii=False)
print("JSON serializado:")
print(texto_json)

# RETO 3 — Parsear JSON de vuelta (simular carga de archivo):
datos_leidos = json.loads(texto_json)
print(f"\nEquipo al cargar: {len(datos_leidos['equipo'])} pokémons")
print(f"Primer pokemon: {datos_leidos['equipo'][0]}")
print(f"Pociones: {datos_leidos['pociones']}")

# RETO 4 — Escribir a archivo y leer (simulado):
archivo = "./entrenador_save.json"
with open(archivo, 'w', encoding='utf-8') as f:
    json.dump(entrenador, f, indent=2, ensure_ascii=False)
print(f"\nGuardado en {archivo}")

# Verificar que se pudo leer de vuelta:
with open(archivo, 'r', encoding='utf-8') as f:
    guardado = json.load(f)
print(f"Verificación: {guardado['nombre']} tiene {guardado['nivel']} insignias")
