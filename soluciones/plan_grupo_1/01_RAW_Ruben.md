# Grupo 1 · Capa RAW · Rubén

> Proyecto: pipeline E12 → producto E13, ruta **agroambiental**. Entrega final: **7 de noviembre de 2026**.
> Diagrama de referencia: `Diagrama ejercicio 12.excalidraw` (raíz del repositorio).

## 1. Tu rol

Eres responsable de la **entrada del pipeline**: recibir los tres archivos originales, comprobar que son los esperados y convertirlos en tablas Parquet con tipos correctos. Lo que entregas lo usa Brayan (SILVER) sin volver a abrir los CSV.

Pregunta del producto: **¿qué cultivos tienen mejor rendimiento por municipio y año?** Tu capa no responde la pregunta; garantiza que los datos que llegan a ella son los correctos y están bien tipados.

| Paso del diagrama | Nota del diagrama | Qué significa para ti |
|---|---|---|
| Configurar ingesta de datos | Comparación de tamaños de descarga; creación y comparación de hash | Comparar bytes y SHA-256 de cada archivo con `kit/fuentes.json` |
| Limpieza de datos | Tipificar y normalizar la info de EVA y DIVIPOLA; usar DuckDB y Parquet | Renombrar columnas, convertir tipos, separar aceptados y rechazados, escribir Parquet |
| Verificación de fuentes ya almacenadas (transversal) | Evitar duplicidades | Si las mismas entradas ya se procesaron con éxito, no volver a escribirlas |

## 2. Convenciones del grupo (iguales para los 4)

- Salidas en `kit/salidas/grupo_1/<run_id>/raw/`. `run_id = uuid4().hex[:12]`. Esa carpeta está fuera de Git (`kit/salidas/` está en `.gitignore`).
- Nunca se modifica nada en `kit/data/raw/`. Nunca se anexan filas a un Parquet existente: cada ejecución escribe en una carpeta nueva.
- Columnas en `snake_case` sin tildes. La unidad va en el sufijo: `_ha`, `_m2`, `_t`, `_t_ha`, `_kg_m2`.
- Códigos DANE siempre como **texto con ceros a la izquierda**: `codigo_departamento` (2 caracteres), `codigo_municipio` (5 caracteres). Nunca como número.
- Decimales con punto. Archivos de texto en UTF-8.
- Varios motivos de rechazo se separan con `|` (igual que en `soluciones/E12_solucion.ipynb`).
- Tu notebook empieza con una celda de parámetros:

  ```python
  RUN_ID = None          # None = generar uno nuevo
  ENTRADA_DIR = REPOSITORIO / 'kit' / 'data' / 'raw'
  SALIDA_DIR = REPOSITORIO / 'kit' / 'salidas' / 'grupo_1' / RUN_ID / 'raw'
  FORZAR = False         # True = reprocesar aunque ya exista una ejecución válida
  ```

  Para encontrar `REPOSITORIO` copia la función `encontrar_repositorio` de `soluciones/E12_solucion.ipynb` (sección 1), cambiando `pqrs_fuentes.json` por `fuentes.json`.
- Funciones que puedes copiar tal cual de `soluciones/E12_solucion.ipynb` (sección 2): `sha256_archivo`, `firma_dataframe`, `agregar_motivo`.
- **Antiduplicidad**: calcula `firma_entrada` = SHA-256 de los tres archivos de entrada. Antes de procesar, lee `kit/salidas/grupo_1/registro_raw.jsonl`; si hay una línea con la misma `firma_entrada` y `estado = "valida"` y `FORZAR` es `False`, muestra `ya procesado en <ruta>` y termina. Al final, agrega **una línea** al registro con `run_id, fecha, firma_entrada, firma_contenido, estado, ruta_salida`.
- **Versionamiento y equipo de ejecución**: en la celda de parámetros declara `RESPONSABLE = 'Rubén'`, `EQUIPO_DESCRIPCION` (tipo de equipo y sistema, p. ej. “Portátil · WSL Ubuntu 26.04”), `VERSION_NOTEBOOK = 'G1_01_raw 1.0.0'` y `VERSION_REGLAS = 'g1-raw-v1'` (súbela si cambias una regla de rechazo). Copia la celda “Entorno de ejecución” (sección 2 de `soluciones/grupo_1/G1_02_silver.ipynb`) cambiando `'capa': 'raw'`: escribe `raw/entorno.json` y el mismo bloque como `entorno` dentro de `controles_raw.json`. Campos: `capa, responsable, equipo_descripcion, version_notebook, version_reglas, fecha, zona_horaria, sistema, python, librerias, git`. No registres hostname, usuario ni rutas absolutas. SILVER compara tu bloque con el suyo y avisa si las versiones difieren.
- Tu notebook: `soluciones/grupo_1/G1_01_raw.ipynb`. Tu rama: `g1/raw-ruben`. Haces PR hacia `collaborators/bpineda`; lo revisa Brayan.

