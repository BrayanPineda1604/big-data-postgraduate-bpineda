# Big Data de posgrado — SUELO SABIO

Curso de 64 horas: diez clases en cinco fines de semana, con **56 h 15 min sincrónicas y 7 h 45 min autónomas**. Preparado por el PhD Esteban Hernández, CyberColombia.

Esta edición utiliza datos abiertos de suelos, territorio, producción agrícola y clima. Sustituye el caso de pedidos sintéticos. Repositorio público: [eshernan/big-data-postgraduate](https://github.com/eshernan/big-data-postgraduate).

## Índice del contenido vigente

- [Programa académico y resultados de aprendizaje](docs/programa.md).
- [Catálogo de 12 fuentes: alcance, tamaño, propósito y advertencias](docs/datasets.md).
- [Entorno, descarga y uso del respaldo docente](docs/entorno.md).
- [Manifiesto de URLs, bytes y SHA-256](kit/fuentes.json).
- [Kit de ejecución](kit/LEEME.txt): [descargador](kit/00_datos.py), [talleres locales](kit/talleres.py), [Spark](kit/spark_taller.py), [dependencias base](kit/requirements.txt) y [dependencias Spark](kit/requirements_spark.txt).
- [Proyecto y evaluación](proyecto/README.md).
- [Controles y orientaciones docentes](docs/controles-docente.md).
- [Verificación de esta integración](docs/validacion.md).
- [Material histórico de pedidos](historico/pedidos/README.md), conservado como referencia de la edición anterior.

## Anexo de otro dominio: Supersalud

[Notebooks docentes de Supersalud](supersalud/README.md): tres archivos históricos integrados desde `dev`, con una propuesta de uso en perfilado, calidad, Parquet y pipelines. El anexo documenta duplicaciones y ajustes pendientes antes de ejecutarlos.

## Plan clase a clase

Cada guía incluye temas por segmento y enlaces a talleres con propósito, descarga, instrucciones, resultados esperados y límites de interpretación.

| Clase | Temas y bloques | Ejercicios |
|---|---|---|
| 01 | [Fundamentos y problema](clases/01-fundamentos-y-problema/README.md) | [E01](talleres/E01.md) |
| 02 | [Descarga y perfilado](clases/02-entorno-y-exploracion/README.md) | [E02](talleres/E02.md), [E03](talleres/E03.md) |
| 03 | [Arquitecturas y formatos](clases/03-arquitecturas-y-formatos/README.md) | [E04](talleres/E04.md) |
| 04 | [Calidad y rendimiento agrícola](clases/04-calidad-y-duckdb/README.md) | [E05](talleres/E05.md), [E06](talleres/E06.md) |
| 05 | [Ejecución con Spark](clases/05-ejecucion-spark/README.md) | [E07](talleres/E07.md) |
| 06 | [Territorio y propiedades del suelo](clases/06-consultas-joins-y-ventanas/README.md) | [E07](talleres/E07.md), [E08](talleres/E08.md), [E09](talleres/E09.md) |
| 07 | [Rendimiento del procesamiento](clases/07-rendimiento/README.md) | [E10](talleres/E10.md) |
| 08 | [Clima y eventos](clases/08-streaming/README.md) | [E11](talleres/E11.md) |
| 09 | [Analítica y gobernanza](clases/09-analitica-y-gobernanza/README.md) | [E12](talleres/E12.md) |
| 10 | [Integración y defensa](clases/10-integracion-y-defensa/README.md) | [E13](talleres/E13.md) |

## Bloques y carga académica

Viernes: antes y después del receso, **3 h 45 min efectivas**. Sábado: mañana y tarde, antes y después de cada receso, con almuerzo entre jornadas, **7 h 30 min efectivas**. Las guías no fijan horas de inicio o finalización.

| Fin de semana | Clases | Sincrónico | Autónomo | Consolidación |
|---|---|---|---|---|
| 1 | 1–2 | 11 h 15 min | 45 min | Pregunta, diccionario y procedencia |
| 2 | 3–4 | 11 h 15 min | 1 h 45 min | Territorios sin correspondencia y contrato de calidad |
| 3 | 5–6 | 11 h 15 min | 1 h 45 min | Planes, mapas y cobertura |
| 4 | 7–8 | 11 h 15 min | 1 h 45 min | Mediciones y eventos tardíos |
| 5 | 9–10 | 11 h 15 min | 1 h 45 min | Informe y defensa, entre clases 9 y 10 |
| Total | 10 | 56 h 15 min | 7 h 45 min | 64 horas |

## Datos y ejecución

Los archivos originales **no se incluyen en Git**. El corte docente ocupa aproximadamente **136,4 MB**; las tres tablas principales, unos **48 MB**. Descargar con el kit o copiar el respaldo fechado y verificarlo. DANE requiere descarga manual; una fuente actualizada puede diferir del SHA-256 registrado y queda pendiente de revisión.

```sh
cd kit
python 00_datos.py --listar
python 00_datos.py --descargar agrosavia eva divipola
python talleres.py perfil
python talleres.py calidad
python talleres.py consultas
```

Instalar primero las dependencias según la guía de entorno. Para geografía y clima se necesitan sus fuentes adicionales. Consultar [E07](talleres/E07.md) y [E11](talleres/E11.md) para Spark y eventos; [E12](talleres/E12.md) evalúa una línea base de persistencia mediante MAE, con separación temporal.

Los archivos de entrada permanecen en `kit/data/raw/` y los resultados en `kit/salidas/`, ambos excluidos de Git. No descargar capas nacionales completas ni series globales cuando el ejercicio solicita una muestra o un recorte.

## Alcance de esta edición

Integración del temario y los scripts disponibles el 2 de octubre de 2026. El libro y las presentaciones de la nueva edición continúan su elaboración por separado; los Word de septiembre se conservan únicamente en el histórico. Los términos de cada fuente se consultan en su catálogo; publicar el repositorio no cambia sus licencias. La instalación en Windows sigue pendiente de validación.
