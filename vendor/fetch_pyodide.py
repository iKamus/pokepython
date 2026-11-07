#!/usr/bin/env python3
"""Descarga Pyodide para uso local (una sola vez, necesita internet).

La app carga Pyodide desde `vendor/pyodide/`, no desde un CDN: así funciona
offline y el navegador no bloquea nada por "tracking prevention".

Uso:
    python vendor/fetch_pyodide.py
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

VERSION = "0.24.1"
BASE = f"https://cdn.jsdelivr.net/pyodide/v{VERSION}/full"
FILES = [
    "pyodide.js",
    "pyodide.asm.js",
    "pyodide.asm.wasm",
    "python_stdlib.zip",
    "pyodide-lock.json",
]
DEST = Path(__file__).resolve().parent / "pyodide"


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    total = 0
    for name in FILES:
        target = DEST / name
        if target.exists() and target.stat().st_size > 1024:
            print(f"  {name:<22} ya está ({target.stat().st_size // 1024} KB)")
            total += target.stat().st_size
            continue
        print(f"  {name:<22} descargando…", end="", flush=True)
        try:
            with urllib.request.urlopen(f"{BASE}/{name}", timeout=120) as r:
                data = r.read()
        except Exception as exc:  # noqa: BLE001
            print(f" FALLÓ ({exc})")
            return 1
        if len(data) < 1024:
            print(" FALLÓ (respuesta vacía)")
            return 1
        target.write_bytes(data)
        print(f" {len(data) // 1024} KB")
        total += len(data)
    print(f"\nPyodide {VERSION} listo en {DEST} ({total // (1024 * 1024)} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
