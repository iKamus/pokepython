"""Bloque 02 · Variables y tipos de datos — SOLUCIÓN

Solución completa de la lección: cada reto asignado con su valor final.
"""

# RETO 1 — Tres variables snake_case:
#   al empezar el ejercicio cada una valía None
nombre_completo = None
edad = None
activo = None

# Valores finales del entrenador:
nombre_completo = "Ash"
edad = 14
activo = True

# RETO 2 — Constante en MAYÚSCULAS con el valor 100:
MAX_NIVEL = 100

# RETO 3 — Cantidad de compañeros en tu equipo:
cantidad_equipo = 6

# RETO 4 — F-string: "{nombre_completo} tiene {edad} años"
mensaje = f"{nombre_completo} tiene {edad} años"

# RETO 5 — Imprimí mensaje con print()
print(mensaje)

# RETO 6 — La misma info concatenando con + y str():
resumen = nombre_completo + " tiene " + str(edad) + " años"
print(resumen)
