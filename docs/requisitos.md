# Requisitos y trazabilidad del Escenario 1

## Fuentes y estado

Fuente principal: `caso1_cauce/caso1_cauce.ipynb` original del ZIP. Los números de
celda siguientes empiezan en **0** y permiten ubicar cada consigna sin depender
de números de ejecución. Complementan los contratos de `src/`, los tests,
`explicacion_escenarios.docx` y el README docente del ZIP. Los materiales de teoría
aportan conceptos; sus ejercicios de Iris, préstamos y spam no son entregables de Cauce.

Estado al cierre del Sprint 0: todos los pasos están **pendientes en el notebook**.
Los pasos 1 y 2 cuentan con una auditoría preliminar separada, sin completar celdas.
La asignación de sprints y los criterios operativos de verificación son planificación
del proyecto; las cantidades y condiciones docentes se identifican explícitamente.

## Matriz de los veinte pasos

Abreviaturas de archivos: **NBK** = `caso1_cauce/caso1_cauce.ipynb`;
**DAT** = `caso1_cauce/datos/`; **SRC** = `caso1_cauce/src/`;
**TST** = `caso1_cauce/tests/`. S1, S2 y S3 indican los sprints futuros.

| Paso / parte / celda | Requerimiento | Objetivo | Archivo involucrado | Entregable esperado | Dependencias | Sprint | Criterio de verificación | Estado inicial |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 / A / 5 | Cargar históricos; filas, nulos, vacíos, duplicados por cliente y texto, clases, canales y palabras por clase. | Conocer composición y calidad. | NBK, DAT/mensajes_historicos.csv | Tablas y explicación de hallazgos. | CSV recuperado y pandas. | S1 | Conteos reproducibles; definir nulos y vacíos; contar palabras por clase. | Pendiente; auditoría preliminar disponible. |
| 2 / A / 7 | Comparar `equipo_derivado` con `equipo_final`: exactitud, F1 macro, matriz normalizada por fila y % de fraude a otro equipo. | Medir el proceso manual. | NBK, DAT/históricos | Línea base e interpretación. | 1. | S1 | Cuatro salidas exigidas; orden de clases y denominador de fraude explícitos. | Pendiente; cálculo exploratorio disponible. |
| 3 / A / 9 | Eliminar duplicados conservando el primero y explicar por qué antes del split. | Evitar repetición de casos entre conjuntos. | NBK | Copia deduplicada y justificación. | 1–2. | S1 | Ningún duplicado por `id_cliente,texto` en la copia; original intacto. | Pendiente. |
| 4 / B / 12 | Implementar `quitar_tildes` y `limpiar_texto`; mostrar cinco ejemplos originales y limpios. | Normalizar la entrada. | SRC/limpieza.py, TST/test_limpieza.py, NBK | Funciones y cinco ejemplos seguros. | 3 y contratos docentes. | S1 | 15 casos de limpieza aprobados; orden y tokens exactos. | Pendiente; dos funciones con excepción. |
| 5 / B / 14 | Crear `texto_limpio`; excluir del training textos de menos de dos palabras y enviarlos a revisión. | Tratar mensajes sin información suficiente. | NBK | Conteo, caracterización y máscara de revisión. | 4. | S1 | Separación rastreable sin borrar originales; explicación del contenido sin datos sensibles. | Pendiente; no se ejecutó limpieza. |
| 6 / C / 17 | Implementar `log_suma_exp`, `NaiveBayesMultinomial` y `terminos_mas_indicativos`. | Construir el algoritmo principal. | SRC/naive_bayes.py, TST/test_naive_bayes.py, NBK | Módulo completo y registro de pruebas. | 4–5; NumPy y contratos. | S1 | 12 casos NB aprobados; cálculo sólo NumPy, sin delegar NB. | Pendiente. |
| 7 / C / 19 | Dividir 80/20, estratificado por `equipo_final`, `random_state=42`. | Reservar prueba final. | NBK | Particiones con índices y distribución. | 3–5. | S2 | Tamaños según población elegible; semilla y estratificación verificadas. | Pendiente. |
| 8 / C / 21 | `CountVectorizer` + clase propia y `MultinomialNB`, ambos con `alpha=1`; igualdad en 100% de prueba. | Verificar equivalencia. | NBK, SRC/naive_bayes.py | Comparación de predicciones. | 6–7. | S2 | Mismos datos y vocabulario; todas las etiquetas coinciden; no ajustar por prueba. | Pendiente. |
| 9 / C / 23 | Mostrar e interpretar los diez términos más indicativos de cada clase. | Explicar señales del clasificador. | NBK, función de términos | Tabla de 5 × 10 términos e interpretación. | 6–8. | S2 | Puntaje relativo definido en docstring; vocabulario alineado. | Pendiente. |
| 10 / D / 26 | GridSearchCV de CountVectorizer + NB, cinco folds estratificados, `f1_macro`; conclusión de cada hiperparámetro. | Optimizar sin fuga. | NBK | Grilla, resultados y conclusiones. | 6–8; entrenamiento solamente. | S2 | Pipeline ajustado dentro de cada fold; cinco particiones y scoring indicados. | Pendiente; grilla concreta no especificada. |
| 11 / D / 28 | Misma búsqueda con TF-IDF + KNN, `metric="cosine"`, `algorithm="brute"`; justificar coseno. | Comparar otra estrategia. | NBK | Búsqueda y comparación de validación. | 7 y protocolo de 10. | S2 | Mismos folds/población; KNN de scikit-learn; justificar cada hiperparámetro. | Pendiente. |
| 12 / D / 30 | Medir predicción de 1.000 mensajes con 25%, 50%, 75% y 100% del training en ambos modelos; gráfico y explicación. | Comparar costo con tamaño. | NBK | Tiempos y gráfico. | 10–11. | S2 | Lote de 1.000, tamaños y hardware explícitos; condiciones comparables; sin selección por test. | Pendiente; repeticiones y lote por definir. |
| 13 / E / 33 | Implementar `derivar` y `evaluar_derivacion`. | Traducir probabilidades a destinos e indicadores. | SRC/derivacion.py, TST/test_derivacion.py, NBK | Funciones completas. | Contratos; 6 para uso posterior. | S3 | Cuatro casos de derivación aprobados, prioridad y `>=` respetados. | Pendiente. |
| 14 / E / 35 | Usar `cross_val_predict` fuera de muestra; elegir dos umbrales con margen para NB y KNN. | Elegir una regla sustentada. | NBK | Probabilidades OOF y umbrales justificados por modelo. | 10–11, 13 y metas confirmadas. | S3 | Cada fila OOF proviene de un modelo que no la entrenó; test reservado; margen explicado. | Pendiente; metas ausentes. |
| 15 / E / 37 | Evaluación única en prueba; tabla de cinco indicadores para NB, KNN y mesa; reporte y matriz del elegido. | Decidir con evidencia comparable. | NBK | Tabla de aceptación, reporte y matriz. | 7, 10–14 y definición de indicadores. | S3 | Mismo test y denominadores; evaluación única; cinco indicadores/metas confirmados. | Pendiente; definición completa ausente. |
| 16 / E / 39 | Analizar diez errores de derivación automática, causa y mejora concreta de cada uno. | Entender límites. | NBK | Diez análisis individuales. | 15. | S3 | Distinguir predicción y destino; no exponer mensajes sensibles; si no hay diez errores, informar y consultar. | Pendiente. |
| 17 / E / 41 | Estimar impacto en un día de 6.500 mensajes. | Comunicar carga y riesgo. | NBK | Proyección de cantidades y supuestos. | 15. | S3 | Proporciones convertidas con denominador correcto; distinguir proyección de medición real. | Pendiente. |
| 18 / F / 44 | Reentrenar elegido con todos los históricos limpios y derivar mensajes nuevos. | Usar el resultado seleccionado. | NBK, ambos CSV | Predicciones y destinos de nuevos. | 14–17; decisión cerrada. | S3 | Sólo después de la evaluación; excluir cortos del training; preservar todas las filas nuevas. | Pendiente. |
| 19 / F / 46 | Exportar `predicciones_caso1.csv`: 2.040 filas y cinco columnas docentes. | Entregar salida consumible. | NBK, caso1_cauce/predicciones_caso1.csv | CSV validado. | 18. | S3 | Columnas exactas: `id_mensaje`, `equipo_predicho`, `prob_max`, `prob_fraude`, `derivacion`; 2.040 IDs correctos. | Pendiente. |
| 20 / G / 48 | Informe aparte para Laura Benítez, `informe_ejecutivo.pdf`. | Comunicar decisión de negocio. | NBK como respaldo, informe_ejecutivo.pdf | PDF ejecutivo separado. | 15–19 y reflexiones. | S3 | Argumentos basados en resultados; destinataria y nombre correctos; detalle de extensión/rúbrica pendiente. | Pendiente. |

