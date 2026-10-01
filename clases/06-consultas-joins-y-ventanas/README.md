# Clase 06 — Agregaciones, joins y ventanas

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 3 · Sábado · 7 h 30 min efectivos · RA3.**

## Objetivo

Reproducir consultas entre motores y justificar joins y ventanas.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Mañana · antes del receso | Agregaciones por ciudad y conciliación exacta de conteos e importes entre DuckDB y Spark. Ejercicio 06.1. |
| Mañana · después del receso y antes del almuerzo | Enriquecimiento ciudad–región: left join, broadcast, conservación de filas, claves duplicadas y regiones nulas. Ejercicio 06.2. |
| Tarde · después del almuerzo y antes del receso | Ventanas, row_number, top 3 por ciudad y desempate por id; consulta adicional por categoría. Ejercicio 06.3. |
| Tarde · después del receso | Comparación de la consulta adicional entre motores, interpretación del plan y justificación del join; revisión de E3. Cierre de ejercicios 06.2 y 06.3. |

## Ejercicios propuestos

### 06.1 — Conciliación entre motores

Ejecutar nuevamente el script y comprobar igualdad exacta de conteos e importes por ciudad entre DuckDB y Spark.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 06.2 — Enriquecimiento

Explicar el left join y broadcast de la dimensión ciudad–región. Comprobar conservación de filas y ausencia de regiones nulas; discutir claves duplicadas.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 06.3 — Ventanas y consulta adicional

Verificar los tres pedidos de mayor importe por ciudad y el desempate por id. Implementar una agregación por categoría y compararla con DuckDB.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [03_spark_lotes.py](../../material_practico/03_spark_lotes.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 03_spark_lotes.py
```

## Entrega y revisión

E3: consultas, comparación entre motores, top 3 y justificación del plan y del join.

E3: 10 % del curso. Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

1 h 45 min después de esta clase: consolidar el pipeline, añadir la consulta y justificar el join.
