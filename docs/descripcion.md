# El problema de Cauce

Cauce necesita que cada mensaje llegue al equipo que puede resolverlo. La mesa de entrada atiende unos 6.500 mensajes diarios con nueve personas. Una derivación equivocada retrasa la respuesta; cuando el mensaje avisa una operación sospechosa, ese tiempo puede impedir que se frene el fraude.

La entrada del clasificador será `texto` y la etiqueta será `equipo_final`, el sector al que realmente correspondía el mensaje. `equipo_derivado` registra la decisión original y sirve para medir la línea base. Los identificadores, las fechas y el canal permiten explorar los datos, pero no serán features del modelo.

## Qué encontramos en los datos

La exploración inicial con pandas se hizo sobre los CSV originales, sin limpiarlos ni quitar filas.

| Característica | Históricos | Nuevos |
| --- | ---: | ---: |
| Mensajes | 8.200 | 2.040 |
| Textos nulos | 11 | 3 |
| Textos vacíos, incluyendo nulos y espacios | 18 | 4 |
| Duplicados por `id_cliente` y `texto`, después del primero | 200 | 40 |
| Textos repetidos, sin considerar cliente | 270 | 49 |
| Filas completamente duplicadas | 0 | 0 |
| `id_mensaje` repetidos | 0 | 0 |

Ambos archivos tienen `id_mensaje`, `fecha_hora`, `id_cliente`, `canal` y `texto`. Sólo el histórico agrega `equipo_derivado` y `equipo_final`. No hay nulos en las otras columnas ni fechas que pandas no pueda interpretar. Los grupos duplicados del histórico no presentan etiquetas finales distintas.

Estas son las categorías exactas de `equipo_final`; se conservarán sin cambios. Las palabras se contaron separando el texto original por espacios, con cero palabras para los nulos.

| Categoría | Mensajes | Porcentaje | Promedio de palabras |
| --- | ---: | ---: | ---: |
| `transferencias` | 2.552 | 31,12% | 16,95 |
| `tarjeta` | 2.057 | 25,09% | 14,81 |
| `cuenta_acceso` | 1.648 | 20,10% | 13,87 |
| `prestamos_inversiones` | 1.029 | 12,55% | 12,58 |
| `fraude` | 914 | 11,15% | 18,22 |

La distribución no es uniforme: fraude tiene menos ejemplos que transferencias. Hay 72 históricos con menos de dos palabras **en los datos originales, antes de quitar duplicados y limpiar**.

| Canal | Históricos | Nuevos |
| --- | ---: | ---: |
| `app_chat` | 3.676 | 927 |
| `whatsapp` | 2.499 | 591 |
| `email` | 1.163 | 310 |
| `formulario_web` | 862 | 212 |

En una copia de trabajo quitamos los 200 duplicados del histórico, conservando el primero, y quedaron 8.000 mensajes. Luego calculamos `texto_limpio`: 7.952 textos no están vacíos y 70 mensajes tienen menos de dos palabras. Esos 70 se reservan para revisión humana: 48 quedaron vacíos y 22 contienen una sola palabra. Los otros 7.930 se dividieron de forma estratificada en 6.344 mensajes de entrenamiento y 1.586 de prueba, con semilla 42. Las copias conservan los índices e identificadores originales.

Los CSV originales siguen intactos. Las 2.040 filas nuevas se conservaron para la entrega, incluso cuando hay duplicados o mensajes que requieren revisión.

## Línea base de la derivación manual

Comparando `equipo_derivado` con `equipo_final` en las 8.200 filas originales:

- 6.774 derivaciones correctas: **82,61% de exactitud**.
- 1.426 errores: **17,39%**.
- F1 macro: **0,8166**, dando el mismo peso a cada equipo.
- 290 de los 914 mensajes de fraude llegaron a otro sector: **31,73% del fraude real**.
- 256 mensajes de otros sectores fueron enviados a fraude.

Estos números describen la mesa de entrada sobre los datos originales. La referencia del escenario, aproximadamente un error cada seis mensajes, es coherente con esta muestra, pero no reemplaza la medición ni se confunde con la validación de los modelos.

## Cómo vamos a resolverlo y evaluarlo

Naive Bayes multinomial permite aprender relaciones entre palabras y equipos mediante conteos. KNN compara esa forma de clasificar con la búsqueda de mensajes históricos parecidos, usando TF-IDF y coseno.

Con CountVectorizer y `alpha=1`, Naive Bayes propio y scikit-learn coincidieron en las 1.586 predicciones del paso 8. Esa coincidencia verifica la implementación y no significa 100% de exactitud frente a las etiquetas reales.

