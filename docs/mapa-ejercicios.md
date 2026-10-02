# Mapa de ejercicios y evaluación

[Índice](../README.md) · [Programa](programa.md) · [Calendario](calendario.md)

Las doce clases suman 64 horas efectivas. Las actividades comparten los bloques existentes: no se exige repetir todas las prácticas en ambos dominios ni ejecutar los notebooks históricos completos. Cada entrega reúne la evidencia producida en clase; una ampliación sustituye una actividad equivalente.

| Clases | Ruta y prerrequisitos | Evidencia única | Peso |
|---|---|---|---|
| 1–2 | T01 y E01–E03; P01 con las tres muestras PQRS | Pregunta, presupuesto de recursos, manifiesto, perfil y claves territoriales | 10 % |
| 3–4 | E04–E06 y P02–P03; ejecutar formatos antes de calidad PQRS | Contrato, conciliación, proyección Parquet, prueba de reejecución y consulta | 10 % |
| 5–6 | E07 después de calidad/consultas agroambientales; E08–E09 con geometrías y rásteres | Equivalencia Spark/DuckDB, cardinalidad y mapa con cobertura explícita | 10 % |
| 7–8 | E10/P04 con formatos ya preparado; I01/E11 con NASA y fuentes de clima | Un informe experimental y una traza de eventos | 20 % |
| 9–11 | E12 como práctica común de evaluación temporal; E13 en el dominio elegido | Producto candidato el 31/10, corrección y ensayo el 06/11, informe final | 35 % |
| 12 | E13 con evidencias reconstruibles | Sustentación final el 07/11 y explicación individual | 15 % |

## Orden mínimo de ejecución

Desde `kit/`, con el entorno activo:

```sh
python pqrs_talleres.py perfil
python pqrs_talleres.py formatos
python pqrs_talleres.py calidad
python pqrs_talleres.py benchmark --repeticiones 3
python pqrs_talleres.py eventos
```

Perfil, formatos, calidad y benchmark usan las muestras incluidas por defecto. Eventos requiere `data/raw/nasa.json`. P03 usa DIVIPOLA para el control territorial cuando está disponible: descargarla antes de solicitar ese control. Los notebooks actuales preparan sus pasos previos; sus celdas se distribuyen entre las clases correspondientes, no se ejecutan todas en cada encuentro.

Para la ruta agroambiental: `talleres.py calidad` → `talleres.py consultas` → `spark_taller.py lotes` o `talleres.py modelo`. Geografía necesita DANE e IGAC; `talleres.py clima` lee NASA, CHIRPS, SoilGrids y WoSIS. E11 lee NASA para Spark.

## Uso de Supersalud histórico y actual

| Material original | Actividad vigente | Ajuste didáctico |
|---|---|---|
| Sesiones históricas 1 y 2, duplicadas | P01 y P03 | Medir perfil y faltantes sin inferir anonimato o errores por edad alta |
| Sesión histórica 3 | P02 | Validar contrato y reejecución; registrar incidencias localmente, sin correo |
| Sesión histórica 4, comparación de motores | E10/P04 | CPU, consulta equivalente, calentamiento, tres repeticiones y memoria observada |
| Sesión histórica 4, índices | E12: discusión de gobernanza | Revisar variables ausentes y supuestos; no fabricar puntuaciones clínicas |
| Sesión histórica 4, bucles de streaming | I01 y E11 | Traza finita con observaciones NASA; distinguir reintentos, atraso y semántica de Spark |

## Límites del alcance

P04 ofrece una ruta con 3.000 filas y otra con 2.444.766. El corte completo requiere unos 1,816 GB de descarga más salidas y temporales. La ruta con muestras permite demostrar equivalencia en equipos limitados; no demuestra rendimiento a escala completa. En ambos casos se declara el alcance.

I01 no implementa recuperación ni toda la semántica de Spark. E11 crea un checkpoint nuevo por ejecución: el entregable básico es una traza y un análisis de recuperación, no afirmar que se probó reinicio desde el mismo estado. Un experimento de recuperación real puede sustituir una ampliación si se implementa y documenta.

E12 evalúa persistencia sobre EVA para todos los equipos. Ese resultado metodológico se identifica aparte del proyecto PQRS; no se mezcla con tasas de salud. Los proyectos PQRS pueden mostrar distribución de reportes por territorio, sin calcular tasas poblacionales si faltan denominadores compatibles y validados.
