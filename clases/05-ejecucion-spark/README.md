# Clase 05 — Modelo de ejecución de Spark

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 3 · Viernes · 3 h 45 min efectivos · RA3.**

## Objetivo

Explicar evaluación diferida, particiones, acciones y transformaciones.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Antes del receso | Arquitectura de Spark: driver, ejecutores y particiones; SparkSession, evaluación diferida, transformaciones y acciones. Ejercicio 05.1. |
| Después del receso | Ejecución local del procesamiento por lotes; trabajos, etapas, agregaciones e intercambios en explain(formatted); límites del modo local. Ejercicios 05.2 y 05.3. |

## Ejercicios propuestos

### 05.1 — Lectura del flujo

Identificar SparkSession, lectura, transformaciones y acciones en el script de lotes; dibujar driver y ejecutores.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 05.2 — Primera ejecución

Con las salidas de la clase 4 disponibles, ejecutar el script de Spark. Identificar qué operaciones disparan trabajos y revisar el resumen.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 05.3 — Plan de ejecución

Leer explain(formatted), localizar agregaciones e intercambios y explicar qué puede observarse en local[2] y qué no demuestra sobre un clúster.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [03_spark_lotes.py](../../material_practico/03_spark_lotes.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 03_spark_lotes.py
```

## Entrega y revisión

Plan de ejecución anotado y explicación de las primeras transformaciones.

Avance formativo de E3. Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

Sin carga adicional; la consolidación se asigna después de la clase 6.
