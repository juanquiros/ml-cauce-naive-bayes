# Cauce · Clasificación de mensajes con Naive Bayes

Trabajo académico de Machine Learning del **Escenario 1: Cauce, una billetera
virtual**. Se evaluará la clasificación automática del texto de mensajes para
derivarlos al equipo correspondiente o a revisión humana, con prioridad para
los posibles fraudes. El contexto docente plantea 6.500 mensajes diarios y nueve
personas en la mesa de entrada.

El algoritmo principal será **Naive Bayes multinomial desde cero con NumPy**;
la comparación utilizará **KNN de scikit-learn**. La entrada será el texto y la
etiqueta correcta será `equipo_final`. Las clases reales son `cuenta_acceso`,
`fraude`, `prestamos_inversiones`, `tarjeta` y `transferencias`.

**Estado: Sprint 0 completado.** Se prepararon materiales, auditorías y
planificación. Los módulos siguen con sus `NotImplementedError`, el notebook
docente está sin resolver y los sprints 1 a 3 están pendientes. La aceptación
final requiere aclaraciones del docente registradas en [requisitos](docs/requisitos.md).
Cambios publicados para revisión en el [pull request del Sprint 0](https://github.com/juanquiros/ml-cauce-naive-bayes/pull/2).

## Estructura

```text
ml-cauce-naive-bayes/
├── AGENTS.md                       instrucciones permanentes
├── README.md
├── requirements.txt                original del docente
├── .gitignore
├── .gitattributes                  preserva bytes originales al clonar
├── caso1_cauce/
│   ├── datos/                      CSV originales, sólo en local
│   ├── src/                        limpieza.py, naive_bayes.py, derivacion.py
│   ├── tests/                      tres módulos docentes sin cambios
│   ├── conftest.py
│   └── caso1_cauce.ipynb            guía de 20 pasos sin resolver
├── scripts/
│   ├── preparar_datos.py           recupera CSV del ZIP sin sobrescribir
│   └── auditar_datos.py            auditoría de lectura y línea base manual
└── docs/
    ├── roadmap.md
    ├── conceptos.md
    ├── requisitos.md
    ├── seguimiento.md
    ├── diagnostico_inicial.md
    ├── analisis_codigo_y_pruebas.md
    └── evidencias/                 estadísticas, hashes, entorno y pytest
```

## Preparar el entorno

Python **3.10 o superior**. Se verificó Python 3.12.14 en Windows. Las dependencias
docentes son NumPy, pandas, SciPy, scikit-learn, Matplotlib, pytest y JupyterLab.
Los scripts de preparación y auditoría se ejecutan desde la raíz del repositorio.

PowerShell, sin necesidad de activar el entorno:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Si `py` no está disponible, usá la ruta de tu Python instalado en el primer
comando. El alias `python` de Microsoft Store no funcionó en esta sesión.
En Linux/macOS, usá `python3 -m venv .venv` y `.venv/bin/python`.

`requirements.txt` mantiene los mínimos originales. Las versiones exactas de la
sesión están en [entorno_sprint0.txt](docs/evidencias/entorno_sprint0.txt);
esa captura corresponde a Windows/Python 3.12, no es un lock universal.
En un entorno equivalente se puede instalar con
`python -m pip install -r docs/evidencias/entorno_sprint0.txt`.

## Recuperar los datos docentes

El repositorio GitHub es **público**. Los CSV contienen identificadores y posibles
datos personales en los mensajes, sin confirmación de que sean ficticios.
Permanecen intactos en local y excluidos del versionado. Cada estudiante necesita
acceso autorizado al ZIP entregado por el docente; no se ofrece descarga pública.

```powershell
.\.venv\Scripts\python.exe scripts\preparar_datos.py "C:\ruta\materiales_estudiantes.zip"
```

El script recupera únicamente los dos CSV de Cauce, verifica sus SHA-256 contra
el [manifiesto](docs/evidencias/integridad_materiales.json) y rechaza sobrescribir
un archivo distinto. No extrae el Escenario 2 ni anonimiza originales.

Auditoría inicial reproducible, sin entrenar ni modificar datos:

```powershell
.\.venv\Scripts\python.exe scripts\auditar_datos.py
```

Para guardar una nueva ejecución local, agregá
`--salida .local/auditoria_datos.json`. La evidencia del Sprint 0 ya está en
[auditoria_datos.json](docs/evidencias/auditoria_datos.json).

## Ejecutar las pruebas

Desde la raíz:

```powershell
.\.venv\Scripts\python.exe -m pytest -q caso1_cauce/tests
```

O desde `caso1_cauce/`:

```powershell
..\.venv\Scripts\python.exe -m pytest -q
```

Estado inicial real: **31 casos recolectados; 30 fallan por funciones pendientes
y 1 pasa**. Es el punto de partida de los materiales, no una implementación
terminada. No se modificaron los tests. Ver [registro](docs/evidencias/pytest_inicial.txt).

## Abrir el notebook

Las rutas del notebook son relativas a la carpeta del caso:

```powershell
Set-Location caso1_cauce
..\.venv\Scripts\python.exe -m jupyterlab caso1_cauce.ipynb
```

Seleccioná el kernel del entorno `.venv`. Las funciones se completarán en los
archivos `.py` cuando se autorice el sprint correspondiente. Antes de la entrega
final se deberá reiniciar y ejecutar todo el notebook.

## Documentación

- [Roadmap y definición de terminado](docs/roadmap.md).
- [Conceptos para estudiar y defender el proyecto](docs/conceptos.md).
- [Matriz de los 20 pasos, preguntas y criterios pendientes](docs/requisitos.md).
- [Seguimiento y decisiones](docs/seguimiento.md).
- [Diagnóstico, materiales, datos y riesgos](docs/diagnostico_inicial.md).
- [Contratos del código e inventario de pruebas](docs/analisis_codigo_y_pruebas.md).
- [Reglas permanentes de trabajo](AGENTS.md).

No se construirá una billetera virtual ni una plataforma comercial. Los próximos
entregables son el notebook resuelto, los módulos implementados, la comparación
experimental, `predicciones_caso1.csv` e `informe_ejecutivo.pdf`; todavía no existen
como resultados del proyecto.
