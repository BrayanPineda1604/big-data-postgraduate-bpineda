# Fixtures del grupo 1

Datos mínimos que cumplen los contratos de cada capa, para que cada integrante trabaje **sin esperar** la salida real de la capa anterior. Son pocas filas, escogidas para cubrir los casos difíciles, con el resultado esperado calculado a mano.

| Carpeta | Contrato | La usa | Cómo se genera |
|---|---|---|---|
| `raw/` | Salida de RAW (`01_RAW_Ruben.md`) | Brayan (SILVER) | `python soluciones/plan_grupo_1/fixtures/generar_fixture_raw.py` desde la raíz del repositorio |
| `silver/` | Salida de SILVER (`02_SILVER_Brayan.md`) | Julián (GOLD) | Ejecutar `soluciones/grupo_1/G1_02_silver.ipynb` con el fixture RAW y copiar `kit/salidas/grupo_1/<run_id>/silver/` aquí |
| `gold/` | Salida de GOLD (`03_GOLD_Julian.md`) | Juan (Presentación) | Pendiente: se genera con el notebook GOLD sobre `silver/` |

Lectura de `silver/unificado/` en DuckDB (los tipos evitan que `05` se convierta en `5`):

```sql
SELECT * FROM read_parquet('soluciones/plan_grupo_1/fixtures/silver/unificado/**/*.parquet',
    hive_partitioning = true,
    hive_types = {'anio': BIGINT, 'codigo_departamento': VARCHAR});
```

## Casos del fixture RAW

**DIVIPOLA (4):** 15001 Tunja, 15248 El Espino, 54001 San José de Cúcuta, 05001 Medellín.

**EVA (8 filas aceptadas):**

| fila_fuente | Municipio | Año | Periodo | Cultivo | Área cosechada (ha) | Producción (t) | Caso que prueba |
|---:|---|---:|---|---|---:|---:|---|
| 2 | 15001 Tunja | 2021 | 2021A | Papa · En fresco | 10 | 200 | Dos periodos del mismo año |
| 3 | 15001 Tunja | 2021 | 2021B | Papa · En fresco | 30 | 900 | Dos periodos del mismo año |
| 4 | 15001 Tunja | 2021 | 2021A | Arveja · En fresco | 5 | 25 | Segundo cultivo en el mismo municipio |
| 5 | 15001 Tunja | 2022 | 2022A | Papa · En fresco | 0 | 0 | Área 0: no apta para rendimiento |
| 7 | 54001 Cúcuta | 2021 | 2021A | Arroz · Paddy | 100 | 500 | Suelo enlazado por alias |
| 8 | 15248 El Espino | 2022 | 2022A | Maíz · Grano seco | 8 | 16 | Suelo enlazado por alias |
| 9 | 05001 Medellín | 2021 | 2021A | Apio · En fresco | 8 | 128 | Sin muestras de suelo |
| 10 | 25999 (inexistente) | 2021 | 2021A | Papa · En fresco | 4 | 40 | Código ausente de DIVIPOLA |

**AGROSAVIA (7 muestras aceptadas):**

| id_muestra | clave_territorial | Año | pH | Caso que prueba |
|---|---|---:|---:|---|
| 101 | BOYACA\|TUNJA | 2021 | 5,0 | Mediana de dos muestras |
| 102 | BOYACA\|TUNJA | 2021 | 6,0 | Mediana de dos muestras |
| 103 | BOYACA\|TUNJA | 2022 | ND | pH nulo: mediana nula, pero cuenta como muestra |
| 104 | NORTE DE SANTANDER\|CUCUTA | 2021 | 7,0 | Alias → SAN JOSE DE CUCUTA |
| 105 | BOYACA\|ESPINO | 2022 | 4,5 | Alias → EL ESPINO |
| 106 | CAUCA\|BORRAR | 2021 | 5,5 | Sin enlace: va a `sin_correspondencia` |
| 107 | BOYACA\|TUNJA | 2019 | 5,2 | Año sin EVA: queda en suelo, no en unificado |

## Resultado esperado de SILVER

También está en `raw/esperado_silver.json`; la sección 14 del notebook SILVER lo compara con la publicación.

| Medida | Valor | Cálculo |
|---|---:|---|
| Filas unificado | 8 | Igual a EVA: las uniones no multiplican filas |
| Filas aptas para rendimiento | 7 | Todas menos la fila 5 (área 0) |
| Códigos EVA sin DIVIPOLA | 1 | 25999 |
| AGROSAVIA enlazadas / sin enlace / por alias | 6 / 1 / 2 | 106 no enlaza; 104 y 105 por alias |
| Filas de `suelo_municipio_anio` | 5 | Tunja 2019, 2021 y 2022; Cúcuta 2021; El Espino 2022 |
| Tunja 2021: muestras, mediana pH | 2, 5,5 | (5,0 + 6,0) / 2 |
| Tunja 2022: muestras, mediana pH | 1, nulo | La única muestra tiene pH ND |
| Filas EVA con suelo | 75 % | 6 de 8: sin suelo Medellín y 25999 |
| Producción total | 1 809 t | 200 + 900 + 25 + 0 + 500 + 16 + 128 + 40 |
| Área cosechada total | 165 ha | 10 + 30 + 5 + 0 + 100 + 8 + 8 + 4 |
| `area_cosechada_m2` de la fila 2 | 100 000 m² | 10 ha × 10 000 |
| Filas de `sin_correspondencia` | 2 | agrosavia `CAUCA\|BORRAR` (1) y eva `25999` (1) |
| Particiones `anio/codigo_departamento` | 5 | 2021: 05, 15, 25, 54 · 2022: 15 |

## Referencia para GOLD (Julián)

Sobre `silver/`, solo filas aptas y por municipio × año × cultivo × estado físico:

| Municipio | Año | Cultivo | Producción (t) | Área (ha) | Rendimiento (t/ha) |
|---|---:|---|---:|---:|---:|
| Tunja | 2021 | Papa · En fresco | 1 100 | 40 | 27,5 (no 25 = promedio de 20 y 30) |
| Tunja | 2021 | Arveja · En fresco | 25 | 5 | 5,0 |
| Cúcuta | 2021 | Arroz · Paddy | 500 | 100 | 5,0 |
| El Espino | 2022 | Maíz · Grano seco | 16 | 8 | 2,0 |
| Medellín | 2021 | Apio · En fresco | 128 | 8 | 16,0 |
| 25999 | 2021 | Papa · En fresco | 40 | 4 | 10,0 |

Tunja 2022 (área 0) no aparece. Rendimiento nacional de Papa · En fresco en 2021 = (1 100 + 40) / (40 + 4) = 25,909 t/ha → índice relativo de Tunja = 27,5 / 25,909 = 1,061; del municipio 25999 = 10 / 25,909 = 0,386. Cultivos presentes en un solo municipio tienen índice 1.
