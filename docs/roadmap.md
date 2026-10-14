# Roadmap del proyecto Cauce

## Introducción y problema

Cauce es un caso universitario de clasificación supervisada de texto. La empresa
del enunciado recibe unos 6.500 mensajes diarios; nueve personas los distribuyen
manualmente y los errores retrasan especialmente la atención de fraude.
El objetivo es predecir el equipo correcto a partir del mensaje y evaluar una
regla que combine derivación automática, prioridad de fraude y revisión humana.

La auditoría inicial encontró 8.200 históricos y 2.040 nuevos. La mesa de entrada
acierta 82,6098% en todos los históricos originales; 31,7287% de los fraudes se
derivan a otro equipo. Son referencias exploratorias, no resultados finales.

## Objetivos y alcance

Implementar Naive Bayes multinomial con NumPy, demostrar equivalencia con
`MultinomialNB`, compararlo con KNN y fundamentar una decisión de negocio.
La documentación debe permitir ejecutar, comprender y defender el trabajo.

Se desarrolla sólo `caso1_cauce/`. No se incluyen el caso Nodo, interfaces, APIs,
bases adicionales, Docker ni despliegue comercial. Se preservan los originales,
los tests docentes y las etiquetas reales. No se usarán metadatos como features.

## Tecnologías y entregables

Python 3.10+, JupyterLab, NumPy, pandas, SciPy para las matrices dispersas del
ecosistema, scikit-learn, Matplotlib y pytest, conforme a `requirements.txt`.
La matemática de Naive Bayes y la derivación usan NumPy; la limpieza, biblioteca
estándar. KNN usa scikit-learn. No hacen falta otras dependencias de aplicación.

Entregables finales: módulos `.py` completos, tests docentes aprobados, notebook
reproducible con los 20 pasos y siete reflexiones, CSV de 2.040 predicciones con
formato docente e informe ejecutivo PDF para Laura Benítez. Los datos y cualquier
salida sensible deben circular por un medio autorizado, sin publicarse en GitHub.

## Estrategia

Resolver las funciones según docstrings y tests, avanzar por dependencias y
registrar resultados reales. Primero se deduplica en una copia; después se
limpia y se separa 80/20 de forma estratificada con semilla 42. El vocabulario y
el IDF se ajustan dentro de cada partición de entrenamiento usando pipelines.
El 20% de prueba se reserva hasta el paso 15. Hiperparámetros y umbrales se eligen
con entrenamiento y validación cruzada, nunca mirando el resultado de prueba.

La matriz completa está en [requisitos](requisitos.md). Todos sus pasos están
pendientes de resolución en el notebook: la auditoría del Sprint 0 no los sustituye.

## Sprint 0 · Análisis, organización y planificación

**Objetivo:** dejar el proyecto preparado sin implementar algoritmos.

Actividades: inspeccionar Git y remoto; revisar ocho materiales; recuperar sólo
Cauce; auditar datasets y línea base; inventariar código, tests, 20 pasos y siete
preguntas; instalar dependencias y ejecutar pytest; documentar reglas y pendientes.
Archivos: README, AGENTS, `.gitignore`, `docs/`, scripts auxiliares y originales
docentes recuperados byte a byte.

Entregables: los cinco documentos obligatorios, análisis técnico complementario,
evidencia reproducible y commits en español. Finaliza con integridad verificada,
revisión del alcance, datos protegidos y resultado de publicación informado.
**Estado: completado; ver [seguimiento](seguimiento.md).**

## Sprint 1 · Exploración, limpieza y Naive Bayes desde cero

**Objetivo:** comprender los datos y terminar la implementación matemática.
**Pasos asignados: 1, 2, 3, 4, 5 y 6 (partes A, B e inicio de C).**

Actividades: reproducir y ampliar la exploración en el notebook, incluyendo
palabras por clase; documentar la línea base; deduplicar una copia conservando
el primero; completar limpieza y mostrar cinco ejemplos sin información personal;
crear `texto_limpio` y registrar los mensajes de menos de dos palabras; completar
`log_suma_exp`, la clase Naive Bayes y términos indicativos.

Archivos: `caso1_cauce/src/limpieza.py`, `src/naive_bayes.py`, notebook y seguimiento.
Entregables: pasos 1–6 explicados, funciones completas y evidencia de sus tests.
Finaliza cuando pasan los 15 casos de limpieza y los 12 de Naive Bayes, incluida
equivalencia numérica densa/dispersa, estabilidad y compatibilidad con pipelines.
Las cuatro pruebas de derivación pueden seguir fallando hasta el Sprint 3.
No se edita el contenido de los CSV ni los tests.

