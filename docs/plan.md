# Plan de trabajo

La referencia principal es `caso1_cauce/caso1_cauce.ipynb`. Los pasos 1 al 6 están completos y ejecutados. Las funciones de limpieza y Naive Bayes aprueban las 27 pruebas originales de esos módulos. Los pasos 7 al 20 y las cuatro pruebas de derivación siguen pendientes.

## Etapas y pasos del notebook

| Etapa | Paso | Actividad |
| --- | ---: | --- |
| 1. Preparación | 1 | **Completo.** Exploración de filas, nulos, vacíos, duplicados, clases, canales y palabras por clase. |
| 1. Preparación | 2 | **Completo.** Línea base manual, con accuracy, F1 macro, matriz normalizada por fila y fraude enviado a otro equipo. |
| 2. Naive Bayes | 3 | **Completo.** Copia sin duplicados, conservando el primero, y explicación de por qué se quitan antes de dividir. |
| 2. Naive Bayes | 4 | **Completo.** Limpieza implementada, 15 pruebas aprobadas y cinco ejemplos inventados de texto original y limpio. |
| 2. Naive Bayes | 5 | **Completo.** `texto_limpio`, máscaras de revisión y entrenamiento: 70 mensajes cortos y 7.930 aptos. |
| 2. Naive Bayes | 6 | **Completo.** Naive Bayes, `log_suma_exp` y términos indicativos implementados; 12 pruebas aprobadas y demostración didáctica. |
| 2. Naive Bayes | 7 | Dividir 80/20, estratificando por `equipo_final`, con `random_state=42`. |
| 2. Naive Bayes | 8 | Entrenar CountVectorizer y ambos Naive Bayes con `alpha=1`; comprobar coincidencia de predicciones del 100% en prueba, como pide la consigna. |
| 2. Naive Bayes | 9 | Obtener e interpretar los diez términos más indicativos de cada clase. |
| 3. Comparación | 10 | Ajustar el pipeline CountVectorizer + Naive Bayes propio con GridSearchCV, cinco particiones estratificadas y `f1_macro`. Explicar cada hiperparámetro. |
| 3. Comparación | 11 | Ajustar TF-IDF + `KNeighborsClassifier(metric="cosine", algorithm="brute")`; justificar coseno frente a euclídea. |
| 3. Comparación | 12 | Medir y graficar el tiempo de predicción de 1.000 mensajes usando 25%, 50%, 75% y 100% del entrenamiento de cada modelo. |
| 4. Resultados | 13 | Completar y probar `derivar` y `evaluar_derivacion`. |
| 4. Resultados | 14 | Obtener probabilidades fuera de muestra con `cross_val_predict` en entrenamiento y elegir ambos umbrales con margen de seguridad, para cada modelo. |
| 4. Resultados | 15 | Evaluar una sola vez en prueba: tabla de cinco indicadores para ambos modelos y mesa de entrada; reporte y matriz del modelo elegido. |
| 4. Resultados | 16 | Analizar diez errores de derivación automática, sus causas y una mejora concreta por error. |
| 4. Resultados | 17 | Estimar el impacto diario sobre 6.500 mensajes. |
| 4. Resultados | 18 | Reentrenar el modelo elegido con todos los históricos limpios y derivar los mensajes nuevos. |
| 4. Resultados | 19 | Generar y verificar `predicciones_caso1.csv`: 2.040 filas y columnas `id_mensaje`, `equipo_predicho`, `prob_max`, `prob_fraude`, `derivacion`. |
| 4. Resultados | 20 | Preparar `informe_ejecutivo.pdf` para Laura Benítez. |

El detalle de los seis primeros pasos está en el notebook. Los datos originales y los preparados se distinguen en `descripcion.md`. El próximo paso pendiente es la división estratificada 80/20 del paso 7.

## Código y qué exigen las pruebas

