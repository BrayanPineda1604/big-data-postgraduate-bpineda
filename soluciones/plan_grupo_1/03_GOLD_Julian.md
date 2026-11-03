# Grupo 1 · Capa GOLD · Julián

> Proyecto: pipeline E12 → producto E13, ruta **agroambiental**. Entrega final: **7 de noviembre de 2026**.
> Diagrama de referencia: `Diagrama ejercicio 12.excalidraw` (raíz del repositorio).

## 1. Tu rol

Eres responsable de **calcular la respuesta**: a partir de los datos unificados de SILVER, obtener el rendimiento de cada cultivo por municipio y año, ordenarlo y comprobar que los totales cuadran. Lo que entregas lo usa Juan (Presentación) para la tabla y el gráfico.

Pregunta del producto: **¿qué cultivos tienen mejor rendimiento por municipio y año?**

| Paso del diagrama | Nota del diagrama | Qué significa para ti |
|---|---|---|
| Carga de los datos pre-procesados | Cargar al motor de análisis | Leer `silver/unificado/` en DuckDB |
| Agrupamiento y generación de información relevante | Extraer la información de los entregables | Consultas SQL: rendimiento, comparación nacional, ranking |
| Almacenamiento | Se almacena la info procesada | Escribir Parquet gold y conciliación |
| Verificación de fuentes ya almacenadas (transversal) | Evitar duplicidades | `registro_gold.jsonl` con `firma_entrada` |

## 2. Convenciones del grupo (iguales para los 4)

- Salidas en `kit/salidas/grupo_1/<run_id>/gold/`. `run_id = uuid4().hex[:12]`. Fuera de Git.
- Nunca se anexan filas a un Parquet existente: cada ejecución escribe en carpeta nueva.
- Columnas `snake_case` sin tildes; unidad en el sufijo: `_ha`, `_m2`, `_t`, `_t_ha`, `_kg_m2`.
- Códigos DANE como texto con ceros: `codigo_departamento` (2), `codigo_municipio` (5).
- Decimales con punto; UTF-8.
- Celda de parámetros al inicio:

  ```python
  RUN_ID = None
  ENTRADA_DIR = REPOSITORIO / 'soluciones' / 'plan_grupo_1' / 'fixtures' / 'silver'   # hasta el 4 nov
  # ENTRADA_DIR = REPOSITORIO / 'kit' / 'salidas' / 'grupo_1' / '<run_id>' / 'silver'  # desde el 4 nov
  SALIDA_DIR = REPOSITORIO / 'kit' / 'salidas' / 'grupo_1' / RUN_ID / 'gold'
  FORZAR = False
  ```

  `REPOSITORIO` con `encontrar_repositorio` de `soluciones/E12_solucion.ipynb` (sección 1), cambiando `pqrs_fuentes.json` por `fuentes.json`.
- Reutiliza `sha256_archivo` y `firma_dataframe` de `soluciones/E12_solucion.ipynb` (sección 2).
- **Antiduplicidad**: `firma_entrada` = firma de contenido (`firma_dataframe`) de las tablas de `silver/` que lees, más tu `VERSION_REGLAS`. No uses el hash de los archivos: dos ejecuciones con los mismos datos producen Parquet distintos byte a byte (E12 §7). Copia el patrón de la sección 5 de `soluciones/grupo_1/G1_02_silver.ipynb`. Antes de procesar, revisa `kit/salidas/grupo_1/registro_gold.jsonl`: si hay una línea con la misma firma y `estado = "valida"` y `FORZAR = False`, muestra `ya procesado en <ruta>` y termina. Al final agrega una línea con `run_id, fecha, firma_entrada, firma_contenido, estado, ruta_salida`.
- **Versionamiento y equipo de ejecución**: en la celda de parámetros declara `RESPONSABLE = 'Julián'`, `EQUIPO_DESCRIPCION` (tipo de equipo y sistema, p. ej. “Portátil · WSL Ubuntu 26.04”), `VERSION_NOTEBOOK = 'G1_03_gold 1.0.0'` y `VERSION_REGLAS`. Copia la celda “Entorno de ejecución” (sección 2 de `soluciones/grupo_1/G1_02_silver.ipynb`) cambiando `'capa': 'gold'`: escribe `gold/entorno.json` y el mismo bloque como `entorno` dentro de `controles_gold.json`. Campos: `capa, responsable, equipo_descripcion, version_notebook, version_reglas, fecha, zona_horaria, sistema, python, librerias, git`. No registres hostname, usuario ni rutas absolutas. Brayan compara los cuatro `entorno.json` antes de unificar.
- Tu notebook: `soluciones/grupo_1/G1_03_gold.ipynb`. Tu rama: `g1/gold-julian`. PR a `collaborators/bpineda`; revisa Brayan.

