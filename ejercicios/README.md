# Ejercicios de pandas y Polars

Los ejercicios se organizan por fin de semana. En este índice, **sesión 1** corresponde al primer fin de semana y **sesión 2** al segundo; cada conjunto reúne las actividades asociadas a las clases del viernes y sábado.

| Sesión de ejercicios | Fin de semana | Ejercicios | Dedicación orientativa |
|---|---|---|---:|
| [Sesión 1](#sesion-1) | 2 y 3 de octubre de 2026 | PD01–PD03 | 4 horas |
| [Sesión 2](#sesion-2) | 9 y 10 de octubre de 2026 | PD04–PD05 | 6 horas |

Cada estudiante copia las plantillas de `ejercicios/` a `soluciones/` en su propio repositorio, conserva sus nombres y desarrolla allí el código y las interpretaciones. Las plantillas originales quedan como material de consulta. Los tiempos suponen el entorno instalado y los datos disponibles.

<a id="sesion-1"></a>

## Sesión 1 · Primer fin de semana: 2 y 3 de octubre

**Propósito:** explorar datos con pandas, reconocer tipos y valores ausentes, construir consultas y comprobar una integración territorial.

### Ejercicios

| Enunciado y plantilla | Trabajo del estudiante | Tiempo |
|---|---|---:|
| [PD01 · Explorar y preparar AGROSAVIA](PD01_exploracion_agrosavia.ipynb) | Inspeccionar campos, convertir pH y fechas, marcar registros para revisión y explicar los controles. | 60 min |
| [PD02 · Consultar y resumir EVA](PD02_consultas_eva.ipynb) | Filtrar datos de Boyacá, comparar consultas, calcular conteos y porcentajes y construir una tabla dinámica. | 70 min |
| [PD03 · Integrar EVA con DIVIPOLA](PD03_integracion_territorial.ipynb) | Validar códigos, revisar correspondencias y calcular rendimiento agrícola con un denominador adecuado. | 70 min |

Se destinan además **20 minutos a preparación** y **20 minutos a reejecución y entrega**: total, **240 minutos**. La [guía práctica de pandas](../docs/manual-pandas.md) sirve como apoyo.

### Entradas y orden de trabajo

- PD01: `kit/data/raw/agrosavia.csv`.
- PD02: `kit/data/raw/eva.csv`.
- PD03: `kit/data/raw/eva.csv` y `kit/data/raw/divipola.csv`.

Desarrolla PD01, PD02 y PD03 en ese orden. Cada notebook carga sus propias entradas y puede ejecutarse de manera independiente.

### Entrega de la sesión 1

| Notebook resuelto | Resultados regenerables |
|---|---|
| `soluciones/PD01_exploracion_agrosavia.ipynb` | `kit/salidas/soluciones/PD01/`: controles de AGROSAVIA. |
| `soluciones/PD02_consultas_eva.ipynb` | `kit/salidas/soluciones/PD02/`: resumen de EVA. |
| `soluciones/PD03_integracion_territorial.ipynb` | `kit/salidas/soluciones/PD03/`: rendimiento municipal y códigos sin correspondencia. |

Los notebooks deben mostrar el desarrollo, las comprobaciones y las conclusiones solicitadas. Se revisan la conservación de filas, la equivalencia de consultas, los denominadores y la interpretación de los resultados.

<a id="sesion-2"></a>

## Sesión 2 · Segundo fin de semana: 9 y 10 de octubre

**Propósito:** aplicar contratos y controles de calidad, normalizar e integrar fuentes, trabajar con CSV y Parquet y comparar pandas con Polars.

### Ejercicios

| Enunciado y plantilla | Trabajo del estudiante | Tiempo |
|---|---|---:|
| [PD04 · Limpieza e integración territorial](PD04_limpieza_integracion_territorial.ipynb) | Leer coordenadas territoriales, limpiar tipos variados, normalizar nombres y unir AGROSAVIA con DIVIPOLA conservando los casos pendientes. | 180 min |
| [PD05 · Particionamiento y comparación pandas–Polars](PD05_particionamiento_pandas_polars.ipynb) | Particionar por año y departamento; comparar lectura, escritura, procesamiento y resultados entre motores. | 180 min |

**Total: 360 minutos.** Los tiempos de cada notebook incluyen controles, publicación y reejecución. Consulta las guías de [pandas](../docs/manual-pandas.md) y [Polars](../docs/manual-polars.md).

### Entradas y orden de trabajo

1. **PD04:** lee `kit/data/raw/agrosavia.csv` y `kit/data/raw/divipola.csv` directamente con `pd.read_csv`. Trabaja con coordenadas geoespaciales tabulares; las coordenadas municipales no representan la ubicación de las muestras de suelo.
2. **PD05:** requiere terminar PD04. Lee `kit/salidas/soluciones/PD04/analisis_integrados.parquet` con `pd.read_parquet` y `pl.read_parquet`. Compara CSV, Parquet único y dos diseños de particionamiento, separando lectura, escritura, procesamiento en memoria y consulta completa desde disco.

Utiliza pandas, PyArrow y Polars CPU del entorno del curso, definidos en `kit/requirements.txt` y `kit/requirements_pqrs.txt`.

### Entrega de la sesión 2

| Notebook resuelto | Resultados regenerables |
|---|---|
| `soluciones/PD04_limpieza_integracion_territorial.ipynb` | `kit/salidas/soluciones/PD04/`: Parquet integrado, controles, equivalencias, resumen y registros pendientes. |
| `soluciones/PD05_particionamiento_pandas_polars.ipynb` | `kit/salidas/soluciones/PD05/`: mediciones, inventario de particiones y controles de equivalencia. |

Se revisan la conservación de originales y filas, los tipos y nulos explícitos, las correspondencias justificadas, la equivalencia de resultados, las mediciones comparables y las conclusiones. No se exige que un motor gane ni que particionar siempre mejore el tiempo.

El estudiante desarrolla el código y las interpretaciones de forma autónoma. Esta organización asocia los ejercicios con el fin de semana correspondiente; no fija nuevas fechas de entrega ni modifica los porcentajes del calendario.

## Preparación y desarrollo para ambas sesiones

La **raíz del repositorio** es `big-data-postgraduate`, que contiene `README.md`, `kit/`, `ejercicios/` y `soluciones/`. En WSL se accede desde la terminal con:

```bash
cd /mnt/c/Users/TUPTC/bigdata
cd big-data-postgraduate
pwd
ls
```

Si tu copia está en otra ubicación, utiliza su ruta real. Cada notebook incluye una sección de ubicación de trabajo con una ruta editable.

1. Abre JupyterLab desde la raíz del repositorio con el entorno `.venv` activo.
2. Duplica las plantillas de la sesión en `soluciones/`, conservando los nombres indicados. Si ya existe una solución, continúa sobre ella.
3. Selecciona el kernel del curso y ajusta la ruta del repositorio.
4. Ejecuta las lecturas iniciales. Respeta la dependencia **PD04 → PD05**.
5. Completa las celdas de desarrollo e interpretación. Antes de entregar, reinicia el kernel y ejecuta todas las celdas en orden.

Los enunciados están en celdas Markdown. Las lecturas muestran rutas y opciones; las conversiones, máscaras, agrupaciones, uniones y exportaciones deben quedar visibles mediante las API de pandas y Polars. No resuelvas las actividades llamando a scripts de talleres ni funciones que oculten las etapas. Los bucles de medición deben mostrar las operaciones medidas.

Si falta un CSV original, prepáralo desde la terminal, en la raíz del repositorio y con el entorno activo:

```bash
python kit/00_datos.py --descargar divipola eva agrosavia
```

Este comando solo prepara las fuentes; el análisis se desarrolla en los notebooks. Los originales permanecen en `kit/data/raw/`. Las carpetas de resultados `kit/salidas/soluciones/PD01/` a `PD05/` están excluidas de Git y deben poder regenerarse.

## Validación de las plantillas

### Sesión 1 · PD01–PD03

Para PD01–PD03 se verificaron el formato de notebook, la sintaxis de las celdas, los enlaces y la suma de los tiempos. Las celdas iniciales se ejecutaron con pandas 2.2.3 desde `ejercicios/` y desde copias en `soluciones/`, utilizando únicamente los tres CSV del manifiesto. El análisis y sus conclusiones quedan pendientes del estudiante.

### Sesión 2 · PD04–PD05

Se comprobaron el formato nbformat 4, sintaxis, enlaces locales y 180 minutos de actividades por plantilla. Se ejecutaron las lecturas iniciales con pandas 2.2.3, Polars 1.35.2 y PyArrow 19.0.1 en macOS, adaptando las rutas y usando salidas temporales. Para comprobar la entrada de PD05 se construyó una integración técnica temporal con los CSV reales, sin incorporarla como solución del alumno. La lectura filtrada del Parquet particionado devolvió las mismas 1.704 filas en ambos motores para la selección de prueba. Se explicitó el esquema Hive para evitar inferencia numérica de claves de carpeta.

Esta verificación cubre las celdas iniciales y la viabilidad de la lectura particionada. Las soluciones, interpretaciones y mediciones completas corresponden al estudiante; no certifica una instalación en Windows/WSL ni resultados de rendimiento.
