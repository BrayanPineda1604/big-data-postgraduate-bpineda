# Clase 04 — Calidad y rendimiento agrícola

[Índice](../../README.md) · [Entorno y descarga](../../docs/entorno.md) · [Datos](../../docs/datasets.md)

Fin de semana 2 · Sábado · 7 h 30 min efectivas.

## Bloques temáticos

| Segmento | Temas y actividades |
|---|---|
| Mañana · antes del receso | Tipos, ausencias, duplicados y rendimiento t/ha. |
| Mañana · después del receso | E05: calidad AGROSAVIA y conciliación. |
| Tarde · después del almuerzo y antes del receso | E06: EVA, SQL y unión territorial. |
| Tarde · después del receso | Cobertura del cruce y revisión entre pares; Entrega del pipeline y tarea autónoma. |

## Talleres y evidencias

### [E05 Calidad de análisis de suelo](../../talleres/E05.md)

Construir un flujo auditable que conserve los datos que requieren revisión y calcule poblaciones analíticas explícitas.

**Entrega:** Para este corte: 92.738 originales = 0 duplicados exactos + 92.727 aptos para pH + 11 en revisión. 2.138 registros requieren revisar correspondencia territorial. Entregar reporte, reglas y dos ejemplos comentados.

### [E06 Rendimiento agrícola e integración SQL](../../talleres/E06.md)

Calcular indicadores con denominadores correctos y conectar datos de suelo con producción sin multiplicar filas.

**Entrega:** 159.616 filas EVA cumplen el dominio del cociente. Se obtienen 107.620 grupos municipio–cultivo–estado–año; 55.498 tienen pH agregado en el cruce. El LEFT JOIN debe conservar los 107.620 grupos.

## Preparación y trabajo autónomo

Conservar los archivos originales y verificar su SHA-256. Consultar en cada taller los datos necesarios, tamaños, comandos y criterios de revisión. Las descargas no se sustituyen por datos inventados.

Fin de semana 2: 1 h 45 min para revisar territorios sin correspondencia y documentar el contrato de calidad.
