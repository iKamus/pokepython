"""Soluciones: compilan, corren y cumplen el matcher de la app — S8 / T9 / S10.

El matcher real vive en `app.js` (`runTests`): un test pasa si `expect` aparece
como substring del código del editor SOLO CUANDO ES CÓDIGO REAL — comentarios y
docstrings se ignoran antes de comparar (T11/S10). Este módulo es su ESPEJO en
Python (`tests/py_matcher.py`): cada solución debe contener el `expect` de cada
test de su lección bajo esa misma regla, además de compilar y ejecutarse con
rc == 0.
"""

import json
import os
import py_compile
import subprocess
import sys
from pathlib import Path

import pytest

from py_matcher import matcher_passes

ROOT = Path(__file__).resolve().parents[1]


def _lessons_by_id():
    data = json.loads((ROOT / "lessons.json").read_text(encoding="utf-8"))
    lessons = [l for mod in data["modules"].values() for l in mod["lessons"]]
    return {l["id"]: l for l in lessons}


LESSONS = _lessons_by_id()


@pytest.mark.parametrize("lesson_id", range(1, 30))
def test_solucion_compila_corre_y_satisface_expect(lesson_id, tmp_path):
    lesson = LESSONS[lesson_id]
    solution_path = ROOT / lesson["solutionFile"]
    # newline='': los tests de la app leen los bytes crudos del archivo.
    source = solution_path.read_text(encoding="utf-8", newline="")

    # 1. Compila (cfile en tmp, fuera del repo).
    py_compile.compile(
        str(solution_path), cfile=str(tmp_path / f"sol_{lesson_id:02d}.pyc"), doraise=True
    )

    # 2. Corre limpio; cwd en tmp para que archivos escritos no aterricen en el repo.
    #    PYTHONIOENCODING=utf-8: en Windows la consola es cp1252 y las soluciones
    #    imprimen emoji/flechas; en la app corren en Pyodide (UTF-8), acá se replica
    #    tanto en el hijo (PYTHONIOENCODING) como en la decodificación del padre.
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, str(solution_path)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        timeout=60,
    )
    assert proc.returncode == 0, (
        f"solución {lesson['solutionFile']} rc={proc.returncode}\n{proc.stderr}"
    )

    # 3. Espejo de app.js runTests: matcher sobre código real (sin comentarios
    #    ni docstrings) y, para expects con ==, ambos lados en alfanuméricos.
    failing = [
        (t["id"], t["expect"])
        for t in lesson["tests"]
        if not matcher_passes(t["expect"], source)
    ]
    assert not failing, (
        f"lección {lesson_id}, {lesson['solutionFile']}: expects sin cumplir bajo "
        f"el matcher de app.js (código limpio): {failing}"
    )
