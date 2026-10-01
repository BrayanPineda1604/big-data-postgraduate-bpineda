# Clase 08 — Streaming, ventanas y eventos tardíos

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 4 · Sábado · 7 h 30 min efectivos · RA4.**

## Objetivo

Interpretar microbatches, tiempo de evento, watermark y estado.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Mañana · antes del receso | Microbatches, tiempo de evento y tiempo de procesamiento; predicción de los cinco lotes y ventanas de cinco minutos. Ejercicio 08.1. |
| Mañana · después del receso y antes del almuerzo | Ejecución del flujo de eventos; actualizaciones de consola, query.lastProgress y avance del watermark de diez minutos. Ejercicio 08.2. |
| Tarde · después del almuerzo y antes del receso | Eventos tardíos, estado y checkpoint; análisis del último evento y de un incidente de recuperación. Ejercicio 08.3. |
| Tarde · después del receso | Límites de la demostración de recuperación; interpretación de la traza e integración con el informe de rendimiento para E4. Cierre de ejercicios 08.2 y 08.3. |

## Ejercicios propuestos

### 08.1 — Predicción de eventos

Leer los cinco lotes antes de ejecutar. Asignar eventos a ventanas de cinco minutos y distinguir orden de llegada de tiempo de evento.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 08.2 — Traza de ejecución

Ejecutar streaming; registrar las actualizaciones de consola y query.lastProgress por lote. Explicar el watermark de diez minutos a partir del avance observado.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 08.3 — Incidente y recuperación

Analizar el último evento tardío, estado y checkpoint. Documentar un fallo hipotético y cómo verificar su recuperación: el script crea un directorio nuevo por ejecución y no prueba recuperación durable.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [05_streaming.py](../../material_practico/05_streaming.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 05_streaming.py
```

## Entrega y revisión

E4: informe de rendimiento y streaming con mediciones, traza de eventos y análisis de incidente.

E4: 20 % del curso. Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

1 h 45 min después de esta clase: interpretar mediciones y documentar el incidente de streaming.