## Siete preguntas de reflexión, sin responder

Se conservan las preguntas del notebook. Las evidencias indicadas son propuestas
para fundamentarlas, no respuestas ni experimentos ya realizados. Cada respuesta
final debe ocupar un párrafo apoyado en los resultados.

| N.º / celda | Pregunta docente | Preparación / respuesta | Evidencia necesaria |
| --- | --- | --- | --- |
| 1 / 50 | Naive Bayes supone que las palabras son independientes dada la clase. ¿Por qué clasifica bien igual? ¿Qué consecuencia tiene esa suposición sobre las probabilidades? | Preparar en S1–S2; responder en S3. | Métricas NB, errores y distribución de probabilidades/confianza observada. |
| 2 / 51 | ¿Qué pasaría con `alpha=0` si aparece una palabra que nunca se vio en la clase `fraude`? | Preparar en S1; responder en S3. | Ejemplo controlado de conteos y log-probabilidades, comparación con suavizado. |
| 3 / 52 | ¿Por qué `equipo_derivado` no puede usarse como variable del modelo? | Preparar en S1; responder en S3. | Esquema de datos y momento en que se conoce cada campo; features efectivamente usados. |
| 4 / 53 | ¿Qué costo tendría KNN en producción comparado con Naive Bayes? ¿En qué situación elegirían KNN igual? | Preparar en S2; responder en S3. | Tiempos del paso 12, tamaño almacenado, calidad e indicadores de derivación. |
| 5 / 54 | ¿Quién debería fijar el máximo de fraude perdido y la exactitud mínima? ¿Qué información tiene que llevar el equipo de datos? | Consultar criterios en S1–S2; responder en S3. | Criterios confirmados y curvas/tablas de cobertura, exactitud y fraude por umbral. |
| 6 / 55 | Si Cauce lanza un seguro para celulares, ¿qué le pasa al modelo y cómo lo detectarían en producción? | Preparar con errores en S2–S3; responder en S3. | Vocabulario, clases actuales, errores y resultados por clase; escenarios hipotéticos identificados como tales. |
| 7 / 56 | ¿Qué datos personales anonimizarían antes de guardar los datos de entrenamiento y cómo afectaría al modelo? | Auditoría en S0; preparar en S1; responder en S3. | Inventario de riesgos, transformaciones propuestas y efecto medido o limitación explícita. |

