# Entorno y procedimiento de descarga

El clon de GitHub no incluye los datos. Obtenerlos por descarga o respaldo antes de ejecutar `--verificar`; hasta entonces la verificación informará archivos ausentes.

## Preparación del portátil

Python 3.12, terminal y editor de texto son suficientes para iniciar. Se recomienda 16 GB de RAM; con 8 GB se trabaja con dos hilos, un departamento y muestras geográficas. Reservar 5 GB para kit y salidas y, como presupuesto preventivo, 10–15 GB para todo el entorno con Python, Spark, Java y QGIS. No se requiere GPU ni nube. La instalación de bibliotecas puede consumir cientos de MB y Spark y QGIS pueden añadir varios GB instalados; estos son rangos de planificación, no mediciones del archivo de datos.

QGIS es opcional para ejecutar los scripts y necesario para la práctica visual de mapas. Descargarlo desde qgis.org y registrar la versión instalada. Spark 4.0.1 se introduce en la sesión 5 y requiere Java 17 o posterior; para una cohorte estable se recomienda fijar Java 17 o 21 y no actualizar en mitad del curso.

## Instalación en macOS y Linux

```
cd /ruta/al/kit
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python 00_datos.py --listar
python 00_datos.py --verificar
```

## Instalación en Windows con CMD

```
cd C:\curso\kit
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python 00_datos.py --verificar
```

Los comandos Windows anteriores corresponden a CMD. Si se usa PowerShell, abrir CMD para seguir esta guía sin cambiar políticas del sistema. Un error de “módulo no encontrado” se resuelve comprobando que python y pip pertenecen al entorno activado. No instalar todas las dependencias en el Python del sistema.

## Tres rutas para obtener los datos

- Ruta A, recomendada para clase: descomprimir el paquete docente, que ya contiene data/raw. Ejecutar --verificar. Permite continuar sin Internet una vez instalado el software.
- Ruta B, práctica de descarga: crear una carpeta nueva, copiar 00_datos.py y fuentes.json, y ejecutar --descargar con los IDs requeridos. No descargar todas las fuentes simultáneamente.
- Ruta C, contingencia: copiar una carpeta raw de respaldo verificada mediante --respaldo. El script comprueba el SHA-256 antes de incorporar archivos.

```
python 00_datos.py --descargar agrosavia divipola eva
python 00_datos.py --descargar igac_capacidad igac_quimica
python 00_datos.py --descargar soilgrids wosis nasa chirps
python 00_datos.py --respaldo "/ruta/kit_original/data/raw" --verificar
```

Las URLs exactas están en fuentes.json y en el [catálogo del repositorio](datasets.md). El descargador limita cada respuesta a tres veces el tamaño de referencia o 2 MB, lo que sea mayor. Rechaza páginas HTML, no sobrescribe archivos existentes y conserva una descarga que cambió como .nueva. Un SHA-256 distinto puede deberse a nuevos datos o a cambios de serialización: el docente revisa esquema, valores y conteos antes de aprobar otro corte. No se considera que un HTTP 200 por sí solo sea una descarga válida.

## Descarga manual de los shapes DANE

[Consultar fuente](<https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/datos-geoestadisticos/>)

- Abrir el catálogo vigente y buscar MGN2025-Nivel. Seleccionar los enlaces de Nivel Departamento y Nivel Municipio en formato Shapefile.
- Guardar los ZIP sin modificar como dane_departamentos.zip y dane_municipios.zip dentro de data/raw. Tamaños observados: 12,52 MB y 71,58 MB. Las etiquetas del catálogo pueden diferir del tamaño descargado.
- Verificar con 00_datos.py --verificar. Para QGIS, extraer cada ZIP a una carpeta propia y abrir su .shp. Conservar .shx, .dbf y .prj en la misma carpeta.
- Si el portal responde 403 o la descarga tarda, usar la copia docente. No insistir con múltiples descargas. El enlace antiguo del MGN devolvió 404 y no debe quedar como dependencia del taller.

No descargar MGN2025_00_COLOMBIA.zip con todos los niveles: el catálogo anuncia aproximadamente 1,5 GB y contiene detalle que no requiere el curso. Los dos ZIP seleccionados incluyen exclusivamente los niveles necesarios. No se reemplazan polígonos por puntos de DIVIPOLA para evitar esa descarga.

## Verificación y organización

```
kit/
  fuentes.json
  00_datos.py
  talleres.py
  spark_taller.py
  data/raw/       # originales sin editar
  salidas/        # resultados reconstruibles
  entregas/      # informes personales
```

Leer salidas/verificacion.json: archivo presente, huella coincidente, conteo esperado, JSON sin error de API y ZIP íntegro. Los scripts reconstruyen y sobrescriben sus salidas homónimas; las conclusiones del estudiante se guardan en entregas. En nuevas descargas registrar fecha, versión, licencia, URL, tamaño y huella. Para reproducibilidad guardar también python --version y python -m pip freeze.

## Uso desde este repositorio

Ejecutar los comandos desde `kit/`. El clon no incluye `data/raw/`: obtener los archivos mediante el descargador o un respaldo docente y luego ejecutar `python 00_datos.py --verificar`. DANE se descarga mediante navegador según las URLs de `fuentes.json`. Las salidas se escriben en `kit/salidas/` y están excluidas de Git.

Los talleres tabulares necesitan AGROSAVIA, EVA y DIVIPOLA; geografía requiere el ZIP municipal y las muestras IGAC; clima requiere NASA, CHIRPS, SoilGrids y WoSIS. Spark por lotes requiere ejecutar primero `calidad` y `consultas`; el modelo requiere `consultas`. El taller de eventos lee NASA directamente. Windows sigue pendiente de validación.

[Volver al índice](../README.md).

## Dependencias adicionales de Spark

Desde `kit/`, con el entorno activo y Java instalado:

```sh
java -version
python -m pip install -r requirements_spark.txt
python spark_taller.py lotes
python spark_taller.py eventos
```

Ejecutar `calidad` y `consultas` antes de `lotes`; disponer de `nasa.json` antes de `eventos`.
