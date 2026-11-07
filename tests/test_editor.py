"""Editor CodeMirror 6: textarea como fuente de verdad, tema y autocompletado — S9/T10.

El `<textarea id="codeEditor">` sigue siendo la única fuente de verdad: la app y
la suite leen `textarea.value`. CodeMirror es una vista montada encima; si el
módulo vendorizado no carga, `body.has-cm` nunca aparece y el textarea queda
usable (degradación progresiva, cubierta en el último test de este archivo).
"""

import pytest

from conftest import ROOT

pytestmark = pytest.mark.browser

MARKER = "Bloque 01"

# Lee tokens CSS como colores computados, para comparar contra estilos reales.
_PROBE_JS = """
() => {
  const probe = document.createElement('span');
  probe.style.position = 'absolute';
  probe.style.visibility = 'hidden';
  document.body.appendChild(probe);
  const token = name => {
    probe.style.color = '';
    probe.style.color = 'var(' + name + ')';
    return getComputedStyle(probe).color;
  };
  const out = {
    theme: document.documentElement.getAttribute('data-theme'),
    bg_code: token('--bg-code'),
    bg_raised: token('--bg-raised'),
    text_muted: token('--text-muted'),
    content_bg: getComputedStyle(document.querySelector('.cm-content')).backgroundColor,
    editor_bg: getComputedStyle(document.querySelector('.cm-editor')).backgroundColor,
    gutter_color: getComputedStyle(document.querySelector('.cm-lineNumbers .cm-gutterElement')).color,
    tooltip_bg: (() => {
      const tip = document.querySelector('.cm-tooltip-autocomplete');
      return tip ? getComputedStyle(tip).backgroundColor : null;
    })(),
  };
  probe.remove();
  return out;
}
"""


def _open_exercise(page, static_site):
    """Navega a la lección 1, espera el montaje de CodeMirror y abre Ejercicio."""
    page.goto(f"{static_site}#/lesson/1")
    page.wait_for_selector("body.has-cm", timeout=15000)
    page.wait_for_function(
        """() => {
            const ed = document.querySelector('#codeEditor');
            return ed && ed.value.includes('Bloque 01');
        }""",
        timeout=15000,
    )
    page.click('.tab[data-tab="ejercicio"]')
    page.wait_for_selector(".cm-content", state="attached")


def test_editor_cm_actualiza_el_textarea_y_reset_lo_restaura(static_site, page):
    """Teclado en el editor -> el textarea se actualiza; Reset restaura ambos."""
    _open_exercise(page, static_site)

    # Arquitectura: el textarea sigue en el DOM (fuente de verdad), oculto a la vista.
    assert page.locator("#codeEditor").count() == 1, "el textarea no se puede remover"
    assert not page.locator("#codeEditor").is_visible(), "con CM montado el textarea se oculta"
    assert page.locator(".cm-editor").is_visible(), "el editor CM debe estar visible"

    initial = page.locator("#codeEditor").input_value()
    assert MARKER in initial

    page.click(".cm-content")
    page.keyboard.press("Control+End")
    page.keyboard.type("hola")
    page.wait_for_function(
        "() => document.querySelector('#codeEditor').value.endsWith('hola')",
        timeout=5000,
    )
    updated = page.locator("#codeEditor").input_value()
    assert updated == initial + "hola", "el textarea debe reflejar el texto tecleado en el editor"

    page.click("#resetBtn")
    page.wait_for_function(
        "expected => document.querySelector('#codeEditor').value === expected",
        arg=initial,
        timeout=5000,
    )
    assert page.locator("#codeEditor").input_value() == initial, "Reset debe restaurar el textarea"
    assert "hola" not in page.locator(".cm-content").inner_text(), (
        "Reset debe restaurar el texto del editor CM"
    )


