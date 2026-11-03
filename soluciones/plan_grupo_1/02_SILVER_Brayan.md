# Grupo 1 · Capa SILVER e integración · Brayan

> Proyecto: pipeline E12 → producto E13, ruta **agroambiental**. Entrega final: **7 de noviembre de 2026**.
> Diagrama de referencia: `Diagrama ejercicio 12.excalidraw` (raíz del repositorio).

## 1. Tu rol

Tienes dos responsabilidades:

1. **Capa SILVER**: unir AGROSAVIA, EVA y DIVIPOLA sin multiplicar filas, dejar un Parquet particionado y limpio para GOLD.
2. **Integración del grupo**: fixtures para que todos trabajen en paralelo, revisión de PR, notebook integrado `soluciones/E12_pipeline_plantilla_grupo_1.ipynb`, ejecuciones A y B, fallo controlado y cierre E12.

Se te asigna esta capa porque concentra las decisiones técnicas más delicadas (normalización de nombres, cardinalidad de joins, particionamiento, idempotencia) y porque el integrador necesita conocer los contratos de entrada y salida de la capa intermedia.

| Paso del diagrama | Nota del diagrama | Qué significa para ti |
|---|---|---|
| Unificación de datos | Unificar AGROSAVIA, EVA y DIVIPOLA | Agregar suelo por municipio-año **antes** del join; EVA es la tabla base |
| Conversión a Parquet y almacenamiento | Particionar por año y municipio (posiblemente extras) | Hive por `anio` y `codigo_departamento` (ver decisión abajo) |
| Limpieza de memoria y caché | Liberar CSV y Parquet de memoria | `del`, `gc.collect()`, cerrar DuckDB; medir memoria antes y después |
| Verificación de fuentes ya almacenadas | Evitar duplicidades | `registro_silver.jsonl` con `firma_entrada` |

**Decisión de particionamiento.** El diagrama propone año y municipio. Con ~1.100 municipios × años y pocas filas por combinación, eso produce miles de archivos diminutos (más metadatos que datos). Se particiona por `anio` y `codigo_departamento` (~33 × años) y `codigo_municipio` se conserva como columna; DuckDB filtra por municipio con los estadísticos de Parquet. Documenta esta decisión en el notebook y en el informe.

## 2. Convenciones del grupo (iguales para los 4)

- Salidas en `kit/salidas/grupo_1/<run_id>/{raw,silver,gold,presentacion}/`. `run_id = uuid4().hex[:12]`. Fuera de Git.
- Nunca se modifica `kit/data/raw/`. Nunca se anexan filas a un Parquet existente.
- Columnas `snake_case` sin tildes; unidad en el sufijo (`_ha`, `_m2`, `_t`, `_t_ha`, `_kg_m2`).
- Códigos DANE como texto con ceros: `codigo_departamento` (2), `codigo_municipio` (5).
- Decimales con punto; UTF-8; motivos múltiples separados por `|`.
- Celda de parámetros al inicio de cada notebook: `RUN_ID`, `ENTRADA_DIR`, `SALIDA_DIR`, `FORZAR = False`. Raíz con `encontrar_repositorio` de `soluciones/E12_solucion.ipynb` (sección 1) usando `kit/fuentes.json` como marcador.
- Funciones reutilizables de `soluciones/E12_solucion.ipynb` (sección 2): `sha256_archivo`, `firma_dataframe`, `validar_contrato`, `agregar_motivo`. `norm()` de `kit/talleres.py`.
- **Antiduplicidad**: `firma_entrada` identifica la entrada de la capa: en RAW, SHA-256 de los CSV; en SILVER y GOLD, firma de **contenido** (`firma_dataframe`) de las tablas leídas más `VERSION_REGLAS`, porque dos ejecuciones con los mismos datos producen Parquet distintos byte a byte (E12 §7). Registro en `kit/salidas/grupo_1/registro_<capa>.jsonl` con `run_id, fecha, firma_entrada, firma_contenido, estado, ruta_salida, version_notebook, version_reglas, python, commit, responsable`. Si existe una entrada `valida` con la misma firma y `FORZAR = False`: “ya procesado”, se reutiliza la ruta.
- **Versionamiento y equipo de ejecución**: la celda de parámetros declara `RESPONSABLE`, `EQUIPO_DESCRIPCION` (tipo de equipo y sistema, p. ej. “Portátil · WSL Ubuntu 26.04”), `VERSION_NOTEBOOK` y `VERSION_REGLAS`. Cada notebook escribe `<capa>/entorno.json` y copia ese bloque como `entorno` dentro de `controles_<capa>.json`, con los mismos campos en las 4 capas: `capa, responsable, equipo_descripcion, version_notebook, version_reglas, fecha, zona_horaria, sistema {plataforma, wsl, arquitectura, cpu, nucleos_logicos, ram_total_gb}, python {version, implementacion, interprete}, librerias {nombre: {instalada, requerida, coincide}}, git {rama, commit, notebook_con_cambios_sin_commit}`. Las versiones se comparan con `kit/requirements.txt` y `kit/requirements_notebooks.txt`; una diferencia es advertencia, no fallo. No se registran hostname, usuario ni rutas absolutas. La celda de referencia es la sección 2 de `soluciones/grupo_1/G1_02_silver.ipynb`; en F3 se comparan los cuatro `entorno.json` antes de unificar.
- Notebooks: `soluciones/grupo_1/G1_0{1..4}_*.ipynb`. Ramas `g1/raw-ruben`, `g1/silver-brayan`, `g1/gold-julian`, `g1/presentacion-juan` → PR a `collaborators/bpineda`.
- Notebook de esta capa: [`soluciones/grupo_1/G1_02_silver.ipynb`](../grupo_1/G1_02_silver.ipynb) (versión 1.0.0, reglas `g1-silver-v1`).