## 3. Entrada

| Archivo | Ruta | Filas aprox. | Observaciones |
|---|---|---:|---|
| AGROSAVIA | `kit/data/raw/agrosavia.csv` | 92 772 | Muestras de suelo; municipio solo por **nombre**; fechas `d/m/aaaa`; valores `ND` |
| EVA | `kit/data/raw/eva.csv` | 166 732 | Producción agrícola; áreas en hectáreas, producción en toneladas; periodos `2021A`, `2021B` |
| DIVIPOLA | `kit/data/raw/divipola.csv` | 1 122 | Códigos y nombres; longitud/latitud con **coma decimal** |

Valores esperados de tamaño y huella: `kit/fuentes.json` → entradas con `id` `agrosavia`, `eva`, `divipola` (campos `bytes` y `sha256`).

Lee siempre como texto: `pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding='utf-8-sig')` (igual que `load()` en `kit/talleres.py`). Así no se pierden los ceros de los códigos.

## 4. Salida (contrato: Brayan depende de esto exactamente)

Carpeta `kit/salidas/grupo_1/<run_id>/raw/`:

### `manifiesto_entradas.json`
Lista con un objeto por fuente:
`id, ruta, bytes, bytes_esperados, sha256, sha256_esperado, coincide (bool), filas_leidas, columnas (lista)`.

### `eva.parquet` — una fila por fila aceptada de EVA

| Columna | Tipo | Origen |
|---|---|---|
| `codigo_departamento` | string (2) | Código Dane departamento, `zfill(2)` |
| `codigo_municipio` | string (5) | Código Dane municipio, `zfill(5)` |
| `departamento` | string | Departamento |
| `municipio` | string | Municipio |
| `grupo_cultivo` | string | Grupo cultivo |
| `cultivo` | string | Cultivo |
| `anio` | int64 | Año |
| `periodo` | string | Periodo |
| `area_sembrada_ha` | float64 | Área sembrada |
| `area_cosechada_ha` | float64 | Área cosechada |
| `produccion_t` | float64 | Producción |
| `rendimiento_publicado_t_ha` | float64 | Rendimiento (solo referencia, no se usa para calcular) |
| `ciclo` | string | Ciclo del cultivo |
| `estado_fisico` | string | Estado físico del cultivo |
| `codigo_cultivo` | string | Código del cultivo |
| `fila_fuente` | int64 | Número de línea en el CSV (encabezado = 1, primera fila = 2) |

### `divipola.parquet` — una fila por municipio

| Columna | Tipo | Regla |
|---|---|---|
| `codigo_departamento` | string (2) | `zfill(2)` |
| `codigo_municipio` | string (5) | `zfill(5)`; **único** |
| `departamento` | string | Nombre Departamento |
| `municipio` | string | Nombre Municipio |
| `tipo` | string | Municipio / Isla / Área no municipalizada |
| `longitud` | float64 | Coma → punto |
| `latitud` | float64 | Coma → punto |
| `clave_territorial` | string | `norm(departamento) + '\|' + norm(municipio)`; **única** |

