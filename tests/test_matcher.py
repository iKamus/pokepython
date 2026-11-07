"""S10 / T11: el matcher valida de verdad — test real, sin xfail (L16 → L27).

Antes, `runTests` comparaba `expect` como substring sobre TODO el código del
editor, comentarios y docstrings incluidos, y cada consigna cita la salida
esperada: el starter intacto aprobaba todos sus tests en 16 de 29 lecciones
(L14), así que presionar Correr sin escribir nada completaba la lección.

T11 quita comentarios y docstrings antes de comparar (espejo en
`tests/py_matcher.py`, algoritmo idéntico a `stripPythonNoise` en `app.js`) y
de-resuelve los starters que venían entregados completos (L26/L27). El criterio
de aceptación es exacto: NINGÚN starter sin tocar aprueba todos sus tests.
"""

from pathlib import Path

from py_matcher import lessons_by_id, starter_passes_all

ROOT = Path(__file__).resolve().parents[1]


def test_starter_intocado_no_pasa_todos_sus_tests():
    """0 de 29: un starter intacto no puede aprobar la totalidad de sus tests."""
    lessons = lessons_by_id()
    assert len(lessons) == 29, f"solo {len(lessons)} lecciones en lessons.json"
    passing = [l["id"] for l in lessons if starter_passes_all(l)]
    assert passing == [], (
        f"{len(passing)} de {len(lessons)} starters intocados aprueban todos sus "
        f"tests (lecciones {passing}): el matcher dejaría de ignorar comentarios/"
        f"docstrings o el starter volvió a quedar resuelto"
    )


def test_app_usa_el_mismo_stripping():
    """El espejo no miente: app.js debe aplicar stripPythonNoise en runTests."""
    app = (ROOT / "app.js").read_text(encoding="utf-8")
    # Una definición (function stripPythonNoise) + un uso (normalizado=…).
    assert app.count("stripPythonNoise(") >= 2, (
        "app.js ya no usa stripPythonNoise: el matcher de la app dejaría de "
        "ignorar comentarios/docstrings y este espejo no lo vería"
    )
    assert "matcherClean(" in app, (
        "app.js ya no normaliza ambos lados de los expects con == (L28)"
    )