| Archivo | Funciones y contrato |
| --- | --- |
| `src/limpieza.py` | `quitar_tildes(texto)` elimina tildes, diéresis y convierte ñ en n. `limpiar_texto(texto)` devuelve `""` para entradas no textuales; pasa a minúsculas, quita tildes y reemplaza, en ese orden, URL, correos, montos y números por `_url_`, `_email_`, `_monto_` y `_num_`. Luego reemplaza signos y emojis por espacios y compacta espacios. Los montos admiten `$`, `gs` y `usd`; `gs` y `usd` deben ser palabras independientes. Los números con puntos o comas internos se toman completos. Las pruebas incluyen mayúsculas, `None`, NaN, montos pegados, `gs.`, saltos de línea y `bugs 15`, que no es un monto. Sólo biblioteca estándar. |
| `src/naive_bayes.py` | `log_suma_exp(a, axis=1)` normaliza con estabilidad numérica. `NaiveBayesMultinomial(alpha=1.0)` implementa `fit(X, y)`, `_log_verosimilitud_conjunta(X)`, `predict_log_proba(X)`, `predict_proba(X)` y `predict(X)`. `fit` devuelve `self` y crea `classes_`, `class_count_`, `feature_count_`, `class_log_prior_` y `feature_log_prob_`, con clases ordenadas. `terminos_mas_indicativos(modelo, vocabulario, n=10)` devuelve un diccionario de listas ordenadas por diferencia entre el logaritmo de la probabilidad del término en la clase y su promedio en las otras clases. Las pruebas verifican conteos a mano, equivalencia con scikit-learn para cuatro valores de alpha, matrices densas y dispersas, probabilidades finitas que suman uno, Pipeline, clonación y GridSearchCV. La matemática usa sólo NumPy; se permite heredar de `ClassifierMixin` y `BaseEstimator`. |
| `src/derivacion.py` | `derivar(proba, clases, umbral_fraude, umbral_confianza)` recibe una matriz de probabilidades y las clases en el orden de sus columnas. Devuelve un array de destinos: primero fraude si su probabilidad es `>= umbral_fraude`; después la clase más probable si su confianza es `>= umbral_confianza`; en el resto, `REVISION = "revision_humana"`. `evaluar_derivacion(y_real, destino)` devuelve las proporciones `cobertura`, `exactitud_automatica` y `fraude_perdido`, entre 0 y 1. Las pruebas comprueban prioridad, igualdad con el umbral, revisión, derivación de todos los casos y los denominadores de cada indicador. Sólo NumPy. |

Se conservarán las interfaces, los tests y `conftest.py`. Los valores usados en las pruebas de derivación son ejemplos para verificar la lógica, no umbrales elegidos para Cauce. Antes de la implementación conviene definir qué devolverá la evaluación si no hay casos automáticos o fraudes: los tests originales no cubren esos extremos.

## Decisiones y restricciones para las siguientes etapas

El vocabulario y el IDF se ajustarán sólo con entrenamiento. Durante la validación, el vectorizador estará dentro del pipeline para ajustarse de nuevo en cada partición. La búsqueda de parámetros y los umbrales no utilizarán prueba. La comparación inicial del paso 8 comprueba la implementación; no se usará su resultado para elegir parámetros.

Los mensajes con menos de dos palabras limpias irán a revisión humana también al clasificar los nuevos. No se eliminarán filas de la salida final. No se usarán `equipo_derivado`, `equipo_final` ni identificadores como entradas del clasificador.

Antes de cerrar el paso 15 hay que consultar al docente cuáles son los cinco indicadores de aceptación y sus metas: `evaluar_derivacion` especifica tres, y los materiales entregados no completan esa lista. También quedan por definir las grillas de parámetros y cómo expresar el margen de seguridad del paso 14; se decidirán con los resultados de validación y los criterios del caso.

Los entregables explícitos son el notebook resuelto, los módulos completos con sus pruebas aprobadas, `predicciones_caso1.csv` e `informe_ejecutivo.pdf`. El notebook debe incluir las tablas, gráficos y explicaciones de sus pasos y entregarse después de reiniciar y ejecutar todo. No aparece una rúbrica con puntajes en los materiales disponibles.

## Preguntas de reflexión

Al terminar se responderán en un párrafo cada una, apoyándose en los resultados: por qué Naive Bayes puede clasificar bien pese a la independencia y cómo afecta sus probabilidades; qué ocurre con `alpha=0` ante términos no observados en fraude; por qué no usar `equipo_derivado`; costo de KNN y cuándo elegirlo; quién fija las metas de fraude perdido y exactitud; cómo detectar una categoría nueva, como seguros para celulares; y qué datos personales anonimizar y cómo influye en el modelo.

La guía de Naive Bayes, su código de ejemplo y los materiales de KNN se usarán para estudiar. Sus ejercicios de clima, préstamos, spam e Iris no se incorporan a la consigna de Cauce. El código complementario de Naive Bayes mezcla atributos categóricos y gaussianos: sirve como referencia de Bayes y logaritmos, pero Cauce requiere la variante multinomial de conteos.
