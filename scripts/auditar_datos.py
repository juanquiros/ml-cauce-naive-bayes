"""Auditoría de sólo lectura y línea base manual; no entrena modelos ni limpia texto."""

import argparse
import hashlib
import json
import platform
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score


def auditar(ruta):
    datos = pd.read_csv(ruta)
    texto = datos["texto"].fillna("")
    duplicados = datos.duplicated(["id_cliente", "texto"])
    grupos = datos.groupby(["id_cliente", "texto"], dropna=False)
    alertas = {
        "email": r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}",
        "url": r"(?:https?://|www\.)\S+",
        "mencion_dni": r"(?i)\bdni\b",
        "mencion_telefono_celular": r"(?i)\b(?:telefono|celular|tel|cel)\b",
        "mencion_cbu_cvu_alias": r"(?i)\b(?:cbu|cvu|alias)\b",
        "digitos_consecutivos_6_o_mas": r"\d{6,}",
    }
    fechas = pd.to_datetime(datos["fecha_hora"], errors="coerce")
    resultado = {
        "sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
        "filas": len(datos),
        "columnas": datos.columns.tolist(),
        "tipos_inferidos": datos.dtypes.astype(str).to_dict(),
        "nulos_por_columna": datos.isna().sum().astype(int).to_dict(),
        "textos_vacios_incluyendo_nulos": int(texto.str.strip().eq("").sum()),
        "textos_solo_espacios_no_nulos": int((datos.texto.notna() & texto.str.strip().eq("")).sum()),
        "duplicados_fila_completa": int(datos.duplicated().sum()),
        "duplicados_cliente_texto_excedentes": int(duplicados.sum()),
        "grupos_cliente_texto_repetidos": int(grupos.size().gt(1).sum()),
        "textos_repetidos_excedentes_sin_distinguir_cliente": int(datos.texto.duplicated().sum()),
        "id_mensaje_repetidos": int(datos.id_mensaje.duplicated().sum()),
        "clientes_distintos": int(datos.id_cliente.nunique()),
        "canales": datos.canal.value_counts().astype(int).to_dict(),
        "fechas_invalidas": int(fechas.isna().sum()),
        "rango_fechas": [str(fechas.min()), str(fechas.max())],
        "alertas_privacidad_filas": {k: int(texto.str.contains(v, regex=True).sum()) for k, v in alertas.items()},
    }
    if "equipo_final" in datos:
        clases = sorted(datos.equipo_final.unique().tolist())
        real, manual = datos.equipo_final, datos.equipo_derivado
        fraude = real.eq("fraude")
        perdido = fraude & manual.ne("fraude")
        resultado.update({
            "objetivo": "equipo_final",
            "clases": clases,
            "distribucion_equipo_final": real.value_counts().astype(int).to_dict(),
            "distribucion_equipo_derivado": manual.value_counts().astype(int).to_dict(),
            "grupos_duplicados_con_etiquetas_distintas": int(grupos.equipo_final.nunique().gt(1).sum()),
            "palabras_por_clase_sin_limpieza": texto.str.split().str.len().groupby(real).agg(["count", "mean", "median", "min", "max"]).to_dict(orient="index"),
            "linea_base_exploratoria_todas_las_filas": {
                "mensajes": len(datos),
                "aciertos": int(real.eq(manual).sum()),
                "errores": int(real.ne(manual).sum()),
                "exactitud": float(accuracy_score(real, manual)),
                "f1_macro": float(f1_score(real, manual, average="macro")),
                "fraudes_reales": int(fraude.sum()),
                "fraudes_derivados_a_otro_equipo": int(perdido.sum()),
                "proporcion_fraude_derivado_a_otro_equipo": float(perdido.sum() / fraude.sum()),
                "orden_clases_matrices": clases,
                "matriz_confusion_conteos": confusion_matrix(real, manual, labels=clases).tolist(),
                "matriz_confusion_normalizada_por_fila": confusion_matrix(real, manual, labels=clases, normalize="true").tolist(),
                "nota": "Exploratoria, sobre datos originales con duplicados; no es evaluación final en prueba.",
            },
        })
    return resultado


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", type=Path, help="JSON agregado; nunca incluye mensajes ni identificadores")
    args = parser.parse_args()
    raiz = Path(__file__).resolve().parents[1]
    resultado = {
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "metodo_vacios": "fillna('').str.strip().eq(''); no se modifica el dataframe",
        "datasets": {n: auditar(raiz / "caso1_cauce/datos" / n) for n in ("mensajes_historicos.csv", "mensajes_nuevos.csv")},
    }
    historicos = pd.read_csv(raiz / "caso1_cauce/datos/mensajes_historicos.csv")
    nuevos = pd.read_csv(raiz / "caso1_cauce/datos/mensajes_nuevos.csv")
    resultado["solapamiento"] = {
        "clientes_compartidos": len(set(historicos.id_cliente) & set(nuevos.id_cliente)),
        "textos_no_vacios_compartidos": sum(
            bool(texto.strip())
            for texto in set(historicos.texto.dropna()) & set(nuevos.texto.dropna())
        ),
        "id_mensaje_compartidos": len(set(historicos.id_mensaje) & set(nuevos.id_mensaje)),
    }
    contenido = json.dumps(resultado, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.salida:
        args.salida.parent.mkdir(parents=True, exist_ok=True)
        args.salida.write_text(contenido, encoding="utf-8")
    else:
        print(contenido)


if __name__ == "__main__":
    main()
