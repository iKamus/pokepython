#!/usr/bin/env python3
"""Servidor local para PokéPython.

La app NO funciona abriendo index.html con doble clic: los módulos ES y los
fetch() están bloqueados en file:// (origen "null"). Necesita un servidor.

Este servidor además manda Cache-Control: no-store. `python -m http.server` no
manda headers de caché y el navegador termina sirviendo app.js viejo, que es una
fuente clásica de "lo arreglé y sigue roto".

Uso:
    python serve.py              # http://127.0.0.1:8000
    python serve.py 9000         # otro puerto
    python serve.py 9000 --open  # abre el navegador
"""

from __future__ import annotations

import functools
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class NoCacheHandler(SimpleHTTPRequestHandler):
    """Sirve los archivos del proyecto sin permitir caché heurística."""

    def end_headers(self) -> None:  # noqa: D102 - hook de la stdlib
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:  # silencio: consola limpia
        pass


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    port = int(args[0]) if args else 8000
    open_browser = "--open" in sys.argv

    handler = functools.partial(NoCacheHandler, directory=str(ROOT))
    try:
        server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    except OSError as exc:
        print(f"No pude abrir el puerto {port}: {exc}", file=sys.stderr)
        print("Probá con otro: python serve.py 8001", file=sys.stderr)
        return 1

    pyodide = ROOT / "vendor" / "pyodide" / "pyodide.asm.wasm"
    if not pyodide.exists():
        print("Falta Pyodide local: corré  python vendor/fetch_pyodide.py", flush=True)

    url = f"http://127.0.0.1:{port}/"
    print(f"PokéPython sirviendo {ROOT}", flush=True)
    print(f"  {url}   (Ctrl+C para cortar)", flush=True)

    if open_browser:
        threading.Timer(0.6, webbrowser.open, args=(url,)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nChau.")
    finally:
        server.shutdown()
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
