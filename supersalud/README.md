# Anexo Supersalud — notebooks docentes

[Índice del curso](../README.md)

Material histórico incorporado desde la rama `dev`, commit `24c7a15`, conservando íntegros los tres notebooks y su historial. Complementa SUELO SABIO con un caso de reclamos de salud; no sustituye los talleres E01–E13 ni añade horas obligatorias al curso.

## Índice y relación con el curso

| Notebook original | Contenido revisado | Clases donde puede utilizarse |
|---|---|---|
| [Sesión 1](ProfesorSesion1SuperSalud_BigData.ipynb) | pandas, tipos, memoria, faltantes, categorías, Parquet, particiones y gráficos | 2: perfilado; 3: formatos; 4: calidad; 7: medición |
| [Sesión 2](ProfesorSesion2SuperSalud_BigData.ipynb) | Contiene las mismas celdas de trabajo que la sesión 1; se conserva por trazabilidad | Misma ruta que la sesión 1; no se cuenta como un taller adicional |
| [Sesión 3](ProfesorSesion3Supersalud_BigData.ipynb) | Configuración JSON, ingesta con Polars, esquemas, Parquet por período/mes y reglas de calidad | 3–4: contratos y pipeline; 9: gobernanza; 10: integración |

Las sesiones 1 y 2 tienen 89 celdas cada una y las mismas fuentes de celda salvo el enlace inicial a Colab. La sesión 3 tiene 41 celdas. Son copias del profesor: contienen resultados guardados y orientaciones. Esos resultados proceden del trabajo original y no son una validación actual.

## Ejercicios de integración propuestos

1. **Perfilado y memoria — clases 2 y 3.** Tomar un fragmento de la sesión 1, identificar la unidad de observación y comparar memoria del DataFrame con tamaño CSV y Parquet. Entregar esquema, tamaño de muestra, tipos y medición; no inferir que reclamos equivalen a personas distintas.
2. **Contrato y calidad — clase 4.** Revisar faltantes, códigos territoriales y reglas del notebook. Separar ausencia, no aplica y valor inválido; mantener códigos como identificadores cuando corresponda. Entregar conciliación de filas y reglas justificadas. La falta de ubicación no demuestra que una petición sea anónima.
3. **Particionamiento — clase 7.** Comparar una consulta temporal sobre Parquet simple y particionado, verificando igualdad de resultados y controlando la carga y las repeticiones. El notebook original no constituye por sí solo un benchmark controlado.
4. **Pipeline y gobernanza — clases 9 y 10.** Revisar la sesión 3 y proponer orden de validación, escritura y registro de incidencias. Sustituir las alertas de correo por un registro local para la práctica. Entregar un diagrama y evidencia de aceptación o rechazo con datos de prueba.

El docente puede sustituir actividades equivalentes dentro de los bloques ya previstos. Los umbrales y categorías del ejercicio histórico son ejemplos para revisar, no reglas institucionales vigentes ni conclusiones clínicas.

## Preparación y límites de ejecución

Los notebooks se incorporan sin modificar su código ni sus salidas. **No se han ejecutado en esta integración y no están listos para ejecutar todas las celdas de corrido en el entorno actual.**

- Trabajar sobre una copia en un entorno separado del kit SUELO SABIO. Las importaciones incluyen pandas, NumPy, Matplotlib, seaborn, requests, PyArrow y, en la sesión 3, Polars. La rama no proporciona un entorno de versiones fijadas ni datasets adjuntos.
- Las sesiones 1 y 2 combinan rutas `/content/`, Google Drive, `raw/` y nombres distintos del CSV. Unificar rutas, codificación y separador antes de usarlas localmente. Algunas celdas escriben sobre archivos de entrada: conservar una copia original independiente.
- Los enlaces iniciales «Open in Colab» apuntan a los originales de `dev`; se conservan como parte del material histórico. Para trabajar con este anexo, abrir en Colab la URL del notebook de `main/supersalud/` o abrirlo con Jupyter.
- Hay descargas con `verify=False` y `curl -k`. Al adaptar la práctica, restaurar la verificación TLS y resolver errores de certificados; no usar esas excepciones como configuración habitual.
- La sesión 3 usa métodos de Polars que requieren comprobar compatibilidad, define dos veces la función de escritura, deja comentada la concatenación y lee una carpeta Parquet preexistente. Su verificación de esquema compara nombres, pero no demuestra igualdad de tipos ni devuelve los DataFrames normalizados.
- Las reglas llaman a `send_email`, cuya implementación no figura en el notebook. No ejecutar esas celdas sin adaptación; usar un registro local de alertas. No se enviaron mensajes ni se configuró correo durante esta revisión.
- Comprobar los tamaños y términos de los datasets antes de descargarlos. La rama contiene únicamente notebooks; no se han comprobado disponibilidad, tamaño ni esquema actual de las URLs originales. Los datos descargados, configuraciones locales y salidas se excluyen de Git.

## Procedencia y comprobación

Integración de los commits `60efa0a`, `75a48b0` y `24c7a15` mediante merge de `origin/dev`, seguida de traslado al directorio `supersalud/`. Se verificaron el JSON, el formato notebook y la igualdad byte a byte con los archivos de origen. Las huellas completas se registran en [procedencia.json](procedencia.json).
