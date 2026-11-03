# Grupo 1 · Presentación y consulta · Juan

> Proyecto: pipeline E12 → producto E13, ruta **agroambiental**. Entrega final: **7 de noviembre de 2026**.
> Diagrama de referencia: `Diagrama ejercicio 12.excalidraw` (raíz del repositorio).

## 1. Tu rol

Eres responsable de **mostrar la respuesta**: convertir el resultado de GOLD en el informe y el gráfico que pide el producto, con los límites de interpretación escritos. También preparas la ficha de auditoría que usará el otro equipo.

Pregunta del producto: **¿qué cultivos tienen mejor rendimiento por municipio y año?**

Entregable del diagrama: *informe agrupado por municipio y año del rendimiento de los cultivos, organizado de manera descendente, y un gráfico de barras apiladas indicando el municipio y la distribución de cultivos en años.*

| Paso del diagrama | Nota del diagrama | Qué significa para ti |
|---|---|---|
| Presentación | Se muestra la info en tabla y gráfica solicitada | Tabla descendente + barras apiladas + texto |

## 2. Convenciones del grupo (iguales para los 4)

- Salidas en `kit/salidas/grupo_1/<run_id>/presentacion/`. `run_id = uuid4().hex[:12]`. Fuera de Git.
- Columnas `snake_case` sin tildes; unidad en el sufijo (`_ha`, `_m2`, `_t`, `_t_ha`, `_kg_m2`). En la tabla y el gráfico finales sí usas nombres legibles con unidad: “Rendimiento (t/ha)”.
- Códigos DANE como texto con ceros: `codigo_departamento` (2), `codigo_municipio` (5).
- Decimales con punto en archivos; en textos del informe puedes usar coma decimal, pero sé consistente.
- Celda de parámetros al inicio:

  ```python
  RUN_ID = None
  ENTRADA_DIR = REPOSITORIO / 'soluciones' / 'plan_grupo_1' / 'fixtures' / 'gold'   # hasta el 4 nov
  # ENTRADA_DIR = REPOSITORIO / 'kit' / 'salidas' / 'grupo_1' / '<run_id>' / 'gold'  # desde el 4 nov
  SALIDA_DIR = REPOSITORIO / 'kit' / 'salidas' / 'grupo_1' / RUN_ID / 'presentacion'
  DEPARTAMENTO = '15'   # código del departamento para el gráfico (ej. 15 = Boyacá); acordar con el grupo
  TOP_CULTIVOS = 5
  ```

  `REPOSITORIO` con `encontrar_repositorio` de `soluciones/E12_solucion.ipynb` (sección 1), cambiando `pqrs_fuentes.json` por `fuentes.json`.
- **Versionamiento y equipo de ejecución**: en la celda de parámetros declara `RESPONSABLE = 'Juan'`, `EQUIPO_DESCRIPCION` (tipo de equipo y sistema, p. ej. “Portátil · WSL Ubuntu 26.04”), `VERSION_NOTEBOOK = 'G1_04_presentacion 1.0.0'` y `VERSION_REGLAS`. Copia la celda “Entorno de ejecución” (sección 2 de `soluciones/grupo_1/G1_02_silver.ipynb`) cambiando `'capa': 'presentacion'` y agregando `matplotlib` a la lista de librerías: escribe `presentacion/entorno.json` y el mismo bloque como `entorno` dentro de `controles_presentacion.json`. Campos: `capa, responsable, equipo_descripcion, version_notebook, version_reglas, fecha, zona_horaria, sistema, python, librerias, git`. No registres hostname, usuario ni rutas absolutas. Brayan compara los cuatro `entorno.json` antes de unificar.
- Tu notebook: `soluciones/grupo_1/G1_04_presentacion.ipynb`. Tu rama: `g1/presentacion-juan`. PR a `collaborators/bpineda`; revisa Brayan.

## 3. Entrada (contrato de Julián)

Carpeta `gold/` con:

- `rendimiento_cultivo.parquet` — una fila por municipio × año × cultivo × estado físico. Columnas: `codigo_departamento, departamento, codigo_municipio, municipio, anio, cultivo, estado_fisico, produccion_t, area_cosechada_ha, area_cosechada_m2, rendimiento_t_ha, rendimiento_kg_m2, rendimiento_nacional_t_ha, indice_relativo, rank_municipio_anio, n_registros, muestras_suelo, mediana_ph`.
  - `rank_municipio_anio = 1` es el cultivo con mejor rendimiento **relativo al promedio nacional** de ese mismo cultivo.
- `conciliacion.parquet`, `consultas_gold.sql`, `controles_gold.json`.

Antes de procesar: `controles_gold.json` con `estado = "valida"`.

**Mientras Julián termina (hasta el 4 nov)** trabaja con `soluciones/plan_grupo_1/fixtures/gold/`.

## 4. Salida

Carpeta `kit/salidas/grupo_1/<run_id>/presentacion/`:

### `informe_rendimiento.csv`
Por cada municipio y año, los `TOP_CULTIVOS` cultivos con `rank_municipio_anio <= TOP_CULTIVOS`, ordenados por `departamento, municipio, anio` y luego `rank_municipio_anio` ascendente (mejor primero = rendimiento descendente).

Columnas: `departamento, municipio, codigo_municipio, anio, rank_municipio_anio, cultivo, estado_fisico, rendimiento_t_ha, rendimiento_kg_m2, rendimiento_nacional_t_ha, indice_relativo, area_cosechada_ha, produccion_t`.

### `informe_rendimiento.md`
La misma tabla en Markdown **solo para `DEPARTAMENTO`** (la tabla nacional es demasiado larga), con un párrafo de lectura arriba.

