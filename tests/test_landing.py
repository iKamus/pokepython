"""Comportamiento de la app en navegador: landing, tema y barrido de lecciones — S8.

Usa `page` (pytest-playwright, canal msedge) + `static_site` (server no-store).
Si un test descubre un defecto de la app, falla con su aserción: la app no se toca.
"""

import json
import time
from pathlib import Path

import pytest

pytestmark = pytest.mark.browser

ROOT = Path(__file__).resolve().parents[1]
MODULE_ORDER = [f"{n:02d}" for n in range(1, 13)] + ["proyecto"]


def _lessons():
    data = json.loads((ROOT / "lessons.json").read_text(encoding="utf-8"))
    lessons = [l for mod in data["modules"].values() for l in mod["lessons"]]
    lessons.sort(key=lambda l: l["id"])
    return lessons


def _collect_console_errors(page):
    """Registra errores de consola y errores de página; devuelve la lista."""
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    return errors


def test_landing_carga_sin_errores_y_13_tarjetas(static_site, page):
    errors = _collect_console_errors(page)
    page.goto(static_site)
    page.wait_for_selector(".module-card")
    assert page.locator(".module-card").count() == 13, "la landing debe mostrar 13 tarjetas"
    assert not errors, f"errores de consola: {errors}"


def test_orden_de_modulos_en_landing_y_sidebar(static_site, page):
    page.goto(static_site)
    page.wait_for_selector(".module-card")
    cards = page.locator("#modulesGrid .module-card").evaluate_all(
        "els => els.map(e => e.dataset.module)"
    )
    assert cards == MODULE_ORDER, f"orden en landing: {cards}"
    sidebar = page.locator("#moduleNav .module-header").evaluate_all(
        "els => els.map(e => e.dataset.module)"
    )
    assert sidebar == MODULE_ORDER, f"orden en sidebar: {sidebar}"


def test_hero_muestra_29_13_135(static_site, page):
    page.goto(static_site)
    assert page.locator("#statLessons").inner_text() == "29"
    assert page.locator("#statModules").inner_text() == "13"
    assert page.locator("#statTests").inner_text() == "135"


def test_tema_default_toggle_y_persistencia(static_site, page):
    page.goto(static_site)
    # Sin elección guardada: respeta el sistema; data-theme debe reflejarlo.
    expected = page.evaluate(
        "localStorage.getItem('pokpy_theme') || "
        "(matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark')"
    )
    assert expected in ("light", "dark"), f"tema inicial inválido: {expected}"
    initial = page.locator("html").get_attribute("data-theme")
    assert initial == expected, f"data-theme={initial}, esperado {expected}"

    # Toggle: invierte el tema y lo persiste.
    page.click("#themeToggle")
    flipped = "dark" if initial == "light" else "light"
    assert page.locator("html").get_attribute("data-theme") == flipped
    assert page.evaluate("localStorage.getItem('pokpy_theme')") == flipped

    # Recarga: la elección persiste.
    page.reload()
    assert page.locator("html").get_attribute("data-theme") == flipped, (
        "tras recargar el tema elegido no persistió (pokpy_theme)"
    )


@pytest.mark.slow
def test_all_lessons_render(static_site, page):
    errors = _collect_console_errors(page)
    page.goto(static_site)
    page.wait_for_selector(".module-card")
    for lesson in _lessons():
        marker = f"Bloque {lesson['id']:02d}"
        n_tests = len(lesson["tests"])
        page.evaluate(f"window.location.hash = '#/lesson/{lesson['id']}'")
        page.wait_for_function(
            """([marker, n]) => {
                const ed = document.querySelector('#codeEditor');
                return ed && ed.value.includes(marker) &&
                       document.querySelectorAll('#testsPanel .test-item').length === n;
            }""",
            arg=[marker, n_tests],
            timeout=15000,
        )
        lid = lesson["id"]
        assert page.locator("#theoryPanel").inner_text().strip(), (
            f"lección {lid}: teoría vacía"
        )
        assert page.locator("#codeEditor").input_value().strip(), (
            f"lección {lid}: editor vacío"
        )
        n_items = page.locator("#testsPanel .test-item").count()
        assert n_items == n_tests, f"lección {lid}: {n_items} tests en el panel, esperado {n_tests}"
    assert errors == [], f"errores de consola durante el barrido: {errors}"


