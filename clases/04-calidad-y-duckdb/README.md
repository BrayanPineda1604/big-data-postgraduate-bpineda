# Clase 04 — ETL, calidad y SQL con DuckDB

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 2 · Sábado · 7 h 30 min efectivos · RA2.**

## Objetivo

Construir un flujo de limpieza y conciliar sus resultados.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Mañana · antes del receso | ETL, tipado, deduplicación exacta y prioridad de las reglas de calidad; predicción de rechazos. Ejercicio 04.1. |
| Mañana · después del receso y antes del almuerzo | Limpieza con DuckDB, cuarentena y conciliación de originales, válidos, rechazados y duplicados con esperado.json. Ejercicio 04.2. |
| Tarde · después del almuerzo y antes del receso | Consultas por ciudad y categoría; importes, exportación e inspección de CSV y Parquet. Ejercicio 04.3. |
| Tarde · después del receso | Interpretación de resultados, trazabilidad de reglas y decisión de almacenamiento; revisión del reporte de calidad para E2. Cierre de ejercicios 04.2 y 04.3. |

## Ejercicios propuestos

### 04.1 — Predicción de calidad

Revisar las reglas del script y anticipar qué sucede si una fila incumple varias. Explicar la prioridad del CASE y la deduplicación exacta.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 04.2 — Limpieza y conciliación

Ejecutar DuckDB; verificar que originales = válidos + rechazados + duplicados. Contrastar conteos e importes con esperado.json.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 04.3 — SQL y almacenamiento

Consultar pedidos e importe por ciudad; inspeccionar limpio.parquet y rechazados.csv. Añadir una consulta por categoría en un archivo propio sin alterar la referencia.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [02_calidad_duckdb.py](../../material_practico/02_calidad_duckdb.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 02_calidad_duckdb.py
```

## Entrega y revisión

E2: código o consultas, contrato, reporte de conciliación y decisión de arquitectura.

E2: 10 % del curso. Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

1 h 45 min después de esta clase: documentar reglas, resolver una consulta y redactar la decisión de arquitectura.
