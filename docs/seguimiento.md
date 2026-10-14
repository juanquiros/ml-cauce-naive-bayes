# Seguimiento del proyecto Cauce

Última revisión: 14/10/2026. Convención: `[ ]` pendiente, `[x]` completado.
Los siguientes sprints requieren nuevas instrucciones del usuario.

## Sprint 0 · Completado

- [x] Revisar estado, rama, historial y remotos antes de cambiar archivos.
- [x] Verificar remoto vacío y visibilidad pública; configurar origin correcto.
- [x] Encontrar y analizar los ocho materiales indicados.
- [x] Recuperar sólo Cauce y requirements; sin incorporar Nodo.
- [x] Verificar doce archivos originales byte a byte contra el ZIP y guardar hashes.
- [x] Identificar 20 pasos, siete reflexiones, dependencias y sprints.
- [x] Revisar contratos, fórmulas, restricciones y todas las pruebas.
- [x] Cargar CSV con pandas; auditar clases, tipos, nulos, vacíos, duplicados y canales.
- [x] Calcular línea base exploratoria sin entrenar modelos ni resolver el notebook.
- [x] Crear entorno, instalar requisitos, verificar pip y registrar pytest inicial.
- [x] Proteger CSV locales; publicar sólo evidencia agregada y recuperación por ZIP.
- [x] Crear roadmap, conceptos, requisitos, seguimiento y diagnóstico.
- [x] Crear README, .gitignore y reglas permanentes en AGENTS.
- [x] Revisar coherencia, enlaces, alcance e integridad de entregables.
- [x] Registrar SHA de commits y resultado real de publicación en el cierre de Git.

Criterio de finalización verificado: documentación y evidencia revisadas,
originales preservados, sin algoritmos implementados y cambios versionados y
publicados. No constituye autorización para iniciar S1.

## Sprint 1 · Pendiente · Pasos 1–6

- [ ] Completar exploración y línea base en el notebook, incluyendo palabras por clase.
- [ ] Deduplicar en una copia conservando el primero; justificar antes del split.
- [ ] Implementar quitar_tildes y limpiar_texto; mostrar cinco ejemplos seguros.
- [ ] Crear texto_limpio; identificar/excluir cortos de training y destinarlos a revisión.
- [ ] Implementar log_suma_exp, estimador NB y términos indicativos con NumPy.
- [ ] Aprobar 15 casos de limpieza y 12 de NB sin modificar los tests.
- [ ] Actualizar explicaciones, decisiones, evidencia y commits.

Finalización: pasos 1–6 resueltos y pruebas de esos módulos aprobadas; originales
CSV intactos. La derivación y el entrenamiento experimental quedan para después.

## Sprint 2 · Pendiente · Pasos 7–12

- [ ] Hacer split 80/20 estratificado con semilla 42 y reservar test final.
- [ ] Verificar 100% de igualdad de etiquetas con MultinomialNB, alpha 1.
- [ ] Mostrar e interpretar diez términos por clase.
- [ ] Optimizar NB con CountVectorizer, cinco folds estratificados y F1 macro.
- [ ] Optimizar KNN con TF-IDF, coseno y brute; justificar hiperparámetros/métrica.
- [ ] Comparar predicción de 1.000 mensajes con los cuatro tamaños docentes.
- [ ] Mantener pipelines sin fuga y registrar condiciones de medición.

Finalización: búsquedas, interpretaciones y tiempos reproducibles; modelos elegidos
por validación. No elegir reglas mirando el test final.

## Sprint 3 · Pendiente · Pasos 13–20

- [ ] Confirmar lista de cinco indicadores, fórmulas, metas y margen de seguridad.
- [ ] Resolver convenciones de casos límite y de exportación de mensajes cortos.
- [ ] Implementar derivación/evaluación y aprobar sus cuatro casos.
- [ ] Elegir umbrales mediante probabilidades OOF en entrenamiento para ambos modelos.
- [ ] Evaluar una vez en test: tabla de NB/KNN/mesa, reporte y matriz del elegido.
- [ ] Analizar diez errores y una mejora por error; proyectar impacto diario.
- [ ] Reentrenar elegido, conservar 2.040 filas nuevas y validar CSV de cinco columnas.
- [ ] Responder las siete reflexiones con resultados experimentales.
- [ ] Entregar informe ejecutivo PDF aparte para Laura Benítez.
- [ ] Verificar 31 casos docentes, reiniciar y ejecutar todo el notebook.
- [ ] Revisar privacidad de salidas y documentar conclusión de aceptación.

## Pruebas y evidencias actuales

| Verificación | Estado real S0 | Evidencia |
| --- | --- | --- |
| Instalación de requirements | Completada en .venv/Python 3.12.14. | `evidencias/entorno_sprint0.txt` |
| pip check | Sin requisitos incompatibles. | Diagnóstico y salida registrada en la sesión. |
| Limpieza | 15 casos fallidos esperados. | `evidencias/pytest_inicial.txt` |
| Naive Bayes | 11 fallidos esperados y 1 aprobado estático. | Mismo registro. |
| Derivación | 4 fallidos esperados. | Mismo registro. |
| Total pytest | 31 casos, 30 fallidos por pendientes, 1 aprobado; salida 1. | Inventario técnico y registro. |
| Auditoría CSV | Ejecutada sin modificación. | `evidencias/auditoria_datos.json` |
| Originales del ZIP | 12/12 coinciden byte a byte. | `evidencias/integridad_materiales.json` |
| Notebook resuelto / ejecución final | Pendiente para S1–S3. | No se ejecutó en S0. |