def test_tema_del_editor_parejo_en_ambos_temas(static_site, page):
    """Colores computados del editor == tokens del tema, en oscuro y en claro."""
    _open_exercise(page, static_site)

    first = page.evaluate(_PROBE_JS)
    assert first["theme"] in ("dark", "light")
    assert first["content_bg"] == first["bg_code"], (
        f".cm-content bg {first['content_bg']} != --bg-code {first['bg_code']} ({first['theme']})"
    )
    assert first["editor_bg"] == first["bg_code"], (
        f".cm-editor bg {first['editor_bg']} != --bg-code {first['bg_code']} ({first['theme']})"
    )
    assert first["gutter_color"] == first["text_muted"], (
        f"gutter {first['gutter_color']} != --text-muted {first['text_muted']} ({first['theme']})"
    )

    # Cambio de tema SIN recarga: el editor se repinta solo (todo es var()).
    page.evaluate("window.__sinRecarga = true")
    page.click("#themeToggle")
    other = "dark" if first["theme"] == "light" else "light"
    page.wait_for_function(
        "t => document.documentElement.getAttribute('data-theme') === t",
        arg=other,
        timeout=5000,
    )
    assert page.evaluate("window.__sinRecarga === true"), "el tema no debe recargar la página"

    second = page.evaluate(_PROBE_JS)
    assert second["theme"] == other
    assert second["content_bg"] == second["bg_code"], (
        f".cm-content bg {second['content_bg']} != --bg-code {second['bg_code']} ({second['theme']})"
    )
    assert second["editor_bg"] == second["bg_code"], (
        f".cm-editor bg {second['editor_bg']} != --bg-code {second['bg_code']} ({second['theme']})"
    )
    assert second["gutter_color"] == second["text_muted"], (
        f"gutter {second['gutter_color']} != --text-muted {second['text_muted']} ({second['theme']})"
    )


def test_autocompletado_sugiere_print(static_site, page):
    """Teclear `pri` abre el tooltip con `print` y el fondo sale de --bg-raised."""
    _open_exercise(page, static_site)

    page.click(".cm-content")
    page.keyboard.press("Control+End")
    page.keyboard.press("Enter")
    page.keyboard.type("pri")
    page.wait_for_selector(".cm-tooltip-autocomplete", timeout=5000)
    labels = page.locator(".cm-tooltip-autocomplete li").all_inner_texts()
    assert any("print" in t for t in labels), f"'print' no está en el tooltip: {labels}"

    colors = page.evaluate(_PROBE_JS)
    assert colors["tooltip_bg"] == colors["bg_raised"], (
        f"tooltip bg {colors['tooltip_bg']} != --bg-raised {colors['bg_raised']}"
    )


@pytest.mark.slow
def test_completado_pyodide_ofrece_miembros_reales(static_site, page):
    """Con Pyodide listo, `obj.` ofrece miembros reales de dir() (p. ej. casefold)."""
    _open_exercise(page, static_site)

    page.click(".cm-content")
    page.keyboard.press("Control+End")
    page.keyboard.press("Enter")
    page.keyboard.type('pok = "hola"')

    # 1er clic: descarga Pyodide; 2do clic: ejecuta y define `pok` en el intérprete.
    page.click("#runBtn")
    try:
        page.wait_for_function(
            "() => document.querySelector('#consoleStatus').textContent === 'Listo'",
            timeout=40000,
        )
    except Exception:
        pytest.skip("Pyodide no cargó desde el CDN en ~40s: se requiere internet")
    page.click("#runBtn")
    page.wait_for_timeout(1500)

    page.click(".cm-content")
    page.keyboard.press("Control+End")
    page.keyboard.press("Enter")
    page.keyboard.type("pok.")
    # `casefold` no está en la lista curada estática: solo puede venir de dir().
    page.wait_for_function(
        """() => [...document.querySelectorAll('.cm-tooltip-autocomplete li')]
                .some(li => li.textContent.includes('casefold'))""",
        timeout=20000,
    )


