# ⚡ PokéPython — Curso de Python con Pokémon

Curso interactivo completo de Python desde cero hasta avanzado, ambientado en el universo Pokémon.

## 🚀 Cómo usar

**Necesita un servidor.** Abrir `index.html` con doble clic NO funciona: el navegador
bloquea los módulos ES y los `fetch()` en `file://` (origen `null`), así que la página
queda vacía. No es un bug de la app, es una regla de seguridad del navegador.

```bash
# Recomendado: el servidor del proyecto (manda no-store, evita caché vieja)
python serve.py            # http://127.0.0.1:8000
python serve.py 9000 --open  # otro puerto y abre el navegador

# Alternativa con la stdlib, si preferís no usar serve.py
python -m http.server 8000  # → ojo: sin headers de caché, puede servir JS viejo
```

> **Runtime local.** Python en el navegador (Pyodide) y el editor (CodeMirror) están
> vendorizados: la app **no depende de ningún CDN** y funciona sin internet. La primera vez,
> si falta el runtime, se baja una sola vez con `python vendor/fetch_pyodide.py` (19 MB);
> `vendor/pyodide/` queda fuera de git para no inflar el repo.

### Tests

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements-dev.txt   # una vez
.venv/Scripts/python -m pytest              # invariantes de datos + soluciones (~3 s)
.venv/Scripts/python -m pytest -m browser   # landing, tema, editor y Pyodide (~25 s)
```

## 📋 Estructura del curso

### Módulo 01 — Fundamentos
| Lección | Tema | Concepto |
|---------|------|----------|
| 1 | ¿Qué es Python? | `print()`, comentarios |
| 2 | Variables y tipos | `str`, `int`, `float`, `bool`, f-strings |
| 3 | Strings | `.upper()`, `.lower()`, `.replace()`, slicing |
| 4 | Números | `+ - * / // % **`, int vs float |
| 5 | Booleanos y condicionales | `if/elif/else`, comparación |
| 6 | Funciones y scope | `def`, parámetros, `return`, global/local |

### Módulo 02 — Entorno y Configuración
| Lección | Tema | Concepto |
|---------|------|----------|
| 7 | Instalación | `python --version`, ejecutar scripts |

### Módulo 03 — Bucles y Secuencias
| Lección | Tema | Concepto |
|---------|------|----------|
| 8 | Listas y bucles | `for`, `while`, métodos de lista |
| 9 | Tuplas y slicing | `()`, `[inicio:fin:paso]`, desempaquetado |
| 10 | while y break/continue | Control de flujo |

### Módulo 04 — Diccionarios y Conjuntos
| Lección | Tema | Concepto |
|---------|------|----------|
| 11 | Diccionarios | `{key: value}`, iterar, nested dicts |
| 12 | Comprensión de listas | `[x for x in ... if ...]` |
| 13 | collections | `Counter`, `defaultdict` |
| 14 | JSON | `json.dumps()`, `json.loads()` |

### Módulo 05 — Manejo de Errores
| Lección | Tema | Concepto |
|---------|------|----------|
| 15 | try/except | Capturar excepciones, `finally` |

### Módulo 06 — Clases y Objetos
| Lección | Tema | Concepto |
|---------|------|----------|
| 16 | Clase Pokemon | `class`, `__init__`, `self`, `__str__` |
| 17 | Métodos especiales | `__add__`, `__eq__`, `__lt__`, `__repr__` |
| 18 | Propiedades | `@property`, `@setter` |
| 19 | Decoradores | `@classmethod`, `@staticmethod` |

### Módulo 07 — Herencia y Polimorfismo
| Lección | Tema | Concepto |
|---------|------|----------|
| 20 | Herencia | `class Hijo(Padre)`, `super()` |
| 21 | Polimorfismo | duck typing, interfaz común |

### Módulo 08 — Big O y Estructuras
| Lección | Tema | Concepto |
|---------|------|----------|
| 22 | Big O Notation | Complejidad temporal O(1), O(n), O(n²) |

### Módulo 09 — Recursión
| Lección | Tema | Concepto |
|---------|------|----------|
| 23 | Recursión | Caso base, paso recursivo |

### Módulo 10 — Algoritmos
| Lección | Tema | Concepto |
|---------|------|----------|
| 24 | Merge Sort | Divide y vencerás, O(n log n) |

### Módulo 11 — Grafos y Árboles
| Lección | Tema | Concepto |
|---------|------|----------|
| 25 | Grafos de Tipos | Nodos, aristas dirigidas, búsqueda |

### Módulo 12 — Programación Dinámica
| Lección | Tema | Concepto |
|---------|------|----------|
| 26 | Memoización | `lru_cache`, caching manual |
| 27 | Knapsack Problem | DP bottom-up, mochila 0/1 |
| 28 | Longest Common Subsequence | Comparar secuencias, LCS |

### Proyecto Final — Batalla Pokémon
| Lección | Tema | Concepto |
|---------|------|----------|
| 29 | Juego de batallas CLI | Integración total |

## 🎮 Interactividad

Cada lección incluye:

- **📖 Teoría** — Explicaciones con ejemplos Pokémon
- **💻 Ejercicio** — Editor de código Python integrado (Pyodide), consola y la tabla de tests
- **🧪 Tests** — Verificación automática dentro de la pestaña Ejercicio: cada reto muestra
  ✓ verde o ✗ roja y qué fragmento falta en tu código
- **✨ Solución** — Respuesta completa disponible al completar

El diagnóstico de errores muestra la línea y la columna del fallo, resalta esa línea en el
editor y deja el traceback completo plegado en la consola. Un error de Python ya no deja los
tests en «?»: la tabla se evalúa igual y la consola sigue respondiendo en la corrida siguiente.

### Atajos de teclado
- `Ctrl + Enter` — Ejecutar código
- `Ctrl + ←` — Lección anterior
- `Ctrl + →` — Lección siguiente
- `Tab` — Indentar en el editor

## 🛠 Tecnologías

- **HTML/CSS vanilla** — Sin frameworks ni build tools
- **JavaScript ES Modules** — SPA con routing por hash
- **Pyodide** — Python 3.11 compilado a WebAssembly, corre en-browser
- **localStorage** — Progreso y preferencia de tema persistidos entre sesiones
- **lessons.json** — Datos del curso como recurso estático
- **Tema claro / oscuro** — Conmutables desde el header; sin elección guardada respeta la preferencia del sistema

## 📚 Referencia

Basado en el [Curso de Python de freeCodeCamp](https://www.freecodecamp.org/learn/scientific-computing-with-python/).

El enfoque original usaba archivos `.py` auto-verificables ejecutados desde terminal. Esta versión web permite practicar directamente en el navegador sin instalar nada.

## 🔜 Próximos pasos

1. Agregar un editor de código con autocompletado para los ejercicios
2. Agregar más ejercicios por lección
3. Implementar validación avanzada (no solo string matching)
4. Sistema de puntos y logros
5. Más proyectos integradores por módulo
