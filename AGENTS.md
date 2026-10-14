# Instrucciones permanentes del proyecto Cauce

## Alcance y fuentes

Este trabajo universitario desarrolla solamente el Escenario 1, Cauce. El material
docente de `caso1_cauce/` define las consignas. Las instrucciones del usuario
definen qué sprint ejecutar; los ejercicios de los materiales complementarios
son referencias de estudio y no autorizan ampliar el trabajo.

Leé `docs/seguimiento.md`, `docs/requisitos.md` y `docs/roadmap.md` antes de avanzar.
El Sprint 0 sólo permite análisis, organización y preparación. No comiences el
Sprint 1 sin una nueva instrucción del usuario. No completes funciones ni celdas
del notebook durante el Sprint 0.

## Reglas para todos los sprints

- Escribí documentación, reportes y mensajes completos de commit en español de
  Argentina, con lenguaje claro y académico. Explicá los conceptos importantes.
- Antes de cambiar archivos, revisá estado, rama, historial y remotos de Git.
  `origin` debe ser `https://github.com/juanquiros/ml-cauce-naive-bayes.git`.
- Usá ramas adecuadas, commits lógicos y descriptivos. No hagas force push ni
  sobrescribas trabajo ajeno. Publicá sólo cuando haya autorización y acceso;
  informá el resultado real, los SHA y cualquier limitación.
- Preservá los datasets originales, los tests del docente y `conftest.py`.
  Nunca modifiques pruebas para hacer pasar una implementación. En el Sprint 0
  también se preservan íntegros los módulos y el notebook originales.
- No incorpores `caso2_nodo/`, aplicaciones web, APIs, bases de datos, Docker,
  autenticación, cloud ni infraestructura comercial. Priorizá la solución sencilla.
- Usá Python 3.10 o superior y las dependencias docentes de `requirements.txt`.
  Naive Bayes se implementará con NumPy; su matemática no puede importar SciPy
  ni delegarse a `sklearn.naive_bayes`. La herencia de scikit-learn está permitida.
  La limpieza usa biblioteca estándar; la derivación usa sólo NumPy.
- KNN se compara con scikit-learn, TF-IDF, coseno y búsqueda `brute`.
- Respetá las etiquetas reales. La entrada del modelo es el texto; el objetivo
  es `equipo_final`. No uses `equipo_derivado`, identificadores ni metadatos como
  features. Ajustá vocabulario, IDF e hiperparámetros sólo con entrenamiento.
- No inventes métricas, metas, umbrales ni resultados. Diferenciá exigencias del
  docente, propuestas propias y decisiones pendientes. Los cinco indicadores
  completos y sus metas requieren confirmación docente (ver requisitos).
- La prioridad de fraude utiliza `>=`, según el módulo original. Los valores de
  los tests son ejemplos de prueba, no umbrales elegidos para Cauce.
- Antes de publicar datos, verificá visibilidad del repo y privacidad. Los CSV
  actuales están excluidos del repositorio público por riesgo de exposición.
  No los fuerces con `git add -f`; no borres ni anonimices los originales.
  Cualquier copia transformada futura requiere trazabilidad y revisión explícita.
- No publiques textos sensibles ni salidas de notebooks que los contengan.
  Revisá también reportes, predicciones y archivos auxiliares.
- Registrá comandos y resultados reales, limitaciones y decisiones en `docs/`.
  Actualizá seguimiento en cada sprint. Antes de la entrega final: pruebas
  docentes aprobadas y notebook reiniciado y ejecutado completo, cuando corresponda.