No se incorporan tests nuevos para los scripts de preparación: se verifican con
ejecuciones de recuperación idempotente y auditoría, conservando originales.

## Problemas pendientes

- [ ] P01: enunciado/rúbrica completos, cinco indicadores y valores objetivo.
- [ ] P02: justificar grillas y margen de seguridad.
- [ ] P03: convención de evaluación sin fraude, sin automáticos o lote vacío.
- [ ] P04: representación de probabilidades de nuevos sin texto suficiente.
- [ ] P05: extensión y rúbrica del PDF ejecutivo.
- [ ] P06: confirmación de carácter ficticio/autorización antes de publicar datos.
- [ ] P07: protocolo común de tiempos sin consumir test.
- [ ] P08: decisiones proporcionadas sobre entradas y empates no especificados.

Ver alcance e impacto de cada pendiente en `requisitos.md`. Son faltantes
documentados, no resultados inventados ni bloqueos de toda la implementación.

## Decisiones técnicas

| Fecha | Decisión | Motivo / fuente |
| --- | --- | --- |
| 14/10/2026 | Sólo Cauce; no modificar código, tests, notebook ni datos en S0. | Pedido del usuario y alcance académico. |
| 14/10/2026 | NB multinomial de texto con NumPy; KNN de sklearn con TF-IDF/coseno. | Contratos y pasos 6, 10 y 11. |
| 14/10/2026 | Objetivo equipo_final; sólo texto como feature. | Dataset y objetivo del escenario; prevención de fuga. |
| 14/10/2026 | Usar >= en ambos umbrales y prioridad de fraude. | Docstring y pruebas de derivación. |
| 14/10/2026 | CSV intactos locales, excluidos de GitHub público. | Riesgo de privacidad sin confirmación de datos ficticios. |
| 14/10/2026 | Entorno aislado Python 3.12.14, requisitos docentes sin cambios. | Compatibilidad >=3.10 y alias Python local no usable. |
| 14/10/2026 | No completar por suposición los cinco indicadores. | Paso 15 incompleto; módulo define sólo tres. |
| 14/10/2026 | S1 pasos 1–6; S2 pasos 7–12; S3 pasos 13–20. | Dependencias y organización solicitada. |
| 14/10/2026 | Recuperación CSV y auditoría como scripts mínimos. | Reproducibilidad sin publicar textos/identificadores ni alterar docentes. |
| 14/10/2026 | Preservar bytes originales con .gitattributes. | core.autocrlf=true; hashes idénticos también en los blobs de Git. |
| 14/10/2026 | Crear main con el commit de materiales y desarrollar documentación en codex/sprint-0. | Remoto vacío con main como rama predeterminada; permite revisar S0 mediante pull request sin reescribir historia. |

## Registro de commits importantes y publicación

| Commit | SHA | Contenido |
| --- | --- | --- |
| Preparar materiales originales de Cauce y proteger los datos locales | `276be59747f139efe277aecac6a0dd2e2c45dfbd` | Base de main: originales sin CSV, reglas permanentes, protección de datos y manifiesto. |
| Documentar el Sprint 0 y agregar auditorías reproducibles | `85ba68cb178d7ae016004089934b9cdf198adeda` | Cinco documentos obligatorios, inventario técnico, README, evidencia y scripts auxiliares. |
| Registrar el cierre verificado y la publicación del Sprint 0 | Consultar `git log -1 --format=%H -- docs/seguimiento.md` | Este cierre: checklist final y publicación comprobada. Su SHA completo se informa en el reporte de entrega. |

Rama de trabajo: `codex/sprint-0`, con seguimiento de `origin/codex/sprint-0`.
`main` contiene la base de materiales originales. Origin apunta al repositorio
solicitado. El comando `git push -u origin main codex/sprint-0` finalizó con
salida 0 y creó ambas ramas; `git ls-remote origin` confirmó sus SHA. El commit
de cierre se publica en la misma rama mediante un push adicional, sin force push.

Pull request abierto contra main:
[Preparar el Sprint 0 del proyecto académico Cauce](https://github.com/juanquiros/ml-cauce-naive-bayes/pull/1).
No se fusionó el PR. El árbol quedó limpio tras los commits y no hay CSV,
entornos virtuales ni temporales versionados. El SHA final y su coincidencia
con el remoto se verifican después del último push y se informan en la entrega.

Verificación de cierre: [verificaciones_sprint0.json](evidencias/verificaciones_sprint0.json).
También se comprobaron recuperación de CSV desde cero en una carpeta aislada,
recuperación idempotente y una segunda auditoría idéntica a la evidencia guardada.
