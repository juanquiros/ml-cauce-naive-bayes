# Análisis del código original y sus pruebas

El Sprint 0 conserva los doce archivos recuperados del ZIP byte a byte. Este
documento especifica trabajo futuro; no contiene implementaciones de las
funciones pendientes. Los docstrings y tests originales son las fuentes de
los contratos siguientes. No se modificarán tests ni `conftest.py`.

## Limpieza

`quitar_tildes(texto: str) -> str` debe preservar el caso y quitar diacríticos,
incluidos diéresis y la tilde de ñ: `Ñ` pasa a `N`. Depende de normalización Unicode
NFKD y eliminación de caracteres combinantes. Es una función pendiente.

`limpiar_texto(texto) -> str` acepta valores heterogéneos y devuelve texto
normalizado. Depende de `quitar_tildes`, expresiones regulares y manejo de espacios.
Está pendiente. Usa sólo biblioteca estándar (`re`, `unicodedata`).

El orden del contrato es obligatorio:

1. Si la entrada no es `str`, devolver cadena vacía (incluye None, NaN y números).
2. Pasar a minúsculas y quitar tildes.
3. Sustituir URL iniciadas en `http://`, `https://` o `www.` por `_url_`.
4. Sustituir correos por `_email_`.
5. Sustituir montos por `_monto_`: `$`, `gs` o `usd`, punto opcional en `gs.`,
   espacios opcionales antes del número y límites de palabra para monedas.
6. Sustituir otros números por `_num_`, manteniendo como unidad los separadores
   internos de miles/decimales (puntos y comas).
7. Sustituir por espacio caracteres fuera de `a-z`, guion bajo o whitespace.
8. Colapsar espacios y recortar extremos.

Sustituir números antes que montos o eliminar guiones bajos rompería el contrato.
`bugs 15` debe conservar «bugs»: `gs` interno no es moneda. No se añaden stemming,
stopwords, traducción ni reglas de anonimización distintas a las solicitadas.
Los tokens reducen algunos identificadores, pero no certifican anonimización.

## Naive Bayes multinomial

Restricciones: cálculos sólo NumPy; no importar SciPy ni utilizar
`sklearn.naive_bayes` dentro de la implementación. Los imports de
`BaseEstimator` y `ClassifierMixin` permiten la integración con scikit-learn.
X puede ser densa o dispersa: selección de filas, sumas por columna y `X @ M`
deben funcionar sin densificar toda la matriz. `np.asarray` normaliza resultados
de sumas/productos cuando sea necesario.

| Función | Entradas y salida | Responsabilidad y fórmula | Dependencias / verificaciones |
| --- | --- | --- | --- |
| `log_suma_exp(a, axis=1)` | Array y eje; array con eje reducido. | `m + log(sum(exp(a-m)))`, con máximo a lo largo del mismo eje. | NumPy, broadcasting y estabilidad; referencia SciPy sólo en tests. |
| `NaiveBayesMultinomial.__init__(alpha=1.0)` | Suavizado; instancia. | Guarda `alpha` como parámetro del estimador. Ya provisto. | No cambiar firma/herencia; clone y get/set_params. |
| `fit(X,y)` | Conteos n×V y etiquetas n; devuelve `self`. | Clases ordenadas por `np.unique`; contar documentos y términos por clase; estimar log-priors y log-probabilidades suavizadas. | Atributos y formas docentes; entrada y como lista o array; densa/dispersa. |
| `_log_verosimilitud_conjunta(X)` | X n×V; array n×C. | `X @ feature_log_prob_.T + class_log_prior_`. | Modelo ajustado, orden de clases y dimensiones. |
| `predict_log_proba(X)` | X n×V; array n×C. | Normalizar J restando log_suma_exp por fila. | Joint scores y estabilidad, conservación de dimensiones. |
| `predict_proba(X)` | X; array n×C. | Exponenciar log-probabilidades; cada fila suma 1. | No exponenciar J sin normalizar; evitar underflow del documento grande. |
| `predict(X)` | X; vector de n etiquetas. | Seleccionar `classes_` según argmax por fila. | Columnas de probabilidades alineadas con clases, desempate consistente con NumPy. |
| `terminos_mas_indicativos(modelo,vocabulario,n=10)` | Modelo, términos en orden de X y n; dict clase→lista. | Ordenar por `log P(t|c) - promedio(log P(t|otras clases))`, de mayor a menor. | Al menos dos clases para esa fórmula; n=3 en test, n=10 en notebook. |