## 3. Entrada (contrato de Brayan)

Carpeta `silver/` con:

- `unificado/` — Parquet Hive `anio=YYYY/codigo_departamento=DD/`. Una fila por registro de EVA. Columnas: `codigo_departamento, departamento, codigo_municipio, municipio, anio, periodo, grupo_cultivo, cultivo, estado_fisico, ciclo, area_sembrada_ha, area_cosechada_ha, area_cosechada_m2, produccion_t, rendimiento_publicado_t_ha, apto_rendimiento (bool), en_divipola (bool), muestras_suelo, mediana_ph, fila_fuente`.
- `dim_municipio.parquet`, `suelo_municipio_anio.parquet`, `sin_correspondencia.parquet`, `controles_silver.json`.

Lectura en DuckDB (los tipos evitan que `05` se convierta en `5`):

```sql
CREATE OR REPLACE VIEW unificado AS
SELECT * FROM read_parquet('<silver>/unificado/**/*.parquet',
    hive_partitioning = true,
    hive_types = {'anio': BIGINT, 'codigo_departamento': VARCHAR});
```

Antes de procesar: `controles_silver.json` con `estado = "valida"`.

**Mientras Brayan termina (hasta el 4 nov)** trabaja con `soluciones/plan_grupo_1/fixtures/silver/`. En `fixtures/README.md` están los resultados esperados calculados a mano: tu notebook debe reproducirlos exactamente.

## 4. Salida (contrato: Juan depende de esto exactamente)

Carpeta `kit/salidas/grupo_1/<run_id>/gold/`:

### `rendimiento_cultivo.parquet`
Una fila por **municipio × año × cultivo × estado físico**, solo con filas `apto_rendimiento = true`.

| Columna | Tipo | Cálculo |
|---|---|---|
| `codigo_departamento` | string (2) | |
| `departamento` | string | |
| `codigo_municipio` | string (5) | |
| `municipio` | string | |
| `anio` | int64 | |
| `cultivo` | string | |
| `estado_fisico` | string | |
| `produccion_t` | float64 | `sum(produccion_t)` |
| `area_cosechada_ha` | float64 | `sum(area_cosechada_ha)` |
| `area_cosechada_m2` | float64 | `sum(area_cosechada_m2)` |
| `rendimiento_t_ha` | float64 | `sum(produccion_t) / sum(area_cosechada_ha)` |
| `rendimiento_kg_m2` | float64 | `rendimiento_t_ha / 10` |
| `rendimiento_nacional_t_ha` | float64 | Mismo cálculo, agrupando solo por `anio, cultivo, estado_fisico` (todo el país) |
| `indice_relativo` | float64 | `rendimiento_t_ha / rendimiento_nacional_t_ha` |
| `rank_municipio_anio` | int64 | `dense_rank()` descendente por `indice_relativo` dentro de `(codigo_municipio, anio)`; 1 = mejor |
| `n_registros` | int64 | `count(*)` de filas de EVA agrupadas |
| `muestras_suelo` | int64 | `max(muestras_suelo)` |
| `mediana_ph` | float64 | `max(mediana_ph)` (es el mismo valor para todo el municipio-año) |

Clave única: `(codigo_municipio, anio, cultivo, estado_fisico)`. Orden de escritura: `codigo_municipio, anio, rank_municipio_anio`.

**Por qué no promedio ni t/ha directo para ordenar:**
- El rendimiento de un año con periodos A y B es `producción total / área total`, **no** el promedio de los dos rendimientos (el promedio da el mismo peso a un periodo de 1 ha que a uno de 100 ha).
- Comparar t/ha entre cultivos distintos no tiene sentido (plátano produce muchas más toneladas por hectárea que café). Por eso el ranking usa `indice_relativo`: cuánto rinde ese cultivo en el municipio comparado con el país. Un índice de 1,3 significa 30 % por encima del promedio nacional de ese mismo cultivo. Se conservan `rendimiento_t_ha` y `rendimiento_kg_m2` como medidas.

### `conciliacion.parquet`

| Columna | Tipo |
|---|---|
| `nivel` | string: `grupo` o `total` |
| `codigo_municipio` | string (nulo en `total`) |
| `anio` | int64 (nulo en `total`) |
| `produccion_silver_t`, `produccion_gold_t` | float64 |
| `area_silver_ha`, `area_gold_ha` | float64 |
| `diferencia_produccion_t`, `diferencia_area_ha` | float64 |
| `cuadra` | bool: `abs(diferencia) < 1e-6` en ambas |

`silver` se calcula desde `unificado` (solo `apto_rendimiento`); `gold` desde `rendimiento_cultivo`.

