# Clase 06 — Territorio y propiedades del suelo

[Índice](../../README.md) · [Entorno y descarga](../../docs/entorno.md) · [Datos](../../docs/datasets.md)

Fin de semana 3 · Sábado · 7 h 30 min efectivas.

## Bloques temáticos

| Segmento | Temas y actividades |
|---|---|
| Mañana · antes del receso | E07: validación de resultados y joins. |
| Mañana · después del receso | E08: shapes DANE e intersección IGAC. |
| Tarde · después del almuerzo y antes del receso | E09: SoilGrids, WoSIS y escala espacial. |
| Tarde · después del receso | QGIS, mapas, cobertura y limitaciones; Entrega geográfica y tarea autónoma. |

## Talleres y evidencias

### [E07 Spark y equivalencia de resultados](../../talleres/E07.md)

Comprender ejecución distribuida y demostrar que cambiar de motor no debe alterar el significado del cálculo.

**Entrega:** control_spark.json debe indicar cero diferencias respecto a DuckDB para el corte docente. Entregar un plan explicado y una consulta de ventana.

### [E08 Shapes y capacidad de uso](../../talleres/E08.md)

Integrar geometrías oficiales y calcular áreas de intersección sin confundir las muestras temáticas con cobertura completa.

**Entrega:** 1.122 geometrías municipales leídas y 15 intersecciones de área positiva en la copia suministrada. Entregar mapa, tabla y explicación del denominador territorial.

### [E09 Propiedades del suelo y profundidad](../../talleres/E09.md)

Distinguir clases cartográficas, mediciones por horizonte y predicciones ráster, evitando comparaciones sin soporte espacial.

**Entrega:** Reporte de unidades, método y profundidad; 1.660 celdas con pH positivo dentro del dominio tras separar los 188 ceros. Entregar un mapa con alcance y una lista de condiciones para validar predicciones.

## Preparación y trabajo autónomo

Conservar los archivos originales y verificar su SHA-256. Consultar en cada taller los datos necesarios, tamaños, comandos y criterios de revisión. Las descargas no se sustituyen por datos inventados.

Fin de semana 3: 1 h 45 min para interpretar planes, corregir mapas y explicar cobertura.
