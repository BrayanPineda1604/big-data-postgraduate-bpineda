# Revisión del material vigente

Preparado por el PhD Esteban Hernández, CyberColombia.

El calendario contractual comprende 12 clases entre el 2 de octubre y el 7 de noviembre de 2026. Se comprobaron 3.840 minutos efectivos de docencia en línea, excluyendo todos los recesos y almuerzos. El trabajo autónomo es opcional y no reemplaza horas de clase.

Las tres URL de Supersalud devolvieron HTTP 206 en una lectura Range de sus cabeceras y coincidieron con las 38 columnas del corte docente el 2 de octubre de 2026. Los CSV completos locales se verificaron por SHA-256, filas y esquema. Sumaron 2.444.766 filas y 1.816.243.049 bytes.

Se ejecutaron perfil, formatos, calidad y benchmark PQRS con muestras y archivos completos. Cinco motores conciliaron exactamente la misma agregación: pandas, Polars, DuckDB-Parquet, DuckDB-particionado y DuckDB-CSV. El lector particionado utiliza explícitamente hive_partitioning=True. Los tiempos incluyen arranque, lectura, consulta y exportación de un resultado pequeño. La RSS se sondeó cada 10 ms. Las mediciones pertenecen a esta máquina y consulta y no se extrapolan a otros equipos.

Los cuatro notebooks actuales se ejecutaron completamente con las muestras de 3.000 filas y las observaciones NASA reales. La reproducción finita obtuvo 13 entregas, 12 registros reales distintos, 11 aceptados, un reintento y un evento tardío. La regla Python no reproduce toda la semántica de Spark.

Los originales agroambientales y sus controles anteriores se conservan en el kit y su manifiesto. El script de modelo genera MAE y cobertura por año, cultivo y estado físico, además del resumen global. Las rutas originales de los notebooks históricos se preservan como referencia, fuera de la ruta de ejecución actual.

Los libros conservan el estilo del book-template y se compilaron con XeLaTeX. Las diapositivas modificadas mantienen tablas, textos y gráficos editables; se revisaron exportaciones y vistas renderizadas. No se verificó en PowerPoint la reproducción de animaciones ni se validó una instalación nueva de Windows o la interacción de QGIS en esta revisión.

## Comprobaciones de esta integración en dev

Se ejecutaron en orden todas las celdas de código de los cuatro notebooks vigentes en procesos Python locales (sin interfaz Jupyter), con las 3.000 filas de las muestras y el corte NASA. Se validó su formato con nbformat. El notebook 03 añade comparación exacta de la agregación de 2024 entre Polars y DuckDB: 2.000 reportes.

El benchmark verificó igualdad entre los cinco motores con tres repeticiones medidas y calentamiento. Se comprobó que rechaza etiquetar el producto de muestras como completo. En esta ejecución restringida no se pudo observar RSS y se obtuvo cero en ese campo: no es una medición de memoria válida. No se repitió el benchmark de 1,816 GB; sus resultados anteriores corresponden a la validación previa del material.

E12 se volvió a ejecutar: 15.267 pares para 2024 y 15.503 para 2025. La salida `evaluacion_por_cultivo.csv` contiene 317 grupos año–cultivo–estado físico; sus conteos y MAE ponderado concilian con el resumen global. Se verificaron cobertura entre 0 y 1, grupos sin año previo y conservación de denominadores.

Se comprobaron los enlaces locales y el calendario estructurado de doce clases y 3.840 minutos. Spark, Windows y QGIS no se volvieron a validar en esta integración. Los notebooks históricos permanecen sin ejecutar ni alterar.

## Nueva base WSL

Las instrucciones vigentes se unificaron en WSL 2 con Ubuntu-26.04, Python 3.12 gestionado por uv y JDK 21. La guía se contrastó con documentación oficial y se revisaron rutas y comandos. No se instaló ni se probó Ubuntu-26.04 en un equipo Windows durante este cambio.
