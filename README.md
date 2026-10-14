# Cauce - Clasificación de mensajes

## Descripción

Cauce es una billetera virtual que recibe unos 6.500 mensajes diarios. Nueve personas los leen y los derivan a distintos equipos. Los errores de derivación demoran la atención, especialmente cuando hay sospechas de fraude.

## Objetivo

Predecir `equipo_final` a partir del texto del mensaje. La decisión de derivación dará prioridad a fraude, enviará automáticamente los casos con suficiente confianza y dejará los casos dudosos para revisión humana.

## Algoritmos

Vamos a implementar Naive Bayes multinomial desde cero con NumPy y comprobar sus resultados contra `MultinomialNB` de scikit-learn. Después lo compararemos con KNN usando TF-IDF y distancia coseno.

Por ahora están preparados los materiales y el análisis inicial. Las funciones del docente y las actividades del notebook siguen pendientes.

## Datos

`mensajes_historicos.csv` contiene 8.200 mensajes con su derivación original y su equipo final. `mensajes_nuevos.csv` contiene 2.040 mensajes sin etiqueta para clasificar al final del trabajo.

Los CSV se conservan localmente y están excluidos de Git. Para preparar otra copia del repositorio, extraé únicamente `materiales_estudiantes/caso1_cauce/datos/` del ZIP docente en `caso1_cauce/datos/`. No hace falta modificar los archivos.

El detalle de los datos y de la línea base está en [la descripción del caso](docs/descripcion.md).

## Tecnologías

Python 3.10 o posterior; NumPy, pandas, SciPy, scikit-learn, matplotlib, pytest y JupyterLab. SciPy se necesita para las matrices dispersas y las pruebas; los cálculos del clasificador propio usarán sólo NumPy.

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

Las pruebas de las funciones pendientes van a fallar con `NotImplementedError` hasta que se complete su implementación.

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