`norm()` es la función de `kit/talleres.py` (línea 7): quita tildes, pasa a mayúsculas y deja solo letras, números y espacios simples. Cópiala exactamente; Brayan usa la misma para unir AGROSAVIA.

### `agrosavia.parquet` — una fila por muestra aceptada

| Columna | Tipo | Origen |
|---|---|---|
| `id_muestra` | string | Secuencial |
| `fila_fuente` | int64 | Línea en el CSV |
| `fecha` | date | Fecha de Análisis, formato `%d/%m/%Y` |
| `anio` | int64 | Año de `fecha` |
| `departamento` | string | Departamento |
| `municipio` | string | Municipio |
| `clave_territorial` | string | `norm(departamento) + '\|' + norm(municipio)` |
| `cultivo` | string | Cultivo |
| `ph` | float64 | pH agua:suelo |
| `materia_organica` | float64 | Materia organica |
| `fosforo` | float64 | Fósforo Bray II |
| `aluminio` | float64 | Aluminio intercambiable |
| `calcio` | float64 | Calcio intercambiable |
| `magnesio` | float64 | Magnesio intercambiable |
| `potasio` | float64 | Potasio intercambiable |
| `cic` | float64 | capacidad de intercambio cationico |
| `conductividad` | float64 | Conductividad electrica |

`ND`, vacío o texto no numérico en columnas numéricas → nulo (no es motivo de rechazo).

### `rechazados.parquet`

| Columna | Tipo | Regla |
|---|---|---|
| `fuente` | string | `agrosavia`, `eva` o `divipola` |
| `fila_fuente` | int64 | Línea en el CSV |
| `motivos` | string | Todos los motivos de la fila separados por `\|` |
| `registro_original` | string | La fila original como JSON |

**Cada fila rechazada aparece una sola vez**, aunque tenga varios motivos.

### `controles_raw.json`
```json
{
  "run_id": "...", "firma_entrada": "...", "estado": "valida",
  "fuentes": {
    "eva": {"leidas": 0, "aceptadas": 0, "rechazadas": 0, "motivos": {"ANIO_INVALIDO": 0}},
    "agrosavia": {...}, "divipola": {...}
  },
  "firmas_contenido": {"eva": "...", "agrosavia": "...", "divipola": "..."},
  "errores": [],
  "entorno": {"capa": "raw", "responsable": "Rubén", "version_notebook": "G1_01_raw 1.0.0", "python": {...}, "librerias": {...}, "...": "ver convención de versionamiento"}
}
```

## 5. Reglas de rechazo

| Fuente | Motivo | Condición |
|---|---|---|
| todas | `DUPLICADO_EXACTO` | Fila idéntica a otra anterior en todas las columnas (se conserva la primera) |
| EVA | `MUNICIPIO_INVALIDO` | Código de municipio que, tras `zfill(5)`, no son 5 dígitos |
| EVA | `ANIO_INVALIDO` | Año vacío o no numérico |
| EVA | `AREA_INVALIDA` | Área cosechada vacía, no numérica o negativa |
| EVA | `PRODUCCION_INVALIDA` | Producción vacía, no numérica o negativa |
| AGROSAVIA | `FECHA_INVALIDA` | Fecha no interpretable con `%d/%m/%Y` |
| AGROSAVIA | `PH_FUERA_DOMINIO` | pH numérico fuera de [0, 14] |
| AGROSAVIA | `TERRITORIO_VACIO` | Departamento o municipio vacío |
| DIVIPOLA | — | No se rechazan filas: si hay código o clave repetidos, el notebook **se detiene** con error |

Área cosechada igual a 0 **no** se rechaza (es un dato válido); SILVER la marca como no apta para rendimiento.

## 6. Tareas por fase

