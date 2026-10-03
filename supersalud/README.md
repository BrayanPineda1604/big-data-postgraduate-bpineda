> Ruta de ejecución vigente: [notebooks adaptados](../kit/Notebooks/README.md), [P01](../talleres/P01.md)–[P04](../talleres/P04.md) y [calendario contractual](../docs/calendario.md). Los cuatro archivos de esta carpeta se conservan como material histórico y no deben ejecutarse como guía actual.

# Anexo Supersalud — notebooks docentes

[Índice del curso](../README.md)

Material histórico incorporado desde la rama `dev`, commit `6aed21d`, conservando los cuatro notebooks y su historial; únicamente se actualizan sus enlaces iniciales a Colab. Complementa SUELO SABIO con un caso de reclamos de salud; se aprovecha mediante P01–P04 e I01 dentro de las doce clases y no añade horas obligatorias.

## Índice y relación con el curso

| Notebook original | Contenido revisado | Clases donde puede utilizarse |
|---|---|---|
| [Sesión 1](ProfesorSesion1SuperSalud_BigData.ipynb) | pandas, tipos, memoria, faltantes, categorías, Parquet, particiones y gráficos | 2: perfilado; 3: formatos; 4: calidad; 7: medición |
| [Sesión 2](ProfesorSesion2SuperSalud_BigData.ipynb) | Contiene las mismas celdas de trabajo que la sesión 1; se conserva por trazabilidad | Misma ruta que la sesión 1; no se cuenta como un taller adicional |
| [Sesión 3](ProfesorSesion3Supersalud_BigData.ipynb) | Configuración JSON, ingesta con Polars, esquemas, Parquet por período/mes y reglas de calidad | 3–4: contratos y pipeline; 9: gobernanza; 10: integración |
| [Sesión 4](ProfesorSesion4Supersalud_BigData.ipynb) | Datos demográficos, índice agregado ilustrativo, comparación pandas–Polars de tiempo/memoria y simulaciones de streaming | 6: integración; 7: rendimiento; 8: ventanas y eventos; 9: interpretación |

Las sesiones 1 y 2 tienen 89 celdas cada una y las mismas fuentes de celda salvo el enlace inicial a Colab. La sesión 3 tiene 41 celdas y la sesión 4, 76. Son copias del profesor: contienen resultados guardados y orientaciones. Esos resultados proceden del trabajo original y no son una validación actual.

## Ejercicios de integración propuestos

1. **Perfilado y memoria — clases 2 y 3.** Tomar un fragmento de la sesión 1, identificar la unidad de observación y comparar memoria del DataFrame con tamaño CSV y Parquet. Entregar esquema, tamaño de muestra, tipos y medición; no inferir que reclamos equivalen a personas distintas.
2. **Contrato y calidad — clase 4.** Revisar faltantes, códigos territoriales y reglas del notebook. Separar ausencia, no aplica y valor inválido; mantener códigos como identificadores cuando corresponda. Entregar conciliación de filas y reglas justificadas. La falta de ubicación no demuestra que una petición sea anónima.
3. **Particionamiento — clase 7.** Comparar una consulta temporal sobre Parquet simple y particionado, verificando igualdad de resultados y controlando la carga y las repeticiones. El notebook original no constituye por sí solo un benchmark controlado.
4. **Pipeline y gobernanza — clases 9 y 10.** Revisar la sesión 3 y proponer orden de validación, escritura y registro de incidencias. Sustituir las alertas de correo por un registro local para la práctica. Entregar un diagrama y evidencia de aceptación o rechazo con datos de prueba.

5. **Rendimiento e integración — clases 6, 7 y 9.** Usar la sesión 4 para revisar claves territoriales, años y denominadores demográficos y comparar implementaciones de un índice agregado en pandas y Polars. Entregar diferencias numéricas, tiempo, memoria y límites de interpretación; el índice es didáctico y no una medida clínica validada.
6. **Ventanas y eventos — clase 8.** Explorar en la sesión 4 ventanas tumbling y sliding, colas acotadas y eventos fuera de orden. Entregar una traza de eventos admitidos y descartados, indicando tiempo de procesamiento, tiempo de evento y tolerancia al atraso. Estos eventos son sintéticos y están separados de los reclamos reales y de la reproducción NASA de E11.

