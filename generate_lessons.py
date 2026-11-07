#!/usr/bin/env python3
"""OBSOLETO — no ejecutar. lessons.json es la fuente de verdad.

Este generador quedó atrás de las correcciones hechas a mano sobre lessons.json.
Correrlo lo sobrescribe y provoca pérdida de datos, verificado: borra el campo
`solutionFile` de las 29 lecciones (el panel ✨ Solución queda vacío), revierte el
expect corregido de la lección 3 (10 → 11), reapunta `codeFile` a archivos que no
existen (./lessons/02_instalacion.py) y duplica el escape de los saltos de línea en
`exercisePrompt`. Si hace falta regenerar, primero portar esos cambios acá.

Genera lessons.json con escape correcto de saltos de línea.
"""
import json
from pathlib import Path

def esc(text):
    """Escapa saltos de línea para JSON."""
    return text.replace('\n', '\\n') if text else ''

lessons = [
    # ── MODULO 01 ──
    {
        "id": 1, "module": "01", "level": "beginner", "type": None,
        "title": "1. ¿Qué es Python?",
        "shortTitle": "¿Qué es Python?",
        "objective": "Entender qué es Python y para qué se usa. Escribir tu primer script.",
        "keyConcept": "Python es un lenguaje de programación interpretado, usado en ciencia de datos, web, automatización y más.",
        "theory": "### El mundo Pokémon necesita código\n\nCada vez que un Pokémon cambia, evoluciona o aprende un movimiento nuevo, detrás hay **código ejecutándose**.\n\nPython es un **lenguaje de propósito general** — significa que podés usarlo para:\n\n- **Ciencia de datos**: analizar estadísticas de combate\n- **Desarrollo web**: crear sitios como este\n- **Automatización**: scripts que hacen tareas repetidas\n- **Juegos**: programar batallas por consola 🎮\n\n```python\n# En Python todo empieza con print()\nprint(\"¡Hola, Entrenador!\")\n```\n\nEl comando `print()` muestra texto en pantalla. Es tu herramienta principal para ver qué está pasando en tu código.",
        "example": "print(\"Python es un lenguaje de propósito general\")\nprint(\"Se usa en ciencia de datos\")\nprint(\"También en desarrollo web\")\nprint(\"Y en automatización de tareas\")",
        "exercisePrompt": "Completá cada TODO. Imprimí exactamente los textos indicados usando `print()`.\\n\\n**Tips:** No uses comillas extra — `print(texto)` imprime solo el contenido del texto, sin comillas.",
        "codeFile": "./lessons/01.py",
        "tests": [
            {"id": "t1", "name": "Reto 1", "description": "Primera línea impresa", "expect": "Python es un lenguaje de propósito general"},
            {"id": "t2", "name": "Reto 2", "description": "Segunda línea impresa", "expect": "Se usa en ciencia de datos"},
            {"id": "t3", "name": "Reto 3", "description": "Tercera línea impresa", "expect": "También en desarrollo web"},
            {"id": "t4", "name": "Reto 4", "description": "Cuarta línea impresa", "expect": "Y en automatización de tareas"}
        ]
    },
    {
        "id": 2, "module": "01", "level": "beginner", "type": "normal",
        "title": "2. Variables y tipos de datos",
        "shortTitle": "Variables y tipos",
        "objective": "Declarar variables con nombres correctos y asignar valores de distintos tipos.",
        "keyConcept": "Las variables son cajas con nombre donde guardás datos. Python infiere el tipo automáticamente.",
        "theory": "### Guardando info de tu Pokémon\n\nImaginá que estás creando una ficha de registro para tu Pokémon. Necesitás guardar:\n\n- Su **nombre** → eso es un texto (`str`)\n- Su **nivel** → eso es un número entero (`int`)\n- Si está en batalla → eso es verdadero/falso (`bool`)\n\n```python\nnombre = \"Pikachu\"       # str → cadena de texto\nnivel = 25               # int → número entero\nen_batalla = True        # bool → booleano\n```\n\n#### Reglas para nombrar variables\n\n- Usá `snake_case` (palabras_separadas_con_guiones_bajos)\n- Empezá con letra o `_`, no con números\n- Nada de caracteres especiales\n- Las CONSTANTES van en MAYÚSCULAS",
        "example": "# Ficha de un Pokémon\nnombre = \"Charizard\"\nnivel = 36\nes_legendario = False\ntipo_principal = \"fuego\"\n\nprint(f\"{nombre} es nivel {nivel}\")\nprint(f\"Tipo: {tipo_principal}\")",
        "exercisePrompt": "Creá las variables que se indican en cada reto. Asigná valores realistas para un entrenador joven.",
        "codeFile": "./lessons/02.py",
        "tests": [
            {"id": "t1", "name": "Variables declaradas", "description": "Nombre, edad y activo existen", "expect": "None"},
            {"id": "t2", "name": "Constante MAX_NIVEL", "description": "Debe ser 100 en mayúsculas", "expect": "100"},
            {"id": "t3", "name": "Cantidad de equipo", "description": "Normalmente 6 Pokémons", "expect": "6"},
            {"id": "t4", "name": "F-string mensaje", "description": "Contiene anios", "expect": "anios"}
        ]
    },
    {
        "id": 3, "module": "01", "level": "beginner", "type": "water",
        "title": "3. Strings — Manipulando texto",
        "shortTitle": "Strings",
        "objective": "Usar métodos de strings para transformar texto de nombres de movimientos y Pokémons.",
        "keyConcept": "Los strings tienen muchos métodos útiles: `.upper()`, `.lower()`, `.replace()`, `.split()`, `.strip()`.",
        "theory": "### Movimientos en mayúsculas\n\nCuando escribís en la Pokédex, a veces querés formatear el texto. Los **strings** (textos) tienen **métodos** que los transforman:\n\n| Método | Qué hace |\n|--------|----------|\n| `.upper()` | TODO A MAYÚSCULAS |\n| `.lower()` | todo a minúsculas |\n| `.capitalize()` / `.title()` | Primera letra mayúscula |\n| `.replace('a','b')` | Reemplaza texto |\n| `.strip()` | Quita espacios sobrantes |\n| `.split(',')` | Divide en lista |\n\n```python\nmovimiento = \"huracán eléctrico\"\nprint(movimiento.upper())       # HURACÁN ELÉCTRICO\nprint(movimiento.replace(\"é\",\"e\"))\n```\n\n#### f-strings — formato poderoso\n\nLa `f` antes de las comillas te permite insertar variables directamente:\n\n```python\npokemon = \"Gengar\"\nnivel = 50\nprint(f\"{pokemon} (Nv.{nivel})\")  # Gengar (Nv.50)\n```",
        "example": "nombre = \"sQUIRTle\"\nmovimiento = \"hidrobomba\".upper()\nprint(nombre.title())     # Squirtle\nprint(movimiento)         # HIDROBOMBA\nprint(len(movimiento))    # 11",
        "exercisePrompt": "Transformá nombres de Pokémons y movimientos usando los métodos de string.",
        "codeFile": "./lessons/03.py",
        "tests": [
            {"id": "t1", "name": ".upper()", "description": "Resultado: PIKACHU", "expect": "PIKACHU"},
            {"id": "t2", "name": ".lower()", "description": "Resultado: pikachu", "expect": "pikachu"},
            {"id": "t3", "name": ".title()", "description": "Resultado: Pikachu", "expect": "Pikachu"},
            {"id": "t4", "name": "len()", "description": "Length of hidrobomba", "expect": "11"},
            {"id": "t5", "name": ".replace()", "description": "Reemplazo _ by space", "expect": "pi kachu"},
            {"id": "t6", "name": "in operator", "description": "Contains chu", "expect": "chu"},
            {"id": "t7", "name": ".strip()", "description": "No spaces left", "expect": "Raichu"}
        ]
    },
    {
        "id": 4, "module": "01", "level": "beginner", "type": "electric",
        "title": "4. Números y operaciones matemáticas",
        "shortTitle": "Números",
        "objective": "Realizar operaciones matemáticas con HP, Attack, Defense y calcular daño.",
        "keyConcept": "Operadores aritméticos: +, -, *, /, //, %, **. Int vs float.",
        "theory": "### Calculando el ataque\n\nEn una batalla, necesitás calcular cuánto daño hace un movimiento.\n\n| Operador | Significado | Ejemplo |\n|----------|-------------|---------|\n| `+` | Suma | `80 + 20 = 100` |\n| `-` | Resta | `100 - 80 = 20` |\n| `*` | Multiplicación | `15 * 2 = 30` |\n| `/` | División decimal | `10 / 3 = 3.33...` |\n| `//` | División entera | `10 // 3 = 3` |\n| `%` | Módulo (resto) | `10 % 3 = 1` |\n| `**` | Potencia | `2 ** 10 = 1024` |\n\n```python\nhp_maximo = 100\nprob_critico = 0.0625\n```",
        "example": "ataque = 90\ndefensa = 55\nvelocidad = 110\nsp_attack = 85\nsp_defense = 75\nhp = 35\ntotal = ataque+defensa+velocidad+sp_attack+sp_defense+hp\nprint(f\"Total stats: {total}\")\npromedio = total / 6\nprint(f\"Promedio: {promedio:.1f}\")",
        "exercisePrompt": "Calculá estadísticas y ratios numéricos aplicándolos a escenarios de entrenamiento Pokémon.",
        "codeFile": "./lessons/04.py",
        "tests": [
            {"id": "t1", "name": "Suma HP", "description": "HP total", "expect": "100"},
            {"id": "t2", "name": "Resta daño", "description": "HP despues", "expect": "65"},
            {"id": "t3", "name": "Multiplicacion ATK", "description": "ATK efectivo", "expect": "105"},
            {"id": "t4", "name": "Division entera", "description": "Por entrenador", "expect": "8"},
            {"id": "t5", "name": "Modulo", "description": "Sobran pokemons", "expect": "1"},
            {"id": "t6", "name": "Potencia", "description": "3^4", "expect": "81"}
        ]
    },
    {
        "id": 5, "module": "01", "level": "beginner", "type": "fire",
        "title": "5. Booleanos y condicionales",
        "shortTitle": "Condicionales",
        "objective": "Tomar decisiones en código con if/elif/else comparando tipos y estados.",
        "keyConcept": "Booleanos son True/False. Condicionales permiten ejecutar código distinto según el estado.",
        "theory": "### Advantage tipo: cuándo atacar\n\nEn Pokémon, **los tipos** definen quién gana a quién. Tu código debe decidir si un movimiento es súper efectivo.\n\n```python\ntipo_movimiento = \"eléctrico\"\ntipo_enemigo = \"agua\"\n\nif tipo_movimiento == \"eléctrico\" and tipo_enemigo == \"agua\":\n    print(\"¡Súper efectivo! x2\")\nelif tipo_movimiento == tipo_enemigo:\n    print(\"Neutral. x1\")\nelse:\n    print(\"No muy efectivo. x0.5\")\n```\n\n#### Operadores de comparación\n\n| Operador | Significado | Ejemplo |\n|----------|-------------|---------|\n| `==` | Igual | `hp == 0` |\n| `!=` | Diferente | `tipo != \"normal\"` |\n| `>` | Mayor que | `vel > 100` |\n| `<` | Menor que | `vel < 50` |\n| `>=` | Mayor o igual | `nivel >= 50` |\n| `<=` | Menor o igual | `nivel <= 10` |",
        "example": "hp = 15\ntipo_mov = \"fuego\"\ntipo_def = \"planta\"\ndefinitivo = hp > 0\nprint(f\"¿En pie? {definitivo}\")  # True\nsuper_efectivo = {\n    \"fuego\": [\"planta\", \"hielo\", \"acero\"],\n    \"agua\": [\"fuego\", \"roca\"]\n}\nsi_efect = any(t in super_efectivo.get(tipo_mov, []) for t in [tipo_def])\nprint(f\"Efectivo: {si_efect}\")",
        "exercisePrompt": "Programá decisiones para diferentes situaciones de batalla y entrenamiento.",
        "codeFile": "./lessons/05.py",
        "tests": [
            {"id": "t1", "name": "Derrotado", "description": "hp <= 0", "expect": "True"},
            {"id": "t2", "name": "Es fuerte", "description": "nivel >= 55", "expect": "True"},
            {"id": "t3", "name": "Tipo advantage", "description": "Agua vs fuego", "expect": "Súper efectivo"},
            {"id": "t4", "name": "Can attack", "description": "and condition", "expect": "True"},
            {"id": "t5", "name": "Super check", "description": "electric vs water", "expect": "True"}
        ]
    },
    {
        "id": 6, "module": "01", "level": "beginner", "type": "psychic",
        "title": "6. Funciones y scope",
        "shortTitle": "Funciones",
        "objective": "Crear funciones reutilizables para calcular daño, saludar y gestionar estados.",
        "keyConcept": "Las funciones encapsulan lógica. Def con parámetros, return devuelve resultado. Scope local vs global.",
        "theory": "### Funciones: tus movimientos especiales\n\nCada función es como un movimiento especial: recibe información (parámetros), ejecuta una acción, y devuelve un resultado.\n\n```python\ndef calcular_dano(ataque, defensa):\n    dano = ataque - defensa // 2\n    return dano\n\nd = calcular_dano(100, 40)\nprint(d)  # 80\n```\n\n#### Parámetros con valor por defecto\n\n```python\ndef curar(pokemon, cantidad=20):\n    pokemon['hp'] += cantidad\n    return pokemon['hp']\n\ncurar(charmander)       # cura 20 (default)\ncurar(charmander, 50)   # cura 50\n```\n\n#### Scope: lo local vs lo global\n\n```python\nhp_global = 100\n\ndef perder_hp(cantidad):\n    global hp_global\n    hp_global -= cantidad\n\ndef restar_local(valor):\n    hp_local = valor\n    return hp_local\n```",
        "example": "def tipo_efectivo(tipo_mov, tipo_def):\n    eficaces = {\n        \"fuego\": [\"planta\", \"hielo\", \"acero\"],\n        \"agua\": [\"fuego\", \"roca\"]\n    }\n    if tipo_def in eficaces.get(tipo_mov, []):\n        return \"x2\"\n    return \"x1\"\n\nbulbasaur = {\"hp\": 30, \"hp_max\": 100}\ndef curar_equipo(pokemon, cantidad=25):\n    pokemon[\"hp\"] = min(pokemon[\"hp\"] + cantidad, pokemon[\"hp_max\"])\n    return pokemon[\"hp\"]\nprint(curar_equipo(bulbasaur))  # 55",
        "exercisePrompt": "Definí funciones que resuelvan problemas comunes de batalla: calcular daño, aplicar curaciones, verificar condiciones.",
        "codeFile": "./lessons/06.py",
        "tests": [
            {"id": "t1", "name": "doble(21)", "description": "Retorna 42", "expect": "42"},
            {"id": "t2", "name": "area_rectangulo", "description": "with default param", "expect": "4"},
            {"id": "t3", "name": "nombre_completo", "description": "Optional surname", "expect": "Lovelace"},
            {"id": "t4", "name": "sumar", "description": "Returns sum", "expect": "15"},
            {"id": "t5", "name": "saludar prints", "description": "Side effect only", "expect": "Hola"},
            {"id": "t6", "name": "Global counter", "description": "Increments", "expect": "2"},
            {"id": "t7", "name": "Local var", "description": "Does not affect global", "expect": "10"}
        ]
    }
]

