# Ejercicios de pandas y Polars

Esta carpeta contiene los enunciados y las plantillas de los ejercicios PD01–PD05. Cada estudiante crea una copia de cada notebook en `soluciones/` de su propio repositorio y desarrolla allí la solución, con el nombre indicado. Las plantillas de `ejercicios/` se conservan como material de consulta.

| Enunciado y plantilla | Ruta de la solución del estudiante |
|---|---|
| [PD01 · Explorar y preparar AGROSAVIA](PD01_exploracion_agrosavia.ipynb) | `soluciones/PD01_exploracion_agrosavia.ipynb` |
| [PD02 · Consultar y resumir EVA](PD02_consultas_eva.ipynb) | `soluciones/PD02_consultas_eva.ipynb` |
| [PD03 · Integrar EVA con DIVIPOLA](PD03_integracion_territorial.ipynb) | `soluciones/PD03_integracion_territorial.ipynb` |

## Primer bloque: cuatro horas (PD01–PD03)

Se parte del entorno del curso operativo y de los tres CSV ya descargados. La [guía práctica de pandas](../docs/manual-pandas.md) sirve como apoyo durante el desarrollo.

| Actividad | Tiempo |
|---|---:|
| Preparación, copia de plantillas y comprobación de rutas | 20 min |
| PD01 · Explorar y preparar AGROSAVIA | 60 min |
| PD02 · Consultar y resumir EVA | 70 min |
| PD03 · Integrar EVA con DIVIPOLA | 70 min |
| Reejecución y entrega | 20 min |
| **Total** | **240 min** |

## Preparación y desarrollo

La **raíz del repositorio** es la carpeta `big-data-postgraduate` que contiene `README.md`, `kit/`, `ejercicios/` y `soluciones/`. En la instalación WSL del curso se accede a ella desde la terminal con:

```bash
cd /mnt/c/Users/TUPTC/bigdata
cd big-data-postgraduate
pwd
ls
```

Si la copia del repositorio está en otra ubicación, se utiliza su ruta real. Cada notebook incluye la celda **«Ubicación de trabajo: ruta visible»**, con la ruta WSL explícita y la explicación de cómo ajustarla. Esta orientación forma parte de los 20 minutos de preparación.

1. Abrir JupyterLab desde la raíz del repositorio con el entorno `.venv` del curso activo.
2. Duplicar cada plantilla de `ejercicios/` y mover la copia a `soluciones/`, conservando el nombre de la tabla anterior. Si ya existe una solución, se continúa sobre ella.
3. Abrir la copia de `soluciones/` y seleccionar el kernel del entorno del curso.
4. Ejecutar la celda inicial de rutas y carga. Cada notebook es independiente y utiliza únicamente los CSV que necesita.
5. Completar las celdas de desarrollo e interpretación siguiendo las instrucciones. Antes de entregar, reiniciar el kernel y ejecutar todas las celdas en orden.

Los enunciados aparecen en celdas Markdown; el código se desarrolla en las celdas correspondientes. Cada actividad incluye un tiempo asignado y comprobaciones sobre los resultados.

## Archivos de entrada y resultados

Las entradas son `kit/data/raw/agrosavia.csv`, `kit/data/raw/eva.csv` y `kit/data/raw/divipola.csv`. Si falta alguna, la descarga se realiza desde la terminal, en la raíz del repositorio y con el entorno del curso activo:

```bash
python kit/00_datos.py --descargar divipola eva agrosavia
```

Los notebooks resueltos se entregan en `soluciones/`. Las tablas CSV generadas se guardan en `kit/salidas/soluciones/PD01/`, `PD02/` y `PD03/`; esas carpetas están excluidas de Git y sus archivos deben poder regenerarse al ejecutar los notebooks. Los CSV originales permanecen en `kit/data/raw/`.

## Validación de las plantillas

Para PD01–PD03 se verificaron el formato de notebook, la sintaxis de las celdas, los enlaces y la suma de los tiempos. Las celdas iniciales se ejecutaron con pandas 2.2.3 desde `ejercicios/` y desde copias en `soluciones/`, utilizando únicamente los tres CSV del manifiesto. El análisis y sus conclusiones quedan pendientes del estudiante.

## Segundo bloque: limpieza, integración y particionamiento (PD04–PD05)

Continuación basada en las clases del 9 y 10 de octubre de 2026. Dedicación orientativa: seis horas con el entorno preparado. El estudiante desarrolla el código y las interpretaciones de forma autónoma; esta ampliación no fija una nueva fecha ni modifica los porcentajes del calendario.

| Plantilla | Tiempo | Solución del estudiante |
|---|---:|---|
| [PD04 · Limpieza e integración territorial](PD04_limpieza_integracion_territorial.ipynb) | 180 min | `soluciones/PD04_limpieza_integracion_territorial.ipynb` |
| [PD05 · Particionamiento y comparación pandas–Polars](PD05_particionamiento_pandas_polars.ipynb) | 180 min | `soluciones/PD05_particionamiento_pandas_polars.ipynb` |

PD04 lee directamente `agrosavia.csv` y `divipola.csv` mediante `pd.read_csv`, con rutas y opciones visibles. Trabaja con coordenadas territoriales tabulares, conversiones, nombres inconsistentes, cardinalidad y equivalencias documentadas. No atribuye las coordenadas municipales a las muestras de suelo.

PD05 depende de `kit/salidas/soluciones/PD04/analisis_integrados.parquet`. Lo lee directamente con `pd.read_parquet` y `pl.read_parquet`. Compara CSV, Parquet y dos diseños de particionamiento; separa lectura, escritura, procesamiento en memoria y consulta completa desde disco. Las salidas se guardan en `kit/salidas/soluciones/PD05/`. Utiliza pandas, PyArrow y Polars CPU del entorno del curso (`kit/requirements.txt` y `kit/requirements_pqrs.txt`).

Las transformaciones deben quedar visibles en las celdas. No se admite resolver las actividades llamando a scripts de talleres ni funciones que oculten las etapas. Los bucles de medición deben mostrar las operaciones medidas. Las plantillas incluyen únicamente preparación y lecturas; el alumno desarrolla limpieza, integración, consultas y controles con las API indicadas.

**Criterios de revisión:** conservación de filas y originales, tipos y nulos explícitos, correspondencias justificadas, equivalencia de resultados, mediciones comparables, reejecución y conclusiones sustentadas. No se exige que un motor gane ni que particionar siempre mejore el tiempo.

### Validación de PD04–PD05

Se comprobaron el formato nbformat 4, sintaxis, enlaces locales y 180 minutos de actividades por plantilla. Se ejecutaron las lecturas iniciales con pandas 2.2.3, Polars 1.35.2 y PyArrow 19.0.1 en macOS, adaptando las rutas y usando salidas temporales. Para comprobar la entrada de PD05 se construyó una integración técnica temporal con los CSV reales, sin incorporarla como solución del alumno. La lectura filtrada del Parquet particionado devolvió las mismas 1.704 filas en ambos motores para la selección de prueba. Se explicitó el esquema Hive para evitar inferencia numérica de claves de carpeta.

Esta verificación cubre las celdas iniciales y la viabilidad de la lectura particionada. Las soluciones, interpretaciones y mediciones completas corresponden al estudiante; no certifica una instalación en Windows/WSL ni resultados de rendimiento.
