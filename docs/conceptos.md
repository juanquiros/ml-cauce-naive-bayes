# Conceptos para desarrollar y defender Cauce

Esta guía reúne lo necesario para entender los datos, la implementación y la
evaluación. Las fuentes principales son la guía de Naive Bayes de la Sesión 4,
los contratos de `src/`, el notebook de Cauce, los capítulos entregados como
`NB.pdf` y `knn.pdf`, las diapositivas M301 y el notebook docente de KNN.

Las explicaciones de validación, métricas y prevención de fuga desarrollan los
términos que pide el notebook; son apoyo pedagógico, no requisitos adicionales.
Todos los mensajes y conteos usados como ejemplos aquí son **inventados para
estudiar**. No reproducen mensajes del dataset ni resultados experimentales.
Las preguntas de reflexión se registran en requisitos y se responderán en S3.

## Datos y aprendizaje

| Concepto | Qué es y para qué sirve | Cómo funciona | Uso en Cauce |
| --- | --- | --- | --- |
| Machine Learning | Métodos que aprenden patrones a partir de ejemplos para resolver una tarea. Permiten evaluar una regla aprendida, en lugar de escribir cada caso a mano. | Se ajusta un modelo con datos y se comprueba su capacidad con otros datos. | Aprender asociaciones entre el texto y el equipo correcto. |
| Aprendizaje supervisado | Aprendizaje con ejemplos cuya respuesta correcta se conoce. | Cada entrada X tiene una etiqueta y; el ajuste relaciona ambas. | Los mensajes históricos tienen `equipo_final`; los nuevos no. |
| Clasificación de textos | Asignación de una categoría a un texto. | Se normaliza el mensaje, se convierte en números y se aplica un clasificador. | Un mensaje como «no puedo entrar a mi cuenta» recibe una de las cinco clases reales. |
| Dataset | Conjunto organizado de observaciones. Sirve para entrenar o evaluar de manera consistente. | En un CSV, cada fila representa un mensaje y cada columna un campo. | Hay históricos etiquetados y nuevos sin etiqueta; no deben confundirse. |
| Atributos o features | Información numérica que recibe el modelo. | En texto puede ser una columna por término, con conteos o pesos. | La palabra «tarjeta» puede ser una feature; `id_cliente` no debe incorporarse. |
| Etiquetas o clases | Respuestas posibles que se quiere predecir. | Se toman de la variable objetivo y se conservan con nombres consistentes. | `cuenta_acceso`, `fraude`, `prestamos_inversiones`, `tarjeta` y `transferencias`. |
| Entrenamiento | Proceso de construir el modelo a partir de ejemplos. | NB estima conteos y probabilidades; KNN conserva ejemplos vectorizados para compararlos luego. | Se usa sólo el subconjunto habilitado para entrenamiento y el texto limpio. |
| Predicción | Aplicación del modelo ya ajustado a una entrada. | Se transforma el texto con el vocabulario aprendido y se calculan clases o probabilidades. | La clase más probable y el destino final pueden diferir por la regla de fraude/revisión. |

`equipo_derivado` describe la decisión manual original; `equipo_final` describe
el equipo que debía recibir el mensaje. La comparación entre ambos mide la línea
base manual. El objetivo del modelo se toma de `equipo_final`, sin entregárselo
como una columna de entrada.

## Bayes y el modelo multinomial

**Naive Bayes** es una familia de clasificadores probabilísticos. Sirve para
estimar qué clase explica mejor las características observadas. Combina una
probabilidad previa de clase con las probabilidades de sus atributos. En Cauce
se utilizará la variante multinomial para conteos de términos, implementada con
NumPy según el módulo docente.

**Teorema de Bayes.** Permite relacionar dos probabilidades condicionales:

```text
P(c | x) = P(x | c) · P(c) / P(x)
```