## Sprint 2 · Entrenamiento, optimización y comparación con KNN

**Objetivo:** producir dos modelos comparables sin consumir la evaluación final.
**Pasos asignados: 7, 8, 9, 10, 11 y 12 (resto de C y parte D).**

Actividades: separar 80/20 estratificado con semilla 42; verificar 100% de
coincidencia de predicciones con `MultinomialNB(alpha=1)`; interpretar diez términos
por clase; optimizar NB y KNN con cinco particiones estratificadas y `f1_macro`;
medir predicción de 1.000 mensajes usando 25%, 50%, 75% y 100% del entrenamiento.
El paso 8 verifica equivalencia, sin elegir configuraciones por el conjunto de prueba.
Para el paso 12 se propone un lote reservado dentro de entrenamiento, con el mismo
lote y condiciones para ambos algoritmos; el protocolo exacto debe quedar explícito.

Archivos: notebook, módulos si se corrigen problemas reales de implementación y
`docs/seguimiento.md`. Entregables: búsquedas, interpretaciones, gráfico y tabla de
tiempos reproducibles. Finaliza con pipelines sin fuga, grillas justificadas,
modelos seleccionados por validación y test final reservado.

## Sprint 3 · Derivación, evaluación final e informe

**Objetivo:** evaluar la decisión de negocio y entregar resultados verificables.
**Pasos asignados: 13, 14, 15, 16, 17, 18, 19 y 20 (partes E, F y G).**

Actividades: completar `derivar` y `evaluar_derivacion`; elegir umbrales con
probabilidades fuera de muestra del entrenamiento, respetando prioridades y
objetivos confirmados; evaluar una única vez en prueba; analizar diez errores;
proyectar el impacto en 6.500 mensajes; reentrenar y predecir los 2.040 nuevos;
responder las reflexiones con evidencia y escribir el informe ejecutivo.

Archivos: `src/derivacion.py`, notebook, `predicciones_caso1.csv`,
`informe_ejecutivo.pdf` y seguimiento. Finaliza con 31 tests aprobados, tabla de
aceptación con metas confirmadas, exportación validada y notebook reiniciado y
ejecutado completo. Si no se cumplen las metas, se informa sin alterar los criterios.

## Criterios de aceptación y decisiones pendientes

El notebook exige cinco indicadores en el paso 15. El módulo de derivación define
tres: cobertura, exactitud automática y fraude perdido. No hay una lista completa
de cinco ni valores objetivo verificables en los materiales disponibles. No se
asume que F1 macro y latencia sean los otros dos. Hace falta consultar el enunciado
completo o al docente antes de declarar aceptación y fijar umbrales definitivos.

Sí están especificados: tests obligatorios, semilla 42, división 80/20, equivalencia
100%, cinco folds con F1 macro, protocolo de tamaños del paso 12, diez términos,
diez errores y formato del CSV. Son exigencias verificables aunque falten metas
de negocio. Ver detalles y preguntas concretas en [requisitos](requisitos.md).

## Riesgos principales

| Riesgo | Tratamiento |
| --- | --- |
| Datos personales en un repositorio público | CSV sólo locales; recuperación por ZIP y hashes; revisar salidas antes de publicar. |
| Metas incompletas | Registrar faltantes; consultar antes de elegir umbrales finales o afirmar aceptación. |
| Duplicados o clientes compartidos entre conjuntos | Deduplicar según consigna antes del split; medir solapamientos y discutir el alcance de la generalización. |
| Fuga de etiquetas o vocabulario | Sólo texto como entrada, pipeline dentro de CV, test reservado. |
| Probabilidades y estabilidad numérica | Logaritmos, suavizado y pruebas; validar umbrales experimentalmente. |
| Costos de KNN y mediciones poco comparables | Mismo lote, equipo, tamaños y condiciones; registrar repeticiones como propuesta metodológica. |
| Datos vacíos o cortos en mensajes nuevos | Conservar las 2.040 filas; definir representación de probabilidades y revisión con el docente. |
| Deriva del lenguaje y clases desbalanceadas | Analizar métricas por clase y errores; tratar monitoreo sólo como discusión académica. |

## Definición de terminado

Cada sprint termina con criterios verificados, evidencia real, documentación
actualizada y un commit lógico en español. El proyecto termina con los 20 pasos,
siete reflexiones, tests intactos y aprobados, ejecución completa desde un entorno
documentado, resultados finales sin fuga, entregables en formato correcto y una
conclusión honesta sobre aceptación y límites. No alcanza con que el notebook
produzca predicciones: debe poder explicarse y reproducirse.