@pytest.mark.slow
def test_salida_de_python_aparece_en_la_consola_de_la_pagina(static_site, page):
    """El stdout de Pyodide se enruta a #consoleOutput (consola de la página).

    Sin setStdout/setStderr, print() solo llega a la consola del navegador (F12)
    y #consoleOutput queda vacío. Corre solutions/01.py (imprime 4 líneas) y
    verifica que esas líneas estén DENTRO de la consola de la página.
    """
    _open_exercise(page, static_site)
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

    # 1er clic: descarga Pyodide; 2do clic: ejecuta el código con stdout capturado.
    page.click("#runBtn")
    try:
        page.wait_for_function(
            "() => document.querySelector('#consoleStatus').textContent === 'Listo'",
            timeout=40000,
        )
    except Exception:
        pytest.skip("Pyodide no cargó desde el CDN en ~40s: se requiere internet")
    page.click("#runBtn")

    expected_lines = [
        "Python es un lenguaje de propósito general",
        "Se usa en ciencia de datos",
        "También en desarrollo web",
        "Y en automatización de tareas",
    ]
    try:
        page.wait_for_function(
            """lines => {
                const out = document.querySelector('#consoleOutput');
                const text = out ? out.innerText : '';
                return lines.every(l => text.includes(l));
            }""",
            arg=expected_lines,
            timeout=15000,
        )
    except Exception:
        captured = page.locator("#consoleOutput").inner_text()
        raise AssertionError(
            f"la salida de Python no llegó a #consoleOutput; "
            f"consola de la página: {ascii(captured)}"
        )

    captured = page.locator("#consoleOutput").inner_text()
    # ascii(): la consola de Windows es cp1252 y el placeholder contiene ▶.
    print(f"[console page] {ascii(captured)}")
    assert captured.strip(), "la consola de la página quedó vacía"
    for line in expected_lines:
        assert line in captured, f"falta la línea {line!r} en #consoleOutput"
    assert "Código ejecutado sin errores" in captured, (
        "falta la línea informativa '— Código ejecutado sin errores.'"
    )


def test_si_falla_el_bundle_el_textarea_queda_usable(static_site, page):
    """Degradación progresiva: bundle roto -> sin body.has-cm, textarea usable."""
    warnings = []
    page.on(
        "console",
        lambda m: warnings.append(m.text) if m.type == "warning" else None,
    )
    page.route(
        "**/vendor/codemirror.bundle.js*",
        lambda route: route.fulfill(status=500, content_type="text/javascript", body=""),
    )
    page.goto(f"{static_site}#/lesson/1")
    page.wait_for_function(
        """() => {
            const ed = document.querySelector('#codeEditor');
            return ed && ed.value.includes('Bloque 01');
        }""",
        timeout=15000,
    )
    # app.js degradó sin montar nada: espera su warning de fallback.
    for _ in range(50):
        if any("CodeMirror no disponible" in w for w in warnings):
            break
        page.wait_for_timeout(100)
    assert any("CodeMirror no disponible" in w for w in warnings), (
        f"sin warning de degradación; consola: {warnings}"
    )
    assert not page.locator("body").evaluate(
        "b => b.classList.contains('has-cm')"
    ), "sin editor no debe marcarse body.has-cm"
    assert not page.locator(".cm-editor").count(), "no debe montarse ningún editor"

    # Y sigue siendo visible y usable: teclear en él actualiza su value.
    page.click('.tab[data-tab="ejercicio"]')
    assert page.locator("#codeEditor").is_visible(), "el textarea debe quedar visible"
    page.click("#codeEditor")
    page.keyboard.type("xyz")
    assert "xyz" in page.locator("#codeEditor").input_value(), (
        "el textarea degradado debe aceptar texto"
    )


# ── Contraste de la paleta de sintaxis ──────────────────────────
# La paridad de color no alcanza: un token puede coincidir con su variable y
# seguir siendo ilegible. En este curso los comentarios son la mitad del código
# del starter, así que cada color de sintaxis debe pasar AA (4.5:1) sobre el
# fondo del editor, en AMBOS temas.