Las siete respuestas siguen vacías en el notebook original.

## Indicadores, métricas y metas

El paso 15 menciona **cinco indicadores de aceptación**, pero no los enumera.
`src/derivacion.py::evaluar_derivacion` especifica sólo estos tres:

| Indicador verificado | Definición docente | Meta numérica |
| --- | --- | --- |
| `cobertura` | Mensajes con destino distinto de `revision_humana` / mensajes totales. | No encontrada. |
| `exactitud_automatica` | Derivaciones automáticas correctas / derivaciones automáticas. | No encontrada. |
| `fraude_perdido` | Fraudes reales enviados automáticamente a otro equipo / fraudes reales. Revisión humana no cuenta como perdido. | No encontrada. |
| Cuarto indicador del paso 15 | No identificado en los materiales. | No encontrada. |
| Quinto indicador del paso 15 | No identificado en los materiales. | No encontrada. |

No se completan los dos renglones faltantes con métricas propias. Los valores
`0.25`, `0.9`, `0.02`, `1.01` y `0.0` de los tests prueban comportamiento; no son
metas ni umbrales operativos. No hay un margen de seguridad numérico definido.

**Métricas exigidas por otras consignas:** exactitud, F1 macro, matriz normalizada
por fila y porcentaje de fraude mal derivado (paso 2); F1 macro en búsqueda
(10–11); tiempo de predicción (12); reporte de clasificación y matriz del elegido
(15). El reporte incluye precisión, recall y F1 por clase. Esto no prueba que
esas métricas completen la lista de aceptación ni les asigna metas.

**Verificaciones numéricas expresas:** división 80/20 con semilla 42; equivalencia
de etiquetas 100% con alpha 1; cinco particiones estratificadas; diez términos
por clase; 1.000 mensajes y cuatro tamaños de training; diez errores; impacto de
6.500 mensajes; 2.040 filas exportadas. Son condiciones de la actividad.

**Propuestas complementarias, no exigencias docentes:** revisar calibración de
probabilidades, dispersión de tiempos por repeticiones, métricas por canal y
solapamiento por cliente. No se agregan experimentos ni dependencias en S0.

## Restricciones, pruebas y archivos finales

