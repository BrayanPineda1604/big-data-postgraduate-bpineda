# Clase 10 — Integración, reproducibilidad y defensa

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 5 · Sábado · 7 h 30 min efectivos · RA1–RA5.**

## Objetivo

Demostrar y defender una solución completa y reproducible.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Mañana · antes del receso | Reproducibilidad del flujo completo: versiones, orden de ejecución, calidad, conciliación, mediciones, eventos y métricas. Ejercicio 10.1. |
| Mañana · después del receso y antes del almuerzo | Revisión cruzada de código, evidencias y límites; resolución y registro de incidencias; preparación de la defensa. Ejercicio 10.2. |
| Tarde · después del almuerzo y antes del receso | Presentación de proyectos y sustentación individual: decisiones de arquitectura, calidad, procesamiento y rendimiento. Ejercicio 10.3. |
| Tarde · después del receso | Continuación de sustentaciones; evaluación analítica, gobernanza, limitaciones y reflexión individual; retroalimentación y cierre de E5 y E6. Ejercicio 10.3. |

## Ejercicios propuestos

### 10.1 — Ejecución integrada

Reproducir el flujo completo con las instrucciones y versiones del equipo; verificar conteos, conciliación, benchmark, eventos y métricas.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 10.2 — Revisión cruzada

Otro equipo revisa orden de ejecución, evidencias y límites. Resolver incidencias y registrar qué pudo verificarse.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 10.3 — Defensa y reflexión

Presentar el proyecto, justificar decisiones y responder individualmente sobre calidad, Spark, rendimiento y evaluación. Registrar limitaciones y próximos pasos.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [01_generar_datos.py](../../material_practico/01_generar_datos.py)
- [02_calidad_duckdb.py](../../material_practico/02_calidad_duckdb.py)
- [03_spark_lotes.py](../../material_practico/03_spark_lotes.py)
- [04_benchmark.py](../../material_practico/04_benchmark.py)
- [05_streaming.py](../../material_practico/05_streaming.py)
- [06_modelo.py](../../material_practico/06_modelo.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 01_generar_datos.py --n 20000
python 02_calidad_duckdb.py
python 03_spark_lotes.py
python 04_benchmark.py
python 05_streaming.py
python 06_modelo.py
```

## Entrega y revisión

E5: proyecto e informe de 8–12 páginas. E6: presentación de 8–10 minutos más preguntas y defensa individual.

E5: 35 %; E6: 15 %. Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

Sin trabajo autónomo posterior obligatorio.

Con más de ocho equipos, distribuir defensas también en la mañana o usar evaluadores adicionales, conservando la carga horaria.