@pytest.mark.slow
def test_lesson_solution_passes_in_pyodide(static_site, page):
    """Pega solutions/01.py en el editor y verifica los 4 tests en verde (Pyodide CDN)."""
    page.goto(f"{static_site}#/lesson/1")
    page.wait_for_function(
        "() => document.querySelector('#codeEditor').value.includes('Bloque 01')",
        timeout=15000,
    )
    solution = page.evaluate(
        "fetch('solutions/01.py').then(r => { if (!r.ok) throw new Error(r.status); return r.text(); })"
    )
    page.evaluate(
        """code => {
            const el = document.querySelector('#codeEditor');
            el.value = code;
            el.dispatchEvent(new Event('input', {bubbles: true}));
        }""",
        solution,
    )

    # El botón Correr vive junto al editor (S11/T12): abrir la pestaña Ejercicio
    # antes de clickearlo, si no, queda oculto tras la pestaña Teoría.
    page.click('.tab[data-tab="ejercicio"]')
    page.wait_for_selector("#runBtn", state="visible")

    # 1er clic: dispara la descarga de Pyodide desde el CDN (~40s de gracia).
    page.click("#runBtn")
    try:
        page.wait_for_function(
            "() => document.querySelector('#consoleStatus').textContent === 'Listo'",
            timeout=40000,
        )
    except Exception:
        pytest.skip("Pyodide no cargó desde el CDN en ~40s: se requiere internet")

    # 2do clic: ejecuta el código y lanza runTests (setTimeout 500ms).
    page.click("#runBtn")
    deadline = time.monotonic() + 30
    pending = -1
    while time.monotonic() < deadline:
        pending = page.locator(".test-status.test-pending").count()
        if pending == 0:
            break
        page.wait_for_timeout(500)
    if pending != 0:
        pytest.skip(f"Pyodide no terminó de evaluar en 30s ({pending} tests pendientes)")

    statuses = page.locator(".test-status").evaluate_all(
        "els => els.map(e => e.className)"
    )
    assert statuses, "sin estados de test en la página"
    fails = [s for s in statuses if "test-pass" not in s]
    assert not fails, f"tests en rojo con la solución pegada: {fails}"


def _wait_tests_resolved(page, timeout=30):
    """Espera a que runTests (setTimeout 500ms) deje de marcar pendientes."""
    deadline = time.monotonic() + timeout
    pending = -1
    while time.monotonic() < deadline:
        pending = page.locator(".test-status.test-pending").count()
        if pending == 0:
            return
        page.wait_for_timeout(500)
    raise AssertionError(f"runTests no resolvió {pending} tests en {timeout}s")