# --- MODULO 02: Instalacion ---
lessons.extend([
    {
        "id": 7, "module": "02", "level": "beginner", "type": "steel",
        "title": "1. Instalación y ejecución",
        "shortTitle": "Instalación",
        "objective": "Verificar que Python está instalado y ejecutar scripts desde terminal.",
        "keyConcept": "Python se instala desde python.org. Archivos .py se ejecutan con python archivo.py.",
        "theory": "### Preparando tu laboratorio\n\nAntes de poder crear Pokémons digitales, necesitás **Python instalado**.\n\n```bash\n# Verificar instalación\npython --version\n\n# Ejecutar un script\n$ python hola.py\nHola Mundo\n```\n\nSi ya tenés Python instalado (verificaste con `python --version`), ¡podés empezar!",
        "example": "# Script simple de verificación\nimport sys\nprint(f\"Python {sys.version}\")\nprint(f\"Ruta: {sys.executable}\")\nprint(\"Listo para entrenar!\")",
        "exercisePrompt": "Verificá tu entorno y completá los ejercicios de entrada.",
        "codeFile": "./lessons/02_instalacion.py",
        "tests": [
            {"id": "t1", "name": "Script ejecutado", "description": "Primer print", "expect": "Script ejecutado"},
            {"id": "t2", "name": "doble(5)", "description": "Debe retornar 10", "expect": "10"},
            {"id": "t3", "name": "doble(21)", "description": "Debe imprimir 42", "expect": "42"},
            {"id": "t4", "name": "10 // 3", "description": "División entera", "expect": "3"},
            {"id": "t5", "name": "2 ** 8", "description": "Potencia", "expect": "256"},
            {"id": "t6", "name": "py + thon", "description": "Concatenación", "expect": "python"}
        ]
    }
])

