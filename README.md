# Cauce - Clasificación de mensajes

## Integrantes

- Andruszyszyn Emanuel
- Quirós Juan

## Descripción

Cauce es una billetera virtual que recibe unos 6.500 mensajes diarios. Nueve personas los leen y los derivan a distintos equipos. Los errores de derivación demoran la atención, especialmente cuando hay sospechas de fraude.

## Objetivo

Predecir `equipo_final` a partir del texto del mensaje. La decisión de derivación dará prioridad a fraude, enviará automáticamente los casos con suficiente confianza y dejará los casos dudosos para revisión humana.

## Algoritmos

Implementamos Naive Bayes multinomial desde cero con NumPy y comprobamos que sus predicciones coinciden con `MultinomialNB` de scikit-learn. Lo comparamos con KNN usando TF-IDF y distancia coseno, con ajuste de parámetros mediante validación cruzada.

Los 20 pasos y las siete preguntas de reflexión están completos. La revisión recomienda provisionalmente **Naive Bayes**, bajo el supuesto de reducir errores generales y carga operativa. En los 6.344 mensajes OOF, produjo 356 errores automáticos, 88 falsas alertas y 33 revisiones; KNN produjo 493, 340 y 201. KNN perdió menos fraudes: 27 frente a 49. Si minimizar ese riesgo es la prioridad dominante, se favorece KNN; para equilibrar costos y capacidad, Cauce debe confirmar sus prioridades.

Sobre los mismos 1.586 mensajes de prueba, Naive Bayes obtuvo 93,88% de accuracy, F1 macro de 0,9346, 99,50% de cobertura y 94,17% de exactitud automática. Perdió 9 de 176 fraudes (5,11%); KNN perdió 6 (3,41%) y la mesa 59 (33,52%). A cambio de tres fraudes menos, KNN generó 59 alertas falsas, 20 errores automáticos y 53 revisiones adicionales. Naive Bayes también predijo más rápido. No se inventaron costos monetarios ni se sumaron errores que ya integran el total.

Conservamos los hiperparámetros del Sprint 2 y los umbrales provisionales de ambos modelos: fraude `0.10` y confianza `0.60`, elegidos con OOF en el Sprint 3. En ese sprint se consultó prueba para elegir KNN; esta revisión reconoce ese antecedente y usa OOF para revisar la política operativa. OOF reutiliza datos de selección y puede resultar optimista. La confirmación independiente requiere nuevos datos etiquetados; faltan las metas oficiales, el riesgo tolerable y la capacidad de atención.

## Datos

`mensajes_historicos.csv` contiene 8.200 mensajes con su derivación original y su equipo final. `mensajes_nuevos.csv` contiene 2.040 mensajes sin etiqueta para clasificar al final del trabajo.

Los CSV se conservan localmente y están excluidos de Git. Para preparar otra copia del repositorio, extraé únicamente `materiales_estudiantes/caso1_cauce/datos/` del ZIP docente en `caso1_cauce/datos/`. No hace falta modificar los archivos.

El detalle de los datos y de la línea base está en [la descripción del caso](docs/descripcion.md).

## Tecnologías

Python 3.10 o posterior; NumPy, pandas, SciPy, scikit-learn, matplotlib, pytest, JupyterLab y ReportLab para el informe PDF. SciPy se necesita para las matrices dispersas y las pruebas; los cálculos del clasificador propio y de derivación usan sólo NumPy.

## Ejecución

Desde la raíz del repositorio, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Set-Location caso1_cauce
..\.venv\Scripts\python.exe -m jupyterlab caso1_cauce.ipynb
```

En otra terminal, desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m pytest -q caso1_cauce/tests --tb=no -rf
```

En Linux o macOS, usá `.venv/bin/python` en lugar de `.venv\Scripts\python.exe`. Abrí JupyterLab desde `caso1_cauce/` para que funcionen las rutas relativas del notebook.

Reiniciá el kernel y ejecutá todo el notebook. La revisión conserva el código y las tablas registradas de las búsquedas del Sprint 2; con `REPRODUCIR_BUSQUEDAS=False` ajusta las configuraciones congeladas y evita repetirlas. OOF usa las mismas cinco particiones estratificadas y semilla 42; no se buscan umbrales nuevos. Los tiempos se calculan con tres repeticiones y pueden variar según el equipo y la carga. Miden predicción de pipelines, no atención al cliente ni un servicio en producción.

Las 31 pruebas originales aprueban: 15 de limpieza, 12 de Naive Bayes y cuatro de derivación.

## Entregables

- [Notebook completo](caso1_cauce/caso1_cauce.ipynb), con resultados y reflexiones.
- [Informe ejecutivo para Laura Benítez](caso1_cauce/informe_ejecutivo.pdf), con información agregada.
- `caso1_cauce/predicciones_caso1.csv`: archivo local verificado de Naive Bayes, con 2.040 filas y las cinco columnas exigidas. Conserva orden e identificadores y se entrega por separado. Hay 2.007 destinos automáticos y 33 revisiones, incluidas 15 por textos cortos. Antes de regenerarlo se conservó un respaldo del CSV anterior de KNN fuera del repositorio público.

## Estructura

```text
README.md
requirements.txt
.gitignore
caso1_cauce/
  datos/                 CSV locales
  src/                   limpieza.py, naive_bayes.py, derivacion.py
  tests/                 pruebas del docente
  conftest.py
  caso1_cauce.ipynb       consignas y actividades
docs/
  descripcion.md         problema, datos y línea base
  conceptos.md           guía de estudio
  plan.md                etapas y pasos del notebook
```

Para continuar, seguí [el plan](docs/plan.md) y consultá [los conceptos](docs/conceptos.md).

## Versiones utilizadas

- Python: `3.12.14 (main, Aug 25 2026, 14:01:42) [MSC v.1944 64 bit (AMD64)]`, obtenido con `sys.version`.
- scikit-learn: `1.9.1`, obtenido con `sklearn.__version__`.
- NumPy: `2.5.4`; pandas: `3.0.6`.

Son las versiones reales de la ejecución completa final. `requirements.txt` establece versiones mínimas; instalarlo en otro entorno puede resolver versiones distintas.