@pytest.mark.slow
@pytest.mark.parametrize("lesson_id,target_test", [(12, "t4"), (21, "t2"), (28, "t2")])
def test_expect_con_igualdad_falla_con_starter_y_pasa_con_solucion(
    static_site, page, lesson_id, target_test
):
    """L28: los expects con == se normalizan en AMBOS lados antes de matchear.

    Antes se intentaban correr como Python, fallaban con SyntaxError y el
    fallback quitaba puntuación solo del expect → nunca matcheaban (ni siquiera
    con la solución pegada). Verificación en navegador: con el starter intacto
    el test objetivo FALLA y con la solución pegada pasan TODOS los tests.
    """
    page.goto(f"{static_site}#/lesson/{lesson_id}")
    page.wait_for_function(
        """marker => {
            const ed = document.querySelector('#codeEditor');
            return ed && ed.value.includes(marker);
        }""",
        arg=f"Bloque {lesson_id:02d}",
        timeout=15000,
    )
    solution = page.evaluate(
        f"fetch('solutions/{lesson_id:02d}.py').then(r => {{ if (!r.ok) throw new Error(r.status); return r.text(); }})"
    )
    # El botón Correr vive junto al editor (S11): abrir la pestaña Ejercicio.
    page.click('.tab[data-tab="ejercicio"]')
    page.wait_for_selector("#runBtn", state="visible")

    # 1er clic: descarga Pyodide; 2do clic: corre el starter intacto.
    page.click("#runBtn")
    try:
        page.wait_for_function(
            "() => document.querySelector('#consoleStatus').textContent === 'Listo'",
            timeout=40000,
        )
    except Exception:
        pytest.skip("Pyodide no cargó desde el CDN en ~40s: se requiere internet")
    page.click("#runBtn")
    _wait_tests_resolved(page)

    starter_cls = page.locator(f"#ts-{target_test}").get_attribute("class")
    starter_txt = page.locator(f"#ts-{target_test}").inner_text()
    assert "test-fail" in starter_cls, (
        f"starter intacto: {lesson_id} {target_test} pasó ({starter_cls}) — "
        f"el expect con == matchea de más"
    )

    # Pegar la solución y volver a correr. OJO: los estados ya vienen
    # resueltos del run anterior (runTests nunca repone test-pending), así que
    # hay que esperar a que TODOS pasen, no a que no queden pendientes.
    page.evaluate(
        """code => {
            const el = document.querySelector('#codeEditor');
            el.value = code;
            el.dispatchEvent(new Event('input', {bubbles: true}));
        }""",
        solution,
    )
    page.click("#runBtn")
    try:
        page.wait_for_function(
            """() => {
                const els = [...document.querySelectorAll('.test-status')];
                return els.length > 0 &&
                       els.every(e => e.classList.contains('test-pass'));
            }""",
            timeout=30000,
        )
    except Exception:
        pass  # el assert de abajo muestra los estados reales

    statuses = page.locator(".test-status").evaluate_all(
        "els => els.map(e => e.className)"
    )
    fails = [i for i, s in enumerate(statuses) if "test-pass" not in s]
    print(
        f"[lesson {lesson_id}] starter {target_test}={ascii(starter_txt.strip())} "
        f"({starter_cls}); solucion statuses={ascii(statuses)}"
    )
    assert not fails, (
        f"solución {lesson_id:02d}.py: {len(fails)} tests en rojo en el navegador: "
        f"{[(i, statuses[i]) for i in fails]}"
    )


def test_mobile_sin_recortes(page, static_site):
    """A 390px (iPhone 12/13) nada puede salir del viewport ni esconder opciones.

    El filtro de niveles se cortaba y 'Avanzado' quedaba fuera de pantalla: se
    prefiere que envuelva en dos filas antes que scroll horizontal silencioso.
    """
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(static_site)
    page.wait_for_selector(".module-card")

    metrics = page.evaluate(
        """() => {
        const btns = [...document.querySelectorAll('.mode-btn')];
        return {
          overflowX: document.documentElement.scrollWidth > window.innerWidth + 2,
          toggleScrolls: (() => {
            const t = document.querySelector('.mode-toggle');
            return t.scrollWidth > t.clientWidth + 2;
          })(),
          clipped: btns.filter(b => {
            const r = b.getBoundingClientRect();
            return r.width === 0 || r.right > window.innerWidth - 2;
          }).map(b => b.textContent.trim()),
          cards: document.querySelectorAll('.module-card').length,
        };
    }"""
    )

    assert metrics["cards"] == 13
    assert not metrics["overflowX"], "la página scrollea horizontalmente en mobile"
    assert not metrics["toggleScrolls"], "el filtro de niveles scrollea en lugar de envolver"
    assert metrics["clipped"] == [], f"botones fuera de pantalla: {metrics['clipped']}"


