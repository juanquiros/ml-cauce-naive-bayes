# Diagnóstico inicial de Cauce

Fecha de auditoría: **14/10/2026**, zona del usuario America/Argentina/Buenos_Aires.
El Sprint 0 prepara un trabajo académico de clasificación de mensajes; no entrena
modelos, no resuelve el notebook y no completa funciones pendientes.

## Materiales encontrados

Los ocho materiales solicitados existen en la carpeta Downloads del usuario.
Sus hashes SHA-256 están en [integridad_materiales.json](evidencias/integridad_materiales.json).
Los nombres se conservan según los archivos reales, incluido el acento Unicode
del notebook de KNN. No se descargaron materiales docentes externos.

| Material | Inspección y aporte | Tratamiento |
| --- | --- | --- |
| `materiales_estudiantes.zip` | Contenido completo inventariado; README general, requisitos y Cauce leídos. Incluye también Nodo. | Sólo se recuperaron los once archivos de Cauce y requirements original. Nodo no se incorporó. |
| `explicacion_escenarios.docx` | Párrafos/tablas: contexto Cauce, 6.500 mensajes, nueve personas, problemas de fraude y comparación NB/KNN. | Referencia local; no se importa el segundo escenario. |
| `Guia_Naive_Bayes_Sesion4.docx` | Lectura de guía y tablas: Bayes, supuestos, suavizado, logs, variantes y ejemplos. | Apoyo de estudio; sus ejercicios adicionales no amplían el alcance. |
| `naive_bayes_desde_cero.py` | Código completo de NB categórico/gaussiano con Python estándar. | Se leyó sin ejecutar ni copiar como implementación de Cauce, que requiere multinomial/NumPy. |
| `NB.pdf` | Ocho páginas escaneadas, sin texto extraíble; renderizadas e inspeccionadas visualmente. Capítulo 6, pp. impresas 177–184: NB, estimación y texto. | Referencia conceptual, sin consignas de aceptación específicas de Cauce. |
| `knn.pdf` | Siete páginas escaneadas, inspección visual completa. Capítulo 8, pp. 230–236: aprendizaje por instancias, KNN, distancias, ponderación y costos. | Referencia conceptual; no exige programar KNN desde cero en Cauce. |
| `ML_Clase_05_1_K_Vecinos_Más_Cercanos.ipynb` | Todas las celdas de código/Markdown: Iris, escalado, KNN, evaluación, búsqueda de k y fronteras. | No se ejecutó ni se agregó Seaborn: es material complementario. |
| `M301_K-Vecinos_mas_Cercanos_sin.pdf` | Nueve páginas: vecinos, k, escalas, distancias, ventajas/desventajas. Texto extraído y páginas inspeccionadas. | Contexto de estudio, sin parámetros de negocio de Cauce. |

**No faltan los ocho archivos mencionados ni los archivos esperados de Cauce.**
Falta información de criterios/rúbrica, no un archivo que pueda recuperarse del
ZIP disponible. Los originales de consulta siguen en Downloads; no se publican
copias de PDFs/DOCX ni el ZIP. Los temporales de lectura/render están en `.local/`,
excluidos de Git. No se modificó ningún adjunto.

## Estado inicial del repositorio y organización

Carpeta de trabajo: `ml-cauce-naive-bayes`. Al inicio sólo existía `.git/`;
`git status --short` no mostraba cambios, la rama era `master`, no había commits
y no había remotos. `git log -5 --oneline` informó que aún no existían commits.
No había instrucciones AGENTS previas aplicables en las carpetas ascendentes
revisadas ni archivos del proyecto que preservar fuera de Git.

Se configuró `origin` con
`https://github.com/juanquiros/ml-cauce-naive-bayes.git` y se creó
`sprint-0`. `git ls-remote` al URL indicado finalizó correctamente y no
devolvió refs: remoto vacío. El conector GitHub confirmó repo **público**, tamaño
0, rama predeterminada `main` y permisos de push. GitHub CLI (`gh`) no está
instalado; Git sí funciona. El resultado final de commits/publicación se registra
en [seguimiento](seguimiento.md), separado de esta fotografía inicial.