_CONTRAST_JS = """
(name) => {
  const probe = document.createElement('span');
  probe.style.position = 'absolute';
  probe.style.visibility = 'hidden';
  document.body.appendChild(probe);
  const resolve = value => {
    probe.style.color = '';
    probe.style.color = value;
    return getComputedStyle(probe).color;
  };
  const rgb = value => (value.match(/\d+/g) || [0, 0, 0]).slice(0, 3).map(Number);
  const lum = value => {
    const [r, g, b] = rgb(value).map(v => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };
  const ratio = (a, b) => {
    const la = lum(a), lb = lum(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  };
  const bgCode = resolve('var(--bg-code)');
  const bgRaised = resolve('var(--bg-raised)');
  const out = {};
  for (const token of ['--syn-keyword', '--syn-string', '--syn-number',
                       '--syn-comment', '--syn-function', '--syn-operator']) {
    const color = resolve('var(' + token + ')');
    out[token + '__code'] = Number(ratio(color, bgCode).toFixed(2));
    out[token + '__raised'] = Number(ratio(color, bgRaised).toFixed(2));
  }
  out.bg_code = bgCode;
  out.bg_raised = bgRaised;
  probe.remove();
  return out;
}
"""


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_syntax_palette_passes_aa_contrast(page, static_site, theme):
    page.add_init_script(f"localStorage.setItem('pokpy_theme', '{theme}')")
    page.goto(f"{static_site}#/lesson/3")
    page.wait_for_selector("body.has-cm")
    page.click('.tab[data-tab="ejercicio"]')
    page.wait_for_selector(".cm-content")

    result = page.evaluate(_CONTRAST_JS)
    assert result["bg_code"], "no se pudo resolver --bg-code"
    assert result["bg_raised"], "no se pudo resolver --bg-raised"
    failing = {k: v for k, v in result.items() if k.startswith("--syn-") and v < 4.5}
    assert not failing, (
        f"tokens bajo AA 4.5:1 en tema {theme}: {failing} "
        f"(--bg-code={result['bg_code']}, --bg-raised={result['bg_raised']})"
    )


# ── Regresiones de la consola de la página ──────────────────────
# Tres defectos reportados por el usuario y reproducidos: el placeholder tapaba
# la salida, el estado quedaba en "Ejecutando..." para siempre, y en arranque en
# frío la corrida seguía sin runtime dejando los tests en "?".

_STARTER_TEXT = "Acá aparecerá la salida"


def _abrir_ejercicio(page, static_site, lesson=1):
    page.goto(f"{static_site}#/lesson/{lesson}")
    page.wait_for_selector("body.has-cm")
    page.click('.tab[data-tab="ejercicio"]')
    page.wait_for_selector(".cm-content")


def _pegar_solucion(page, lesson=1):
    code = (ROOT / "solutions" / f"{lesson:02d}.py").read_text(encoding="utf-8")
    page.evaluate(
        """(code) => {
        const ed = document.querySelector('#codeEditor');
        ed.value = code;
        ed.dispatchEvent(new Event('input', { bubbles: true }));
    }""",
        code,
    )


def _correr_y_esperar(page, timeout=45000):
    page.evaluate("() => document.querySelector('#runBtn').click()")
    page.wait_for_function(
        """() => {
        const out = document.querySelector('#consoleOutput').innerText;
        const listo = out.includes('ejecutado sin errores') || out.includes('PythonError');
        return listo;
    }""",
        timeout=timeout,
    )
    page.wait_for_timeout(1500)  # runTests se dispara 500 ms después de la corrida


@pytest.mark.slow
def test_consola_no_conserva_el_placeholder_y_marca_listo(page, static_site):
    _abrir_ejercicio(page, static_site)
    _pegar_solucion(page)
    _correr_y_esperar(page)

    salida = page.inner_text("#consoleOutput")
    assert _STARTER_TEXT not in salida, f"el placeholder sigue arriba de la salida:\n{salida}"
    assert "Python es un lenguaje de propósito general" in salida, salida
    assert page.inner_text("#consoleStatus").strip() == "Listo"


@pytest.mark.slow
def test_arranque_en_frio_corre_y_marca_los_tests(page, static_site):
    """Primera corrida de la sesión: initPyodide tiene que esperar la carga real.

    Si no espera, la corrida sigue sin runtime y los tests quedan en "?".
    """
    _abrir_ejercicio(page, static_site)
    _pegar_solucion(page)
    _correr_y_esperar(page, timeout=60000)

    estados = page.eval_on_selector_all(
        "#testsPanel .test-status",
        "els => els.map(e => e.className)",
    )
    assert estados, "el panel de tests está vacío"
    pending = [e for e in estados if "test-pending" in e]
    assert not pending, f"quedaron tests sin resolver: {estados}"
    assert all("test-pass" in e for e in estados), f"la solución no pasó todo: {estados}"
