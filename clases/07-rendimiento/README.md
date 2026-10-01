# Clase 07 — Medición y optimización

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 4 · Viernes · 3 h 45 min efectivos · RA4.**

## Objetivo

Diseñar e interpretar un experimento reproducible de formatos.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Antes del receso | Hipótesis de rendimiento, variables controladas, equipo, hilos y memoria; sesgos de caché y diseño del experimento CSV–Parquet. Ejercicio 07.1. |
| Después del receso | Ejecución del benchmark, orden alternado, calentamiento y medianas; igualdad de resultados, tamaño de archivos y límites de las conclusiones. Ejercicios 07.2 y 07.3. |

## Ejercicios propuestos

### 07.1 — Diseño experimental

Declarar hipótesis, consulta, tamaño, equipo, hilos y memoria. Identificar variables controladas y sesgos por caché.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 07.2 — Benchmark CSV–Parquet

Ejecutar el script: seis iteraciones por formato con orden alternado; excluir la iteración 0 del cálculo de la mediana, como hace el código.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 07.3 — Interpretación

Tabular medianas y tamaños de archivo. Verificar igualdad de respuestas y explicar por qué no se exige que un formato siempre gane. Proponer una mejora sin afirmar resultados no medidos.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [04_benchmark.py](../../material_practico/04_benchmark.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 04_benchmark.py
```

## Entrega y revisión

Primera parte de E4: diseño experimental, tiempos y conclusiones con límites.

Avance del informe E4 (20 % junto con streaming). Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

Sin carga adicional; la interpretación final se consolida después de la clase 8.