`P(c | x)` es la probabilidad posterior de una clase dado el mensaje; `P(x | c)`
es la verosimilitud del mensaje dada la clase; `P(c)` es la probabilidad a priori;
`P(x)` normaliza. Para elegir la clase alcanza comparar los numeradores, porque
el denominador es común. En Cauce se normalizará además para obtener una fila
de probabilidades que la regla de derivación pueda utilizar.

**Probabilidad a priori.** Resume la frecuencia de una clase antes de leer un
mensaje. Se estima como `N_c / N`, cantidad de documentos de esa clase sobre el
total de entrenamiento. Por ejemplo, 20 mensajes de fraude entre 100 darían 0,20;
son números didácticos. En Cauce la clase guarda su logaritmo en `class_log_prior_`.

**Probabilidad condicional.** Mide la probabilidad de un evento al conocer otro.
Sirve para distinguir qué términos son frecuentes dentro de cada clase. En el
modelo multinomial se estima `P(término | clase)` a partir de los conteos de
palabras, no de la cantidad de documentos que contienen la palabra. En Cauce
se almacena en escala logarítmica en `feature_log_prob_`.

**Independencia condicional.** Es el supuesto de tratar los atributos como
independientes cuando se conoce la clase. Permite descomponer un cálculo conjunto
en factores sencillos. Para texto, el modelo usa las frecuencias de términos
sin representar toda la estructura de una oración. En Cauce es una hipótesis de
modelado que se debe evaluar con resultados; no una afirmación sobre el lenguaje.

**Naive Bayes multinomial.** Representa un documento mediante los conteos no
negativos de sus términos. Sirve para clasificación textual con vocabularios
grandes. Aprende por clase un vector de frecuencias suavizadas y, para predecir,
combina las contribuciones de las palabras presentes. En Cauce se requiere:

```text
N_c  = documentos de la clase c
N_ct = suma de apariciones del término t en documentos de c
V    = cantidad de términos del vocabulario

P(c)     = N_c / N
P(t | c) = (N_ct + alpha) / (suma_t N_ct + alpha · V)
J(x, c)  = log P(c) + suma_t x_t · log P(t | c)
```

La guía también estudia atributos categóricos y gaussianos. Su denominador
categórico es distinto del multinomial de texto. El archivo complementario
`naive_bayes_desde_cero.py` ilustra esos otros tipos; no reemplaza la clase de Cauce.

**Conteo de palabras.** Es la cantidad de apariciones de cada término en un
documento. Sirve para representar mensajes con números. Con vocabulario
`[cuenta, tarjeta]`, «tarjeta tarjeta cuenta» se representa como `[1, 2]`.
En Cauce el orden de las columnas debe coincidir en entrenamiento y predicción.

**Suavizado de Laplace.** Agrega un pseudoconteo a cada término para estimar
probabilidades con pocos datos. El suavizado aditivo usa `alpha`; con `alpha=1`
se llama Laplace. La suma del denominador también aumenta para conservar la
normalización. En Cauce se verifica alpha 1 y se comparan distintos valores en
los tests y en una búsqueda futura. No se eligió todavía un alpha experimental.

**Logaritmos en probabilidades.** Permiten sustituir productos muy pequeños por
sumas y evitar que la computadora los redondee a cero, problema llamado underflow.
Sirven también para usar un producto matricial en todos los documentos/clases.
En Cauce se calcula `J = X @ feature_log_prob_.T + class_log_prior_` y se normaliza:

```text
log_suma_exp(a) = m + log(suma exp(a - m)), con m = máximo de a
log P(c | x)    = J(x, c) - log_suma_exp(J(x, :))
P(c | x)        = exp(log P(c | x))
```

El máximo y la suma se calculan por fila cuando `axis=1`; hay que cuidar las
dimensiones al restar. Estas fórmulas son una explicación para estudiar la
implementación pendiente, no código ya implementado.

## Vectorización y comparación