### `barras_apiladas.png`
- Eje X: municipio y año (por ejemplo `Tunja 2021`, `Tunja 2022`…), para los **15 municipios de `DEPARTAMENTO` con más producción total**.
- Segmentos apilados: **participación del área cosechada** de cada cultivo en ese municipio-año (suma 100 %). Los 8 cultivos con más área del departamento con color propio; el resto en “Otros”.
- Título, ejes con unidad, leyenda y fuente (“EVA, cálculo grupo 1”).
- **No se apilan rendimientos**: t/ha de cultivos distintos no se pueden sumar. La barra muestra la distribución de cultivos en el tiempo; la tabla muestra cuál rinde mejor.
- Puedes usar matplotlib o seaborn (ya están en el entorno del curso). Opcional: segunda figura con el `indice_relativo` del cultivo top por municipio.

### `consultas_presentacion.sql`
Las consultas DuckDB usadas para la tabla y el gráfico, con un comentario cada una.

### `controles_presentacion.json`
`run_id, filas_entrada, filas_informe, municipios_grafico, produccion_total_gold_t, produccion_total_presentacion_t, area_departamento_gold_ha, area_departamento_grafico_ha, estado`.

### `texto_resultados_limites.md`
Texto para el informe E13 (1–2 páginas):
1. Qué muestra la tabla y cómo leer `indice_relativo`.
2. Tres hallazgos concretos del departamento elegido, con cifras y unidades.
3. Límites (obligatorio): resultados de asociación, no de causa; el rendimiento depende de clima, tecnología y manejo que no están en los datos; el suelo (AGROSAVIA) se asocia por municipio-año, no por parcela, y su cobertura es parcial; áreas muy pequeñas dan rendimientos inestables; EVA son estimaciones agregadas, no mediciones de campo.
4. Un resultado que **no** se puede inferir de los datos (exigido en E13).

### `ficha_auditoria.md` (plantilla)
Para la auditoría cruzada (E12 §8): `equipo auditor, fecha, consulta reproducida (copiada de consultas_gold.sql o consultas_presentacion.sql), resultado esperado, resultado obtenido, control revisado, hallazgo o control satisfactorio, evidencia (ruta/archivo), acción, comprobación posterior, limitación de interpretación explicada`. Brayan la completa con el otro equipo el 6 nov.

## 5. Tareas por fase

| Fase | Fecha | Qué haces |
|---|---|---|
| F0 Acuerdo | 31 oct | Lee este archivo. Activa el entorno, crea la rama `g1/presentacion-juan` y el notebook con secciones: parámetros, carga, tabla, gráfico, controles, textos. Acuerda con el grupo el `DEPARTAMENTO`. |
| F1 Desarrollo | 1–3 nov | Tabla y gráfico con `fixtures/gold/`. Borrador de `ficha_auditoria.md` y estructura de `texto_resultados_limites.md`. |
| F2 Datos reales | **4–5 nov** | Cambia `ENTRADA_DIR` a la salida real de Julián. Ajusta el gráfico (colores, etiquetas legibles). Escribe los hallazgos con cifras reales. |
| F3 Integración | 5 nov | Brayan copia tus secciones al notebook integrado; corrige lo que surja. Entrega la ficha a Brayan. |
| F4 Auditoría y entrega | 6–7 nov | En la clínica, ayuda a que el otro equipo reproduzca una consulta. En la sustentación presentas la tabla, el gráfico y los límites. |

## 6. Controles que tu notebook debe mostrar (con `assert`)

1. Todas las columnas del contrato de entrada existen.
2. En `informe_rendimiento.csv`, dentro de cada municipio-año, `rank_municipio_anio` va de menor a mayor y `indice_relativo` de mayor a menor.
3. `produccion_total_presentacion_t` (sumando **todas** las filas de `rendimiento_cultivo` que leíste) == `produccion_total_gold_t` de `controles_gold.json`.
4. En el gráfico, cada barra suma 100 % (tolerancia 0,01).
5. El área total del departamento que usaste en el gráfico == la misma suma calculada directamente sobre `rendimiento_cultivo` para ese departamento y municipios.
6. La imagen se guarda y se vuelve a abrir sin error.

## 7. Criterios de entrega (“hecho cuando…”)

- [ ] `Kernel → Restart & Run All` sin errores con fixture y con datos reales.
- [ ] Los 7 archivos de salida existen.
- [ ] Los 6 controles pasan y se ven en el notebook.
- [ ] El gráfico se entiende sin explicación: título, ejes con unidad, leyenda, fuente.
- [ ] `texto_resultados_limites.md` incluye cifras con unidad, los límites y un resultado no inferible.
- [ ] `ficha_auditoria.md` entregada a Brayan antes del 6 nov.
- [ ] PR con el notebook y los `.md` de texto (sin Parquet, CSV ni PNG pesados), aprobado por Brayan.

## 8. Cómo usar la IA en tu capa

- Pega la sección 3 (entrada) y la descripción del gráfico de la sección 4 antes de pedir código.
- Pide **un paso a la vez**: primero la consulta que arma la tabla; luego la que calcula la participación de área; luego el gráfico.
- Si la IA propone apilar `rendimiento_t_ha`, recházalo: no se puede sumar rendimiento de cultivos distintos.
- Usa la IA para mejorar la redacción del texto de límites, pero las cifras deben salir de tu notebook, no del asistente.
- Nunca quites un `assert` para que pase.

## 9. Riesgos y límites

- Un municipio con un solo año o un solo cultivo produce barras poco informativas; elige municipios con varios años.
- Si `DEPARTAMENTO` tiene pocos datos, cambia de departamento y regístralo en el notebook.
- Nombres de municipio repetidos en distintos departamentos: en la tabla nacional incluye siempre `departamento` y `codigo_municipio`.