# --- MODULO 03: Bucles ---
lessons.extend([
    {
        "id": 8, "module": "03", "level": "beginner", "type": "grass",
        "title": "1. Listas y bucles",
        "shortTitle": "Listas y bucles",
        "objective": "Trabajar con listas de Pokémons y recorrerlas con for e while.",
        "keyConcept": "Listas con []. Bucle for recorre elementos. Métodos: append, pop, remove, sort, len, insert.",
        "theory": "### Tu equipo de 6 Pokémons\n\nUna **lista** es una colección ordenada de cosas.\n\n```python\nequipo = [\"Pikachu\", \"Charmander\", \"Squirtle\", \"Bulbasaur\", \"Jigglypuff\", \"Meowth\"]\n\nfor pokemon in equipo:\n    print(f\"🔹 {pokemon}\")\n```\n\n#### Métodos de lista\n\n| Método | Qué hace |\n|--------|----------|\n| `.append(x)` | Agrega al final |\n| `.insert(i, x)` | Inserta en posición |\n| `.remove(x)` | Elimina por valor |\n| `.pop()` | Saca el último |\n| `len(lista)` | Cantidad de elementos |\n| `.sort()` | Ordena la lista |\n| `.reverse()` | Invierte el orden |\n\n#### Enumerate — índice + valor\n\n```python\nfor i, poke in enumerate(equipo):\n    print(f\"#{i+1}: {poke}\")\n```",
        "example": "equipos_ronda = [\n    [\"Pikachu\", \"Charizard\", \"Blastoise\", \"Venusaur\", \"Snapdragon\", \"Eevee\"],\n    [\"Gengar\", \"Alakazam\", \"Golem\", \"Arcanine\", \"Pidgeot\", \"Rapidash\"]\n]\ndef contador_equipos():\n    total = 0\n    for equipo in equipos_ronda:\n        total += len(equipo)\n        print(f\"Equipo con {len(equipo)} pokémons\")\n    print(f\"Total: {total} pokémons\")\ncontador_equipos()",
        "exercisePrompt": "Trabajá con listas de Pokémons: crear, añadir, eliminar, iterar, slicing.",
        "codeFile": "./lessons/07_listas.py",
        "tests": [
            {"id": "t1", "name": "Lista inicial", "description": "6 starters", "expect": "starters"},
            {"id": "t2", "name": "Append", "description": "7 despues de agregar", "expect": ".append("},
            {"id": "t3", "name": "Pop", "description": "Regresa a 6", "expect": ".pop()"},
            {"id": "t4", "name": "Insert", "description": "Insertó al inicio", "expect": ".insert(0"}
        ]
    },
    {
        "id": 9, "module": "03", "level": "beginner", "type": "ground",
        "title": "2. Tuplas y slicing",
        "shortTitle": "Tuplas",
        "objective": "Usar tuplas para datos inmutables y slicing para extraer partes de secuencias.",
        "keyConcept": "Tuplas usan () y son inmutables. Slicing: [inicio:fin:paso]. Desempaquetado.",
        "theory": "### Stats inmutables y cortes de equipo\n\nLas **tuplas** son como listas pero **no se pueden modificar**. Ideales para datos fijos.\n\n```python\nstats = (35, 55, 40, 50, 65, 90)  # HP, Atk, Def, SpA, SpD, Spe\n# stats[0] = 100  # ❌ Error! Las tuplas no se modifican\n```\n\n#### Slicing — sacar porciones\n\n```python\nnumeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]\nnumeros[2:5]    # [2, 3, 4]\nnumeros[:3]     # [0, 1, 2]\nnumeros[-3:]    # últimos 3\nnumeros[::-1]   # invertido\n```\n\n#### Desempaquetado\n\n```python\nprimeros_3 = (\"Charizard\", \"Blastoise\", \"Venusaur\")\na, b, c = primeros_3\n```",
        "example": "stats = (35, 55, 40, 50, 65, 90)\nprint(f\"HP={stats[0]}, Speed={stats[-1]}\")\nprimeros_3 = stats[:3]\ninvertidos = stats[::-1]\na, b, c, d, e, f = stats",
        "exercisePrompt": "Trabajá con tuplas, slicing y desempaquetado.",
        "codeFile": "./lessons/08_tuplas.py",
        "tests": [
            {"id": "t1", "name": "Tuple creada", "description": "Stats base Pikachu", "expect": "(35,"},
            {"id": "t2", "name": "Index access", "description": "HP and speed", "expect": "stats["},
            {"id": "t3", "name": "Slice first 3", "description": "First slice", "expect": "[::3]"},
            {"id": "t4", "name": "Negative index", "description": "Speed with -1", "expect": "[-1]"},
            {"id": "t5", "name": "Reverse tuple", "description": "Full reversal", "expect": "[::-1]"},
            {"id": "t6", "name": "Unpack", "description": "Unpacked into vars", "expect": "= stats"},
            {"id": "t7", "name": "Slice step", "description": "Every second item", "expect": "[::2]"}
        ]
    },
    {
        "id": 10, "module": "03", "level": "beginner", "type": "ghost",
        "title": "3. Bucles while y break/continue",
        "shortTitle": "While",
        "objective": "Controlar flujos con while, break y continue para simulaciones de batalla.",
        "keyConcept": "while repite mientras condición sea True. break sale del bucle. continue salta a la siguiente iteración.",
        "theory": "### Simulación de batalla turn a turn\n\nUn `while` sirve para repetir algo hasta que pase algo específico.\n\n```python\nhp_pikachu = 50\nhp_charmander = 45\nturno = 0\nwhile hp_pikachu > 0 and hp_charmander > 0:\n    turno += 1\n    hp_charmander -= 10\n    hp_pikachu -= 8\n    print(f\"Turno {turno}: Pikachu {hp_pikachu}HP\")\nif hp_pikachu > 0:\n    print(\"¡Pikachu ganó!\")\nelse:\n    print(\"Charmander ganó...\")\n```",
        "example": "hp_pikachu = 50\nhp_charmander = 45\nturno = 0\nwhile hp_pikachu > 0 and hp_charmander > 0:\n    turno += 1\n    hp_charmander -= 10\n    hp_pikachu -= 8\n    print(f\"Turno {turno}: Pikachu {hp_pikachu}HP\")\nprint(f\"Ganador: {hp_pikachu} vs {hp_charmander}\" if hp_pikachu > 0 else \"Charmander\")",
        "exercisePrompt": "Programá simulaciones de batalla y loops controlados con while/break/continue.",
        "codeFile": "./lessons/09_while.py",
        "tests": [
            {"id": "t1", "name": "Count to 5", "description": "While loop runs 5 times", "expect": "while"},
            {"id": "t2", "name": "Victory HP reaches 0", "description": "Enemy HP decreases", "expect": "hp_enemigo"},
            {"id": "t3", "name": "Break works", "description": "Exits when hp <= 0", "expect": "break"},
            {"id": "t4", "name": "Continue skips", "description": "Skips fainted pokemon", "expect": "continue"}
        ]
    }
])