| ID | Requisito | Verificación / etapa |
| --- | --- | --- |
| R01 | Sólo Cauce; Python 3.10+; sin plataforma comercial. | Árbol del repo, requisitos y revisión de alcance en cada sprint. |
| R02 | Limpieza con biblioteca estándar y orden docente. | `test_limpieza.py`: 9 funciones, 15 casos parametrizados; S1. |
| R03 | Matemática NB sólo con NumPy; no importar SciPy ni usar NB de sklearn para implementar. | Revisión de fuente y `test_naive_bayes.py`: 9 funciones, 12 casos; S1. sklearn NB sólo es referencia de verificación. |
| R04 | NumPy y matrices dispersas; herencia ClassifierMixin/BaseEstimator; Pipeline, clone y GridSearchCV. | Pruebas NB y pasos 8–11; S1–S2. |
| R05 | Derivación sólo NumPy, clases alineadas, fraude prioritario con `>=`. | `test_derivacion.py`: 4 casos; S3. |
| R06 | No modificar tests ni conftest; en S0 tampoco módulos, datasets ni notebook. | Comparación byte a byte y SHA-256 contra ZIP; evidencia de S0. |
| R07 | Entrada textual y etiqueta `equipo_final`; no introducir respuesta ni metadatos como features. | Inspección del pipeline y validación sin fuga; S1–S3. |
| R08 | CSV originales protegidos; ninguna muestra sensible pública. | `.gitignore`, revisión de archivos preparados y salidas; todos los sprints. |
| R09 | Funciones en `.py`, notebook explicativo; reiniciar y ejecutar todo antes de entregar. | Ejecución limpia en S3; no ejecutar notebook completo en S0. |
| R10 | Notebook resuelto, módulos, CSV e informe con nombres docentes. | Pasos 1–20 y validación de exportación; S3. |
| R11 | Documentación y commits en español de Argentina, sin force push. | AGENTS y revisión de historial; todos los sprints. |
| R12 | Fuentes preservadas y resultados verificables. | Manifiesto, evidencia de auditoría, entorno y registro de comandos. |

Inventario completo de cada prueba, fórmulas y casos límite en
[análisis de código y pruebas](analisis_codigo_y_pruebas.md). Se ejecutaron 31
casos originales: 30 fallidos esperados y 1 aprobado; no hay implementación final.

## Información faltante y validación propuesta

| ID | Falta o ambigüedad | Decisión afectada | Cómo resolver / cuándo |
| --- | --- | --- | --- |
| P01 | Lista exacta de cinco indicadores y sus valores objetivo; no hay enunciado detallado de veinte pasos fuera del notebook. | Aceptación y elección de umbrales con margen. | Pedir al docente el enunciado/rúbrica completos y confirmar nombres, fórmulas, metas y sentido de desigualdades antes del paso 14. |
| P02 | Grillas de hiperparámetros y margen de seguridad no especificados. | Costo/alcance de búsqueda y selección. | Proponer grillas pequeñas fundamentadas en S2; validar margen con metas en S3. |
| P03 | Casos sin automáticos, sin fraude real o lote vacío no definidos por `evaluar_derivacion`; tests no los cubren. | Denominadores cero y resultado de evaluación. | Consultar convención esperada; documentar una decisión antes de implementar S3 sin alterar tests. |
| P04 | Tratamiento de `equipo_predicho`, `prob_max` y `prob_fraude` en nuevos sin texto suficiente no detallado. | Conservar 2.040 filas y representar revisión correctamente. | Confirmar formato esperado y convención en S3; no eliminar filas ni inventar probabilidades. |
| P05 | Extensión, contenido obligatorio y rúbrica del PDF ejecutivo ausentes. | Formato del paso 20. | Consultar antes de redactar; proponer problema, comparación, impacto, decisión y límites como estructura propia. |
| P06 | Autorización de publicación y carácter ficticio de identificadores/mensajes no acreditados. | Publicación de datasets y resultados sensibles. | Confirmar con responsable/docente; mientras tanto mantenerlos locales. No impide trabajar con copias autorizadas. |
| P07 | Lote, repeticiones y alcance de medición del paso 12 no detallados. | Comparabilidad de tiempos. | Definir en S2 un protocolo común documentado que reserve el test final. |
| P08 | Posibles empates de argmax y requisitos de validación de entradas no detallados. | Comportamiento en situaciones límite. | Mantener compatibilidad con orden de clases/NumPy; documentar decisiones sin añadir requisitos docentes ficticios. |

Estas consultas no bloquean la preparación ni la implementación básica del
Sprint 1. Sí impiden afirmar una aceptación de negocio completa con la información actual.