## 3. Entrada (contrato de Rubén)

`kit/salidas/grupo_1/<run_id>/raw/`: `manifiesto_entradas.json`, `eva.parquet`, `divipola.parquet`, `agrosavia.parquet`, `rechazados.parquet`, `controles_raw.json`.

- `eva.parquet`: `codigo_departamento, codigo_municipio, departamento, municipio, grupo_cultivo, cultivo, anio:int64, periodo, area_sembrada_ha, area_cosechada_ha, produccion_t, rendimiento_publicado_t_ha:float64, ciclo, estado_fisico, codigo_cultivo, fila_fuente:int64`.
- `divipola.parquet`: `codigo_departamento, codigo_municipio (único), departamento, municipio, tipo, longitud:float64, latitud:float64, clave_territorial (única)`.
- `agrosavia.parquet`: `id_muestra, fila_fuente, fecha:date, anio:int64, departamento, municipio, clave_territorial, cultivo, ph, materia_organica, fosforo, aluminio, calcio, magnesio, potasio, cic, conductividad:float64`.

Antes de procesar: `controles_raw.json` con `estado = "valida"`; si no, SILVER no empieza.

**Mientras Rubén termina (hasta el 3 nov)** usa `soluciones/plan_grupo_1/fixtures/raw/` (lo creas tú en F0).

## 4. Salida (contrato: Julián depende de esto exactamente)

Carpeta `kit/salidas/grupo_1/<run_id>/silver/`:

### `dim_municipio.parquet`
`codigo_departamento, codigo_municipio, departamento, municipio, longitud, latitud` — clave única `codigo_municipio`.

### `suelo_municipio_anio.parquet`
Agregado de AGROSAVIA aceptada y enlazada con DIVIPOLA por `clave_territorial`.

| Columna | Tipo | Regla |
|---|---|---|
| `codigo_municipio` | string (5) | Desde DIVIPOLA |
| `anio` | int64 | Año de la muestra |
| `muestras` | int64 | Conteo de muestras |
| `mediana_ph` | float64 | Mediana de `ph` no nulo |
| `mediana_materia_organica` | float64 | |
| `mediana_fosforo` | float64 | |

Clave única `(codigo_municipio, anio)`.

### `unificado/` — Parquet Hive `anio=YYYY/codigo_departamento=DD/`
Grano: **una fila por fila aceptada de EVA**.

