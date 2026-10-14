# Conceptos para estudiar Cauce

Los ejemplos de esta guía son inventados. Sirven para entender los conceptos; no son resultados del dataset ni de modelos entrenados.

## Datos y aprendizaje

**Machine Learning.** Es una forma de aprender patrones a partir de datos para predecir casos nuevos. En vez de escribir una regla para cada frase, usamos mensajes históricos para aprender qué palabras se relacionan con cada equipo de Cauce.

**Aprendizaje supervisado.** El entrenamiento utiliza ejemplos con una respuesta conocida. En Cauce tenemos el mensaje y `equipo_final`: el modelo compara los patrones de los textos con esas etiquetas para aprender a clasificarlos.

**Clasificación.** Consiste en asignar una categoría entre varias posibles. Cauce tiene cinco equipos, así que es una clasificación multiclase. Por ejemplo, un mensaje sobre recuperar la contraseña podría corresponder a `cuenta_acceso`.

**Dataset.** Es el conjunto de ejemplos con el que trabajamos. Cada fila representa un mensaje y las columnas contienen su texto y otros datos. Los históricos permiten aprender y evaluar; los nuevos se clasificarán una vez elegido el modelo.

**Variables, features y etiquetas.** Las variables son los campos disponibles. Las features son la representación que recibe el modelo, como los conteos de palabras; la etiqueta es la respuesta que queremos predecir. En Cauce, `texto` produce las features y `equipo_final` es la etiqueta. Un identificador distingue filas, pero no describe el contenido del reclamo.

**Entrenamiento.** Es el ajuste del modelo con ejemplos etiquetados. Naive Bayes cuenta mensajes y términos por clase; KNN conserva las representaciones de los textos para buscar vecinos después. El vocabulario se aprende con los textos de entrenamiento.

**Predicción.** Aplica lo aprendido a un mensaje nuevo. El texto se limpia y se transforma con el vectorizador ya ajustado. El modelo devuelve una clase y probabilidades; la regla de derivación decide después si enviarlo a un equipo o a revisión humana.

## Probabilidades y Naive Bayes

**Probabilidad condicional.** Mide la probabilidad de un evento sabiendo que ocurrió otro:

$$
P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(B)>0.
$$

`A` y `B` son eventos, y `A ∩ B` significa que ocurren ambos. En Cauce, `P(t | c)` expresa la probabilidad de un término `t` dentro de una clase `c`. Que una palabra sea frecuente en fraude no significa, por sí solo, que todo mensaje con esa palabra sea fraude.

**Teorema de Bayes.** Permite invertir la condición para calcular la probabilidad de una clase dado un mensaje:

$$
P(c\mid x)=\frac{P(x\mid c)P(c)}{P(x)}.
$$

`c` es el equipo y `x` representa el mensaje. `P(c)` es la probabilidad a priori del equipo; `P(x | c)`, la verosimilitud del mensaje en ese equipo; `P(x)`, la evidencia común a todas las clases; y `P(c | x)`, la probabilidad a posteriori. Elegimos la clase con mayor posterior. Por ejemplo, combinamos cuán habitual es fraude con qué tan compatibles son las palabras del mensaje con esa clase.

**Naive Bayes.** Es una familia de clasificadores que aplica Bayes con una simplificación de independencia condicional. Aprende probabilidades por clase y combina la información de las features. En Cauce usaremos la variante multinomial porque representamos textos mediante conteos de términos.

**Independencia condicional.** Supone que, conocida la clase, las observaciones de términos se pueden combinar como factores independientes. En texto es una aproximación: palabras como “no” y “reconozco” suelen aparecer relacionadas. Reduce la cantidad de probabilidades que hay que estimar, pero puede contar evidencia relacionada varias veces y dar probabilidades demasiado extremas. Por eso una confianza alta del modelo no garantiza que esté bien calibrado.

