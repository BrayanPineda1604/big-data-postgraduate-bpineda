# Controles y guía del docente

Los controles siguientes corresponden únicamente al corte fechado suministrado. Si cambia una fuente, volver a ejecutar los scripts y publicar otra versión del manifiesto. El número de registros no se impone como condición universal de calidad; sirve para comprobar que todos trabajan con la misma entrada.

| Control | Referencia |
| --- | --- |
| AGROSAVIA entrada | 92.738 |
| Duplicados exactos | 0 |
| Aptos para analizar pH | 92.727 |
| Revisión por pH no numérico | 11 |
| Territorio sin enlace exacto | 2.138 |
| EVA entrada | 166.732 |
| EVA apto para cociente | 159.616 |
| Grupos agrícolas | 107.620 |
| Grupos agrícolas con pH | 55.498 |
| Intersecciones de muestras IGAC | 15 |

## Respuestas orientadoras

- Duplicado no equivale a repetición legítima: dos análisis de una misma localidad pueden corresponder a fechas o parcelas diferentes. Solo se eliminan copias definidas y documentadas.
- Una fila con ND en una propiedad puede servir para otra pregunta. El estado de calidad depende del producto, por ejemplo análisis de pH o rendimiento.
- Una unión muchos-a-uno conserva filas; una unión entre muestras individuales y registros agrícolas puede inflar conteos. Agregar a la unidad común antes de unir.
- La media simple de rendimientos asigna el mismo peso a áreas distintas. El cociente de sumas utiliza la superficie cosechada como ponderador dentro de grupos compatibles.
- Un mapa de cinco polígonos describe esos polígonos. El espacio no cubierto no equivale a suelo sin problemas, ni a ausencia del atributo.
- Las mediciones WoSIS por horizonte y los píxeles SoilGrids solo se comparan después de alinear profundidad, posición, método y soporte. El kit permite demostrar por qué esa validación requiere más datos.
- NASA y CHIRPS combinan fuentes y resoluciones diferentes. Comparar unidades y períodos es necesario, pero no garantiza igualdad.
- La última ventana de un flujo puede seguir abierta aunque no entren más archivos. Fin de archivos y fin de tiempo de evento son conceptos distintos.

## Contingencias durante la clase

| Situación | Acción |
| --- | --- |
| Portal DANE lento o 403 | Usar ZIP verificado del kit; mantener la descarga manual como procedimiento documentado. |
| Hash de descarga cambió | Conservar .nueva, comparar con el corte y no mezclar cohortes. |
| Pocos recursos de RAM | Dos hilos, un departamento y muestras; cerrar QGIS al ejecutar Spark si hace falta. |
| Ceros en SoilGrids sin NoData | Reportar y separar provisionalmente; no inventar corrección. |
| Código no encontrado | Registrar anti-join y revisar vigencia/nombre con evidencia. |
| Java ausente | Instalar Java 17/21 según la guía de la plataforma; comprobar antes de E07. |
| Streaming no muestra ventana final | Inspeccionar watermark y modo append; no fabricar observaciones. |

## Fuentes técnicas y metodológicas

DuckDB, lectura CSV y tipos

[Consultar fuente](<https://duckdb.org/docs/stable/data/csv/overview>)

Apache Spark 4.0.1, instalación

[Consultar fuente](<https://spark.apache.org/docs/4.0.1/api/python/getting_started/install.html>)

Apache Spark 4.0.1, Structured Streaming

[Consultar fuente](<https://spark.apache.org/docs/4.0.1/streaming/apis-on-dataframes-and-datasets.html>)

QGIS, intersección vectorial

[Consultar fuente](<https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html>)

ISRIC, propiedades y factores de SoilGrids

[Consultar fuente](<https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_01.html>)

ISRIC, WoSIS y licencias

[Consultar fuente](<https://docs.isric.org/globaldata/wosis/faq-wosis.html>)

NASA POWER, API diaria

[Consultar fuente](<https://power.larc.nasa.gov/docs/services/api/temporal/daily/>)

CHIRPS v3

[Consultar fuente](<https://chc.ucsb.edu/data/chirps3>)

UPRA, metodología EVA

[Consultar fuente](<https://upra.gov.co/es-co/eva>)

Citar entidad, nombre exacto del conjunto, versión/corte, fecha de descarga y URL. DIVIPOLA y EVA declaran CC BY-SA 4.0 en los metadatos descargados; revisar los términos de cada capa adicional y la licencia por registro de WoSIS. La copia local preserva trazabilidad y disponibilidad para la cohorte.