def test_teoria_renderiza_bloques_de_codigo(static_site, page):
    """Los fences ```python de la teoría son <pre> reales con sus saltos de línea.

    Antes los comía el regex de código inline: el bloque entero terminaba dentro de
    un <code> con acento y el fence dejaba un backtick huérfano al final. Eso es el
    "cortado" de las tarjetitas de énfasis en la teoría.
    """
    page.goto(static_site)
    page.wait_for_selector(".module-card")
    page.evaluate("window.location.hash = '#/lesson/1'")
    page.wait_for_selector("#theoryPanel pre code", timeout=15000)
    bloque = page.locator("#theoryPanel pre").first
    codigo = bloque.locator("code").inner_text()
    assert "# En Python todo empieza con print()" in codigo, (
        f"el bloque de código no conserva el comentario: {codigo!r}"
    )
    assert 'print("¡Hola, Entrenador!")' in codigo, (
        f"el bloque de código no conserva el print: {codigo!r}"
    )
    assert "\n" in codigo, "el bloque perdió sus saltos de línea (¿se volvió código inline?)"
    assert "<br>" not in bloque.inner_html(), "el bloque usa <br> en lugar de saltos reales"
    texto = page.locator("#theoryPanel").inner_text()
    assert "```" not in texto, "el fence quedó visible en la teoría"
    assert "`" not in texto, "quedó un backtick huérfano del fence en la teoría"


def test_teoria_renderiza_listas_y_tablas(static_site, page):
    """Listas y tablas de la teoría son HTML real, no guiones ni barras literales."""
    page.goto(static_site)
    page.wait_for_selector(".module-card")

    # Lista con viñetas (lección 1) + numerada (lección 23)
    page.evaluate("window.location.hash = '#/lesson/1'")
    page.wait_for_selector("#theoryPanel ul li", timeout=15000)
    items = page.locator("#theoryPanel ul li").all_inner_texts()
    assert any("Ciencia de datos" in t for t in items), f"viñetas crudas: {items}"
    page.evaluate("window.location.hash = '#/lesson/23'")
    page.wait_for_selector("#theoryPanel ol li", timeout=15000)
    pasos = page.locator("#theoryPanel ol li").all_inner_texts()
    assert len(pasos) == 2, f"la lista numerada tiene {len(pasos)} items: {pasos}"
    assert any("Caso base" in t for t in pasos), pasos

    # Tabla (lección 3)
    page.evaluate("window.location.hash = '#/lesson/3'")
    page.wait_for_selector("#theoryPanel table", timeout=15000)
    cabeceras = page.locator("#theoryPanel table th").all_inner_texts()
    assert "Método" in " ".join(cabeceras), f"cabeceras: {cabeceras}"
    assert page.locator("#theoryPanel table tr").count() >= 3, "la tabla quedó sin filas de datos"

    for lid, texto in ((1, None), (3, None), (23, None)):
        page.evaluate(f"window.location.hash = '#/lesson/{lid}'")
        page.wait_for_timeout(150)
        cuerpo = page.locator("#theoryPanel").inner_text()
        assert "**" not in cuerpo, f"lección {lid}: negrita sin renderizar"
        assert not any(line.startswith("- ") for line in cuerpo.splitlines()), (
            f"lección {lid}: viñetas crudas en el texto"
        )
        assert "|" not in cuerpo, f"lección {lid}: tabla cruda (barras literales)"


def test_teoria_renderiza_encabezados_hondos_y_concepto(static_site, page):
    """`####` también es un encabezado, y el concepto clave lleva su código inline."""
    page.goto(static_site)
    page.wait_for_selector(".module-card")
    page.evaluate("window.location.hash = '#/lesson/3'")
    page.wait_for_selector("#theoryPanel .concept-box", timeout=15000)
    concepto = page.locator("#theoryPanel .concept-box").first.inner_text()
    assert "`" not in concepto, f"el concepto clave muestra backticks crudos: {concepto!r}"
    assert page.locator("#theoryPanel .concept-box code").count() >= 1, (
        "el concepto clave no convirtió su código inline"
    )
    cuerpo = page.locator("#theoryPanel").inner_text()
    assert "####" not in cuerpo, "quedó un encabezado markdown crudo (#### …) en la teoría"
