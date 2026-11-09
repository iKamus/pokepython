"""Invariantes de datos de lessons/*.py y lessons*.json sin navegador — S8 / T9.

Propiedades exactas de la spec S8: estructura del JSON, módulos, archivos en disco,
tema del starter (guard de la permutación de T6), calidad de los tests, espejo con
lessons_corrected.json y compilación de todos los starters.
"""

import ast
import json
import py_compile
import re
import shutil
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

import py_matcher

ROOT = Path(__file__).resolve().parents[1]
MODULE_KEYS = {f"{n:02d}" for n in range(1, 13)} | {"proyecto"}
EXPECTED_IDS = list(range(1, 30))
# Runtime de Pyodide que la app carga desde ./vendor/pyodide/ (S3).
PYODIDE_FILES = (
    "pyodide.js",
    "pyodide.asm.js",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
)
MIN_RUNTIME_BYTES = 1024


def _load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def _flat_lessons(data):
    lessons = [l for mod in data["modules"].values() for l in mod["lessons"]]
    lessons.sort(key=lambda l: l["id"])
    return lessons


def _norm(text):
    """Minúsculas sin acentos ni puntuación."""
    text = unicodedata.normalize("NFD", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return " ".join(text.split())


def test_lessons_json_parsea_con_29_lecciones():
    data = _load("lessons.json")
    assert data["totalLessons"] == 29, f"totalLessons={data['totalLessons']}, esperado 29"
    ids = [l["id"] for l in _flat_lessons(data)]
    assert ids == EXPECTED_IDS, f"ids={ids}"
    assert len(set(ids)) == 29, "ids duplicados en lessons.json"


def test_modulos_son_exactamente_los_13():
    data = _load("lessons.json")
    keys = set(data["modules"])
    assert keys == MODULE_KEYS, f"módulos={sorted(keys)}"
    assert len(keys) == 13, f"hay {len(keys)} módulos, esperado 13"


def test_codefile_y_solutionfile_existen_en_disco():
    for lesson in _flat_lessons(_load("lessons.json")):
        for field in ("codeFile", "solutionFile"):
            value = lesson.get(field)
            assert value, f"lección {lesson['id']} sin {field}"
            assert (ROOT / value).is_file(), f"lección {lesson['id']}: falta {value}"


def test_docstring_del_starter_coincide_con_el_titulo():
    """Guard de la permutación de T6: el starter de NN habla del tema de la lección NN."""
    for lesson in _flat_lessons(_load("lessons.json")):
        source = (ROOT / lesson["codeFile"]).read_text(encoding="utf-8")
        doc = ast.get_docstring(ast.parse(source))
        assert doc, f"{lesson['codeFile']} sin docstring"
        first_line = doc.splitlines()[0]
        titulo = re.sub(r"^\d+\.\s*", "", lesson["title"])          # "N. Tema" → "Tema"
        tema_doc = re.sub(r"^Bloque\s+\d+\s*·\s*", "", first_line)  # "Bloque NN · " → "Tema"
        t_titulo, t_doc = _norm(titulo), _norm(tema_doc)
        assert t_doc == t_titulo or t_doc.startswith(t_titulo + " "), (
            f"lección {lesson['id']}: docstring '{first_line}' no corresponde a '{lesson['title']}'"
        )


def test_cada_leccion_tiene_tests_validos():
    for lesson in _flat_lessons(_load("lessons.json")):
        tests = lesson["tests"]
        assert len(tests) >= 4, f"lección {lesson['id']}: {len(tests)} tests, mínimo 4"
        ids = [t["id"] for t in tests]
        assert len(ids) == len(set(ids)), f"lección {lesson['id']}: ids de test repetidos"
        for t in tests:
            for field in ("id", "name", "expect"):
                assert str(t.get(field, "")).strip(), (
                    f"lección {lesson['id']}: test {t.get('id')} sin {field}"
                )


def test_lessons_corrected_coincide_con_lessons_json():
    data = _load("lessons.json")
    corrected = _load("lessons_corrected.json")
    ids = {l["id"] for l in _flat_lessons(data)}
    ids_corr = {l["id"] for l in _flat_lessons(corrected)}
    assert ids_corr == ids, f"ids distintos: {sorted(ids_corr ^ ids)}"
    sols = {l["solutionFile"] for l in _flat_lessons(data)}
    sols_corr = {l["solutionFile"] for l in _flat_lessons(corrected)}
    assert sols_corr == sols, f"solutionFile distintos: {sorted(sols_corr ^ sols)}"


def test_todos_los_starters_compilan(tmp_path):
    """py_compile con cfile en tmp: nada de __pycache__ dentro del repo."""
    paths = sorted((ROOT / "lessons").glob("*.py"))
    assert len(paths) >= 29, f"solo {len(paths)} archivos en lessons/"
    for path in paths:
        py_compile.compile(
            str(path), cfile=str(tmp_path / f"{path.stem}.pyc"), doraise=True
        )


# Vocabulario del curso: si el panel se llama "Ejemplo Pokémon", el ejemplo tiene que
# hablar de Pokémon y no de Python en general.
POKEMON_TERMS = (
    "pokemon", "pokemons", "pikachu", "charmander", "squirtle", "bulbasaur", "entrenador",
    "pokedex", "tipo", "tipos", "hp", "nivel", "movimiento", "movimientos",
    "evolucion", "evolucionar", "batalla", "equipo", "stat", "stats",
    "pocion", "revivir", "fuego", "agua", "planta", "electrico", "hielo",
    "acero", "roca", "volador", "medalla", "gimnasio", "dano", "ataque",
)


def test_cada_ejemplo_habla_de_pokemon():
    """El panel se llama "Ejemplo Pokémon": un ejemplo de Python genérico lo desmiente."""
    for lesson in _flat_lessons(_load("lessons.json")):
        ejemplo = _norm(lesson.get("example") or "")
        assert ejemplo, f"lección {lesson['id']} sin example"
        assert set(ejemplo.split()) & set(POKEMON_TERMS), (
            f"lección {lesson['id']}: el ejemplo no habla de Pokémon — "
            f"{(lesson.get('example') or '').splitlines()[0][:70]!r}"
        )


def test_todos_los_ejemplos_corren(tmp_path):
    """Un ejemplo que no corre al pegarlo enseña a copiar errores."""
    for lesson in _flat_lessons(_load("lessons.json")):
        archivo = tmp_path / f"ejemplo_{lesson['id']}.py"
        archivo.write_text(lesson["example"], encoding="utf-8")
        corrida = subprocess.run(
            # -X utf8: los ejemplos imprimen emoji y la consola de Windows usa cp1252.
            [sys.executable, "-X", "utf8", str(archivo)],
            capture_output=True, text=True, encoding="utf-8",
        )
        ultima = (corrida.stderr.strip().splitlines() or [""])[-1]
        assert corrida.returncode == 0, f"lección {lesson['id']}: {ultima}"


def test_ningun_starter_aprueba_un_test():
    """Un ejercicio sin resolver no puede aprobar ningún test (S10).

    Regla del curso: el starter nunca viene resuelto. Se mide con el matcher real
    en las 29 lecciones, así que un starter que vuelva a entregarse con la
    respuesta escrita rompe la suite con el id de la lección.
    """
    ls = {l["id"]: l for l in py_matcher.lessons_by_id()}
    culpables = []
    for lid, leccion in sorted(ls.items()):
        starter = py_matcher._read(ROOT / leccion["codeFile"])
        pasan = [t["id"] for t in leccion["tests"] if py_matcher.matcher_passes(t["expect"], starter)]
        if pasan:
            culpables.append(f"{lid}:{pasan}")
    assert not culpables, f"starters que aprueban sin resolver: {culpables}"


def test_no_quedan_errores_ortograficos_ni_controles():
    banned_plain = ["hierarquias", "Advantage tipo", "crashing del programa", "infinite recursion"]
    banned_regex = re.compile(r"\banios\b", re.IGNORECASE)
    control_ranges = [
        (0x0001, 0x0008),
        (0x000B, 0x000B),
        (0x000C, 0x000C),
        (0x000E, 0x001F),
        (0x007F, 0x009F),
    ]

    files = []
    files += sorted((ROOT / "lessons").glob("*.py"))
    files += sorted((ROOT / "solutions").glob("*.py"))
    files += [ROOT / "lessons.json", ROOT / "lessons_corrected.json", ROOT / "index.html",
              ROOT / "app.js", ROOT / "README.md", ROOT / "generate_lessons.py"]

    violations = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            violations.append(f"{path}:0: no se pudo leer ({e})")
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if banned_regex.search(line):
                violations.append(f"{path.relative_to(ROOT)}:{lineno}: patron prohibido \\banios\\b")
            low = line.lower()
            for pat in banned_plain:
                if pat.lower() in low:
                    violations.append(f"{path.relative_to(ROOT)}:{lineno}: patron prohibido {pat!r}")
            for ch in line:
                cp = ord(ch)
                for lo, hi in control_ranges:
                    if lo <= cp <= hi:
                        violations.append(
                            f"{path.relative_to(ROOT)}:{lineno}: caracter de control U+{cp:04X}"
                        )
                        break
    assert not violations, "violaciones encontradas:\n" + "\n".join(violations)


def test_runtime_pyodide_completo_y_versionado():
    """Un ▶ Correr publicado no puede depender de archivos que git no lleva (S3).

    GitHub Pages sirve solo lo comiteado: si el runtime falta o está ignorado, la app
    responde 404 al cargar Pyodide. Dos chequeos independientes:

    1. los 5 archivos existen en `vendor/pyodide/` y pesan más de 1 KB;
    2. git no ignora `vendor/pyodide/` (si git no está disponible, se skipea SOLO esto).
    """
    faltantes = []
    for name in PYODIDE_FILES:
        path = ROOT / "vendor" / "pyodide" / name
        if not path.is_file():
            faltantes.append(f"{name}: no existe")
        else:
            tamano = path.stat().st_size
            if tamano <= MIN_RUNTIME_BYTES:
                faltantes.append(f"{name}: {tamano} bytes (mínimo {MIN_RUNTIME_BYTES})")
    assert not faltantes, (
        "el runtime de Pyodide está incompleto en vendor/pyodide/; "
        "bajalo con: python vendor/fetch_pyodide.py\n" + "\n".join(faltantes)
    )

    if shutil.which("git") is None:
        pytest.skip("git no está disponible: no se puede comprobar si vendor/pyodide/ está ignorado")
    repo = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=ROOT, capture_output=True, text=True,
    )
    if repo.returncode != 0:
        pytest.skip(f"{ROOT} no es un repo git: no se puede comprobar si vendor/pyodide/ está ignorado")

    ignorado = subprocess.run(
        ["git", "check-ignore", "-v", "vendor/pyodide/pyodide.js"],
        cwd=ROOT, capture_output=True, text=True,
    )
    # 0 = ignorado, 1 = no ignorado, 128 = error de git.
    assert ignorado.returncode == 1, (
        "vendor/pyodide/pyodide.js está ignorado por git "
        f"({ignorado.stdout.strip() or ignorado.stderr.strip()}; exit {ignorado.returncode}). "
        "Pages solo publica lo comiteado: ▶ Correr daría 404. "
        "Sacá la regla de vendor/pyodide/ del .gitignore."
    )
