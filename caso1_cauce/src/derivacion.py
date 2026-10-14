"""Regla de derivación de mensajes y sus indicadores de negocio.

Completá las dos funciones. Solo NumPy. Verificá tu trabajo con:  python -m pytest -q tests/test_derivacion.py
"""
import numpy as np

REVISION = "revision_humana"


def derivar(proba, clases, umbral_fraude, umbral_confianza):
    """Decide el destino de cada mensaje a partir de las probabilidades del modelo.

    proba : array (n_mensajes, n_clases) con P(clase | mensaje); columnas en el orden de `clases`.
    clases : lista o array con los nombres de las clases (incluye "fraude").

    Regla, en este orden de prioridad:
    1. Si P(fraude) >= umbral_fraude, el destino es "fraude" (aunque no sea la clase más probable).
    2. Si no, y la probabilidad máxima >= umbral_confianza, el destino es la clase más probable.
    3. En cualquier otro caso, el destino es REVISION ("revision_humana").

    Devuelve un array de n_mensajes strings.
    """
    proba = np.asarray(proba, dtype=float)
    clases = np.asarray(clases)
    if proba.ndim != 2 or clases.ndim != 1 or proba.shape[1] != len(clases):
        raise ValueError("Las columnas de proba deben coincidir con las clases.")
    posiciones_fraude = np.flatnonzero(clases == "fraude")
    if len(posiciones_fraude) != 1:
        raise ValueError("Debe haber una única clase fraude.")
    if not np.isfinite(proba).all() or ((proba < 0) | (proba > 1)).any():
        raise ValueError("Las probabilidades deben ser finitas y estar entre 0 y 1.")

    posible_fraude = proba[:, posiciones_fraude[0]] >= umbral_fraude
    confiables = (~posible_fraude) & (proba.max(axis=1) >= umbral_confianza)
    # object permite conservar revision_humana y nombres de clases de distinta longitud.
    destino = np.full(proba.shape[0], REVISION, dtype=object)
    destino[posible_fraude] = "fraude"
    destino[confiables] = clases[proba[confiables].argmax(axis=1)]
    return destino


def evaluar_derivacion(y_real, destino):
    """Calcula los indicadores del negocio. Devuelve un dict con tres claves:

    - "cobertura": proporción de mensajes derivados automáticamente (destino distinto de REVISION).
    - "exactitud_automatica": entre los derivados automáticamente, proporción con destino == y_real.
    - "fraude_perdido": entre los mensajes cuyo y_real es "fraude", proporción derivada automáticamente
      a un equipo que no es "fraude". Los enviados a revisión humana no cuentan como perdidos.

    Los tres valores son proporciones entre 0 y 1 (float).
    Si un indicador no tiene denominador, devuelve np.nan: no hay una proporción observada.
    """
    y_real = np.asarray(y_real)
    destino = np.asarray(destino)
    if y_real.ndim != 1 or destino.ndim != 1 or y_real.shape != destino.shape:
        raise ValueError("Debe haber un destino por cada etiqueta real.")
    automaticos = destino != REVISION
    fraudes = y_real == "fraude"
    perdidos = fraudes & automaticos & (destino != "fraude")
    return {
        "cobertura": float(automaticos.mean()) if len(destino) else float("nan"),
        "exactitud_automatica": float((destino[automaticos] == y_real[automaticos]).mean())
        if automaticos.any() else float("nan"),
        "fraude_perdido": float(perdidos.sum() / fraudes.sum()) if fraudes.any() else float("nan"),
    }