En fit: `class_count_` tiene forma C; `feature_count_`, C×V;
`class_log_prior_`, C; `feature_log_prob_`, C×V; `classes_`, C.
Se exige `log P(c)=log(N_c/N)` y
`log P(t|c)=log((N_ct+alpha)/(sum_t N_ct+alpha*V))`.
La suma del denominador es de **términos**, no documentos.

Equivalencia futura: usar exactamente los mismos X, y, alpha y orden de clases
en el modelo propio y `MultinomialNB`; comparar priors, probabilidades de términos,
log-probabilidades, probabilidades y etiquetas. El test parametriza alpha con
0.01, 0.5, 1.0 y 2.0, pide `atol=1e-8` en log-probabilidades y `atol=1e-10` en
probabilidades (sin cambiar los `rtol` de `assert_allclose`). También cubre salida
dispersa de CountVectorizer. El paso 8 exige igualdad de etiquetas del 100% en
prueba con alpha 1. No se ha realizado esa verificación de modelos todavía.

Casos no cubiertos o no especificados: alpha negativo, conteos negativos, entrada
vacía, vocabulario de tamaño cero, predicción sin fit, dimensión incompatible,
filas de log_suma_exp con todos los valores `-inf` y términos indicativos con una
sola clase. Se registran para decisiones proporcionadas al alcance, sin modificar
las pruebas ni atribuirles requisitos que no contienen. El ejemplo alpha 0 de
reflexión se estudiará aparte; no autoriza forzar todos los casos a ser finitos.

## Derivación

`REVISION = "revision_humana"` ya está definido. Las dos funciones están pendientes
y sólo pueden utilizar NumPy.

`derivar(proba, clases, umbral_fraude, umbral_confianza)` recibe una matriz n×C,
una lista/array de nombres que incluye `fraude` y dos umbrales. Devuelve un array
de n strings. Hay que localizar la columna de fraude por su nombre, no asumir
una posición fija. El contrato decide, en orden:

1. Si `P(fraude) >= umbral_fraude`, destino `fraude`, aun si otro equipo es más probable.
2. Si no, y `max(P) >= umbral_confianza`, destino de mayor probabilidad.
3. En otro caso, `revision_humana`.

La igualdad está incluida; el «supera» del resumen del sprint se interpreta con
el `>=` explícito del código docente. El dtype del resultado debe admitir nombres
largos sin truncar `revision_humana`. Los umbrales definitivos se elegirán con OOF
en S3. Los tests incluyen 1.01 para desactivar el disparo especial de fraude:
no debe añadirse una validación que rechace ese caso docente.

`evaluar_derivacion(y_real,destino)` devuelve un dict de tres float entre 0 y 1:
cobertura = automáticos/total; exactitud automática = correctos automáticos/automáticos;
fraude perdido = fraudes enviados automáticamente a otro equipo/fraudes reales.
Revisión no es un error de automatización ni un fraude perdido según este contrato.
Los casos sin fraude, sin automáticos o sin mensajes no tienen convención definida
en docstring/tests: pendiente de validación antes de implementar.

## Inventario completo de las pruebas

Los nombres siguientes se ubican en `caso1_cauce/tests/`. «Casos» cuenta la expansión
de parametrizaciones, no la cantidad de asserts. Los ejemplos de tests son
artificiales del docente; no son registros del dataset ni umbrales de negocio.

### test_limpieza.py · 9 funciones, 15 casos

| Prueba | Casos | Función | Qué espera / caso especial | Conocimiento necesario |
| --- | --- | --- | --- | --- |
| `test_quitar_tildes` | 1 | quitar_tildes | Ñandú/pingüino/acción sin diacríticos, mayúscula preservada. | Unicode y marcas combinantes. |
| `test_no_texto_devuelve_vacio` | 1 | limpiar_texto | None, NaN e int producen `""`. | Tipos y faltantes. |
| `test_minusculas_tildes_y_puntuacion` | 1 | limpiar_texto | Frase con signos y mayúsculas pasa a palabras minúsculas sin tildes. | Orden de normalización. |
| `test_montos` | 5 | limpiar_texto | `$ 15.000`, `$15000`, `$ 8.350,50`, `Gs. 150.000` y `USD 20` producen `_monto_`. | Regex, monedas, límites y separadores. |
| `test_numeros` | 3 | limpiar_texto | DNI con puntos, un entero y número de operación producen `_num_`, con resto del texto conservado. | Sustitución de secuencias y puntuación. |
| `test_urls_y_correos` | 1 | limpiar_texto | URL https y www, más correo, generan los tokens correctos. | Captura antes de quitar símbolos. |
| `test_palabras_que_contienen_gs_no_son_montos` | 1 | limpiar_texto | `bugs 15` → `bugs _num_`. | Límites de palabra. |
| `test_emojis_y_espacios` | 1 | limpiar_texto | Sin emojis, saltos ni espacios repetidos; extremos recortados. | Whitespace y reemplazo por espacios. |
| `test_texto_vacio` | 1 | limpiar_texto | Cadena vacía, emoji solo y puntos solos devuelven vacío. | Resultado sin tokens. |

