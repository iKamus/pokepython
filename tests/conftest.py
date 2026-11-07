"""Fixtures compartidas de la suite S8.

El server estático efímero agrega `Cache-Control: no-store` a cada respuesta:
`python -m http.server` no manda cabeceras de cache y los tests de navegador
terminarían midiendo assets viejos del navegador.
"""

import functools
import socket
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

# Raíz del sitio estático: curso_pokemon_web/ (carpeta padre de tests/).
ROOT = Path(__file__).resolve().parents[1]


class _NoStoreHandler(SimpleHTTPRequestHandler):
    """Sirve ROOT y fuerza no-store para que el navegador siempre reciba lo fresco."""

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):  # silencio: el server es de tests
        pass


@pytest.fixture(scope="session")
def static_site():
    """URL base (con / final) de un server efímero sobre ROOT, en 127.0.0.1."""
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    handler = functools.partial(_NoStoreHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{port}/"
    finally:
        server.shutdown()
        server.server_close()