| Concepto | Qué es y para qué sirve | Cómo funciona | Uso en Cauce |
| --- | --- | --- | --- |
| CountVectorizer | Transformador de scikit-learn que convierte textos en conteos. | `fit` aprende el vocabulario; `transform` cuenta términos y devuelve una matriz dispersa. Los términos fuera del vocabulario no agregan columnas. | Primer paso del pipeline NB. Se ajusta sólo con entrenamiento en cada fold. |
| TF-IDF | Ponderación de términos según frecuencia local y rareza en el corpus. Reduce el peso relativo de términos ubicuos. | Combina TF, frecuencia del término, con IDF, frecuencia documental inversa. En scikit-learn hay suavizado y normalización configurables. | `TfidfVectorizer` representa mensajes para KNN. IDF también se aprende sólo de training. |
| KNN | Clasificador que consulta los k ejemplos más cercanos. Sirve como comparación basada en semejanza. | Guarda ejemplos vectorizados, mide distancias al predecir y agrega sus votos; `weights` puede cambiar la ponderación. | Se usa `KNeighborsClassifier` de scikit-learn, sin implementación propia, con coseno y `brute`. |
| Similitud del coseno | Medida del ángulo entre dos vectores; compara orientación. | `sim(x,z) = (x·z)/(norma(x)·norma(z))`; la distancia coseno es `1 - sim`. Hay que considerar vectores de norma cero. | Métrica exigida para KNN sobre TF-IDF; su comportamiento se justificará con el experimento. |
| Pipeline | Secuencia que transforma entradas y aplica un estimador. Sirve para mantener juntas las etapas aprendidas. | Al entrenar, ajusta vectorizador y clasificador en orden; en predicción reutiliza las transformaciones. | Permite que GridSearchCV ajuste vocabulario dentro de cada fold. La clase propia debe ser clonable. |
| Matriz dispersa | Representación que guarda principalmente valores distintos de cero. Ahorra memoria cuando el vocabulario es grande. | Almacena conteos y posiciones sin construir una tabla densa de todos los ceros. | NB debe aceptar la salida dispersa de CountVectorizer sin importar SciPy en su matemática ni convertir todo X a denso. |

Las diapositivas y el notebook de Iris muestran escalado numérico y otras
distancias. Son contexto para entender KNN. La receta específica de Cauce exige
TF-IDF y coseno; no exige trasladar `StandardScaler`, Iris ni Seaborn al proyecto.

## Separar datos y elegir configuraciones

**Separación de entrenamiento y prueba.** Reserva datos que no intervienen en
decisiones de ajuste para estimar generalización. Se divide por índices y se
mantiene la proporción de clases mediante estratificación. En Cauce corresponde
80/20 con `random_state=42`, después de la deduplicación y tratamiento docente de
textos cortos. Comparar resultados sobre training no sustituye evaluar en prueba.

**Validación cruzada.** Repite entrenamiento/validación en particiones del
conjunto de entrenamiento. Sirve para comparar configuraciones sin recurrir al
test final. En cada fold se entrena con una parte y se mide en la parte restante.
En Cauce se exigen cinco particiones estratificadas en las búsquedas.

**GridSearchCV.** Prueba una grilla de configuraciones mediante validación
cruzada. Sirve para seleccionar hiperparámetros de forma sistemática. Clona el
pipeline por candidato/fold y resume la métrica elegida. En Cauce se exige
`f1_macro`, y se debe concluir sobre cada hiperparámetro. La grilla concreta no
está definida en el material y se justificará en S2.

**Hiperparámetros.** Son decisiones fijadas antes de ajustar un modelo, distintas
de los valores aprendidos. Sirven para controlar su comportamiento. Ejemplos:
`alpha`, `ngram_range`, `min_df`, `n_neighbors` y `weights`. Son candidatos de
estudio, no una grilla impuesta ni seleccionada. En Cauce los nombres de un
pipeline permiten buscarlos como `nb__alpha` o `vec__min_df`.