| Columna | Tipo | Regla |
|---|---|---|
| `codigo_departamento` | string (2) | Partición |
| `departamento` | string | Nombre DIVIPOLA (si no hay correspondencia, el de EVA) |
| `codigo_municipio` | string (5) | |
| `municipio` | string | Nombre DIVIPOLA (si no hay correspondencia, el de EVA) |
| `anio` | int64 | Partición |
| `periodo` | string | |
| `grupo_cultivo` | string | |
| `cultivo` | string | |
| `estado_fisico` | string | |
| `ciclo` | string | |
| `area_sembrada_ha` | float64 | |
| `area_cosechada_ha` | float64 | |
| `area_cosechada_m2` | float64 | `area_cosechada_ha × 10 000` |
| `produccion_t` | float64 | |
| `rendimiento_publicado_t_ha` | float64 | Solo referencia |
| `apto_rendimiento` | bool | `area_cosechada_ha > 0` y `produccion_t >= 0` |
| `en_divipola` | bool | `codigo_municipio` existe en `dim_municipio` |
| `muestras_suelo` | int64 | De `suelo_municipio_anio` (0 si no hay) |
| `mediana_ph` | float64 | Nulo si no hay muestras |
| `fila_fuente` | int64 | Trazabilidad a `eva.csv` |

Al leer con DuckDB: `read_parquet('<silver>/unificado/**/*.parquet', hive_partitioning = true)`. Los tipos de las columnas de partición se fijan con `hive_types = {'anio': BIGINT, 'codigo_departamento': VARCHAR}` para que `05` no se convierta en `5`.

### `sin_correspondencia.parquet`
`fuente, clave, filas` — claves de AGROSAVIA sin código en DIVIPOLA y códigos de EVA ausentes de DIVIPOLA. Se conservan explícitamente (E12 §3).

### `controles_silver.json`
`run_id, firma_entrada, estado, filas_eva_entrada, filas_unificado, filas_aptas_rendimiento, agrosavia_enlazadas, agrosavia_sin_enlace, eva_sin_divipola, cobertura_suelo_pct, memoria_mb_antes, memoria_mb_despues, firma_contenido, errores`.

## 5. Pasos de la capa

1. Validar contrato de entrada (`validar_contrato`) y estado RAW.
2. `dim_municipio` desde DIVIPOLA.
3. AGROSAVIA → aplicar `ALIAS_TERRITORIAL` (18 renombres oficiales inequívocos dentro del mismo departamento, p. ej. `NORTE DE SANTANDER|CUCUTA` → `SAN JOSE DE CUCUTA`) y `merge(..., how='left', validate='many_to_one')` con DIVIPOLA; separar no enlazadas a `sin_correspondencia`.
4. Agregar suelo por `(codigo_municipio, anio)` → `suelo_municipio_anio`.
5. EVA `LEFT JOIN dim_municipio` (many-to-one) `LEFT JOIN suelo_municipio_anio` (many-to-one). Comprobar `len(unificado) == len(eva)`.
6. Columnas derivadas (`area_cosechada_m2`, `apto_rendimiento`, `en_divipola`).
7. Escribir Hive con `pyarrow.parquet.write_to_dataset(..., partition_cols=['anio','codigo_departamento'])` o `COPY ... (FORMAT parquet, PARTITION_BY (anio, codigo_departamento))` en DuckDB.
8. Releer y comprobar filas y firma.
9. Limpieza de memoria: medir `RssAnon` de `/proc/self/status` (no RSS: Parquet usa mmap), `del` de DataFrames, `gc.collect()`, `con.close()`, medir otra vez.
10. Registro y antiduplicidad.

## 6. Tareas por fase