# --- MODULO 04: Diccionarios ---
lessons.extend([
    {
        "id": 11, "module": "04", "level": "intermediate", "type": "bug",
        "title": "1. Diccionarios — La Pokédex",
        "shortTitle": "Diccionarios",
        "objective": "Crear y manipular diccionarios para representar fichas de Pokémons.",
        "keyConcept": "Diccionarios {clave: valor}. Acceder con clave, iterar keys/values/items.",
        "theory": "### Construyendo la Pokédex\n\nUn **diccionario** mapea claves a valores. Cada Pokémon es un diccionario:\n\n```python\npikachu = {\n    \"nombre\": \"Pikachu\",\n    \"tipo\": \"electrico\",\n    \"nivel\": 25,\n    \"habilidades\": [\"fuerzasonica\", \"voltetick\"]\n}\nprint(pikachu[\"nombre\"])  # Pikachu\n```\n\n#### Métodos de diccionario\n\n| Método | Qué hace |\n|--------|----------|\n| `.keys()` | Todas las claves |\n| `.values()` | Todos los valores |\n| `.items()` | Pares clave-valor |\n| `.get(key, default)` | Obtener con fallback |\n| `.update(dict2)` | Fusionar diccionarios |",
        "example": "pokdex = {\n    25: {\"nombre\": \"Pikachu\", \"tipo\": \"electrico\"},\n    6: {\"nombre\": \"Charizard\", \"tipo\": \"fuego\"},\n    9: {\"nombre\": \"Blastoise\", \"tipo\": \"agua\"}\n}\nprint(pokdex[25][\"nombre\"])  # Pikachu\nprint(list(pokdex.keys()))     # [25, 6, 9]",
        "exercisePrompt": "Construí tu Pokédex personal con diccionarios.",
        "codeFile": "./lessons/10_diccionarios.py",
        "tests": [
            {"id": "t1", "name": "Dictionary created", "description": "Charizard with data", "expect": "{\\\"nombre\\\""},
            {"id": "t2", "name": "Modify type", "description": "Type changed", "expect": "[\\\"tipo\\\"]"},
            {"id": "t3", "name": "Add abilities", "description": "New key added", "expect": "[\\\"habilidades\\\"]"},
            {"id": "t4", "name": "Iterate items", "description": "Print each pair", "expect": "items()"},
            {"id": "t5", "name": "Get with default", "description": "Returns fallback", "expect": ".get("},
            {"id": "t6", "name": "Set of types", "description": "Eliminates duplicates", "expect": "set("}
        ]
    },
    {
        "id": 12, "module": "04", "level": "intermediate", "type": "poison",
        "title": "2. Comprensión de listas y diccionarios",
        "shortTitle": "Comprensión",
        "objective": "Escribir comprensiones concisas para transformar listas de Pokémons.",
        "keyConcept": "List comprehension: [expresion for item in iterable if condicion]. Dict comp: {k:v for ...}",
        "theory": "### Transformar tu equipo en una línea\n\nLas **list comprehensions** crean listas nuevas elegantemente:\n\n```python\npokemons = [\"Pikachu\", \"Charmander\", \"Squirtle\", \"Bulbasaur\"]\nnombres_largos = [p.lower() for p in pokemons if len(p) > 8]\n# ['charmander', 'bulbasaur']\n```\n\n#### Dict comprehension\n\n```python\nstats = {\"hp\": 35, \"attack\": 55, \"defense\": 40}\npokdex_num = {i: name for i, name in enumerate([...], start=1)}\n```",
        "example": "pokemons = [\"pikachu\", \"charizard\", \"blastiose\"]\nnombres_mayu = [p.upper() for p in pokemons]\nlongos = [p for p in pokemons if len(p) > 8]\nniveles = [25, 36, 42]\npor_nombre = {nom: niv for nom, niv in zip(nombres, niveles)}",
        "exercisePrompt": "Transformá colecciones con list y dict comprehensions.",
        "codeFile": "./lessons/11_comprension.py",
        "tests": [
            {"id": "t1", "name": "Upper case list", "description": "All names upper", "expect": ".upper()"},
            {"id": "t2", "name": "Filter long", "description": "Names longer than 8", "expect": "len(p)"},
            {"id": "t3", "name": "Dict comprehension", "description": "Name -> level map", "expect": "{:"},
            {"id": "t4", "name": "Conditional comprehension", "description": "Divisible by 5", "expect": "% 5 == 0"},
            {"id": "t5", "name": "Nested comprehension", "description": "Two nested loops", "expect": "for" },
            {"id": "t6", "name": "Extract stats", "description": "Nested dict extraction", "expect": "[\\\"stats\\\"][\\\"attack\\\"]"}
        ]
    },
    {
        "id": 13, "module": "04", "level": "intermediate", "type": "rock",
        "title": "3. collections — defaultdict y Counter",
        "shortTitle": "Collections",
        "objective": "Usar Counter y defaultdict para análisis de datos Pokémon.",
        "keyConcept": "Counter cuenta ocurrencias. defaultdict provee valores por defecto automáticos.",
        "theory": "### Analizando tu equipo\n\n```python\nfrom collections import Counter, defaultdict\n\n# Counter: cuenta frecuencias\nmovimientos = [\"impactrueno\", \"rayo\", \"impactrueno\", \"voltiocambio\", \"rayo\", \"impactrueno\"]\ncuenta = Counter(movimientos)\nprint(cuenta.most_common(2))  # [('impactrueno', 3), ('rayo', 2)]\n\n# defaultdict: valores iniciales automáticos\ntipos_por_numero = defaultdict(list)\ntipos_por_numero[25].append(\"Pikachu\")\n# Sin KeyError!\n```",
        "example": "from collections import Counter, defaultdict\ntipos = [\"electrico\", \"fuego\", \"agua\", \"electrico\", \"planta\", \"fuego\"]\ncuenta_tipos = Counter(tipos)\nprint(cuenta_tipos.most_common(2))\ngroup = defaultdict(list)\nfor name, t in [(\"pika\",\"electrico\"),(\"raichu\",\"electrico\"),(\"charz\",\"fuego\")]:\n    group[t].append(name)\nfor tipo, pok in group.items():\n    print(f\"{tipo}: {pok}\")",
        "exercisePrompt": "Analizá distribuciones y agrupaciones con collections.",
        "codeFile": "./lessons/12_collections.py",
        "tests": [
            {"id": "t1", "name": "Counter creates", "description": "Counts frequencies", "expect": "Counter("},
            {"id": "t2", "name": "most_common", "description": "Returns sorted", "expect": "most_common()"},
            {"id": "t3", "name": "defaultdict groups", "description": "Aggregates without KeyError", "expect": "defaultdict("},
            {"id": "t4", "name": "Sum with defaultdict", "description": "Accumulates correctly", "expect": "+="}
        ]
    },
    {
        "id": 14, "module": "04", "level": "intermediate", "type": "dark",
        "title": "4. json — Guardar y cargar equipo",
        "shortTitle": "JSON",
        "objective": "Persistir datos de Pokémons con el módulo json.",
        "keyConcept": "json.dumps convierte dict a string. json.loads convierte string a dict.",
        "theory": "### Guardar tu progreso de entrenador\n\n```python\nimport json\nteamp_data = {\"nombre\": \"Red\", \"equipo\": [\"Pikachu\", \"Charizard\"], \"insignias\": 8}\ntexto = json.dumps(teamp_data, indent=2, ensure_ascii=False)\nprint(texto)\ndatos = json.loads(texto)\nprint(datos[\"nombre\"])  # Red\n```",
        "example": "import json\nentrenador = {\"nombre\": \"Red\", \"nivel\": 8, \"equipo\": [\"Pikachu\",\"Charizard\",\"Blastoise\",\"Venusaur\",\"Eevee\",\"Alakazam\"], \"pociones\": 10}\ntexto_json = json.dumps(entrenador, indent=2, ensure_ascii=False)\nprint(texto_json)\ndatos_leidos = json.loads(texto_json)\nprint(f\"Equipo: {len(datos_leidos['equipo'])} pokémons\")",
        "exercisePrompt": "Serializá y deserializá datos de entrenador con JSON.",
        "codeFile": "./lessons/13_json.py",
        "tests": [
            {"id": "t1", "name": "JSON serializes", "description": "Converts to string", "expect": "json.dumps("},
            {"id": "t2", "name": "Parsed back", "description": "Load returns dict", "expect": "json.loads("},
            {"id": "t3", "name": "Write to file", "description": "Dump to file", "expect": "json.dump("},
            {"id": "t4", "name": "Read from file", "description": "Load from file", "expect": "json.load("}
        ]
    }
])

# --- MODULO 05: Errores ---
lessons.extend([
    {
        "id": 15, "module": "05", "level": "intermediate", "type": "ice",
        "title": "1. try/except — Errores controlados",
        "shortTitle": "Try/Except",
        "objective": "Capturar excepciones para manejar errores sin crashing del programa.",
        "keyConcept": "try bloquea código riesgoso, except captura el error, finally siempre se ejecuta.",
        "theory": "### Prevención en batalla\n\nNo todo sale como esperás en batalla. Un `try/except` previene crashes:\n\n```python\npokemons_en_campo = [\"Pikachu\", \"Charizard\"]\nposicion = 2\ntry:\n    pokemon = pokemons_en_campo[posicion]\n    print(f\"Saca a {pokemon}\")\nexcept IndexError:\n    print(\"¡Índice fuera de rango!\")\nfinally:\n    print(\"Fin del intento de cambio.\")\n```",
        "example": "def cambiar_pokemon(equipo, posicion):\n    try:\n        pokemon = equipo[posicion]\n        return f\"Enviando a {pokemon}...\"\n    except IndexError:\n        return \"❌ Posición inválida. Solo hay posiciones del 0 al 5.\"\n    except TypeError:\n        return \"❌ Debes pasar un número entero.\"\n    finally:\n        print(\"Intento procesado.\")\nprint(cambiar_pokemon([\"Pika\", \"Char\", \"Blast\"], 0))\nprint(cambiar_pokemon([\"Pika\", \"Char\", \"Blast\"], 5))\nprint(cambiar_pokemon([\"Pika\", \"Char\", \"Blast\"], \"dos\"))",
        "exercisePrompt": "Prevení crashes manejando errores elegantes.",
        "codeFile": "./lessons/14_try_except.py",
        "tests": [
            {"id": "t1", "name": "ZeroDivision handled", "description": "No crash with b=0", "expect": "ZeroDivisionError"},
            {"id": "t2", "name": "KeyError handled", "description": "ID not found managed", "expect": "KeyError"},
            {"id": "t3", "name": "Parse robust", "description": "Handles wrong type and value", "expect": "except"},
            {"id": "t4", "name": "Finally executes", "description": "Cleanup always happens", "expect": "finally"}
        ]
    }
])

