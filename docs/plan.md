# Plan de trabajo

La referencia principal es `caso1_cauce/caso1_cauce.ipynb`. Los 20 pasos están completos y el notebook se ejecutó desde cero, sin errores. Las siete preguntas tienen sus respuestas y las 31 pruebas originales aprueban. Los umbrales y la recomendación son provisionales porque faltan los criterios oficiales de aceptación.

## Etapas y pasos del notebook

| Etapa | Paso | Actividad |
| --- | ---: | --- |
| 1. Preparación | 1 | **Completo.** Exploración de filas, nulos, vacíos, duplicados, clases, canales y palabras por clase. |
| 1. Preparación | 2 | **Completo.** Línea base manual, con accuracy, F1 macro, matriz normalizada por fila y fraude enviado a otro equipo. |
| 2. Naive Bayes | 3 | **Completo.** Copia sin duplicados, conservando el primero, y explicación de por qué se quitan antes de dividir. |
| 2. Naive Bayes | 4 | **Completo.** Limpieza implementada, 15 pruebas aprobadas y cinco ejemplos inventados de texto original y limpio. |
| 2. Naive Bayes | 5 | **Completo.** `texto_limpio`, máscaras de revisión y entrenamiento: 70 mensajes cortos y 7.930 aptos. |
| 2. Naive Bayes | 6 | **Completo.** Naive Bayes, `log_suma_exp` y términos indicativos implementados; 12 pruebas aprobadas y demostración didáctica. |
| 2. Naive Bayes | 7 | **Completo.** División estratificada 80/20 con semilla 42: 6.344 mensajes de entrenamiento y 1.586 de prueba. |
| 2. Naive Bayes | 8 | **Completo.** CountVectorizer + ambos Naive Bayes con `alpha=1`: coincidencia del 100% y probabilidades numéricamente próximas. |
| 2. Naive Bayes | 9 | **Completo.** Diez términos indicativos por clase, calculados con entrenamiento e interpretados. |
| 3. Comparación | 10 | **Completo.** GridSearchCV de CountVectorizer + Naive Bayes: 16 combinaciones, cinco particiones estratificadas y F1 macro. |
| 3. Comparación | 11 | **Completo.** GridSearchCV de TF-IDF + KNN con coseno y `brute`: 12 combinaciones y las mismas particiones. |
| 3. Comparación | 12 | **Completo.** Tabla y gráfico de tiempos: lote fijo de 1.000 mensajes, cuatro tamaños y tres repeticiones de cada pipeline. |
| 4. Resultados | 13 | **Completo.** Derivación con prioridad de fraude y evaluación con denominadores definidos; cuatro pruebas aprobadas. |
| 4. Resultados | 14 | **Completo.** OOF de ambos pipelines, 56 pares por modelo y análisis de sensibilidad; umbrales provisionales fijados antes de prueba. |
| 4. Resultados | 15 | **Completo.** Evaluación única de los tres métodos sobre 1.586 mensajes, cinco indicadores descriptivos, reporte y matriz de KNN. |
| 4. Resultados | 16 | **Completo.** Diez errores automáticos reales, descripciones anonimizadas, posibles causas y mejoras propuestas. |
| 4. Resultados | 17 | **Completo.** Proyección sobre 6.500 mensajes, separando cortos y aptos, con comparación manual sobre la misma fracción apta. |
| 4. Resultados | 18 | **Completo.** KNN reajustado con 7.930 históricos aptos y aplicado a los mensajes nuevos; cortos forzados a revisión. |
| 4. Resultados | 19 | **Completo.** CSV UTF-8 local validado: 2.040 filas y las cinco columnas exigidas, sin agregar índice ni quitar duplicados nuevos. |
| 4. Resultados | 20 | **Completo.** Informe ejecutivo de tres páginas A4 para Laura Benítez, generado con agregados y revisado visualmente. |

El detalle de todos los pasos está en el notebook. `descripcion.md` distingue datos originales, validación, evaluación final y proyección. El desarrollo funcional está cerrado; los criterios pendientes limitan la aprobación para una implementación real.

## Código y qué exigen las pruebas