Estructura preparada: `caso1_cauce/` original, `requirements.txt`, README,
`.gitignore`, AGENTS, cinco documentos obligatorios, análisis técnico adicional,
evidencias y dos scripts auxiliares. Ver árbol en README. Los dos CSV permanecen
en `caso1_cauce/datos/` local, ignorados por Git. No existe `caso2_nodo/` en el proyecto.
Se agregó `.gitattributes` porque `core.autocrlf=true` podría cambiar los saltos
de línea al clonar: los archivos docentes se preservan sin conversión de texto.

## Entorno Python y dependencias

La instalación del usuario incluye Python 3.14.7, inicialmente sin dependencias
del proyecto; el alias `python` de Microsoft Store no fue consistente/usable.
Se creó `.venv` con el Python **3.12.14** del runtime disponible y se instalaron
los requisitos originales. No se cambió el Python global ni el requirements docente.

| Dependencia | Mínimo docente | Versión instalada verificada |
| --- | --- | --- |
| NumPy | 1.26 | 2.5.4 |
| pandas | 2.1 | 3.0.6 |
| SciPy | 1.11 | 1.18.1 |
| scikit-learn | 1.4 | 1.9.1 |
| Matplotlib | 3.8 | 3.11.2 |
| pytest | 8.0 | 9.1.1 |
| JupyterLab | 4.0 | 4.6.4 |

