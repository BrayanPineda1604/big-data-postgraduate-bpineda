# Modo de presentar y conducir el curso

Preparado por el PhD Esteban Hernández, CyberColombia.

La presentación institucional introduce la pregunta y el concepto. La guía contiene pasos, datos y criterios. El notebook permite observar y modificar el procedimiento. El cierre exige evidencia propia y una explicación del resultado. Cada recurso tiene una función y los mismos IDs de actividad.

## Ritmo de cada bloque online

- Abrir con una pregunta verificable y declarar el dato o supuesto que se usará.
- Exponer un concepto durante 10–20 min y demostrar una operación breve con el archivo real.
- Trabajar en salas de dos o tres estudiantes con una consigna y producto concreto. Alternar quién ejecuta, quién revisa y quién documenta.
- Compartir una tabla o control agregado y discutir unidades, denominador y límite de interpretación.
- Registrar en entregas/ el resultado y la decisión. El docente consulta los controles del corte y evita evaluar solo la cantidad de herramientas utilizadas.

## Presentaciones centrales y material de ampliación

Sesión 1: cinco V, restricciones y ficha de problema. Sesión 2: ingesta, perfil y códigos. Sesión 3: formatos, contrato y reejecución. Sesión 4: calidad, consulta e integración. La introducción a eventos se ubica en la sesión 8. Las presentaciones vigentes distribuyen Spark, rendimiento, eventos y analítica en las sesiones 5, 7, 8 y 9. No requieren ejecutar Spark ni instalar Dask, GPU o plataformas gestionadas en el primer fin de semana.

## Datos observados y supuestos de capacidad

Los tamaños descargados y conteos del kit se identifican como observados. T01 trabaja escenarios de capacidad, no descargas de esos tamaños. Fórmulas: RAM estimada = factor de materialización × bytes; tiempo aislado = bytes/tasa efectiva; cola acumulada = (entrada − servicio) × tiempo mientras la entrada supera al servicio. Los factores son hipótesis que deben medirse para un equipo y carga de trabajo concretos.

| Tamaño hipotético | RAM si factor = 3 | Descarga a 12,5 MB/s |
| --- | --- | --- |
| 2 GB | 6 GB | 2 min 40 s |
| 20 GB | 60 GB | 26 min 40 s |
| 2 TB | 6 TB | 44 h 26 min 40 s |

Unidades decimales. Los tiempos son estimaciones de operaciones aisladas, sin sumarlos como un pipeline universal. Streaming, filtros, caché, compresión y concurrencia pueden cambiar las medidas. T01: 25 min para calcular la tabla, comparar un portátil con 10 GB de RAM utilizable y justificar el procesamiento por bloques o remoto. Entrega: estrategia por tamaño, restricciones y dos supuestos.

## Profundidad de posgrado

Cada taller pide hipótesis, criterio de aceptación, evidencia y una crítica. Una operación correcta se acompaña de cardinalidad, procedencia, unidades y condiciones en las que el resultado deja de ser válido. La ampliación puede investigar un método o motor diferente, pero no añade otra entrega obligatoria fuera de las 64 horas.

## Matriz de coherencia

| Sesiones | Evidencia central | Recursos |
| --- | --- | --- |
| 1–2 | Ficha, manifiestos y perfil | E01–E03, P01, T01 |
| 3–4 | Parquet, contratos y controles | E04–E06, P02–P03 |
| 5–6 | Equivalencia, consultas y mapas | E07–E09 |
| 7–8 | Rendimiento y traza de eventos | E10–E11, P04, I01 |
| 9–10 | Evaluación temporal y auditoría | E12–E13 |
| 11–12 | Correcciones y defensa final | E13 |

## Entorno de referencia

Todas las instalaciones de Python, entornos virtuales, bibliotecas y herramientas del curso parten de [WSL 2 con Ubuntu-26.04](instalacion-wsl.md). Los scripts y notebooks se ejecutan en el entorno de Ubuntu descrito allí.