**Naive Bayes multinomial.** Modela los conteos de términos. Para cada clase aprende su frecuencia de documentos y la frecuencia de cada palabra. Si `N` es el total de documentos de entrenamiento y `N_c` la cantidad de la clase `c`:

$$
P(c)=\frac{N_c}{N}.
$$

El conteo de documentos determina el prior; el conteo de palabras determina las probabilidades de términos. Son cantidades distintas. La representación no conserva el orden de las palabras, salvo la información que puedan aportar los n-gramas, como “no reconozco”.

**Suavizado de Laplace.** Agrega una pequeña cantidad a los conteos para que un término del vocabulario no tenga probabilidad cero en una clase donde no apareció:

$$
P(t\mid c)=\frac{n_{ct}+\alpha}{T_c+\alpha V}.
$$

`n_ct` cuenta las apariciones del término `t` en los documentos de la clase `c`; `T_c` es el total de apariciones de todos los términos de esa clase; `V` es el tamaño del vocabulario; y `alpha` es el suavizado aditivo. Con `alpha=1` se llama Laplace. Como ejemplo, si “robaron” aparece 3 veces entre 20 términos de fraude y el vocabulario tiene 10 términos, su probabilidad suavizada es `(3+1)/(20+10)=4/30`.

Con `alpha=0`, un término conocido en el vocabulario pero no observado en una clase puede anular su verosimilitud. Si todas las clases quedan con probabilidad cero, no se puede normalizar: la implementación informa un error y pide suavizado positivo. Una palabra totalmente fuera del vocabulario no crea una columna nueva al predecir: el vectorizador la ignora.

### Puntajes, logaritmos y normalización

Multiplicar muchas probabilidades pequeñas puede producir underflow: la computadora redondea el resultado a cero. El clasificador suma logaritmos:

$$
s_c(x)=\log P(c)+\sum_{t=1}^{V}x_t\log P(t\mid c),
\qquad \hat c=\operatorname*{argmax}_c s_c(x).
$$

`x_t` es el conteo del término `t` en el mensaje; `s_c` es el puntaje de la clase; `ĉ` es la clase predicha; `argmax` elige la clase con mayor puntaje. El factor multinomial común a las clases no cambia esa elección y se cancela al normalizar.

Para obtener probabilidades que sumen uno:

$$
\log P(c\mid x)=s_c(x)-L(x),
\qquad L(x)=m+\log\sum_j\exp(s_j(x)-m),
\qquad m=\max_j s_j(x).
$$

`j` recorre las clases y `m` es el puntaje máximo del mensaje. La resta del máximo estabiliza la suma de exponenciales, que calcula `log_suma_exp`. Finalmente, `P(c | x)` se obtiene aplicando la exponencial al logaritmo normalizado.

Para interpretar el modelo, `terminos_mas_indicativos` compara el logaritmo de la probabilidad de cada término en una clase con su promedio en las otras. Esto destaca palabras que diferencian equipos, no simplemente las palabras más frecuentes. En el paso 9 se aplica al modelo entrenado con la porción de entrenamiento del histórico.

## Representación del texto y KNN

**CountVectorizer.** Convierte mensajes en una matriz de conteos, con una columna por término del vocabulario. Si el vocabulario fuera `tarjeta`, `robaron`, el texto “robaron tarjeta tarjeta” produciría `[2, 1]`. En Cauce será la representación de entrada de Naive Bayes. Su salida dispersa guarda principalmente los valores distintos de cero.

**TF-IDF.** Combina frecuencia del término en un documento (TF) con una ponderación inversa según cuántos documentos lo contienen (IDF). Reduce el peso de palabras presentes en muchos mensajes y resalta las más específicas. Una forma suavizada de IDF, usada por defecto en scikit-learn, es:

$$
\operatorname{idf}(t)=\log\frac{1+N}{1+\operatorname{df}(t)}+1.
$$