### test_naive_bayes.py · 9 funciones, 12 casos

| Prueba | Casos | Función | Qué espera / caso especial | Conocimiento necesario |
| --- | --- | --- | --- | --- |
| `test_atributos_y_formas` | 1 | fit | Clases a,b,c; conteos C y matrices C×40 con atributos públicos correctos. | Arrays, agrupación por clase, shapes. |
| `test_calculo_a_mano` | 1 | fit | Priors 2/3 y 1/3; términos `[3,3,1]/7` y `[1,1,4]/6` en log. | Conteos multinomiales y Laplace. |
| `test_igual_que_scikit_learn` | 4 | fit y predicciones | Mismos priors, términos, log-probabilidades, probabilidades y etiquetas para cuatro alpha. | Fórmulas, tolerancias y equivalencia numérica. |
| `test_acepta_matrices_dispersas` | 1 | fit, predict_proba, predict | Salida dispersa del vectorizador, y como lista; probabilidades equivalentes y etiquetas fraude/transferencias. | Álgebra densa/dispersa y orden de clases. |
| `test_probabilidades_validas_y_sin_underflow` | 1 | predict_proba, predict_log_proba | Valores finitos y filas que suman 1, incluido documento multiplicado por 5.000. | Logaritmos y normalización estable. |
| `test_log_suma_exp` | 1 | log_suma_exp | Equivalencia con scipy.special.logsumexp en amplitudes grandes y dos -1000. | Máximo por eje y broadcasting. |
| `test_la_matematica_no_usa_scipy` | 1 | módulo | Ningún import/from scipy en la fuente. Única prueba que ya pasa. | Restricción de implementación y revisión estática. |
| `test_funciona_dentro_de_un_pipeline` | 1 | estimador integrado | Predicción fraude, clonación conserva alpha=1, búsqueda CV con alpha 0.1/1.0. | Herencia, parámetros, Pipeline, clone, GridSearchCV. |
| `test_terminos_mas_indicativos` | 1 | términos | Tres términos por cada una de tres clases; incluye señales específicas del corpus de prueba. | Diferencia de log-probabilidades y orden descendente. |

### test_derivacion.py · 4 funciones, 4 casos

| Prueba | Casos | Función | Qué espera / caso especial | Conocimiento necesario |
| --- | --- | --- | --- | --- |
| `test_derivar` | 1 | derivar | Cinco destinos: cuenta_acceso, fraude prioritario aunque no máximo, revisión, fraude, tarjeta; umbrales 0.25/0.9. | Máscaras y prioridades. |
| `test_derivar_umbral_de_fraude_tiene_prioridad` | 1 | derivar | Con umbral 0.02 todos van a fraude; incluye igualdad y conflicto con confianza. | Comparación inclusiva y precedencia. |
| `test_derivar_sin_umbral_de_confianza_deriva_todo` | 1 | derivar | Umbral fraude 1.01 y confianza 0; clases como lista; todos usan argmax. | No limitar indebidamente umbrales; vectorización. |
| `test_evaluar_derivacion` | 1 | evaluar_derivacion | Cobertura 4/6, exactitud automática 2/4 y fraude perdido 1/3; revisión excluida del numerador de fraude. | Denominadores y proporciones. |

## Ejecución inicial real

Desde `caso1_cauce/`, el 14/10/2026:

```powershell
..\.venv\Scripts\python.exe -m pytest -q --tb=no -rf
```

Resultado: **31 casos, 30 fallidos, 1 aprobado**, salida 1, duración reportada
9,75 s. Limpieza: 15 fallidos; NB: 11 fallidos y 1 aprobado; derivación: 4 fallidos.
Las fallas se deben a `NotImplementedError` en los stubs originales. No hubo
errores de importación/recolección. El registro íntegro está en
[pytest_inicial.txt](evidencias/pytest_inicial.txt). No se cambiaron los módulos
para obtener otro resultado. La exigencia de aprobar todos corresponde a la
implementación de los sprints siguientes.
