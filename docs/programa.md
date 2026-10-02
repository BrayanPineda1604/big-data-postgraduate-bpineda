# Programa académico de 64 horas

Este programa desarrolla competencias de ingeniería y análisis de datos mediante el caso SUELO SABIO. Los estudiantes construirán un flujo reproducible que conecta análisis de laboratorio de suelos, división territorial, producción agrícola y fuentes agroclimáticas. La pregunta conductora es qué puede afirmarse sobre las propiedades del suelo y el rendimiento agrícola con la información pública disponible, y qué evidencia adicional hace falta para decidir a escala de parcela.

Esta edición sustituye el caso sintético de pedidos y las consignas prácticas de la edición de septiembre de 2026. Mantiene los fundamentos de Big Data y la exigencia de posgrado. Todos los ejercicios aplicados utilizan archivos abiertos originales o productos derivados trazables. Las hipótesis de escalamiento y los cambios en el orden de llegada se distinguen de observaciones reales.

## Propósito y resultados de aprendizaje

Diseñar, ejecutar y evaluar un sistema local de ingesta, calidad, integración y análisis que conserve la procedencia y el significado de los datos. El estudiante debe justificar cuándo un portátil es suficiente y qué cambiaría al crecer el volumen, la concurrencia o las exigencias de actualización.

- RA1. Formular una pregunta verificable, identificar la unidad de análisis y evaluar cobertura, licencias y límites de las fuentes.
- RA2. Descargar y verificar archivos, conservar el corte original, tipar variables y reportar datos aptos y pendientes de revisión.
- RA3. Integrar códigos territoriales, tablas y geometrías sin multiplicar observaciones ni confundir escalas espaciales.
- RA4. Comparar DuckDB y Spark local, medir formatos y explicar particiones, joins, ventanas y eventos tardíos.
- RA5. Evaluar una línea base temporal, documentar incertidumbre y defender un producto reproducible con límites explícitos.

## Bloques y carga académica

| Componente | Tiempo efectivo |
| --- | --- |
| Viernes: antes y después del receso | 3 h 45 min |
| Sábado: mañana y tarde, antes y después de cada receso; almuerzo entre jornadas | 7 h 30 min |
| Cinco fines de semana | 56 h 15 min |
| Trabajo autónomo guiado | 7 h 45 min |
| Total académico, excluidas pausas | 64 h |

Se conservan diez sesiones online, cinco viernes y cinco sábados. Las 64 horas incluyen 7 h 45 min autónomas, como en el programa anterior. La instalación y la comprobación inicial se realizan durante la sesión 2, no como una carga obligatoria adicional. Si una institución exige 64 horas exclusivamente sincrónicas, deberá programar 7 h 45 min adicionales de interacción.

## Estructura curricular

| Fin de semana | Núcleo y ejercicios | Autónomo |
| --- | --- | --- |
| 1 | Fundamentos, descarga y perfilado. E01–E03. | 45 min |
| 2 | Arquitecturas, Parquet, calidad y SQL. E04–E06. | 1 h 45 min |
| 3 | Spark, geometrías y propiedades del suelo. E07–E09. | 1 h 45 min |
| 4 | Benchmark y reproducción de eventos climáticos. E10–E11. | 1 h 45 min |
| 5 | Línea base, gobernanza e integración. E12–E13. | 1 h 45 min |

## Fundamentos que se conservan

Volumen, velocidad, variedad y veracidad; escalamiento vertical y horizontal; ley de Amdahl; latencia y throughput; ciclo de vida del dato; sistemas distribuidos y tolerancia a fallos. Warehouse, lake y lakehouse, papel de Hadoop/HDFS y modelos NoSQL se estudian mediante decisiones de arquitectura. La implementación se concentra en Python, DuckDB, Parquet, Spark local y herramientas geográficas de escritorio.

Los archivos tabulares de esta cohorte caben en un portátil. Su tamaño no demuestra una necesidad de cómputo distribuido. La complejidad surge también de esquemas heterogéneos, profundidades, fechas, escalas, geometrías y versiones territoriales. Spark local permite estudiar ejecución y planes; sus tiempos no predicen el rendimiento de un clúster.

## Evaluación

| Evidencia | Peso |
| --- | --- |
| E01–E03: procedencia, descarga y perfilado | 10 % |
| E04–E06: calidad, formatos y SQL | 10 % |
| E07–E09: Spark e integración geográfica | 10 % |
| E10–E11: experimento y eventos | 20 % |
| E12–E13: proyecto e informe técnico | 35 % |
| Sustentación individual | 15 % |

La rúbrica valora corrección y conservación de unidades (30 %), reproducibilidad y trazabilidad (25 %), justificación técnica (25 %) y comunicación de limitaciones (20 %), aplicada dentro de cada entrega. Se penaliza afirmar cobertura nacional a partir de muestras, sumar rendimientos, convertir ausencias a cero, introducir fuga temporal o presentar asociaciones como causalidad. La nota mínima y las reglas de asistencia corresponden al programa institucional.

## Producto integrador

Cada equipo presenta un pipeline ejecutable, un catálogo de fuentes, tablas Parquet, una consulta equivalente entre motores, un mapa con cobertura explícita, un experimento de rendimiento, evidencia de eventos y una evaluación temporal. El informe de 8 a 12 páginas debe separar resultados observados, estimaciones, limitaciones y propuesta de escalamiento. La defensa dura 8 minutos más 4 de preguntas; hasta ocho equipos caben en el bloque final previsto. Con más equipos se utilizan salas simultáneas y evaluadores adicionales dentro del mismo horario.
