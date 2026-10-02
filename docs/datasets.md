# Catálogo de fuentes y tamaños

Preparado por el PhD Esteban Hernández, CyberColombia.

El corte agroambiental conserva doce archivos originales, 136,4 MB. Supersalud aporta tres CSV completos adicionales, 1.816.243.049 bytes (1,816 GB decimales), y tres muestras reales de 1.000 filas, 2.234.994 bytes en total. Son quince fuentes/archivos originales de trabajo; las muestras se derivan de los tres CSV, sin contarse como otras fuentes. Las versiones, separadores, tamaños y hashes están en fuentes.json y pqrs_fuentes.json.

## D01 AGROSAVIA

92.738 filas y 32 columnas. Análisis de laboratorio con fechas, territorio, cultivo y propiedades químicas.

Archivo docente: agrosavia.csv. Descarga observada: 20.380 MB (20,379,743 bytes). Alcance: completo.

Propósito: E01, E02, E04, E05, E06 y E13. pH no disponible: 11 filas.

Atención: Conservar ND, unidades y método analítico. No hay coordenadas de muestras en este CSV. No asignarles las coordenadas municipales de DIVIPOLA.

[Fuente](<https://www.datos.gov.co/api/views/ch4u-f3i5/rows.csv?accessType=DOWNLOAD>)

## D02 DIVIPOLA

1.122 registros y 7 columnas. Corte declarado: 30 de diciembre de 2024.

Archivo docente: divipola.csv. Descarga observada: 0.071 MB (70,850 bytes). Alcance: completo.

Propósito: E03, E05, E06 y E13. Clave municipal de cinco caracteres.

Atención: Incluye 1.103 municipios, 18 áreas no municipalizadas y una isla. Un punto territorial no es un polígono ni la posición de una muestra de suelo.

[Fuente](<https://www.datos.gov.co/api/views/gdxc-w37w/rows.csv?accessType=DOWNLOAD>)

## D03 MGN departamentos 2025

33 polígonos, incluido Bogotá D.C. ZIP con SHP, SHX, DBF y PRJ.

Archivo docente: dane_departamentos.zip. Descarga observada: 12.524 MB (12,524,421 bytes). Alcance: completo.

Propósito: E08 y E13. Contexto cartográfico departamental.

Atención: Descarga por navegador. Mantener componentes juntos y revisar el archivo PRJ. Los límites del MGN se usan con finalidad geoestadística.

[Fuente](<https://geoportal.dane.gov.co/descargas/mgn_2025/MGN2025_DPTO_POLITICO.zip>)

## D04 MGN municipios 2025

1.122 geometrías. Campo mpio_cdpmp de cinco caracteres.

Archivo docente: dane_municipios.zip. Descarga observada: 71.576 MB (71,576,494 bytes). Alcance: completo.

Propósito: E03, E08 y E13. Cruce territorial y geometrías.

Atención: mpio_ccdgo tiene solo tres caracteres. Usar mpio_cdpmp; no unir por nombres ni por códigos municipales incompletos. El corte cartográfico es 2025.

[Fuente](<https://geoportal.dane.gov.co/descargas/mgn_2025/MGN2025_MPIO_GRAFICO.zip>)

## D05 EVA UPRA 2019 a 2025

166.732 filas, 18 columnas. Área sembrada y cosechada, producción y rendimiento.

Archivo docente: eva.csv. Descarga observada: 27.490 MB (27,489,649 bytes). Alcance: completo.

Propósito: E06, E07, E10, E12 y E13. Rendimiento por cultivo, territorio y período.

Atención: Cultivos transitorios cambian su referencia metodológica desde 2022. Comparar períodos compatibles y estado físico. No sumar ni promediar sin ponderación rendimientos t/ha.

[Fuente](<https://www.datos.gov.co/api/views/uejq-wxrr/rows.csv?accessType=DOWNLOAD>)

## D06 Correlación de suelos IGAC

10 registros de atributos de unidades cartográficas a escala 1:100.000. Esta muestra no incluye geometría.

Archivo docente: igac_correlacion.json. Descarga observada: 0.012 MB (11,827 bytes). Alcance: muestra.

Propósito: E01, E04 y E09. Contraste de esquemas, taxonomía y metadatos.

Atención: No se puede dibujar un mapa a partir de estos diez atributos sin obtener geometrías. No confundir unidades cartográficas con muestras puntuales.

[Fuente](<https://mapas.igac.gov.co/server/rest/services/agrologia/correlacionsuelosnacional/MapServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&resultRecordCount=10&f=json>)

## D07 Capacidad de uso IGAC

Cinco polígonos con clase y descripción de capacidad. GeoJSON en EPSG:4326.

Archivo docente: igac_capacidad.json. Descarga observada: 0.096 MB (95,845 bytes). Alcance: muestra.

Propósito: E08 y E13. Intersección y limitaciones de uso.

Atención: La muestra no representa el país. Capacidad de uso no es rendimiento agrícola medido. Recalcular área después de intersectar.

[Fuente](<https://mapas.igac.gov.co/server/rest/services/agrologia/capacidaddeusodelastierrasterritorionacional/MapServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&outSR=4326&resultRecordCount=5&f=geojson>)

## D08 Propiedades químicas IGAC

Cinco polígonos con clases de pH, aluminio, fósforo y otras propiedades.

Archivo docente: igac_quimica.json. Descarga observada: 0.030 MB (30,182 bytes). Alcance: muestra.

Propósito: E08, E09 y E13. Calidad química y comparación de escalas.

Atención: Los intervalos como ≤ 5.5 son categorías, no números puntuales. No sustituir el intervalo por su extremo ni derivar un índice de salud sin justificación.

[Fuente](<https://mapas.igac.gov.co/server/rest/services/agrologia/distribucionycalidaddelaspropiedadesquimicasterritorionacional/MapServer/0/query?where=1%3D1&outFields=*&returnGeometry=true&outSR=4326&resultRecordCount=5&f=geojson>)

## D09 SoilGrids pH

Recorte GeoTIFF de 44 × 42 celdas, media predicha de pH a 0–5 cm. Caja: longitud -73,4 a -73,3; latitud 5,5 a 5,6.

Archivo docente: soilgrids.tif. Descarga observada: 0.002 MB (1,815 bytes). Alcance: muestra.

Propósito: E09 y E13. Datos ráster y factores de escala.

Atención: Dividir valores por 10. Se detectaron 188 celdas cero sin NoData declarado: ponerlas en revisión y excluirlas provisionalmente de la media interpretativa. No descargar el mundo completo.

[Fuente](<https://maps.isric.org/mapserv?map=/map/phh2o.map&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID=phh2o_0-5cm_mean&FORMAT=image/tiff&SUBSETTINGCRS=http://www.opengis.net/def/crs/EPSG/0/4326&SUBSET=long(-73.4,-73.3)&SUBSET=lat(5.5,5.6)>)

## D10 WoSIS Colombia

Diez registros de horizontes/capas de tres perfiles, filtrados para Colombia.

Archivo docente: wosis.json. Descarga observada: 0.007 MB (7,399 bytes). Alcance: muestra.

Propósito: E09 y E13. Profundidad, método y licencia por registro.

Atención: No son diez perfiles independientes. Las coordenadas y profundidades deben coincidir antes de contrastar con SoilGrids. Revisar licencia de cada proveedor.

[Fuente](<https://maps.isric.org/mapserv?map=%2Fmap%2Fwosis_latest.map&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=ms%3Awosis_latest_phaq&COUNT=10&OUTPUTFORMAT=geojson&FILTER=%3CFilter+xmlns%3D%22http%3A%2F%2Fwww.opengis.net%2Ffes%2F2.0%22%3E%3CPropertyIsEqualTo%3E%3CValueReference%3Ecountry_name%3C%2FValueReference%3E%3CLiteral%3EColombia%3C%2FLiteral%3E%3C%2FPropertyIsEqualTo%3E%3C%2FFilter%3E>)

## D11 NASA POWER

31 días de enero de 2025. Temperatura T2M y precipitación PRECTOTCORR para 5,54 N, -73,36.

Archivo docente: nasa.json. Descarga observada: 0.002 MB (1,555 bytes). Alcance: muestra.

Propósito: E11 y E13. JSON, agregación temporal y reproducción de eventos.

Atención: Punto demostrativo, no observación directa en una finca. Mantener el estándar temporal del archivo. -999 es dato faltante, no lluvia negativa.

[Fuente](<https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR&community=AG&longitude=-73.36&latitude=5.54&start=20250101&end=20250131&format=JSON>)

## D12 CHIRPS v3

GeoTIFF mensual de Latinoamérica, enero de 2025. 1.720 × 1.900 celdas.

Archivo docente: chirps.tif. Descarga observada: 4.213 MB (4,212,510 bytes). Alcance: muestra.

Propósito: E11 y E13. Recorte ráster y comparación de lluvia mensual.

Atención: No sumar lluvia entre píxeles como si fueran días. En este archivo hay valores -9999 y no se declara NoData; enmascarar negativos antes de resumir. No descargar todo el histórico.

[Fuente](<https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/latam/tifs/chirps-v3.0.2025.01.tif>)

Conjunto completo del kit: 136,4 MB de archivos originales, con los shapefiles todavía comprimidos. Extraer shapes y crear salidas aumenta el espacio. Para prácticas tabulares bastan AGROSAVIA, EVA y DIVIPOLA, aproximadamente 48 MB. El docente distribuye la copia fechada antes de la sesión; cada estudiante verifica las huellas y practica una descarga pequeña.

## D13 PQRS/PQRD Supersalud 2023-II

Archivo PQRD_2023_II.csv: 716,697 reportes, 38 columnas, 532.70 MB. Separador ';'; codificación utf-8-sig. El campo periodo almacena el año; corte_archivo se añade para conservar el semestre y archivo de origen. Muestra derivada de las primeras 1.000 filas: 0.752 MB. Uso: P01–P04, contratos, calidad y medición. Procedencia: Superintendencia Nacional de Salud, licencia CC BY 4.0 según metadatos conservados.

[Fuente](<https://mapas.supersalud.gov.co/arcgisportal/sharing/rest/content/items/515d4c6366854f549b24c704320f10f4/data>)

Descarga comprobada por lectura HTTP Range de la cabecera y coincidencia de sus 38 columnas el 2 de octubre de 2026. La copia local completa tiene hash registrado y perfil reproducible. Descargar un archivo por vez o usar la copia docente; no materializar los tres CSV originales juntos en RAM.

## D14 PQRS/PQRD Supersalud 2024-I

Archivo PQRD_2024_I.csv: 781,601 reportes, 38 columnas, 576.71 MB. Separador ','; codificación utf-8-sig. El campo periodo almacena el año; corte_archivo se añade para conservar el semestre y archivo de origen. Muestra derivada de las primeras 1.000 filas: 0.737 MB. Uso: P01–P04, contratos, calidad y medición. Procedencia: Superintendencia Nacional de Salud, licencia CC BY 4.0 según metadatos conservados.

[Fuente](<https://mapas.supersalud.gov.co/arcgisportal/sharing/rest/content/items/b52330a16b3940c39d38cb164c9dc014/data>)

Descarga comprobada por lectura HTTP Range de la cabecera y coincidencia de sus 38 columnas el 2 de octubre de 2026. La copia local completa tiene hash registrado y perfil reproducible. Descargar un archivo por vez o usar la copia docente; no materializar los tres CSV originales juntos en RAM.

## D15 PQRS/PQRD Supersalud 2024-II

Archivo PQRD_2024_II.csv: 946,468 reportes, 38 columnas, 706.84 MB. Separador ';'; codificación utf-8-sig. El campo periodo almacena el año; corte_archivo se añade para conservar el semestre y archivo de origen. Muestra derivada de las primeras 1.000 filas: 0.746 MB. Uso: P01–P04, contratos, calidad y medición. Procedencia: Superintendencia Nacional de Salud, licencia CC BY 4.0 según metadatos conservados.

[Fuente](<https://mapas.supersalud.gov.co/arcgisportal/sharing/rest/content/items/b257c9907b754b0cabb55a32e706bdee/data>)

Descarga comprobada por lectura HTTP Range de la cabecera y coincidencia de sus 38 columnas el 2 de octubre de 2026. La copia local completa tiene hash registrado y perfil reproducible. Descargar un archivo por vez o usar la copia docente; no materializar los tres CSV originales juntos en RAM.

OBJECTID se trata como clave candidata local al archivo; su unicidad se mide antes de usarlo. id_afec identifica afectados y no se presupone clave de reclamo. Se distinguen ubicación del peticionario, afectado y entidad. La dimensión territorial puede contextualizar cada dominio por separado; no hay unión fila a fila entre reportes de salud y muestras de suelo. Los códigos sin cruce se conservan para revisar vigencia, extensión y normalización con evidencia.