El docente puede sustituir actividades equivalentes dentro de los bloques ya previstos. Los umbrales y categorías del ejercicio histórico son ejemplos para revisar, no reglas institucionales vigentes ni conclusiones clínicas.

## Preparación y límites de ejecución

Los notebooks conservan su código y sus salidas; los enlaces de Colab se ajustan al directorio `supersalud/` de `main`. **No se han ejecutado en esta integración y no están listos para ejecutar todas las celdas de corrido en el entorno actual.**

- Trabajar sobre una copia en un entorno separado del kit SUELO SABIO. Las importaciones incluyen pandas, NumPy, Matplotlib, seaborn, requests, PyArrow y, en la sesión 3, Polars. Los originales no aportaban un entorno fijado; la ruta vigente sí incluye dependencias y tres muestras reales en `kit/`.
- Las sesiones 1 y 2 combinan rutas `/content/`, Google Drive, `raw/` y nombres distintos del CSV. Unificar rutas, codificación y separador antes de usarlas localmente. Algunas celdas escriben sobre archivos de entrada: conservar una copia original independiente.
- Los enlaces iniciales «Open in Colab» apuntan a `main/supersalud/`. También se pueden abrir los archivos con Jupyter desde esta carpeta.
- Hay descargas con `verify=False` y `curl -k`. Al adaptar la práctica, restaurar la verificación TLS y resolver errores de certificados; no usar esas excepciones como configuración habitual.
- La sesión 3 usa métodos de Polars que requieren comprobar compatibilidad, define dos veces la función de escritura, deja comentada la concatenación y lee una carpeta Parquet preexistente. Su verificación de esquema compara nombres, pero no demuestra igualdad de tipos ni devuelve los DataFrames normalizados.
- Las reglas llaman a `send_email`, cuya implementación no figura en el notebook. No ejecutar esas celdas sin adaptación; usar un registro local de alertas. No se enviaron mensajes ni se configuró correo durante esta revisión.
- Comprobar los tamaños y términos de los datasets antes de descargarlos. Este anexo conserva únicamente los notebooks históricos; la ruta vigente documenta sus cortes comprobados en `kit/pqrs_fuentes.json`. Los datos descargados, configuraciones locales y salidas se excluyen de Git.

## Particularidades de la sesión 4

- Incluye instalaciones adicionales de psutil, Streamz, Dask y memory_profiler. Son instrucciones originales, no un entorno fijado y validado para el curso actual.
- Una celda selecciona `engine="gpu"`; para un portátil sin GPU compatible debe revisarse la variante CPU antes de ejecutar. No se presupone que instalar Polars habilite GPU.
- Varias demostraciones asíncronas se ejecutan hasta interrupción manual; la última incluye una duración acotada. Ejecutar cada bloque por separado y detenerlo antes de iniciar otro.
- Las mediciones originales no acreditan una ventaja universal: revisar calentamiento, conversiones, repetición y equivalencia de resultados.

## Procedencia y comprobación

Esta actualización de `dev` integra la organización realizada en `main` e incorpora la sesión 4 del commit `6aed21d`. Los cuatro notebooks quedan en `supersalud/`, sin copias en la raíz. Se comprobaron su estructura JSON, sus enlaces y la conservación de todas las celdas de código y salidas respecto a los originales. Las huellas originales y actualizadas se registran en [procedencia.json](procedencia.json). No se ejecutaron los notebooks ni se descargaron datasets durante esta reorganización.

## Ruta vigente para ejecutar

Usar [los notebooks actuales](../kit/Notebooks/README.md) y el [mapa de ejercicios](../docs/mapa-ejercicios.md). Los originales de este anexo permanecen sin nuevas modificaciones.

## Instalación vigente

Los comandos de instalación guardados en los originales son históricos. Para utilizarlos en el curso, adaptar las prácticas al entorno [WSL 2 con Ubuntu-26.04](../docs/instalacion-wsl.md). No seguir rutas de instalación nativas de Windows, macOS o Colab como alternativa a la guía vigente.

Para la ejecución vigente, clonar `main` en `/mnt/c/Users/TUPTC/bigdata/big-data-postgraduate` y usar los notebooks actuales de `kit/Notebooks/`. Las rutas internas de los notebooks históricos son referencias del ejercicio original, no instrucciones vigentes de instalación.
