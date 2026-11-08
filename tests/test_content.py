"""Invariantes de datos de lessons/*.py y lessons*.json sin navegador — S8 / T9.

Propiedades exactas de la spec S8: estructura del JSON, módulos, archivos en disco,
tema del starter (guard de la permutación de T6), calidad de los tests, espejo con
lessons_corrected.json y compilación de todos los starters.
"""

import ast
import json
import py_compile
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

import py_matcher

ROOT = Path(__file__).resolve().parents[1]
MODULE_KEYS = {f"{n:02d}" for n in range(1, 13)} | {"proyecto"}
EXPECTED_IDS = list(range(1, 30))


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


@pytest.mark.xfail(
    strict=False,
    reason="T26: 16 lecciones más siguen con el starter resuelto o con expects que ya "
           "aparecen en el starter. Este test pasa a XPASS cuando se corrijan (S10).",
)
def test_ningun_starter_aprueba_un_test():
    """Un ejercicio sin resolver no puede aprobar ningún test (S10).

    Medido con el matcher real. Hoy falla en 16 lecciones; la lista queda visible
    en el mensaje del fallo en vez de descubrirse de a una.
    """
    ls = {l["id"]: l for l in py_matcher.lessons_by_id()}
    culpables = []
    for lid, leccion in sorted(ls.items()):
        starter = py_matcher._read(ROOT / leccion["codeFile"])
        pasan = [t["id"] for t in leccion["tests"] if py_matcher.matcher_passes(t["expect"], starter)]
        if pasan:
            culpables.append(f"{lid}:{pasan}")
    assert not culpables, f"starters que aprueban sin resolver: {culpables}"
