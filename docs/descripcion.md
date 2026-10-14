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

La distribución no es uniforme: fraude tiene menos ejemplos que transferencias. Hay 72 históricos con menos de dos palabras **antes de limpiar**. Ese número se volverá a calcular sobre `texto_limpio` en el paso 5.

| Canal | Históricos | Nuevos |
| --- | ---: | ---: |
| `app_chat` | 3.676 | 927 |
| `whatsapp` | 2.499 | 591 |
| `email` | 1.163 | 310 |
| `formulario_web` | 862 | 212 |

En la próxima etapa se quitarán los duplicados del histórico en una copia de trabajo, conservando el primero, antes de dividir entrenamiento y prueba. Los originales seguirán intactos. Las 2.040 filas nuevas deberán conservarse para la entrega, incluso si hay duplicados o mensajes que requieran revisión.

## Línea base de la derivación manual

Comparando `equipo_derivado` con `equipo_final` en las 8.200 filas originales:

- 6.774 derivaciones correctas: **82,61% de exactitud**.
- 1.426 errores: **17,39%**.
- F1 macro: **0,8166**, dando el mismo peso a cada equipo.
- 290 de los 914 mensajes de fraude llegaron a otro sector: **31,73% del fraude real**.
- 256 mensajes de otros sectores fueron enviados a fraude.

Estos números describen la mesa de entrada; todavía no hay resultados de modelos entrenados. La referencia del escenario, aproximadamente un error cada seis mensajes, es coherente con esta muestra, pero no reemplaza la medición.

## Cómo vamos a resolverlo y evaluarlo

Naive Bayes multinomial permite aprender relaciones entre palabras y equipos mediante conteos. Su entrenamiento y su predicción son sencillos y rápidos. KNN servirá para comparar esa forma de clasificar con la búsqueda de mensajes históricos parecidos, usando TF-IDF y coseno.

Vamos a comparar accuracy, precision, recall y F1 por clase, F1 macro y matrices de confusión. También se medirá el tiempo de predicción. La regla final agregará cobertura automática, exactitud entre los casos automáticos y fraude perdido: los fraudes enviados automáticamente a otro equipo. La revisión humana no cuenta como fraude perdido en esa definición.

Los umbrales se elegirán con probabilidades fuera de muestra del entrenamiento. El conjunto de prueba se usará una sola vez para la evaluación final. Todavía faltan confirmar los cinco indicadores completos y sus metas de aceptación que menciona el paso 15.

## Privacidad

Los archivos incluyen identificadores de clientes y textos sobre operaciones financieras. Una búsqueda preliminar encontró secuencias numéricas largas en 653 históricos y 166 mensajes nuevos; también hay referencias a DNI. Esto no confirma que sean datos reales ni que estén anonimizados. Sin autorización de publicación, los CSV quedan fuera del repositorio público. La documentación contiene sólo agregados y ejemplos inventados, sin mensajes completos de clientes.