# --- MODULO 06: Clases ---
lessons.extend([
    {
        "id": 16, "module": "06", "level": "intermediate", "type": "fairy",
        "title": "1. Clases básicas — Clase Pokémon",
        "shortTitle": "Clase Pokémon",
        "objective": "Crear una clase Pokemon con atributos y métodos básicos.",
        "keyConcept": "class define un objeto. __init__ inicializa atributos. self refiere al objeto.",
        "theory": "### Definir tu propia especie\n\nUna **clase** es un molde para crear objetos. La clase Pokemon define qué tiene cada Pokémon:\n\n```python\nclass Pokemon:\n    def __init__(self, nombre, tipo, nivel=5):\n        self.nombre = nombre\n        self.tipo = tipo\n        self.nivel = nivel\n        self.hp_max = nivel * 10\n        self.hp = self.hp_max\n\n    def __str__(self):\n        return f\"{self.nombre} (Nv.{self.nivel}) - {self.hp}/{self.hp_max}HP\"\n\nmi_pokemon = Pokemon(\"Pikachu\", \"electrico\")\nprint(mi_pokemon)\n```",
        "example": "class Pokemon:\n    def __init__(self, nombre, tipo, nivel=5):\n        self.nombre = nombre\n        self.tipo = tipo\n        self.nivel = nivel\n        self.hp_max = nivel * 10\n        self.hp = self.hp_max\n        self.movimientos = [\"Placaje\"]\n    def __str__(self):\n        return f\"{self.nombre} Nv.{self.nivel} - {self.hp}/{self.hp_max}HP\"\n    def aprender(self, mov):\n        if mov not in self.movimientos:\n            self.movimientos.append(mov)\n            print(f\"{self.nombre} aprendió {mov}!\")\n    def recibir_dano(self, dano):\n        self.hp = max(0, self.hp - dano)\n    def curar(self, cantidad=20):\n        self.hp = min(self.hp + cantidad, self.hp_max)\n        print(f\"{self.nombre} recuperó {cantidad}HP. HP: {self.hp}\")\npika = Pokemon(\"Pikachu\", \"electrico\", 20)\npika.aprender(\"Thunderbolt\")\npika.recibir_dano(50)\npika.curar(25)\nprint(pika)",
        "exercisePrompt": "Definí una clase Pokemon completa con atributos, métodos de combate y utilidades.",
        "codeFile": "./lessons/15_clase.py",
        "tests": [
            {"id": "t1", "name": "Class defined", "description": "__init__ initializes properly", "expect": "class Pokemon"},
            {"id": "t2", "name": "Learn move", "description": "Move added to list", "expect": "append"},
            {"id": "t3", "name": "Take damage", "description": "HP reduces correctly", "expect": "max(0"},
            {"id": "t4", "name": "Healing", "description": "HP increases but does not exceed max", "expect": "min("}
        ]
    },
    {
        "id": 17, "module": "06", "level": "intermediate", "type": "normal",
        "title": "2. Métodos especiales",
        "shortTitle": "Dunder Methods",
        "objective": "Implementar métodos especiales para operación de objetos.",
        "keyConcept": "__add__, __mul__, __eq__, __len__, __gt__ permiten usar operadores nativos.",
        "theory": "### Hacer objetos que operen naturalmente\n\n```python\nclass Pokeball:\n    def __init__(self, tipo=\"standard\"):\n        self.tipo = tipo\n        self.capacidad = 1\n    def __add__(self, otro):\n        nueva = Pokeball(self.tipo)\n        nueva.capacidad = self.capacidad + otro.capacidad\n        return nueva\n    def __eq__(self, otro):\n        return self.tipo == otro.tipo\n    def __repr__(self):\n        return f\"Pokeball({self.tipo})\"\n\nb1 = Pokeball(\"master\")\nb2 = Pokeball(\"master\")\nprint(b1 == b2)  # True\nprint(repr(b1))  # Pokeball(master)",
        "example": "class Movimiento:\n    def __init__(self, nombre, potencia, pp=20):\n        self.nombre = nombre\n        self.potencia = potencia\n        self.pp = pp\n    def __str__(self):\n        return f\"{self.nombre} (potencia:{self.potencia}) [{self.pp}PP]\"\n    def __lt__(self, otro):\n        return self.potencia < otro.potencia\n    def usar(self):\n        if self.pp > 0:\n            self.pp -= 1\n            return self.potencia\n        return None\nbola = Movimiento(\"Thunderbolt\", 90)\nrayo = Movimiento(\"Rayo\", 40)\nprint(bola > rayo)  # True\nbola.usar(); bola.usar(); bola.usar()\nprint(bola)",
        "exercisePrompt": "Creá clases con métodos dunder para hacerlas intuitivas.",
        "codeFile": "./lessons/16_metodos_especiales.py",
        "tests": [
            {"id": "t1", "name": "__str__ implemented", "description": "Readable representation", "expect": "__str__"},
            {"id": "t2", "name": "__lt__ compares", "description": "Less by power", "expect": "__lt__"},
            {"id": "t3", "name": "__eq__ equality", "description": "Equality by name", "expect": "__eq__"},
            {"id": "t4", "name": "Usage reduces PP", "description": "PP decrements on use", "expect": "self.pp"}
        ]
    },
    {
        "id": 18, "module": "06", "level": "intermediate", "type": "flying",
        "title": "3. Propiedades (@property)",
        "shortTitle": "Properties",
        "objective": "Usar propiedades para controlar acceso a atributos sensibles.",
        "keyConcept": "@property crea getters/setters validados.",
        "theory": "### Proteger el HP con propiedades\n\nLas propiedades permiten validar valores cuando se asignan:\n\n```python\nclass Pokemon:\n    @property\n    def hp(self):\n        return self._hp\n\n    @hp.setter\n    def hp(self, valor):\n        if 0 <= valor <= 100:\n            self._hp = valor\n        else:\n            raise ValueError(\"HP debe estar entre 0 y 100\")\n```\n\nTambién puedes crear propiedades de **solo lectura** (sin setter).",
        "example": "class Pokemon:\n    def __init__(self, nombre, nivel=1):\n        self.nombre = nombre\n        self._nivel = nivel\n        self._hp_max = nivel * 20\n        self._hp = self._hp_max\n    @property\n    def nivel(self):\n        return self._nivel\n    @nivel.setter\n    def nivel(self, v):\n        if 1 <= v <= 100:\n            self._nivel = v\n            self._hp_max = v * 20\n    @property\n    def hp(self):\n        return self._hp\n    @hp.setter\n    def hp(self, v):\n        self._hp = max(0, min(v, self._hp_max))\n    @property\n    def vivo(self):\n        return self._hp > 0\n    @property\n    def porcentaje_hp(self):\n        return round(self._hp / self._hp_max * 100, 1)\np = Pokemon(\"Pikachu\")\nprint(f\"Nivel: {p.nivel}, HP: {p.hp}, Vivo: {p.vivo}, {p.porcentaje_hp}%\")\np.hp = 80; p.hp = 5\nprint(f\"HP: {p.hp}, Porcentaje: {p.porcentaje_hp}%\")",
        "exercisePrompt": "Definí propiedades con validación para atributos sensibles de tus clases Pokémon.",
        "codeFile": "./lessons/17_properties.py",
        "tests": [
            {"id": "t1", "name": "Property nivel getter", "description": "Returns internal _nivel", "expect": "@property"},
            {"id": "t2", "name": "Property nivel setter", "description": "Validates range 1-100", "expect": "@nivel.setter"},
            {"id": "t3", "name": "Property hp setter", "description": "Limits HP to max", "expect": "@hp.setter"},
            {"id": "t4", "name": "Living property", "description": "True if HP > 0", "expect": "hp > 0"}
        ]
    },
    {
        "id": 19, "module": "06", "level": "intermediate", "type": "dragon",
        "title": "4. Decoradores @classmethod y @staticmethod",
        "shortTitle": "Decoradores",
        "objective": "Usar decoradores para métodos de clase y estáticos.",
        "keyConcept": "@classmethod recibe clase como primer arg. @staticmethod no necesita self ni cls.",
        "theory": "### Fábricas y utilidades en clases\n\n```python\nclass Pokemon:\n    @classmethod\n    def huevo(cls, tipo):\n        return cls(f\"Huevo-{tipo}\", tipo)\n    @staticmethod\n    def ventaja(tipo_a, tipo_b):\n        eficientes = {\"fuego\": [\"planta\", \"hielo\"]}\n        return tipo_b in eficientes.get(tipo_a, [])\n\nhuevo = Pokemon.huevo(\"agua\")\nefectivo = Pokemon.ventaja(\"fuego\", \"planta\")\n```",
        "example": "class TypeChart:\n    SUPER = {\"fuego\": {\"planta\", \"hielo\", \"acero\"}, \"agua\": {\"fuego\", \"roca\"}}\n    @classmethod\n    def from_dict(cls, data):\n        obj = cls()\n        return obj\n    @staticmethod\n    def efecto(tipo_mov, tipo_def):\n        return 2.0 if tipo_def in TypeChart.SUPER.get(tipo_mov, set()) else 1.0\n    @property\n    def tipos_cubiertos(self):\n        covered = set()\n        for defs in TypeChart.SUPER.values():\n            covered.update(defs)\n        return sorted(covered)\ntc = TypeChart()\nprint(TypeChart.efecto(\"fuego\", \"planta\"))\nprint(tc.tipos_cubiertos)",
        "exercisePrompt": "Definí métodos de clase fábricas, estáticos de consulta y propiedades computadas.",
        "codeFile": "./lessons/18_decoradores.py",
        "tests": [
            {"id": "t1", "name": "@classmethod factory", "description": "Creates instance from class", "expect": "@classmethod"},
            {"id": "t2", "name": "@staticmethod", "description": "Function without self", "expect": "@staticmethod"},
            {"id": "t3", "name": "Type effect calculates", "description": "Returns correct multiplier", "expect": "SUPER"},
            {"id": "t4", "name": "tipos_cubiertos", "description": "Property computes correctly", "expect": "@property"}
        ]
    }
])

