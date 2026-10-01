# Clase 09 — Analítica, evaluación y gobernanza

[Índice del curso](../../README.md) · [Entorno](../../docs/entorno.md) · [Proyecto y evaluación](../../proyecto/README.md)

**Fin de semana 5 · Viernes · 3 h 45 min efectivos · RA5.**

## Objetivo

Evaluar un modelo introductorio y documentar su gobernanza.

## Preparación

Revisar las evidencias de la clase anterior y conservar las salidas de los laboratorios. Consultar las dependencias de ejecución en la guía de entorno.

## Bloques de la clase

| Segmento | Temas y actividades |
|---|---|
| Antes del receso | Definición de entrega tardía, variables disponibles y fuga de información; separación temporal, línea base y regresión logística. Ejercicio 09.1 e inicio de 09.2. |
| Después del receso | Precisión, recall, F1, matriz de confusión y prevalencia; interpretación del modelo; origen, linaje, acceso, retención y límites de los datos. Cierre de 09.2 y ejercicio 09.3. |

## Ejercicios propuestos

### 09.1 — Objetivo y fuga de información

Definir entrega tardía como delivery_minutes > 60. Explicar por qué delivery_minutes no puede usarse como predictor y revisar la separación temporal.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 09.2 — Línea base y modelo

Ejecutar el script de modelo; comparar baseline y regresión logística con precisión, recall, F1, matriz de confusión y prevalencia. Interpretar resultados sin exigir superioridad del modelo.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

### 09.3 — Gobernanza e integración

Documentar origen sintético, linaje, acceso, retención y limitaciones. Revisar qué evidencias faltan para reproducir el proyecto.

**Evidencia:** registrar procedimiento, resultado y una conclusión razonada en la entrega de esta clase.

## Material y ejecución

[Programa académico](../../01_Programa_academico_Big_Data_64_horas.docx) · [Guía docente](../../02_Guia_academica_Big_Data_material_docente.docx). La guía docente contiene orientaciones y respuestas.

- [06_modelo.py](../../material_practico/06_modelo.py)

Desde `material_practico/`, con el entorno del curso activo y los prerrequisitos disponibles:

```sh
python 06_modelo.py
```

## Entrega y revisión

Métricas comentadas, ficha de gobernanza y borrador del informe final.

Avance formativo del proyecto E5. Se revisa corrección, evidencia, reproducibilidad y razonamiento; ejecutar sin explicar no completa la actividad.

## Trabajo autónomo

1 h 45 min antes de la clase 10: preparar informe y presentación; esta es la carga autónoma del módulo 5.
