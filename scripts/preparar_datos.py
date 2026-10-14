"""Recupera sólo los dos CSV originales de Cauce, sin sobrescribir archivos."""

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip_docente", type=Path)
    args = parser.parse_args()
    raiz = Path(__file__).resolve().parents[1]
    manifiesto = json.loads(
        (raiz / "docs/evidencias/integridad_materiales.json").read_text(encoding="utf-8")
    )
    pendientes = []
    with ZipFile(args.zip_docente) as archivo:
        for nombre in ("mensajes_historicos.csv", "mensajes_nuevos.csv"):
            relativo = f"caso1_cauce/datos/{nombre}"
            contenido = archivo.read(f"materiales_estudiantes/{relativo}")
            esperado = manifiesto["archivos_docentes"][relativo]
            if hashlib.sha256(contenido).hexdigest() != esperado:
                raise SystemExit(f"El CSV del ZIP no coincide con el auditado: {nombre}")
            destino = raiz / relativo
            if destino.exists():
                if destino.read_bytes() != contenido:
                    raise SystemExit(f"Se conserva sin cambios el archivo distinto: {destino}")
                print(f"Ya existe y coincide: {relativo}")
            else:
                pendientes.append((destino, contenido))
    for destino, contenido in pendientes:
        destino.parent.mkdir(parents=True, exist_ok=True)
        with destino.open("xb") as salida:
            salida.write(contenido)
        print(f"Recuperado sin modificaciones: {destino.relative_to(raiz)}")
    print("CSV conservados en local. Su publicación sigue suspendida por privacidad.")


if __name__ == "__main__":
    main()