# --- MODULO 07: Herencia ---
lessons.extend([
    {
        "id": 20, "module": "07", "level": "intermediate", "type": "psychic",
        "title": "1. Herencia — Subclases",
        "shortTitle": "Herencia",
        "objective": "Crear subclases que hereden y extiendan comportamiento de Pokémon.",
        "keyConcept": "class Hijo(Padre) hereda todo. super() llama al padre. Override sobrescribe.",
        "theory": "### Evolución: de clase base a especializados\n\nLa **herencia** permite crear clases basadas en otras:\n\n```python\nclass Pokemon:\n    def __init__(self, nombre, tipo):\n        self.nombre = nombre\n        self.tipo = tipo\n    def hablar(self):\n        return f\"{self.nombre} dice...\"\n\nclass Electrico(Pokemon):\n    def __init__(self, nombre, voltaje):\n        super().__init__(nombre, \"electrico\")\n        self.voltaje = voltaje\n    def atacar(self):\n        return f\"¡{self.nombre} lanzó Rayo ({self.voltaje}V)!\"\n\npika = Electrico(\"Pikachu\", 50000)\nprint(pika.atacar())  # ¡Pikachu lanzó Rayo (50000V)!\nprint(pika.hablar())  # Pikachu dice... (heredado)\n```\n\nPodés **override** métodos heredados para cambiar el comportamiento.",
        "example": "class Pokemon:\n    def __init__(self, nombre, tipo, nivel=1, hp_base=50):\n        self.nombre = nombre\n        self.tipo = tipo\n        self.nivel = nivel\n        self.hp_max = hp_base + nivel * 10\n        self.hp = self.hp_max\n    def ganar_xp(self, xp):\n        for _ in range(xp // 100):\n            self.subir_nivel()\n    def subir_nivel(self):\n        self.nivel += 1\n        self.hp_max += 10\n        self.hp = self.hp_max\n        print(f\"{self.nombre} subió a nivel {self.nivel}!\")\n    def puede_evolucionar(self):\n        return False\n\nclass Electrico(Pokemon):\n    def __init__(self, nombre, voltaje=100000):\n        super().__init__(nombre, \"electrico\")\n        self.voltaje = voltaje\n    def puede_evolucionar(self):\n        return self.nivel >= 16\n\npika = Electrico(\"Pikachu\", 50000)\nfor _ in range(20):\n    pika.ganar_xp(100)\nprint(pika.name); print(pika.puede_evolucionar())",
        "exercisePrompt": "Creá hierarquías de especies con herencia, overrides y super().",
        "codeFile": "./lessons/19_herencia.py",
        "tests": [
            {"id": "t1", "name": "Electric inherits Pokemon", "description": "instance is Pokemon", "expect": "isinstance"},
            {"id": "t2", "name": "Fuego subclass", "description": "Extends Pokemon with fire moves", "expect": "class Fuego"},
            {"id": "t3", "name": "Agua subclass", "description": "Extends Pokemon with water moves", "expect": "class Agua"},
            {"id": "t4", "name": "Override learning", "description": "Electric only learns electric moves", "expect": "super().aprender"}
        ]
    },
    {
        "id": 21, "module": "07", "level": "intermediate", "type": "ghost",
        "title": "2. Polimorfismo",
        "shortTitle": "Polimorfismo",
        "objective": "Usar polimorfismo para tratar subclases como su clase padre.",
        "keyConcept": "Polimorfismo: objetos distintos comparten interfaz. duck typing en Python.",
        "theory": "### Un equipo diverso, misma interfaz\n\nEl **polimorfismo** permite tratar objetos distintos de forma uniforme:\n\n```python\ndef iniciar_combate(eq1, eq2):\n    p1 = eq1[0]  # puede ser Electrico, Fuego, Agua...\n    p2 = eq2[0]\n    print(f\"¡{p1} vs {p2}!\")\n    while p1.hp > 0 and p2.hp > 0:\n        p1.atacar(p2)  # same method, different behavior!\n        p2.atacar(p1)\n\nclass Electrico(Pokemon): ...\nclass Fuego(Pokemon): ...\n\npikachu = Electrico(\"Pikachu\")\ncharmander = Fuego(\"Charmander\")\niniciar_combate([pikachu], [charmander])\n```",
        "example": "class Pokemon:\n    def __init__(self, nombre, tipo):\n        self.nombre = nombre\n        self.tipo = tipo\n        self.hp = 100\n    def atacar(self, objetivo):\n        pass\nclass Electrico(Pokemon):\n    def atacar(self, objetivo):\n        dano = 20 if objetivo.tipo == \"agua\" else 10\n        objetivo.hp = max(0, objetivo.hp - dano)\n        print(f\"{self.nombre} → {objetivo.nombre}: {dano} daño\")\nclass Fuego(Pokemon):\n    def atacar(self, objetivo):\n        dano = 20 if objetivo.tipo == \"planta\" else 10\n        objetivo.hp = max(0, objetivo.hp - dano)\n        print(f\"{self.nombre} → {objetivo.nombre}: {dano} daño\")\npikachu = Electrico(\"Pikachu\", \"electrico\")\nchar = Fuego(\"Char\", \"fuego\")\npikachu.atacar(char)\nprint(f\"Char HP: {char.hp}\")",
        "exercisePrompt": "Creá un sistema de batalla donde cada tipo ataca diferente pero con la misma interfaz.",
        "codeFile": "./lessons/20_polimorfismo.py",
        "tests": [
            {"id": "t1", "name": "Polymorphism works", "description": "atacar() works on all", "expect": "def atacar"},
            {"id": "t2", "name": "Type advantage", "description": "Damage varies by type", "expect": "== objetivo.tipo"},
            {"id": "t3", "name": "Battle simulates", "description": "Alternating turns", "expect": "while"},
            {"id": "t4", "name": "Winner detected", "description": "HP of loser equals 0", "expect": "ganador ="}
        ]
    }
])

# --- MODULO 08: Big O ---
lessons.extend([
    {
        "id": 22, "module": "08", "level": "intermediate", "type": "steel",
        "title": "1. Big O Notation",
        "shortTitle": "Big O",
        "objective": "Analizar la complejidad temporal de funciones usando Pokémons como ejemplo.",
        "keyConcept": "Big O mide cómo escala el tiempo. O(1), O(log n), O(n), O(n²).",
        "theory": "### ¿Qué tan rápido es tu estrategia?\n\n| Complejidad | Nombre | Ejemplo Pokémon |\n|------------|--------|-----------------|\n| O(1) | Constante | Acceso directo a stat por índice |\n| O(log n) | Logarítmica | Buscar en Pokédex ordenada |\n| O(n) | Lineal | Buscar un Pokémon en lista |\n| O(n²) | Cuadrática | Comparar cada vs cada |\n\n```python\n# O(1) - Acceso directo\npokemons = [\"Pikachu\", \"Charmander\", \"Squirtle\"]\nprint(pokemons[0])\n\n# O(n) - Recorrer toda la lista\nfor poke in pokemons:\n    print(poke)\n\n# O(n²) - Comparar cada pareja\nfor p1 in pokemons:\n    for p2 in pokemons:\n        compare(p1, p2)\n```",
        "example": "pokemons = [\"Bulbasaur\", \"Charmander\", \"Pikachu\", \"Squirtle\"]\nprint(pokemons[0])  # O(1)\nfor p in pokemons:  # O(n)\n    print(p)",
        "exercisePrompt": "Implementa funciones con distintas complejidades temporales analizándolas.",
        "codeFile": "./lessons/21_big_o.py",
        "tests": [
            {"id": "t1", "name": "Search sequential", "description": "Returns index or -1", "expect": "return"},
            {"id": "t2", "name": "O(1) access", "description": "Directs access to first", "expect": "[0]"},
            {"id": "t3", "name": "Sum HP linear", "description": "Sums all HP", "expect": "sum"},
            {"id": "t4", "name": "Comparisons quadratic", "description": "nC2 pairs", "expect": "* (n-1) / 2"}
        ]
    }
])

