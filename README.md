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

Los 20 pasos y las siete preguntas de reflexión están completos. Elegimos KNN para el ejercicio porque perdió menos fraudes al aplicar la regla de derivación, aunque Naive Bayes tuvo mejores métricas generales y predijo más rápido.

Sobre 1.586 mensajes de prueba, KNN obtuvo 92,81% de accuracy y F1 macro de 0,9260. La regla cubrió 96,15% de los mensajes con 92,66% de exactitud automática y 3,41% de fraude perdido; la mesa perdió 33,52% del fraude sobre los mismos registros.

Los umbrales provisionales son fraude `0.10` y confianza `0.60`, elegidos con probabilidades OOF antes de evaluar prueba. Los criterios oficiales de aceptación siguen pendientes de confirmación.

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

Reiniciá el kernel y ejecutá todo el notebook. Las búsquedas usan cinco particiones estratificadas y semilla 42; la selección OOF de umbrales precede a la evaluación final. Los tiempos se calculan con tres repeticiones y pueden variar según el equipo y la carga de ejecución.

Las 31 pruebas originales aprueban: 15 de limpieza, 12 de Naive Bayes y cuatro de derivación.

## Entregables

- [Notebook completo](caso1_cauce/caso1_cauce.ipynb), con resultados y reflexiones.
- [Informe ejecutivo para Laura Benítez](caso1_cauce/informe_ejecutivo.pdf), con información agregada.
- `caso1_cauce/predicciones_caso1.csv`: 2.040 filas con las cinco columnas exigidas. Se genera al ejecutar el notebook y se entrega localmente porque contiene identificadores. Hay 1.957 destinos automáticos y 83 revisiones, incluidas 15 por textos cortos.

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