| Fase | Fecha | Qué haces |
|---|---|---|
| F0 Acuerdo | 31 oct | Lee este archivo. Activa el entorno (`source .venv/bin/activate`), crea la rama `g1/raw-ruben` y el notebook vacío con las secciones de abajo. Abre los tres CSV y mira 5 filas de cada uno. |
| F1 Desarrollo | 1–2 nov | Sección 1: rutas y parámetros. Sección 2: manifiesto (bytes + SHA-256 vs `kit/fuentes.json`). Sección 3: EVA. Sección 4: DIVIPOLA. Sección 5: AGROSAVIA. Sección 6: rechazados y controles. Sección 7: registro y antiduplicidad. |
| F2 Datos reales | **3 nov (fecha límite)** | Ejecuta todo desde cero; avisa a Brayan con la ruta `kit/salidas/grupo_1/<run_id>/raw/`. Él empieza a usarla ese mismo día. Corrige lo que te reporte. |
| F3 Integración | 5 nov | Brayan copia tus secciones al notebook integrado. Atiende sus preguntas y corrige errores. |
| F4 Auditoría y entrega | 6–7 nov | En la clínica, otro equipo revisa tus controles. En la sustentación explicas tu capa: qué se verificó, cuántas filas se rechazaron y por qué. |

Tú no dependes de nadie: tus entradas ya están en el repositorio. Eres el primero de la cadena, así que la fecha del **3 de noviembre** es la más importante del plan.

## 7. Controles que tu notebook debe mostrar (con `assert`)

1. Para cada fuente, `coincide == True` en el manifiesto. Si no coincide, se registra como error y el estado queda `fallida` (no se sigue).
2. Para cada fuente: `leidas == aceptadas + rechazadas`.
3. Ninguna `fila_fuente` aparece dos veces en `rechazados.parquet` para la misma fuente.
4. Columnas y tipos de cada Parquet iguales al contrato (compara la lista de columnas en orden y `df.dtypes`).
5. `codigo_municipio` siempre tiene 5 caracteres; `codigo_departamento` siempre 2.
6. `divipola.parquet`: `codigo_municipio` y `clave_territorial` únicos.
7. Releer cada Parquet escrito y comprobar que tiene las mismas filas que el DataFrame que guardaste.
8. Ejecutar dos veces seguidas: la segunda vez debe decir `ya procesado`. Con `FORZAR = True`, debe producir la misma `firma_contenido`.

## 8. Criterios de entrega (“hecho cuando…”)

- [ ] `Kernel → Restart & Run All` termina sin errores.
- [ ] Existen los 6 archivos de salida con los nombres exactos del contrato.
- [ ] Los 8 controles de la sección 7 pasan y se ven en las salidas del notebook.
- [ ] `controles_raw.json` tiene `estado = "valida"` y los conteos por motivo.
- [ ] Cada sección del notebook tiene un texto corto que explica qué hace y por qué.
- [ ] Una celda final resume: filas leídas, aceptadas y rechazadas por fuente, y los 3 motivos más frecuentes.
- [ ] PR abierto con solo el notebook (sin CSV ni Parquet) y aprobado por Brayan.
- [ ] Brayan confirma que su notebook SILVER lee tus archivos sin cambios.

## 9. Cómo usar la IA en tu capa

- Pega en el asistente la sección 4 (contrato) y la sección 5 (reglas) de este archivo antes de pedir código.
- Pide **un paso a la vez**: “Escribe la celda que calcula bytes y SHA-256 de estos tres archivos y los compara con este JSON”. Ejecuta y revisa antes del siguiente.
- Si el código generado usa `pd.read_csv` sin `dtype=str`, corrígelo: los códigos perderían los ceros.
- Pide que te explique cada línea que no entiendas; vas a sustentarla.
- Nunca borres un `assert` para que el notebook “pase”. Si falla, el dato o el código está mal: averigua cuál.

## 10. Riesgos y límites

- AGROSAVIA no trae código de municipio: la `clave_territorial` es el único puente con DIVIPOLA. Si `norm()` no se aplica igual en las dos tablas, la unión de Brayan falla.
- DIVIPOLA tiene longitud/latitud con coma; si no las conviertes, quedan nulas.
- Un hash distinto al esperado puede significar que el archivo se descargó otra vez y cambió. No lo “arregles”: regístralo y avisa al grupo.