# --- MODULO 09: Recursion ---
lessons.extend([
    {
        "id": 23, "module": "09", "level": "intermediate", "type": "dragon",
        "title": "1. Fundamentos de Recursión",
        "shortTitle": "Recursión",
        "objective": "Entender recursión con casos base y recursive paso.",
        "keyConcept": "Función que se llama a sí misma. Casos base previenen infinite recursion.",
        "theory": "### La regla de oro de la recursión\n\nTodo problema recursivo necesita:\n1. **Caso base**: cuándo parar\n2. **Caso recursivo**: cómo avanzar hacia el caso base\n\n```python\ndef evolution_chain(pokemon, current_level=1):\n    forms = {\"bulbasaur\": [\"ivysaur\", \"venusaur\"], \"charmander\": [\"charmeleon\", \"charizard\"]}\n    if current_level > 2 or pokemon not in forms:\n        return [pokemon]\n    next_form = forms[pokemon][current_level - 1]\n    return [pokemon] + evolution_chain(next_form, current_level + 1)\n\ncadena = evolution_chain(\"bulbasaur\")\n# ['bulbasaur', 'ivysaur', 'venusaur']\n```",
        "example": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\ndef fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)\nprint(fact(5))       # 120\nprint(fib(10))      # 55",
        "exercisePrompt": "Resolvé problemas recursivos: factorial, fibonacci, sumas, cadenas de evolución.",
        "codeFile": "./lessons/22_recursion.py",
        "tests": [
            {"id": "t1", "name": "Factorial", "description": "Base cases and recursion correct", "expect": "if n <= 1"},
            {"id": "t2", "name": "Recursive sum", "description": "Accumulates correctly", "expect": "lista[0] +"},
            {"id": "t3", "name": "Power", "description": "Base^exp via recursion", "expect": "base *"},
            {"id": "t4", "name": "Evolution chain", "description": "Complete list of forms", "expect": "chains"}
        ]
    }
])

# --- MODULO 10: Algorithms ---
lessons.extend([
    {
        "id": 24, "module": "10", "level": "advanced", "type": "psychic",
        "title": "1. Merge Sort",
        "shortTitle": "Merge Sort",
        "objective": "Implementar Merge Sort para ordenar Pokémons por stats.",
        "keyConcept": "Divide y vencerás: O(n log n) ordenamiento estable.",
        "theory": "### Ordenando tu equipo por fuerza\n\n**Merge Sort** divide la lista en mitades, ordena cada mitad, y las fusiona:\n\n```python\ndef merge_sort(arr, key=lambda x: x):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid], key)\n    right = merge_sort(arr[mid:], key)\n    return merge(left, right, key)\n```",
        "example": "def merge_sort(arr, key=lambda x: x):\n    if len(arr) <= 1: return arr\n    mid = len(arr)//2\n    return merge(merge_sort(arr[:mid], key), merge_sort(arr[mid:], key), key)\ndef merge(left, right, key=lambda x: x):\n    r = []; i = j = 0\n    while i < len(left) and j < len(right):\n        if key(left[i]) <= key(right[j]): r.append(left[i]); i += 1\n        else: r.append(right[j]); j += 1\n    r.extend(left[i:]); r.extend(right[j:])\n    return r\npokemons = [{\"name\":\"A\",\"speed\":50},{\"name\":\"B\",\"speed\":90}]\nordenado = merge_sort(pokemons, key=lambda p: p[\"speed\"])",
        "exercisePrompt": "Implementá Merge Sort completo y ordená Pokémons por distintos stats.",
        "codeFile": "./lessons/23_merge_sort.py",
        "tests": [
            {"id": "t1", "name": "Merge sort basic", "description": "Sorts list correctly", "expect": "merge_sort"},
            {"id": "t2", "name": "Sort by key", "description": "Sorts by specified field", "expect": "lambda"},
            {"id": "t3", "name": "Stable sort", "description": "Maintains relative order", "expect": "<="},
            {"id": "t4", "name": "Empty edge case", "description": "Returns [] for empty input", "expect": "len(arr) <= 1"}
        ]
    }
])

# --- MODULO 11: Graphs ---
lessons.extend([
    {
        "id": 25, "module": "11", "level": "advanced", "type": "psychic",
        "title": "1. Grafos de Tipos",
        "shortTitle": "Grafo Tipos",
        "objective": "Modelar relaciones de tipo como grafo dirigido.",
        "keyConcept": "Tipos como nodos, ventajas como aristas dirigidas.",
        "theory": "### El grafo de matchups\n\nCada tipo Pokémon es un nodo. Las flechas muestran quién vence a quién.\n\n```python\nclass TypeGraph:\n    def __init__(self):\n        self.adyacencia = {}\n    def add_edge(self, from_t, to_t, strength=1.0):\n        self.adyacencia.setdefault(from_t, {})[to_t] = strength\n    def superior_a(self, tipo):\n        return list(self.adyacencia.get(tipo, {}).keys())\n```\n\nPodés encontrar el mejor ataque contra cualquier tipo consultando el grafo inverso.",
        "example": "grafo = {\"fuego\": {\"planta\", \"hielo\", \"acero\"}, \"agua\": {\"fuego\", \"roca\"}}\ndef quien_superior(ofensivo):\n    return grafao.get(ofensivo, set())\nprint(quien_superior(\"fuego\"))  # {'planta', 'hielo', 'acero'}",
        "exercisePrompt": "Construí un grafo completo de matchup tipo y consultalo para optimizar estrategias.",
        "codeFile": "./lessons/24_grafos.py",
        "tests": [
            {"id": "t1", "name": "Graph built", "description": "Directed graph with edges", "expect": "grafo"},
            {"id": "t2", "name": "Who wins", "description": "Correct multiplier", "expect": "def_tipo in"},
            {"id": "t3", "name": "Best options", "description": "List of effective types", "expect": "mejores"},
            {"id": "t4", "name": "Default normal", "description": "Returns normal if none better", "expect": "[\\\"normal\\\"]"}
        ]
    }
])

