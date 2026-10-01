# Big Data — Posgrado

Plan del curso y recorrido de ejercicios para **10 clases en cinco fines de semana**: **56 h 15 min sincrónicas + 7 h 45 min autónomas = 64 horas académicas**. Caso transversal: pedidos y tiempos de entrega con datos sintéticos.

**Estado:** versión inicial del plan del curso, con publicación en GitHub autorizada por Esteban Hernández.

Repositorio: [eshernan/big-data-postgraduate](https://github.com/eshernan/big-data-postgraduate).

## Índice general

- [Programa académico de 64 horas](01_Programa_academico_Big_Data_64_horas.docx): objetivos, resultados de aprendizaje, calendario y evaluación.
- [Guía académica docente](02_Guia_academica_Big_Data_material_docente.docx): desarrollo conceptual, orientaciones, rúbricas y respuestas; revisar antes de distribuir al alumnado.
- [Entorno y secuencia de ejecución](docs/entorno.md): instalación propuesta, prerrequisitos y resultados de control.
- [Material práctico](material_practico/LEEME.txt) y [dependencias](material_practico/requirements.txt).
- [Proyecto integrador y evaluación](proyecto/README.md): entregas, pesos y plantilla de evidencias.
- Fuentes existentes de generación: [construir_documentos.py](construir_documentos.py) y [contenido_guia.py](contenido_guia.py). No es necesario ejecutarlas para seguir las clases; pueden regenerar documentos y material, por lo que sus cambios deben revisarse antes de ejecutarlas.

## Plan clase a clase

Cada enlace abre objetivos, bloques temáticos, consignas, scripts y entregables. Los ejercicios son una planificación propuesta basada en el programa existente; no implican una nueva validación de los laboratorios.

| Clase | Fin de semana / día | Tema y guía | Tiempo efectivo | Ejercicios previstos | Producto |
|---|---|---|---|---|---|
| 01 | 1 / viernes | [Fundamentos y formulación del problema](clases/01-fundamentos-y-problema/README.md) | 3 h 45 min | Diagnóstico sin nota; ¿Se necesita Big Data?; Ficha del problema | Ficha inicial del problema y diagnóstico. |
| 02 | 1 / sábado | [Entorno, datos sintéticos y exploración](clases/02-entorno-y-exploracion/README.md) | 7 h 30 min | Verificación del entorno; Generación reproducible; Perfil y diccionario | E1: ficha del problema, perfil inicial y diccionario de datos. |
| 03 | 2 / viernes | [Arquitecturas, modelos y formatos](clases/03-arquitecturas-y-formatos/README.md) | 3 h 45 min | Arquitectura del caso; Comparación de formatos; Contrato de datos | Decisión de almacenamiento y borrador del contrato de datos. |
| 04 | 2 / sábado | [ETL, calidad y SQL con DuckDB](clases/04-calidad-y-duckdb/README.md) | 7 h 30 min | Predicción de calidad; Limpieza y conciliación; SQL y almacenamiento | E2: código o consultas, contrato, reporte de conciliación y decisión de arquitectura. |
| 05 | 3 / viernes | [Modelo de ejecución de Spark](clases/05-ejecucion-spark/README.md) | 3 h 45 min | Lectura del flujo; Primera ejecución; Plan de ejecución | Plan de ejecución anotado y explicación de las primeras transformaciones. |
| 06 | 3 / sábado | [Agregaciones, joins y ventanas](clases/06-consultas-joins-y-ventanas/README.md) | 7 h 30 min | Conciliación entre motores; Enriquecimiento; Ventanas y consulta adicional | E3: consultas, comparación entre motores, top 3 y justificación del plan y del join. |
| 07 | 4 / viernes | [Medición y optimización](clases/07-rendimiento/README.md) | 3 h 45 min | Diseño experimental; Benchmark CSV–Parquet; Interpretación | Primera parte de E4: diseño experimental, tiempos y conclusiones con límites. |
| 08 | 4 / sábado | [Streaming, ventanas y eventos tardíos](clases/08-streaming/README.md) | 7 h 30 min | Predicción de eventos; Traza de ejecución; Incidente y recuperación | E4: informe de rendimiento y streaming con mediciones, traza de eventos y análisis de incidente. |
| 09 | 5 / viernes | [Analítica, evaluación y gobernanza](clases/09-analitica-y-gobernanza/README.md) | 3 h 45 min | Objetivo y fuga de información; Línea base y modelo; Gobernanza e integración | Métricas comentadas, ficha de gobernanza y borrador del informe final. |
| 10 | 5 / sábado | [Integración, reproducibilidad y defensa](clases/10-integracion-y-defensa/README.md) | 7 h 30 min | Ejecución integrada; Revisión cruzada; Defensa y reflexión | E5: proyecto e informe de 8–12 páginas. E6: presentación de 8–10 minutos más preguntas y defensa individual. |

## Bloques de clase y trabajo autónomo

Los viernes se organizan en dos bloques: **antes del receso** y **después del receso**. Los sábados se organizan en cuatro bloques: **mañana antes y después del receso**, y **tarde antes y después del receso**, con el almuerzo entre ambas jornadas. Cada guía de clase detalla los temas y ejercicios de cada segmento, sin horas de inicio o finalización.

La carga efectiva se mantiene en **3 h 45 min por viernes** y **7 h 30 min por sábado**, sin contar recesos ni almuerzo. Las fechas están pendientes del calendario institucional.

| Módulo / clases | Sincrónico | Autónomo | Actividad autónoma | Total |
|---|---|---|---|---|
| 1 / 1–2: fundamentos y problema | 11 h 15 min | 45 min | Precisar problema y diccionario después de clase 2 | 12 h |
| 2 / 3–4: arquitectura y calidad | 11 h 15 min | 1 h 45 min | Documentar reglas, consulta y arquitectura después de clase 4 | 13 h |
| 3 / 5–6: Spark | 11 h 15 min | 1 h 45 min | Consolidar pipeline, consulta y join después de clase 6 | 13 h |
| 4 / 7–8: rendimiento y eventos | 11 h 15 min | 1 h 45 min | Interpretar mediciones e incidente después de clase 8 | 13 h |
| 5 / 9–10: analítica e integración | 11 h 15 min | 1 h 45 min | Preparar informe y presentación antes de clase 10 | 13 h |
| Total | 56 h 15 min | 7 h 45 min | | 64 h |

La instalación del estudiante forma parte de la clase 2. Los ejercicios de ampliación sustituyen actividades equivalentes y no agregan carga obligatoria. La variante de 64 horas completamente sincrónicas del programa requiere dos encuentros adicionales y no es la distribución adoptada aquí.

## Organización del repositorio

```text
big-data-postgraduate/
├── README.md
├── clases/                    # Diez carpetas numeradas, cada una con su guía
├── docs/entorno.md             # Preparación y dependencias entre laboratorios
├── proyecto/README.md         # Evaluación y entrega integradora
├── material_practico/         # Seis scripts compartidos, LEEME y requirements
├── 01_Programa_academico_Big_Data_64_horas.docx
├── 02_Guia_academica_Big_Data_material_docente.docx
├── construir_documentos.py
└── contenido_guia.py
```

Los scripts permanecen juntos porque comparten `material_practico/datos/` mediante rutas relativas. Las carpetas de clases enlazan a esos archivos. Los originales de `output/Curso_Big_Data` permanecen en su ubicación; no se incluyen aquí archivos temporales, datos generados ni paquetes ZIP.

## Próximas decisiones

Confirmar fechas, revisar la planificación por clase, validar el entorno Windows y definir la licencia. El repositorio se publica inicialmente con visibilidad privada.