| Archivo | Funciones y contrato |
| --- | --- |
| `src/limpieza.py` | `quitar_tildes(texto)` elimina tildes, diéresis y convierte ñ en n. `limpiar_texto(texto)` devuelve `""` para entradas no textuales; pasa a minúsculas, quita tildes y reemplaza, en ese orden, URL, correos, montos y números por `_url_`, `_email_`, `_monto_` y `_num_`. Luego reemplaza signos y emojis por espacios y compacta espacios. Los montos admiten `$`, `gs` y `usd`; `gs` y `usd` deben ser palabras independientes. Los números con puntos o comas internos se toman completos. Las pruebas incluyen mayúsculas, `None`, NaN, montos pegados, `gs.`, saltos de línea y `bugs 15`, que no es un monto. Sólo biblioteca estándar. |
| `src/naive_bayes.py` | `log_suma_exp(a, axis=1)` normaliza con estabilidad numérica. `NaiveBayesMultinomial(alpha=1.0)` implementa `fit(X, y)`, `_log_verosimilitud_conjunta(X)`, `predict_log_proba(X)`, `predict_proba(X)` y `predict(X)`. `fit` devuelve `self` y crea `classes_`, `class_count_`, `feature_count_`, `class_log_prior_` y `feature_log_prob_`, con clases ordenadas. `terminos_mas_indicativos(modelo, vocabulario, n=10)` devuelve un diccionario de listas ordenadas por diferencia entre el logaritmo de la probabilidad del término en la clase y su promedio en las otras clases. Las pruebas verifican conteos a mano, equivalencia con scikit-learn para cuatro valores de alpha, matrices densas y dispersas, probabilidades finitas que suman uno, Pipeline, clonación y GridSearchCV. La matemática usa sólo NumPy; se permite heredar de `ClassifierMixin` y `BaseEstimator`. |
| `src/derivacion.py` | `derivar(proba, clases, umbral_fraude, umbral_confianza)` recibe una matriz de probabilidades y las clases en el orden de sus columnas. Devuelve un array de destinos: primero fraude si su probabilidad es `>= umbral_fraude`; después la clase más probable si su confianza es `>= umbral_confianza`; en el resto, `REVISION = "revision_humana"`. `evaluar_derivacion(y_real, destino)` devuelve las proporciones `cobertura`, `exactitud_automatica` y `fraude_perdido`, entre 0 y 1. Las pruebas comprueban prioridad, igualdad con el umbral, revisión, derivación de todos los casos y los denominadores de cada indicador. Sólo NumPy. |

Se conservaron las interfaces, los tests y `conftest.py`. Los valores usados en las pruebas de derivación son ejemplos para verificar la lógica, no metas de Cauce. Los indicadores sin denominador devuelven NaN y sus casos especiales se comprobaron sin modificar las pruebas originales.

## Decisiones y restricciones para las siguientes etapas

El vocabulario y el IDF se ajustarán sólo con entrenamiento. Durante la validación, el vectorizador estará dentro del pipeline para ajustarse de nuevo en cada partición. La búsqueda de parámetros y los umbrales no utilizarán prueba. La comparación inicial del paso 8 comprueba la implementación; no se usará su resultado para elegir parámetros.

Los mensajes con menos de dos palabras limpias irán a revisión humana también al clasificar los nuevos. No se eliminarán filas de la salida final. No se usarán `equipo_derivado`, `equipo_final` ni identificadores como entradas del clasificador.

Las grillas de parámetros ya se evaluaron y sus mejores estimadores se conservan en memoria al ejecutar el notebook. La comparación de tiempos usa copias de esas configuraciones: reserva un lote fijo de 1.000 mensajes del entrenamiento y ajusta con 25%, 50%, 75% y 100% de los 5.344 restantes. Ese lote no entra al ajuste de los modelos medidos y prueba no se usa en el experimento.

Los materiales no completan los cinco indicadores oficiales, sus metas ni el margen de seguridad. Se usaron cinco indicadores descriptivos y un criterio provisional propio de mejora respecto de la mesa, estable en particiones y umbrales vecinos. Esas definiciones siguen pendientes de confirmación; también se propone revisar la posible inconsistencia de etiqueta observada.

Los entregables explícitos son el notebook resuelto, los módulos completos con sus pruebas aprobadas, `predicciones_caso1.csv` e `informe_ejecutivo.pdf`. El notebook debe incluir las tablas, gráficos y explicaciones de sus pasos y entregarse después de reiniciar y ejecutar todo. No aparece una rúbrica con puntajes en los materiales disponibles.

## Preguntas de reflexión

Las siete preguntas están respondidas con los resultados y sus límites: independencia y probabilidades, suavizado, entrada del clasificador, costo de KNN, definición de metas, nuevas categorías y privacidad. Se conservaron sus enunciados originales.

La guía de Naive Bayes, su código de ejemplo y los materiales de KNN se usarán para estudiar. Sus ejercicios de clima, préstamos, spam e Iris no se incorporan a la consigna de Cauce. El código complementario de Naive Bayes mezcla atributos categóricos y gaussianos: sirve como referencia de Bayes y logaritmos, pero Cauce requiere la variante multinomial de conteos.