# --- MODULO 12: DP ---
lessons.extend([
    {
        "id": 26, "module": "12", "level": "advanced", "type": "psychic",
        "title": "1. Memoización",
        "shortTitle": "Memoización",
        "objective": "Aplicar memoización y cache automático para optimizar cálculos.",
        "keyConcept": "Memoización almacena resultados previos. @lru_cache decorator automatiza.",
        "theory": "### Optimizar el moverset óptimo\n\n```python\nfrom functools import lru_cache\n\n@lru_cache(maxsize=None)\ndef win_probability(attacker_hp, defender_hp, turns_left):\n    if turns_left <= 0:\n        return 1.0 if attacker_hp > 0 else 0.0\n    return 0.7 * win_prob(...) + 0.3 * win_prob(...)\n\nprint(win_probability(100, 20, 5))  # Probabilidad calculada una vez, cacheada después\n```",
        "example": "from functools import lru_cache\n@lru_cache(maxsize=None)\ndef fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\nprint(fib(10))  # 55 — instantáneo gracias al cache",
        "exercisePrompt": "Optimizá funciones recursivas con memoización manual y decorators.",
        "codeFile": "./lessons/25_memoization.py",
        "tests": [
            {"id": "t1", "name": "Memoized fib", "description": "Cache avoids recalculations", "expect": "cache[n]"},
            {"id": "t2", "name": "LRU decorated", "description": "Automatic caching", "expect": "@lru_cache"},
            {"id": "t3", "name": "Bottom-up path", "description": "Shortest path found", "expect": "min("},
            {"id": "t4", "name": "Visited protection", "description": "Prevents cycles", "expect": "visited"}
        ]
    },
    {
        "id": 27, "module": "12", "level": "advanced", "type": "ice",
        "title": "2. Knapsack Problem",
        "shortTitle": "Knapsack",
        "objective": "Resolver el problema de mochila para elegir items óptimos.",
        "keyConcept": "Mochila 0/1: max valor con límite de peso. Tabla DP row×col.",
        "theory": "### Armario de preparación\n\nSeleccioná items manteniendo el peso máximo:\n\n```python\ndef knapsack(capacidad, pesos, valores, n):\n    dp = [[0]*(capacidad+1) for _ in range(n+1)]\n    for i in range(1,n+1):\n        for w in range(capacidad+1):\n            if pesos[i-1] <= w:\n                dp[i][w] = max(dp[i-1][w], dp[i-1][w-pesos[i-1]] + valores[i-1])\n            else:\n                dp[i][w] = dp[i-1][w]\n    return dp[n][capacidad]\n```",
        "example": "items = [{\"name\":\"Poción\",\"peso\":1,\"val\":20},{\"name\":\"Revivir\",\"peso\":2,\"val\":80}]\nwts = [i['peso'] for i in items]\nvals = [i['val'] for i in items]\nresult = knapsack(3, wts, vals, len(items))\nprint(result)",
        "exercisePrompt": "Implementá knapsack con tabla DP y backtrack para ver qué items se eligieron.",
        "codeFile": "./lessons/26_knapsack.py",
        "tests": [
            {"id": "t1", "name": "Knapsack table", "description": "Table built correctly", "expect": "dp[i][w] ="},
            {"id": "t2", "name": "Max value returned", "description": "Optimal result", "expect": "dp[n][capacidad]"},
            {"id": "t3", "name": "Trace items", "description": "Backtrack finds correct selection", "expect": "selected.append"},
            {"id": "t4", "name": "Capacity limit", "description": "Total weight <= capacity", "expect": "pesos[i - 1] <="}
        ]
    },
    {
        "id": 28, "module": "12", "level": "advanced", "type": "fighting",
        "title": "3. Longest Common Subsequence",
        "shortTitle": "LCS",
        "objective": "Implementar LCS para comparar secuencias de movimientos.",
        "keyConcept": "LCS compara dos secuencias y encuentra subsecuencia común más larga.",
        "theory": "### Comparar movesets óptimos\n\n```python\ndef lcs(seq1, seq2):\n    m, n = len(seq1), len(seq2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1,m+1):\n        for j in range(1,n+1):\n            if seq1[i-1] == seq2[j-1]:\n                dp[i][j] = dp[i-1][j-1]+1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    # Backtrack para reconstruir\n    common = []\n    i, j = m, n\n    while i>0 and j>0:\n        if seq1[i-1]==seq2[j-1]:\n            common.append(seq1[i-1]); i-=1; j-=1\n        elif dp[i-1][j]>dp[i][j-1]: i-=1\n        else: j-=1\n    return common[::-1]\n```",
        "example": "moves1 = [\"Thunderbolt\",\"Volt Tackle\",\"Quick Attack\"]\nmoves2 = [\"Thunderbolt\",\"Discharge\",\"Quick Attack\",\"Electro Ball\"]\ncommon = lcs(moves1, moves2)\nprint(common)  # ['Thunderbolt', 'Quick Attack']",
        "exercisePrompt": "Compará movesets de diferentes Pokémon usando LCS completo con reconstrucción.",
        "codeFile": "./lessons/27_lcs.py",
        "tests": [
            {"id": "t1", "name": "LCS length calc", "description": "Correct length", "expect": "dp[m][n]"},
            {"id": "t2", "name": "LCS sequence", "description": "Subsequence reconstructed", "expect": "seq1[i-1] =="},
            {"id": "t3", "name": "Empty sequences", "description": "Returns 0/[] for empty inputs", "expect": "dp = [["},
            {"id": "t4", "name": "No common elements", "description": "Returns 0 if no match", "expect": "max("}
        ]
    },
    {
        "id": 29, "module": "proyecto", "level": "advanced", "type": "dragon",
        "title": "Batalla Pokémon Completa",
        "shortTitle": "Proyecto Final",
        "objective": "Construir un juego CLI de batallas Pokémon integrando todas las técnicas del curso.",
        "keyConcept": "Integración: POO + herencia + polimorfismo + estructuras + algoritmos + DP.",
        "theory": "### El desafío final\n\nConstruí un **juego de batallas Pokémon** por consola que use:\n- Clases con herencia (Pokemon, tipos especializados)\n- Polimorfismo (todos tienen atacar()) y propiedades\n- Diccionarios para Pokédex y inventario\n- Try/except para manejo de errores de input\n- JSON para guardar/cargar partida\n- Algoritmos para matchmaking y elección de movimientos óptimos\n\nEste proyecto sintetiza **todo** lo aprendido en los bloques anteriores en una aplicación cohesiva y funcional.",
        "example": "import json, random\nfrom datetime import datetime\n\nclass Pokemon:\n    TIPOS_SUPER = {\"electrico\":[\"agua\",\"volador\"],\"fuego\":[\"planta\",\"hielo\",\"acero\"],\"agua\":[\"fuego\",\"roca\",\"tierra\"]}\n    def __init__(self,nombre,tipo,nivel=5):\n        self.nombre=nombre;self.tipo=tipo;self.nivel=nivel\n        self.hp_max=nivel*20;self.hp=self.hp_max;self.movimientos=[\"Placaje\"]\n    @property\n    def vivo(self): return self.hp > 0\n    def __str__(self): return f\"{self.nombre} Nv.{self.nivel} {self.tipo} HP:{self.hp}/{self.hp_max}\"\n    def recibir_dano(self,d): self.hp=max(0,self.hp-d)\n    def curar(self,c=20): self.hp=min(self.hp+c,self.hp_max)\n\nclass Electrico(Pokemon):\n    def __init__(self,nombre,voltaje=50000):\n        super().__init__(nombre,\"electrico\")\n        self.voltaje=voltaje;self.movimientos=[\"Chispazo\",\"Rayo\",\"Thunderbolt\"]\n    def atacar(self,target):\n        mult=2.0 if target.tipo in self.TIPOS_SUPER.get(\"electrico\",[]) else 1.0\n        mult=0.5 if target.tipo==\"planta\" else mult\n        d=max(1,int((self.nivel*8*self.voltage/10000)*mult))\n        target.recibir_dano(d);print(f\"⚡{self.nombre}->{target.nombre} {d}DMG\")\n\npikachu=Electrico(\"Pikachu\",50000);charmander=Pokemon(\"Charmander\",\"fuego\",5)\nprint(pikacha);print(charmander)\npikachu.atacar(charmander);print(charmander)",
        "exercisePrompt": "Esta es tu oportunidad de integrar TODO lo aprendido. Implementá un juego de batallas Pokémon funcional.",
        "codeFile": "./lessons/28_proyecto_final.py",
        "tests": [
            {"id": "t1", "name": "Pokemon class exists", "description": "Has init, __str__, viver", "expect": "class Pokemon"},
            {"id": "t2", "name": "Types inherit", "description": "Electric, Fire, Water subtypes", "expect": "class Electrico"},
            {"id": "t3", "name": "Attack polymorphic", "description": "Each type attacks differently", "expect": "def atacar"},
            {"id": "t4", "name": "Battle simulates", "description": "Turn-based combat loop", "expect": "while"},
            {"id": "t5", "name": "Save/load", "description": "JSON persistence", "expect": "json"}
        ]
    }
])

# === Write the JSON ===
output_path = Path(__file__).parent / "lessons_corrected.json"
data = {
    "modules": {},
    "totalLessons": len(lessons)
}

# Group lessons by module
for lesson in lessons:
    mod = lesson.pop("module")  # Extract module before storing
    if mod not in data["modules"]:
        data["modules"][mod] = {"title": "", "description": "", "lessons": []}
    data["modules"][mod]["lessons"].append(lesson)

# Add module metadata
module_meta = {
    "01": {"title": "Fundamentos", "description": "Tu primer día como entrenador: print, variables y tipos de datos."},
    "02": {"title": "Entorno y Configuración", "description": "Preparar tu laboratorio de entrenamiento: instalación y configuración del entorno."},
    "03": {"title": "Bucles y Secuencias", "description": "Recorrer equipos de Pokémons, repetir acciones y trabajar con listas."},
    "04": {"title": "Diccionarios y Conjuntos", "description": "Organizar información compleja con diccionarios y deduplicar con sets."},
    "05": {"title": "Manejo de Errores", "description": "Prevenir crashes y manejar errores elegantes como un entrenador experto."},
    "06": {"title": "Clases y Objetos", "description": "Introducción a la Programación Orientada a Objetos usando clases de Pokémon."},
    "07": {"title": "Herencia y Polimorfismo", "description": "Construir jerarquías de clases: especies, tipos evolutivos y comportamientos compartidos."},
    "08": {"title": "Big O y Estructuras", "description": "Comprender complejidad algorítmica implementando pilas, colas y listas enlazadas."},
    "09": {"title": "Recursión", "description": "Funciones que se llaman a sí mismas: evolución, trees de matchup, backtrack."},
    "10": {"title": "Algoritmos de Búsqueda", "description": "Búsqueda binaria y algoritmos de ordenamiento aplicados a datos Pokémon."},
    "11": {"title": "Grafos y Árboles", "description": "Modelar matchups de tipo como grafo, explorar BFS/DFS."},
    "12": {"title": "Programación Dinámica", "description": "Memoización y DP para resolver problemas de optimalidad en batalla."},
    "proyecto": {"title": "Proyecto Final", "description": "Un juego de batallas Pokémon completo que integra todo lo aprendido."}
}
for mod_id, meta in module_meta.items():
    if mod_id in data["modules"]:
        data["modules"][mod_id]["title"] = meta["title"]
        data["modules"][mod_id]["description"] = meta["description"]

# Validate before writing
json_str = json.dumps(data, indent=2, ensure_ascii=False)
# Count lessons total
total_in_modules = sum(len(mod["lessons"]) for mod in data["modules"].values())
assert total_in_modules == len(lessons), f"Mismatch: {total_in_modules} vs {len(lessons)}"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(json_str)
f.close()

print(f"[OK] Generated {output_path}")
print(f"   Modules: {len(data['modules'])}")
print(f"   Total lessons: {total_in_modules}")

# Also verify it parses
with open(output_path, encoding='utf-8') as f:
    verified = json.load(f)
print("[OK] Verified JSON loads successfully!")
# Replace original
import shutil
shutil.copy(str(output_path), str(Path(__file__).parent / "lessons.json"))
print("[OK] Replaced lessons.json")