**Probabilidades fuera de muestra (OOF).** Son predicciones para cada ejemplo
realizadas por un modelo que no lo usó al entrenar. Sirven para elegir reglas
con una estimación más honesta que las probabilidades de entrenamiento. En
Cauce se solicitan mediante `cross_val_predict` para escoger umbrales dentro
del training. El conjunto de prueba sigue reservado.

**Fuga de información.** Ocurre cuando el aprendizaje o las decisiones usan
información que no estaría disponible al predecir o que pertenece a evaluación.
Produce resultados demasiado optimistas. Puede aparecer por features que revelan
la etiqueta, por aprender vocabulario/IDF con toda la tabla, por duplicados entre
conjuntos o por ajustar umbrales mirando el test. En Cauce se evita revisando
columnas, deduplicando antes del split y encerrando lo aprendido en un pipeline.

## Métricas y decisión

Para una clase como `fraude`, **TP** son fraudes predichos correctamente, **FP**
mensajes de otras clases predichos como fraude y **FN** fraudes predichos como
otra clase. Las métricas de clasificación siguientes se calculan sobre clases
predichas; los indicadores de derivación se calculan sobre destinos finales.

| Concepto | Qué es y para qué sirve | Cómo funciona | Uso en Cauce |
| --- | --- | --- | --- |
| Exactitud (accuracy) | Proporción global de aciertos. Resume rendimiento general. | `aciertos / total`. Puede ocultar errores en clases menos frecuentes. | Línea base manual y comparación del clasificador; no confundir con exactitud sólo de automáticos. |
| Precisión | Entre los predichos de una clase, qué proporción corresponde a esa clase. Mide falsas alarmas. | `TP / (TP + FP)`. | Interpretar el reporte por clase del paso 15. No hay una meta docente de precisión identificada. |
| Recall | Entre los casos reales de una clase, qué proporción se detecta. Mide omisiones. | `TP / (TP + FN)`. | Examinar especialmente fraude, junto con el destino de revisión. |
| F1 macro | Promedio no ponderado del F1 de las clases. Da el mismo peso a cada clase. | Cada F1 combina precisión y recall como `2PR/(P+R)`; luego se promedian. | Métrica de selección exigida en GridSearchCV y línea base. |
| Matriz de confusión | Tabla de clases reales frente a predichas. Permite localizar tipos de error. | Filas reales, columnas predichas; diagonal correcta. Normalizar por fila divide por el total real de cada clase. | La línea base exige normalización por fila y un orden de clases declarado. |
| Umbrales de confianza | Valores que convierten probabilidades en decisiones. Permiten graduar automatización y revisión. | Se compara `P(fraude)` con un umbral y luego el máximo con otro. | Fraude tiene prioridad con `>=`; después clase de máxima probabilidad con `>=`; en otro caso, revisión humana. Los valores siguen pendientes. |

**Indicadores de derivación.** Si `A` es el número de destinos automáticos y `N`
el total, cobertura es `A/N`. Si `C` de esos destinos son correctos, exactitud
automática es `C/A`. Si `L` fraudes reales fueron enviados automáticamente a
otro equipo y existen `F` fraudes reales, fraude perdido es `L/F`. Los fraudes
en revisión humana no cuentan como perdidos según el contrato docente.
Los denominadores cero requieren una convención aún no especificada.

Ejemplo exclusivamente didáctico: de 100 mensajes, 70 automáticos y 63 correctos
dan cobertura 0,70 y exactitud automática 0,90. Si hay diez fraudes y uno va
automáticamente a un equipo incorrecto, fraude perdido es 0,10. Estos valores
no son metas ni resultados de Cauce.

Al defender el proyecto habrá que distinguir lo medido de lo proyectado, una
clase predicha de un destino final y una probabilidad estimada de una garantía.
Los criterios de aceptación faltantes deben confirmarse; no se derivan de un
ejemplo teórico ni de los valores usados por los tests.