`N` es el número de documentos de entrenamiento y `df(t)` la cantidad que contiene `t`. TF-IDF multiplica ese valor por la frecuencia del término y normalmente normaliza el vector. En Cauce representará los textos para KNN. El IDF se ajustará sólo en entrenamiento.

**KNN.** Clasifica buscando los `k` ejemplos más cercanos y combinando sus etiquetas mediante votos, uniformes o ponderados. En Cauce buscará mensajes históricos parecidos con `KNeighborsClassifier`; `k` y las ponderaciones se elegirán por validación. La distancia coseno compara la orientación de los vectores:

$$
d_{\cos}(u,v)=1-\frac{u\cdot v}{\lVert u\rVert\lVert v\rVert}.
$$

`u` y `v` son vectores no nulos de dos mensajes; el punto indica producto escalar y las barras, su norma. La fracción es la similitud del coseno: en estos vectores de términos no negativos, un valor cercano a uno indica orientaciones parecidas. La distancia es uno menos esa similitud. Mensajes que comparten términos relevantes pueden ser cercanos aunque difieran en longitud. Con vectores normalizados, euclídea y coseno pueden ordenar igual a los vecinos; la consigna pide coseno y búsqueda `brute`. KNN conserva el entrenamiento y compara contra él al predecir, por lo que medimos su tiempo en el paso 12.

## Separación, validación y métricas

**Entrenamiento y prueba.** Separamos datos para evaluar con ejemplos que el modelo no aprendió. La consigna fija 80% para entrenamiento y 20% para prueba, con estratificación por clase y semilla 42. Quitamos duplicados antes de dividir para evitar que la misma copia aparezca en ambos conjuntos.

**Validación cruzada.** Divide el entrenamiento en particiones: se ajusta con algunas y se valida con la restante, repitiendo el proceso. En Cauce usamos cinco particiones estratificadas para ajustar parámetros con F1 macro. El pipeline vuelve a aprender vocabulario e IDF dentro de cada partición, sin usar información de su validación. Las probabilidades fuera de muestra permitirán elegir umbrales sin consultar prueba.

**Hiperparámetros.** Son decisiones que fijamos antes de entrenar, a diferencia de los conteos o las probabilidades que el modelo aprende. En Cauce probamos `alpha` (suavizado), `ngram_range` (palabras individuales o también pares consecutivos) y `min_df` (mínimo de documentos que contienen un término) para Naive Bayes. Para KNN probamos `n_neighbors` (cantidad de vecinos), `weights` (votos iguales o ponderados por distancia) y `ngram_range`.

**GridSearchCV.** Entrena y valida cada combinación de una grilla de hiperparámetros, y compara sus promedios de validación. Con `scoring="f1_macro"` elige la combinación con mayor F1 macro promedio; `best_estimator_` conserva el pipeline reajustado con todo el entrenamiento. Usamos las mismas cinco particiones para ambos modelos y mantenemos el vectorizador dentro del pipeline. Un buen promedio de validación ayuda a elegir parámetros, pero no reemplaza la evaluación final en prueba.

**Matriz de confusión.** Cuenta las combinaciones de clase real y clase predicha. Usaremos filas reales y columnas predichas: la diagonal contiene los aciertos. Normalizar por fila permite ver qué porcentaje de cada equipo se confunde con los demás, especialmente cuánto fraude termina en tarjeta o transferencias.

Para precision, recall y F1 miramos una clase contra el resto. `TP` son sus aciertos; `FP`, mensajes de otras clases asignados a ella; y `FN`, mensajes reales de esa clase asignados a otra.

**Accuracy o exactitud.** Es la proporción total de predicciones correctas:

$$
\operatorname{accuracy}=\frac{\text{aciertos}}{\text{mensajes evaluados}}.
$$

Resume el desempeño general de Cauce, pero puede esconder errores en fraude porque hay menos ejemplos de esa clase.

