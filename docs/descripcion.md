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

Los materiales no completan la lista de cinco indicadores oficiales ni fijan sus metas o el margen de seguridad. En Sprint 3 usamos un criterio provisional: mejorar exactitud automática y fraude perdido respecto de la mesa en cada partición OOF, conservar la mejora con umbrales vecinos y maximizar cobertura entre esos puntos. Conservamos fraude `0.10` y confianza `0.60` para ambos modelos, sin repetir búsquedas ni cambiar los hiperparámetros del Sprint 2.

La revisión usa las consecuencias OOF sobre 6.344 mensajes de entrenamiento, incluidos 707 fraudes reales y 5.637 no fraudes:

| Indicador OOF | Naive Bayes | KNN |
| --- | ---: | ---: |
| Fraudes mal derivados | 49 | 27 |
| Falsas alertas de fraude | 88 | 340 |
| Otros errores automáticos | 219 | 126 |
| Errores automáticos totales | 356 | 493 |
| Revisiones humanas | 33 | 201 |
| Cobertura | 99,48% | 96,83% |
| Exactitud automática | 94,36% | 91,97% |
| Fraude perdido | 6,93% | 3,82% |

Recomendamos provisionalmente **Naive Bayes** bajo el supuesto de reducir errores generales y carga operativa (escenario B): menos alertas falsas y revisiones, mayor exactitud automática y menor tiempo de predicción. Si evitar fraudes mal derivados es la prioridad dominante (A), se favorece KNN. Para equilibrar riesgo y capacidad (C), el responsable de Cauce debe confirmar prioridades y costos relativos; no inventamos costos monetarios ni afirmamos un ganador único.

La prueba vuelve a describirse sobre los mismos **1.586 mensajes aptos**, incluidos 176 fraudes reales y 1.410 no fraudes. Los 70 cortos no integran esta muestra:

| Método | Accuracy | F1 macro | Cobertura | Exactitud de derivación | Fraude perdido |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mesa de entrada | 83,54% | 0,8237 | 100% | 83,54% | 33,52% |
| Naive Bayes | 93,88% | 0,9346 | 99,50% | 94,17% | 5,11% |
| KNN | 92,81% | 0,9260 | 96,15% | 92,66% | 3,41% |

| Consecuencia en prueba | Naive Bayes | KNN | KNN menos NB |
| --- | ---: | ---: | ---: |
| Fraudes mal derivados | 9 | 6 | −3 |
| Falsas alertas de fraude | 16 | 75 | +59 |
| Otros errores automáticos | 67 | 31 | −36 |
| Errores automáticos totales | 92 | 112 | +20 |
| Revisiones humanas | 8 | 61 | +53 |

Accuracy y F1 macro describen la clase predicha. Cobertura divide por todos los mensajes; exactitud, por los destinos automáticos; fraude perdido, por los fraudes reales. Revisión no cuenta como pérdida. Las falsas alertas dividen por no fraudes: 1,13% para NB y 5,32% para KNN. Revisión divide por todos: 0,50% y 3,85%. La cobertura manual significa decisiones ya realizadas, no automatización.

KNN evita tres fraudes perdidos adicionales, pero agrega carga de alertas y revisión. Sus otros errores automáticos son menos; por eso una comparación de costos debe separar categorías. La sensibilidad hipotética en OOF usa `ΔC = −22*c_fraude + 252*c_alerta − 93*c_otro + 168*c_revision`: KNN se favorece con resultado negativo, NB con positivo. Cada costo corresponde a una categoría distinta; no se suma nuevamente el total de errores.

En Sprint 3 se consultó esta prueba para elegir KNN. La revisión reconoce ese antecedente: la recomendación actual no constituye una confirmación independiente de prueba. OOF también reutiliza datos que participaron en selección de parámetros y umbrales, y puede resultar optimista. No cambiamos decisiones técnicas para mejorar prueba ni creamos otra división como supuesta muestra independiente; se necesitan datos etiquetados nuevos.

Analizamos diez de los 92 errores automáticos de Naive Bayes. Hay consultas con varias intenciones y pedidos sin contexto, incluido un fraude cuyo texto no explica el problema. Un caso etiquetado como préstamos denuncia acceso sin permiso: se señala como posible inconsistencia a revisar, sin modificar la referencia. Las descripciones están anonimizadas.

## Proyección diaria y mensajes nuevos

Para 6.500 mensajes usamos la fracción de cortos `70/8000`: 56,9 revisiones por textos cortos y 6.443,1 mensajes aptos. Aplicamos las proporciones de prueba sólo a los aptos:

| Cantidad esperada por día | Naive Bayes | KNN |
| --- | ---: | ---: |
| Destinos automáticos | 6.410,6 | 6.195,3 |
| Automáticos correctos | 6.036,9 | 5.740,3 |
| Automáticos incorrectos | 373,8 | 455,0 |
| Fraudes enviados a otro equipo | 36,6 | 24,4 |
| Falsas alertas de fraude | 65,0 | 304,7 |
| Revisión humana total, incluyendo cortos | 89,4 | 304,7 |

La referencia manual sobre la misma fracción apta estima 1.060,3 derivaciones incorrectas y 239,7 fraudes mal derivados. No estimamos el resultado de la atención de los cortos ni de las revisiones. Las cantidades son expectativas si la distribución futura se parece a la muestra, no un día medido ni resultados OOF. Fraude perdido y alertas falsas ya están incluidos en errores automáticos.

Reentrenamos Naive Bayes con los **7.930 históricos aptos**, `alpha=0.1`, unigramas y bigramas, `min_df=2` y los umbrales conservados. Los 2.040 mensajes nuevos produjeron **2.007 destinos automáticos y 33 revisiones**, incluidas 15 por textos cortos. No tienen etiquetas finales para medir exactitud. El CSV validado conserva filas, identificadores y orden originales y queda local; antes de regenerarlo se respaldó el resultado anterior de KNN fuera del repositorio público. El PDF contiene sólo agregados.

Los criterios oficiales siguen pendientes de confirmación. También deben acordarse riesgo tolerable, costos relativos, capacidad de revisión y calidad de anotación. La recomendación provisional no demuestra aptitud para producción.

## Privacidad

Los archivos incluyen identificadores de clientes y textos sobre operaciones financieras. Una búsqueda preliminar encontró secuencias numéricas largas en 653 históricos y 166 mensajes nuevos; también hay referencias a DNI. Esto no confirma que sean datos reales ni que estén anonimizados. Sin autorización de publicación, los CSV quedan fuera del repositorio público. La documentación contiene agregados, ejemplos didácticos inventados y descripciones anonimizadas de errores reales, sin transcripciones de clientes.
