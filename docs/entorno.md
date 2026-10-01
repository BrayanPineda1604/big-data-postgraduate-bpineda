# Entorno y orden de ejecución

[Índice del curso](../README.md)

Entorno de referencia del material existente: Python 3.12, Java 17 y versiones de [requirements.txt](../material_practico/requirements.txt). La validación de Windows sigue pendiente; estas instrucciones no constituyen una instalación comprobada allí.

## Instalación

Desde la raíz del repositorio, en macOS/Linux:

```sh
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r material_practico/requirements.txt
```

En Windows, terminal CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r material_practico\requirements.txt
```

Java debe estar instalado y disponible en PATH; comprobar que JAVA_HOME apunta al JDK previsto. La instalación y las rutas se verificarán durante la clase 2.

```sh
python --version
java -version
python -c "import duckdb; print(duckdb.sql('SELECT 2 + 2').fetchone())"
python -c "import pandas, pyarrow, sklearn; print('Bibliotecas disponibles')"
```

La consulta debe producir `(4,)`. Verificar el inicio de Spark con el laboratorio 03 después de generar y depurar los datos.

## Secuencia compartida

Todos los scripts usan rutas relativas: ejecutarlos desde `material_practico/`.

```sh
cd material_practico
python 01_generar_datos.py --n 20000
python 02_calidad_duckdb.py
python 03_spark_lotes.py
python 04_benchmark.py
python 05_streaming.py
python 06_modelo.py
```

| Script | Clase | Entrada necesaria | Resultado principal |
|---|---|---|---|
| 01_generar_datos.py | 2 | Ninguna | pedidos.csv y esperado.json |
| 02_calidad_duckdb.py | 4 | Salidas de 01 | limpio.parquet, limpio.csv, rechazados.csv, resumen_duckdb.csv |
| 03_spark_lotes.py | 5–6 | Salidas de 01 y 02; Java | resumen_spark/ y conciliación entre motores |
| 04_benchmark.py | 7 | limpio.csv y limpio.parquet de 02 | tiempos.csv y medianas en consola |
| 05_streaming.py | 8 | Java; genera sus propios eventos | stream_<id>/ y progreso en consola |
| 06_modelo.py | 9 | limpio.parquet de 02 | metricas.json |

Las salidas quedan bajo `material_practico/datos/`, excluido de Git. Conservar las evidencias seleccionadas para cada entrega. Reejecutar 01 reemplaza las entradas; después deben actualizarse las salidas dependientes.

Para 20 000 registros y semilla 64, el material establece 20 100 filas originales, 100 duplicados exactos, 506 rechazados, 19 494 válidos y 600 736 176 centavos de importe válido. DuckDB y Spark deben coincidir exactamente. Los tiempos y las métricas del modelo se interpretan; no se inventa un umbral de aprobación.

Consultar [LEEME de los laboratorios](../material_practico/LEEME.txt). Al organizar el repositorio no se han vuelto a ejecutar los scripts ni instalado dependencias.
