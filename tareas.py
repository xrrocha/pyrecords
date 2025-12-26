#!/usr/bin/env python3
"""
Tareas de desarrollo para PyRecords.

Uso:
    python tareas.py <comando>

Comandos:
    dev      Ejecutar Marimo en modo edición
    build    Exportar notebook a WASM
    serve    Servir el export WASM localmente
    help     Mostrar esta ayuda
"""
import subprocess
import sys
from pathlib import Path

# Directorio raíz del proyecto
ROOT = Path(__file__).parent
NOTEBOOKS = ROOT / "notebooks"
DIST = ROOT / "dist"


def dev():
    """Ejecutar Marimo en modo edición."""
    print("🚀 Iniciando Marimo...")
    subprocess.run(["marimo", "edit", "00_tuberia_nula.py"], cwd=NOTEBOOKS)


def build():
    """Exportar notebook a WASM para distribución serverless."""
    print("📦 Exportando a WASM...")
    subprocess.run([
        "marimo", "export", "html-wasm",
        "00_tuberia_nula.py",
        "-o", str(DIST),
        "--mode", "run"
    ], cwd=NOTEBOOKS)
    print(f"✅ Exportado a {DIST}/")


def serve():
    """Servir el export WASM localmente."""
    if not DIST.exists():
        print("❌ No existe el directorio dist/. Ejecuta 'python tareas.py build' primero.")
        sys.exit(1)
    print(f"🌐 Sirviendo en http://localhost:8000")
    subprocess.run([sys.executable, "-m", "http.server", "8000", "--directory", str(DIST)])


def help_cmd():
    """Mostrar ayuda."""
    print(__doc__)
    print("Comandos disponibles:")
    print("  dev      Ejecutar Marimo en modo edición")
    print("  build    Exportar notebook a WASM")
    print("  serve    Servir el export WASM localmente")
    print("  help     Mostrar esta ayuda")


COMANDOS = {
    "dev": dev,
    "build": build,
    "serve": serve,
    "help": help_cmd,
}


def main():
    if len(sys.argv) < 2:
        help_cmd()
        sys.exit(0)

    comando = sys.argv[1]
    if comando not in COMANDOS:
        print(f"❌ Comando desconocido: {comando}")
        help_cmd()
        sys.exit(1)

    COMANDOS[comando]()


if __name__ == "__main__":
    main()