En cinco particiones estratificadas del entrenamiento, Naive Bayes obtuvo F1 macro promedio de **0,935575** con `alpha=0.1`, `ngram_range=(1,2)` y `min_df=2`. KNN obtuvo **0,928744** con nueve vecinos, `weights="distance"` y `ngram_range=(1,2)`. Estos resultados corresponden a validación cruzada.

El experimento de tiempos reserva 1.000 mensajes dentro de entrenamiento y ajusta ambos modelos con subconjuntos del resto. Naive Bayes fue más rápido en los cuatro tamaños; su tiempo se mantuvo aproximadamente estable, mientras que el de KNN creció con más mensajes almacenados. La tabla y el gráfico del paso 12 contienen las mediciones de los pipelines completos, promediadas sobre tres repeticiones. No representan un sistema en producción ni una proyección diaria.

## Umbrales y evaluación final

Los materiales no completan la lista de cinco indicadores oficiales ni fijan sus metas o el margen de seguridad. Usamos un criterio provisional propio: mejorar exactitud automática y fraude perdido respecto de la mesa en cada partición OOF, conservar la mejora con umbrales vecinos y maximizar cobertura entre esos puntos estables. La selección independiente dio fraude `0.10` y confianza `0.60` para ambos modelos.

En OOF, Naive Bayes obtuvo 99,48% de cobertura, 94,36% de exactitud automática y 6,93% de fraude perdido; KNN obtuvo 96,83%, 91,97% y 3,82%, respectivamente. Después de fijar las decisiones, evaluamos una vez sobre los mismos **1.586 mensajes aptos**. Los 70 mensajes cortos no integran esta prueba.

| Método | Accuracy | F1 macro | Cobertura | Exactitud de derivación | Fraude perdido |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mesa de entrada | 83,54% | 0,8237 | 100% | 83,54% | 33,52% |
| Naive Bayes | 93,88% | 0,9346 | 99,50% | 94,17% | 5,11% |
| KNN | 92,81% | 0,9260 | 96,15% | 92,66% | 3,41% |

Accuracy y F1 describen el clasificador directo; los otros indicadores describen destinos después de los umbrales. Para la mesa, se comparan decisiones manuales ya realizadas. Fraude perdido cuenta sólo fraudes enviados automáticamente a otro sector: revisión humana queda fuera del numerador.

Elegimos **KNN** priorizando fraude: perdió 6 de 176 fraudes, frente a 9 de Naive Bayes y 59 de la mesa. Su clasificador tuvo recall de fraude de 85,80% y precision de 94,97%. La regla recuperó otros casos, pero envió 75 mensajes no fraudulentos a Fraude. Naive Bayes ofreció mayor exactitud, cobertura y velocidad; la decisión implica ese costo, no una superioridad general de KNN.

Analizamos diez de los 112 errores automáticos. Aparecieron consultas con varias intenciones, falta de contexto y vocabulario compartido. Un caso etiquetado como préstamos describe acceso sin autorización: se señala como posible inconsistencia a revisar, sin modificar la referencia.

## Proyección diaria y mensajes nuevos

La proyección sobre 6.500 mensajes usa la fracción de cortos `70/8000`: estima unos **6.195 destinos automáticos y 305 revisiones**, incluidas 57 por textos cortos. Se esperan unos 5.740 automáticos correctos y 455 incorrectos; unos 24 fraudes llegarían a otro equipo. La referencia manual sobre la misma fracción apta estima 1.060 derivaciones incorrectas y 240 fraudes mal derivados. No estimamos el resultado de atención de los cortos ni de la revisión.

Son valores esperados si la distribución futura se parece a la muestra; no describen un día medido ni resultados de validación cruzada. Los denominadores y cálculos están en el paso 17.

Reentrenamos KNN con los **7.930 históricos aptos**, sin cambiar parámetros ni umbrales. Los 2.040 mensajes nuevos produjeron **1.957 destinos automáticos y 83 revisiones**, incluidas 15 por textos cortos. Sin etiquetas finales no podemos medir su exactitud. El CSV validado conserva filas e identificadores originales y queda local; el PDF contiene sólo agregados.

Los criterios oficiales siguen pendientes de confirmación. La elección provisional y el análisis de sensibilidad no demuestran aptitud para producción; también falta verificar capacidad de revisión, costo de avisos falsos y calidad de anotación.

## Privacidad

Los archivos incluyen identificadores de clientes y textos sobre operaciones financieras. Una búsqueda preliminar encontró secuencias numéricas largas en 653 históricos y 166 mensajes nuevos; también hay referencias a DNI. Esto no confirma que sean datos reales ni que estén anonimizados. Sin autorización de publicación, los CSV quedan fuera del repositorio público. La documentación contiene agregados, ejemplos didácticos inventados y descripciones anonimizadas de errores reales, sin transcripciones de clientes.