### `consultas_gold.sql`
Todas las consultas SQL usadas, en orden, con un comentario por consulta. Juan y el otro equipo las reutilizan en la auditoría.

### `controles_gold.json`
`run_id, firma_entrada, estado, filas_unificado, filas_aptas, filas_gold, grupos_conciliados, grupos_con_diferencia, produccion_total_t, area_total_ha, firma_contenido, errores`.

## 5. Tareas por fase

| Fase | Fecha | Qué haces |
|---|---|---|
| F0 Acuerdo | 31 oct | Lee este archivo. Activa el entorno, crea la rama `g1/gold-julian` y el notebook con secciones: parámetros, carga, rendimiento, nacional e índice, ranking, conciliación, escritura y registro. Lee `kit/talleres.py`, función `consultas()`: ya calcula `sum(produccion_t)/sum(area_ha)` con DuckDB, es tu punto de partida. |
| F1 Desarrollo | 1–3 nov | Construye todo contra `fixtures/silver/`. Compara tu resultado con la tabla esperada de `fixtures/README.md`. |
| F2 Datos reales | **4 nov** | Cambia `ENTRADA_DIR` a la salida real de Brayan. Ejecuta todo; entrega la ruta `gold/` a Juan **el 4 nov**. |
| F3 Integración | 5 nov | Brayan copia tus secciones al notebook integrado; corrige lo que surja. |
| F4 Auditoría y entrega | 6–7 nov | El otro equipo repite una de tus consultas de `consultas_gold.sql`. En la sustentación explicas por qué el rendimiento es cociente de sumas y por qué se ordena por índice relativo. |

Juan necesita tu `gold/` real el 4 nov; mientras tanto él trabaja con `fixtures/gold/`.

## 6. Controles que tu notebook debe mostrar (con `assert`)

1. Clave `(codigo_municipio, anio, cultivo, estado_fisico)` única en `rendimiento_cultivo`.
2. Ningún `rendimiento_t_ha` nulo, infinito ni negativo (por eso se filtra `apto_rendimiento`).
3. `rendimiento_kg_m2 == rendimiento_t_ha / 10` en todas las filas.
4. `conciliacion`: todas las filas con `cuadra = true`, incluida la de `total`.
5. Para cada `(codigo_municipio, anio)` existe al menos un cultivo con `rank_municipio_anio = 1`.
6. Con el fixture: resultados iguales a los esperados de `fixtures/README.md`.
7. Releer los Parquet escritos: mismas filas y columnas en el orden del contrato.
8. Ejecutar dos veces: la segunda dice `ya procesado`; con `FORZAR = True`, misma `firma_contenido`.

## 7. Criterios de entrega (“hecho cuando…”)

- [ ] `Kernel → Restart & Run All` sin errores con fixture y con datos reales.
- [ ] Los 4 archivos de salida existen con nombres y columnas exactos del contrato.
- [ ] Los 8 controles pasan y se ven en el notebook.
- [ ] `controles_gold.json` con `estado = "valida"` y `grupos_con_diferencia = 0`.
- [ ] El notebook muestra, como ejemplo, los 5 mejores cultivos de un municipio conocido en un año.
- [ ] Cada sección tiene un texto corto que explica qué calcula y en qué unidad.
- [ ] PR con solo el notebook, aprobado por Brayan.
- [ ] Juan confirma que su notebook lee `gold/` sin cambios.

## 8. Cómo usar la IA en tu capa

- Pega en el asistente la sección 3 (entrada) y la tabla de `rendimiento_cultivo` antes de pedir SQL.
- Pide **una consulta a la vez**: “Escribe en DuckDB la consulta que agrupa por municipio, año, cultivo y estado físico y calcula producción, área y rendimiento como cociente de sumas”. Ejecútala con el fixture y compara con el resultado esperado antes de seguir.
- Si la IA propone `avg(rendimiento_publicado_t_ha)`, recházalo: es el error de denominador que el curso penaliza.
- Pide que te explique `dense_rank() OVER (PARTITION BY ... ORDER BY ... DESC)` hasta que puedas explicarlo tú; lo vas a sustentar.
- Nunca quites un `assert` para que pase. Si la conciliación no cuadra, falta un filtro o sobra un join.

## 9. Riesgos y límites

- Un cultivo sembrado en un solo municipio tiene índice relativo 1 por definición; menciónalo en la interpretación.
- Cultivos con área muy pequeña pueden dar rendimientos extremos. No los borres; Juan puede filtrar por área mínima en la presentación, declarándolo.
- `estado_fisico` (en fresco, seco, etc.) cambia el rendimiento: nunca juntes dos estados del mismo cultivo.
- `muestras_suelo` y `mediana_ph` son contexto del municipio, no explican el rendimiento del cultivo.