La creación del entorno se realizó con la ruta absoluta del intérprete Python
3.12.14 disponible. El primer comando siguiente es su equivalente con el launcher
de Python; los demás corresponden a la instalación y auditoría ejecutadas.
Se ejecutan desde la raíz salvo pytest:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pip freeze
.\.venv\Scripts\python.exe scripts\auditar_datos.py --salida docs\evidencias\auditoria_datos.json
.\.venv\Scripts\python.exe scripts\preparar_datos.py 'C:\Users\quiro\Downloads\materiales_estudiantes.zip'
```

`pip check`: **No broken requirements found.** Versiones completas en
[entorno_sprint0.txt](evidencias/entorno_sprint0.txt). La instalación descargó
dependencias Python necesarias; no se incorporaron nuevos datasets ni tutoriales.
JupyterLab quedó instalado, pero no se inició una sesión interactiva ni se ejecutó
el notebook completo, ya que contiene funciones pendientes.

Desde `caso1_cauce/` se ejecutó:

```powershell
..\.venv\Scripts\python.exe -m pytest -q --tb=no -rf
```

**Resultado: 31 casos, 30 fallidos y 1 aprobado, 9,75 s, salida 1.** Los fallidos
llegan a `NotImplementedError` originales; pasa la prueba estática que prohíbe
importar SciPy en NB. No hubo errores de importación o recolección. Es un estado
de partida esperado, no un defecto de un clasificador terminado. El registro
está en [pytest_inicial.txt](evidencias/pytest_inicial.txt) y el inventario completo
en [análisis de código y pruebas](analisis_codigo_y_pruebas.md).

## Auditoría de datasets, sin modificarlos

Se usó `pandas.read_csv` con UTF-8 y tipos inferidos. Con pandas 3.0.6 las columnas
se reportan como `str`; otras versiones pueden mostrarlas como `object`.
`fecha_hora` se carga inicialmente como texto y se parseó sólo en una serie
auxiliar para verificar fechas, sin cambiar el CSV ni las columnas originales.

| Característica | Históricos | Nuevos |
| --- | ---: | ---: |
| Registros | 8.200 | 2.040 |
| Columnas | 7 | 5 |
| Nulos en `texto` | 11 | 3 |
| Textos sin caracteres luego de strip, incluyendo nulos | 18 | 4 |
| Textos no nulos sólo con espacios | 7 | 1 |
| Duplicados de fila completa | 0 | 0 |
| Duplicados excedentes por `id_cliente,texto`, conservar primero | 200 | 40 |
| Grupos repetidos por esa clave | 200 | 40 |
| Duplicados excedentes de texto sin distinguir cliente | 270 | 49 |
| IDs de mensaje repetidos | 0 | 0 |
| Clientes distintos | 7.969 | 1.998 |
| Fechas inválidas al parsear | 0 | 0 |

Columnas comunes: `id_mensaje`, `fecha_hora`, `id_cliente`, `canal`, `texto`.
Sólo históricos: `equipo_derivado`, `equipo_final`. Todos los campos excepto
`texto` tienen cero nulos en ambos datasets. Históricos: del 01/06/2026 al
31/08/2026; nuevos: del 21/09/2026 al 27/09/2026. Hay 13 clientes y 16 textos no
vacíos compartidos entre ambos archivos, sin IDs de mensaje compartidos.
La repetición textual puede aparecer entre clientes; no autoriza cambiar la
clave de deduplicación docente. No hay grupos duplicados históricos con etiquetas
finales contradictorias. No se eliminaron registros durante esta auditoría.

### Objetivo y clases reales

`equipo_derivado` es el equipo asignado originalmente por la mesa de entrada.
`equipo_final` es el equipo correcto después de la resolución/revisión histórica.
La variable objetivo debe ser **equipo_final**. Usar la primera como feature
introduciría información del proceso que se busca sustituir y condicionaría la
comparación con la mesa. Los IDs, fecha y canal se conservan para auditoría y
trazabilidad, sin incorporarlos al modelo textual.

| Clase final | Registros | Porcentaje | Equipo derivado originalmente: registros |
| --- | ---: | ---: | ---: |
| transferencias | 2.552 | 31,1220% | 2.619 |
| tarjeta | 2.057 | 25,0854% | 2.110 |
| cuenta_acceso | 1.648 | 20,0976% | 1.614 |
| prestamos_inversiones | 1.029 | 12,5488% | 977 |
| fraude | 914 | 11,1463% | 880 |

Los nombres coloquiales «cuentas» y «préstamos» del DOCX contextual no sustituyen
las etiquetas `cuenta_acceso` y `prestamos_inversiones` del dataset.

| Canal | Históricos | Nuevos |
| --- | ---: | ---: |
| app_chat | 3.676 | 927 |
| whatsapp | 2.499 | 591 |
| email | 1.163 | 310 |
| formulario_web | 862 | 212 |

Cantidad de palabras del texto original: se separó por whitespace, contando nulos
como longitud cero. No es limpieza ni identifica todavía todos los textos que
quedarán cortos después de normalizar.

| Clase | Media | Mediana | Mínimo | Máximo |
| --- | ---: | ---: | ---: | ---: |
| cuenta_acceso | 13,87 | 13 | 0 | 46 |
| fraude | 18,22 | 17 | 0 | 50 |
| prestamos_inversiones | 12,58 | 12 | 0 | 33 |
| tarjeta | 14,81 | 14 | 0 | 42 |
| transferencias | 16,95 | 17 | 0 | 41 |

El conteo del paso 5 se resolverá en S1 con `texto_limpio`, no con estas longitudes.

## Línea base exploratoria de la mesa de entrada

Población: **todas las 8.200 filas originales**, antes de deduplicar, limpiar o
separar. Ver [JSON agregado](evidencias/auditoria_datos.json) para valores completos.

| Medida | Resultado |
| --- | ---: |
| Aciertos manuales | 6.774 |
| Errores manuales | 1.426 |
| Exactitud | 0,8260975609756097 (82,6098%) |
| F1 macro | 0,8165552063793191 |
| Fraudes reales | 914 |
| Fraudes enviados a otro equipo | 290 |
| Fraude derivado a otro equipo / fraude real | 0,3172866520787746 (31,7287%) |

Entre los 290 fraudes mal derivados: 52 fueron a cuenta_acceso, 153 a tarjeta y
85 a transferencias. Se acertaron 624 fraudes. El denominador del porcentaje de
fraude es 914, no 8.200. El error global es 17,3902%, cercano al «uno de cada seis»
del relato, sin exigir que esa aproximación coincida exactamente.

Matriz normalizada por fila, porcentajes; filas = equipo final y columnas =
derivación manual. Orden abreviado: CA cuenta_acceso, F fraude, PI prestamos_inversiones,
T tarjeta, TR transferencias. Cada fila suma aproximadamente 100% por redondeo.

| Real / manual | CA | F | PI | T | TR |
| --- | ---: | ---: | ---: | ---: | ---: |
| CA | 81,74 | 5,58 | 0,00 | 5,89 | 6,80 |
| F | 5,69 | 68,27 | 0,00 | 16,74 | 9,30 |
| PI | 2,24 | 0,00 | 86,49 | 2,43 | 8,84 |
| T | 5,59 | 3,89 | 0,00 | 83,71 | 6,81 |
| TR | 3,02 | 3,29 | 3,41 | 4,43 | 85,85 |

Estos resultados no comparan modelos ni equivalen al paso 15. En S3 la mesa
debe medirse sobre la misma población de prueba que NB y KNN. Si se interpreta
su destino registrado como una decisión sin abstención, su cobertura es 100%;
eso describe el registro, no ausencia de trabajo humano ni un objetivo docente.

## Privacidad, calidad y fuga

GitHub es público. Los CSV contienen una columna `id_cliente` y texto libre.
La búsqueda de alertas contó 609 históricos y 148 nuevos con secuencias de seis
o más dígitos; hay 217/48 menciones de DNI, 772/184 de teléfono o celular y 113/25
de CBU/CVU/alias. Son alertas que pueden incluir montos u otros números, no una
verificación de identidad real. No se encontraron correos o URL con los patrones
básicos usados; eso no descarta otros datos personales. No consta que los datos
sean ficticios o que esté autorizada su publicación pública.

Decisión: **suspender la publicación de ambos CSV**, conservarlos intactos en
local, ignorarlos con rutas específicas y ofrecer recuperación verificable desde
el ZIP docente. No se borraron ni anonimizaron originales. El manifiesto conserva
hashes, no identificadores. La documentación usa agregados, sin mensajes sensibles.
El notebook original no tiene salidas guardadas. La privacidad debe revisarse
también en futuros ejemplos, errores, CSV de predicciones y PDF.

Otros riesgos: desbalance de clases; vacíos y textos que quedarán cortos; duplicados
que inflen resultados; clientes/textos compartidos; vocabulario o IDF ajustado
fuera del fold; umbrales ajustados mirando prueba; probabilidades extremas y
crecimiento de costo KNN. El split estratificado docente no garantiza separación
por cliente ni temporal: se debe explicar ese límite, sin reemplazar la consigna.

## Requisitos ambiguos y próximos pasos

No se hallaron la lista completa de cinco indicadores de aceptación ni sus metas
numéricas. Se verificaron tres definiciones en `evaluar_derivacion`; los otros dos
y todas las metas quedan pendientes. Tampoco se especifican las grillas, el margen
de seguridad, ciertos denominadores cero, el detalle del informe ni qué valores
exportar como probabilidades de mensajes nuevos sin texto suficiente.
Las consultas concretas y su etapa están en [requisitos](requisitos.md).

Para iniciar S1: leer reglas, verificar integridad local, reproducir exploración
y línea base en el notebook, deduplicar una copia y completar limpieza y NB según
tests. Solicitar criterios completos con anticipación. No seleccionar todavía
umbrales ni comenzar S1 como parte de esta entrega.
