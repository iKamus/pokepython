"""Espejo en Python del matcher de `app.js` (`runTests`) — S10 / T11.

El matcher compara `expect` en minúsculas contra el código del editor, pero SOLO
sobre código real: `strip_python_noise` elimina comentarios (`# ...`) y docstrings
(cadenas triple comilla que abren una sentencia) con la misma máquina de estados
que `stripPythonNoise` en `app.js`. Sin ese paso, las consignas — que citan la
salida esperada — aprueban el starter intacto (L14 / L26).

Ramas de `matcher_passes` (mismas que runTests):
- expect normal → substring sobre el código limpio en minúsculas;
- expect con `==`, `!=` o `assert ` → primero la app intenta correrlo en Pyodide
  (intento OPCIONAL que solo puede mejorar el resultado, L28) y, si no da True,
  compara expect y código ambos reducidos a minúsculas alfanuméricas
  (`matcher_clean`). El espejo implementa esa comparación determinista: en este
  corpus ningún expect evalúa a True solo (todos dan SyntaxError), así que ambos
  lados coinciden.

Ambos lados deben mantener el mismo algoritmo:
- cadenas de una y de tres comillas, con escapes por barra invertida;
- `# ...` hasta fin de línea SOLO fuera de cadenas (`print("#")` se conserva);
- triple comilla se elimina solo si abre una sentencia a nivel 0 (docstring de
  módulo/clase/función); una triple comilla que forma parte de una expresión
  (una asignación, un argumento) se conserva.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_TRIPLE = ('"""', "'''")
_SINGLE = ('"', "'")
_OPEN = "([{"
_CLOSE = ")]}"


def strip_python_noise(source: str) -> str:
    """Quita comentarios y docstrings; conserva cadenas que son parte de código."""
    out = []
    i = 0
    n = len(source)
    prev = ""       # último código no vacío visto (los comentarios no lo tocan)
    depth = 0       # profundidad de ( [ { — dentro de un paréntesis no hay docstring)

    while i < n:
        c = source[i]

        # ── Triple comilla (docstring o cadena multilinea) ──
        if source.startswith(_TRIPLE[0], i) or source.startswith(_TRIPLE[1], i):
            q = source[i:i + 3]
            is_doc = depth == 0 and prev in ("", ":")
            j = i + 3
            while j < n:
                if source[j] == "\\":
                    j += 2
                    continue
                if source.startswith(q, j):
                    j += 3
                    break
                j += 1
            else:
                j = n  # sin cierre: se lleva el resto
            if not is_doc:
                out.append(source[i:j])
                prev = '"'
            i = j
            continue

        # ── Cadena de una línea ──
        if c in _SINGLE:
            j = i + 1
            while j < n:
                if source[j] == "\\":
                    j += 2
                    continue
                if source[j] == c:
                    j += 1
                    break
                if source[j] == "\n":
                    break  # sin cierre: defensa, corta en el fin de línea
                j += 1
            out.append(source[i:j])
            prev = '"'
            i = j
            continue

        # ── Comentario hasta fin de línea (solo fuera de cadenas) ──
        if c == "#":
            while i < n and source[i] != "\n":
                i += 1
            continue

        out.append(c)
        if c in _OPEN:
            depth += 1
        elif c in _CLOSE:
            depth = max(0, depth - 1)
        if not c.isspace():
            prev = c
        i += 1

    return "".join(out)


def matcher_clean(s: str) -> str:
    """Minúsculas y solo alfanuméricos — espejo de matcherClean() en app.js."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def matcher_passes(expect: str, source: str) -> bool:
    """¿El expect cumple bajo la regla de runTests para el código dado?"""
    normalized = strip_python_noise(source).lower()
    expected = expect.lower()
    if "assert " in expected or "==" in expected or "!=" in expected:
        return matcher_clean(expected) in matcher_clean(normalized)
    return expected in normalized


def lessons_by_id():
    data = json.loads((ROOT / "lessons.json").read_text(encoding="utf-8"))
    lessons = [l for mod in data["modules"].values() for l in mod["lessons"]]
    lessons.sort(key=lambda l: l["id"])
    return lessons


def _read(path):
    """read_text sin traducir fin de línea: el navegador ve los bytes crudos
    (CRLF incluido), así que el espejo también. newline='' desde Python 3.13."""
    return Path(path).read_text(encoding="utf-8", newline="")


def starter_passes_all(lesson, *, strip: bool = True):
    """¿El starter sin tocar aprueba TODOS los tests bajo la regla indicada?"""
    source = _read(ROOT / lesson["codeFile"])
    if not strip:
        # Regla previa a T11 (L14): substring crudo sobre TODO el archivo.
        source = source.lower()
        return all(t["expect"].lower() in source for t in lesson["tests"])
    return all(matcher_passes(t["expect"], source) for t in lesson["tests"])


def solution_failing_expects(lesson, *, strip: bool = True):
    """Devuelve [(test_id, expect), ...] que la solución no cumple."""
    source = _read(ROOT / lesson["solutionFile"])
    if not strip:
        source_l = source.lower()
        return [
            (t["id"], t["expect"])
            for t in lesson["tests"]
            if t["expect"].lower() not in source_l
        ]
    return [
        (t["id"], t["expect"])
        for t in lesson["tests"]
        if not matcher_passes(t["expect"], source)
    ]