**Precision.** Entre los mensajes clasificados como una clase, indica qué proporción realmente le corresponde:

$$
\operatorname{precision}=\frac{TP}{TP+FP}.
$$

En fraude ayuda a medir cuántas alertas enviadas al equipo son correctas. Por ejemplo, 8 fraudes reales entre 10 alertas dan precision de 0,8.

**Recall.** Entre los mensajes reales de una clase, mide qué proporción recuperó el clasificador:

$$
\operatorname{recall}=\frac{TP}{TP+FN}.
$$

Si detecta 8 de 12 fraudes reales, su recall es `8/12`. Sirve para estudiar cuánto fraude deja de reconocer el modelo.

**F1-score.** Combina precision y recall con su media armónica:

$$
F1=\frac{2\,\operatorname{precision}\,\operatorname{recall}}
{\operatorname{precision}+\operatorname{recall}}.
$$

Baja si una de las dos métricas es baja. F1 macro promedia el F1 de las cinco clases con igual peso, así que una clase numerosa no domina la comparación. Si un denominador es cero, habrá que fijar y comunicar la convención usada para calcular la métrica.

## Umbrales y derivación

**Umbrales de decisión.** Son límites que transforman las probabilidades en una acción. En Cauce primero se compara `P(fraude)` con `umbral_fraude`; después, si no se activa esa prioridad, se compara la probabilidad máxima con `umbral_confianza`. Si ninguna condición se cumple, el destino es revisión humana. Las comparaciones incluyen la igualdad (`>=`).

Bajar el umbral de fraude puede recuperar más fraudes y enviar más casos de otros equipos a ese sector. Subir el de confianza suele reducir la cobertura automática y aumentar la revisión. Los elegimos con probabilidades OOF, sin tomar los números de los tests como valores definitivos. Como faltan metas oficiales, el punto es provisional: mejora respecto de la mesa en cada partición y en umbrales vecinos, con la mayor cobertura entre esos puntos estables.

La evaluación de la regla distingue:

| Indicador | Cálculo y uso en Cauce |
| --- | --- |
| Cobertura | Automáticos / total. Mide cuántos mensajes dejan de requerir derivación humana. |
| Exactitud automática | Automáticos correctos / automáticos. Mide la calidad de los destinos decididos sin revisión. |
| Fraude perdido | Fraudes enviados automáticamente a otro equipo / fraudes reales. Mide los casos críticos que se desvían; revisión humana no cuenta como pérdida. |

El recall del clasificador y el fraude perdido de la regla tienen definiciones distintas. Un mensaje enviado a revisión no queda reconocido automáticamente como fraude, pero tampoco se considera perdido según el contrato de `evaluar_derivacion`.

Si un indicador no tiene denominador, `evaluar_derivacion` devuelve NaN: no hay una proporción observada. Por ejemplo, sin mensajes automáticos la cobertura puede ser cero, pero la exactitud automática no está definida. Sin fraudes reales, el fraude perdido tampoco está definido. En un conjunto vacío, los tres indicadores quedan no disponibles.

**Costos de derivación.** Una falsa alerta es un mensaje no fraudulento enviado a Fraude; su tasa divide por los no fraudes. Una revisión requiere intervención humana; su tasa divide por todos los mensajes. Para comparar costos relativos sin contar errores dos veces, separamos fraude perdido, falsas alertas, otros errores automáticos y revisiones. El total de errores automáticos ya incluye las tres primeras categorías. Cada una puede tener un costo distinto y no conocemos los valores económicos de Cauce.

**Límite de la selección.** OOF evita ajustar cada predicción con su propio ejemplo, pero reutilizar esas particiones para elegir parámetros o umbrales puede favorecer sus métricas. Además, si prueba ya se consultó para elegir el modelo, una revisión sobre esa misma prueba no es independiente. Confirmar la recomendación requiere nuevos mensajes etiquetados; no alcanza con volver a dividir los datos ya evaluados.
