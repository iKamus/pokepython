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

> **Runtime versionado.** Python en el navegador (Pyodide 0.24.1) y el editor
> (CodeMirror 6) están vendorizados en el repo: la app **no depende de ningún CDN** y
> funciona offline desde el primer clone, sin bajar nada. `vendor/pyodide/` son 5
> archivos (19 MB) que se versionan junto con el resto del sitio, porque GitHub Pages
> solo sirve lo comiteado. `python vendor/fetch_pyodide.py` sigue existiendo como
> herramienta de reparación: es el único paso que necesita internet y solo hay que
> ejecutarlo si alguien borra el runtime.

### Tests

```bash
python -m venv .venv && .venv/Scripts/pip install -r requirements-dev.txt   # una vez
.venv/Scripts/python -m pytest                     # datos + soluciones, sin navegador (~5 s)
.venv/Scripts/python -m pytest -m browser          # landing, tema, editor y Pyodide (~25 s)
.venv/Scripts/python -m pytest -m "browser and slow"   # solo el barrido de 29 lecciones
```

`pytest.ini` ya trae `addopts = -m "not browser"`, así que `pytest` a secas es la suite
rápida y `-m browser` la de navegador (el `-m` de la línea de comandos pisa al de
`addopts`). La suite de navegador usa `--browser-channel=msedge`, así que necesita
Microsoft Edge instalado (viene con Windows; en Linux/macOS hay que tenerlo y, si no está,
cambiá el canal o instalá los navegadores de Playwright con `playwright install`). En
Linux/macOS la ruta del intérprete es `.venv/bin/python` en lugar de `.venv/Scripts/python`.

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

## 🌐 Publicación

El sitio se publica como **estático en GitHub Pages** desde un repo público, sirviendo la
raíz de la rama publicada tal cual: no hay build, ni paso de compilación, ni archivos que
se generen al desplegar.

Pages lo monta bajo un subpath (`https://<owner>.github.io/<repo>/`) y **no hay ningún base
path que configurar**: la app usa rutas relativas (`./vendor/...`, `./lessons.json`) y hash
routing (`#/lesson/N`), así que funciona igual en `/` que en `/<repo>/`. Todo lo que la app
pide en tiempo de ejecución está versionado en el repo (Pyodide incluido), así que ▶ Correr
funciona desde el primer clone y en el sitio publicado.

El límite duro de GitHub es de **100 MB por archivo**, y recomienda mantener el repo por
debajo de 1 GB. El archivo más pesado del proyecto es `vendor/pyodide/pyodide.asm.wasm` con
8,6 MB, así que **no se usa Git LFS** ni hace falta.

## 📚 Referencia

Basado en el [currículo de Python de freeCodeCamp](https://www.freecodecamp.org/learn/python-v9/).

El enfoque original usaba archivos `.py` auto-verificables ejecutados desde terminal. Esta versión web permite practicar directamente en el navegador sin instalar nada.

## 🔜 Próximos pasos

1. Sistema de puntos y logros
2. Más proyectos integradores por módulo

## ⚖️ Licencia y atribución

El curso sigue la secuencia y los temas del [currículo de Python de
freeCodeCamp](https://www.freecodecamp.org/learn/python-v9/). El **texto derivado de ese
currículo** —teoría, ejemplos y consignas de `lessons/`, `solutions/` y `lessons.json`— se
distribuye bajo [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es):
se puede compartir y adaptar con atribución, sin uso comercial y bajo la misma licencia.

El **código de la aplicación** —`app.js`, `styles.css`, `index.html`, `serve.py`, `tests/` y
`vendor/`— queda bajo **MIT**, ver [`LICENSE`](LICENSE). Esa licencia no cubre el contenido
del currículo, que sigue bajo CC BY-NC-SA 4.0.