| Fase | Fecha | SILVER | Integración |
|---|---|---|---|
| F0 Acuerdo | 31 oct | Rama `g1/silver-brayan`, esqueleto del notebook | Compartir los 4 .md. Crear `soluciones/plan_grupo_1/fixtures/{raw,silver,gold}/` con 6–10 filas por archivo que cumplan cada contrato e incluyan: un duplicado, un municipio sin DIVIPOLA, un área 0, dos periodos del mismo año y dos cultivos en el mismo municipio. Escribir en `fixtures/README.md` el resultado esperado calculado a mano (filas, rendimiento, ranking). |
| F1 Desarrollo | 1–3 nov | SILVER completo contra `fixtures/raw/` | Responder dudas; verificar que los fixtures sirven a Julián y Juan |
| F2 Datos reales | 3–4 nov | Ejecutar con la salida real de Rubén (3 nov). Entregar `silver/` real a Julián **el 4 nov** | Revisar PR de Rubén; comprobar que los contratos encajan |
| F3 Integración | 5 nov | Ajustes | Copiar las secciones RAW, SILVER, GOLD y PRESENTACIÓN al notebook integrado (secciones 3–7 de la plantilla). Ejecución A y B en carpetas distintas; comparar `firma_contenido` de cada capa; fallo controlado (retirar una columna obligatoria en memoria → no se publica y `publicacion_valida.json` sigue apuntando a la ejecución anterior). |
| F4 Auditoría y entrega | 6–7 nov | Sustentar SILVER | Clínica: coordinar auditoría cruzada con otro equipo; registrar hallazgos y reejecución; cierre E12 §9; entrega |

## 7. Controles obligatorios

1. `len(unificado) == len(eva aceptada)` (el join no multiplica filas).
2. `suelo_municipio_anio` y `dim_municipio` con claves únicas.
3. `agrosavia_enlazadas + agrosavia_sin_enlace == filas agrosavia`.
4. `sum(produccion_t)` y `sum(area_cosechada_ha)` iguales antes y después del join (por año y total).
5. Releer `unificado/` con DuckDB y `hive_partitioning`: mismas filas, `codigo_departamento` sigue siendo texto de 2 caracteres.
6. `memoria_mb_antes` y `memoria_mb_despues` registrados (informativo: el asignador puede retener memoria sin que eso invalide la publicación).
7. Dos ejecuciones con `FORZAR = True` → misma `firma_contenido`; sin `FORZAR` → “ya procesado”.

## 8. Criterios de entrega

**SILVER**
- [ ] `Restart & Run All` sin errores con fixture y con datos reales.
- [ ] Los 5 artefactos del contrato existen y pasan los 7 controles.
- [ ] Decisión de particionamiento y cobertura de suelo explicadas en el notebook.
- [ ] Julián confirma que GOLD lee `silver/` sin cambios.

**Integración**
- [x] Fixtures RAW y SILVER con resultados esperados publicados el 31 oct (`fixtures/README.md`).
- [ ] Fixture GOLD para Juan.
- [ ] Los 3 PR revisados contra su contrato.
- [ ] `E12_pipeline_plantilla_grupo_1.ipynb` ejecuta de cero todo el recorrido.
- [ ] Registros de ejecución A y B, comparación de firmas por capa, fallo controlado documentado.
- [ ] Ficha de auditoría (plantilla de Juan) completa con evidencia del otro equipo.
- [ ] Criterios E12 cumplidos: ejecución completa, conteos explicables, agregado consistente, reejecución estable.
- [ ] Sin datos ni salidas en Git.

## 9. Uso de IA

- Úsala para revisar PR: pega el contrato y el `df.dtypes` / lista de columnas del notebook del compañero y pide diferencias.
- Pídele casos borde para los fixtures (nombres con tildes, `BOGOTÁ, D.C.`, municipios homónimos en distintos departamentos).
- Ayuda a tus compañeros a formular prompts de un paso a la vez con su contrato pegado.

## 10. Riesgos y límites

- **Enlace por nombre**: AGROSAVIA usa nombres que no siempre coinciden con DIVIPOLA. Con los datos completos el enlace directo es 97,7 %; los 18 alias declarados lo suben a 99,96 % (2 099 muestras). Las 37 restantes (`…|BORRAR`, departamento dudoso como `CUNDINAMARCA|TOCA`) quedan en `sin_correspondencia`. Ningún nombre se corrige a mano sin regla escrita y versionada.
- **Cobertura temporal**: AGROSAVIA cubre 2014–2025 y EVA 2019–2025. Con los datos completos, el 52,45 % de las filas EVA tiene suelo en su municipio-año; es un hallazgo, no un fallo.
- El suelo se asocia por municipio-año; no describe la parcela del cultivo. Es contexto, no explicación del rendimiento.
- Eres el cuello de botella: si RAW se retrasa, sigue con el fixture y no bloquees a Julián.
