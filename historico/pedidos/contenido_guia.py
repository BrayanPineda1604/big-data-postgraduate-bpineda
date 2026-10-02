guide = new_doc('Guía académica de Big Data', 'Material para docencia laboratorios y preparación de presentaciones\nPosgrado  |  Curso de 64 horas')
text(guide,'''Esta guía permite desarrollar las diez sesiones del curso mediante explicaciones, ejemplos, prácticas reproducibles y evaluación. El eje es un sistema ficticio de pedidos: los estudiantes transforman registros, verifican su calidad, construyen consultas, estudian el procesamiento de eventos y evalúan un modelo de entregas tardías.

El documento está dirigido al docente. Incluye respuestas y orientaciones de evaluación que conviene separar de la versión distribuida a estudiantes antes de cada actividad. El material se organiza para que cada unidad pueda convertirse posteriormente en una presentación, conservando los ejemplos, las preguntas y las demostraciones.

La carga total es de 64 horas: 56 horas y 15 minutos sincrónicos y 7 horas y 45 minutos autónomos. Se utiliza la agenda del programa académico, con recesos de 15 minutos y una hora de almuerzo los sábados. Las prácticas se realizan en un portátil; la discusión de clústeres y arquitecturas de producción amplía lo observado localmente.

# 1 Uso del material

## Ruta de lectura y enseñanza

Antes de la primera sesión, el docente debe revisar el caso, preparar el entorno y ejecutar el generador. En clase conviene introducir cada problema antes de mostrar el código. Se solicita una predicción, se ejecuta el experimento y se contrasta el resultado con esa predicción. Esta secuencia permite evaluar comprensión en lugar de limitar la actividad a copiar instrucciones.

La ruta de práctica es 01 generar datos, 02 depurar con DuckDB, 03 procesar con Spark, 04 medir formatos, 05 procesar eventos y 06 evaluar el modelo. Los programas completos aparecen dentro de esta guía y se suministran como archivos para evitar errores al copiar código desde Word. Los archivos deben ejecutarse desde la misma carpeta de trabajo.

## Mapa del documento

- Sección 2 Preparación del entorno y definición del caso transversal.
- Sección 3 Fundamentos y formulación del problema.
- Sección 4 Arquitecturas almacenamiento y calidad.
- Sección 5 Procesamiento con Apache Spark.
- Sección 6 Rendimiento y procesamiento de eventos.
- Sección 7 Analítica y gobernanza.
- Sección 8 Proyecto integrador rúbricas y plantillas de entrega.
- Sección 9 Banco de preguntas y solucionario.
- Sección 10 Guiones para preparar las presentaciones.
- Sección 11 Glosario y referencias.

## Acuerdos de trabajo

Los estudiantes conservarán los datos de entrada y producirán las salidas en archivos distintos. Cada resultado deberá indicar con qué versión del código, tamaño de datos y configuración se obtuvo. Al discutir rendimiento se informará el equipo utilizado. Los errores formarán parte del análisis: se registrará la causa, la corrección y el efecto sobre los resultados.

Las actividades de ampliación son alternativas para grupos que avancen más rápido. No constituyen tareas obligatorias adicionales a las 64 horas. El docente puede sustituir un reto por otro equivalente para mantener la carga y los resultados de aprendizaje.
''')
chapter(guide,'2 Preparación técnica y caso transversal')
text(guide,'''## Entorno de referencia

Se propone Python 3.12, Java 17 y las versiones del archivo requirements.txt. La combinación es una referencia para conservar un entorno uniforme durante el curso. No es necesario utilizar la versión más reciente de cada biblioteca. La instalación inicial necesita conexión; una vez descargados los paquetes, los laboratorios utilizan datos locales.

Instale Python desde su distribución oficial y un JDK 17 compatible con el sistema operativo. Verifique que java -version muestre la versión correcta y que JAVA_HOME apunte a la raíz de ese JDK. PySpark 4.0.1 admite Python 3.9 o posterior y requiere Java 17 o posterior [R1]. En Windows deben comprobarse las rutas y permisos con anticipación; no es necesario descargar ejecutables no verificados para seguir el curso.

Abra una terminal en la carpeta material_practico. Cree un entorno virtual para el curso y ejecute los siguientes comandos. Si Python 3.12 no es el Python predeterminado, utilice el ejecutable correspondiente.
''')
h(guide,'macOS y Linux',3)
code(guide,'''python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyter lab''')
h(guide,'Windows con la terminal de comandos',3)
code(guide,r'''py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m jupyter lab''')
p(guide,'En PowerShell se puede invocar directamente .venv\\Scripts\\python.exe sin cambiar políticas de ejecución. El intérprete elegido por Jupyter debe corresponder al entorno donde se instalaron los paquetes. Ejecute los programas desde la terminal activada o copie sus bloques en un notebook de ese entorno.')
h(guide,'Versiones de referencia',3)
code(guide,(LAB/'requirements.txt').read_text())
h(guide,'Comprobación mínima',3)
code(guide,'''python --version
java -version
python -c "import duckdb; print(duckdb.sql('SELECT 2 + 2').fetchone())"
python -c "import pandas, pyarrow, sklearn; print('Bibliotecas disponibles')"''')
p(guide,'Resultado esperado de la consulta: (4,). El inicio de Spark se comprobará con el programa 03 una vez producida la salida limpia. Si el equipo tiene 8 GB, conserve 20 000 registros, cierre aplicaciones pesadas y utilice local[2]. Un límite de memoria de DuckDB controla principalmente su gestor de memoria; el consumo total del proceso puede ser mayor. Debe quedar memoria libre para el sistema operativo y la videoconferencia.')
table(guide,['Problema observable','Verificación y acción'],[
('ModuleNotFoundError','Confirmar el intérprete activo y ejecutar python -m pip en ese entorno.'),
('Java gateway exited','Verificar java -version, JAVA_HOME y compatibilidad. Reiniciar el proceso de Python después del cambio.'),
('No se encuentra datos/limpio.parquet','Ejecutar 01 y luego 02 desde la carpeta material_practico.'),
('Equipo sin memoria suficiente','Reducir el número de filas, cerrar otras aplicaciones y evitar collect sobre toda la tabla.'),
('Error al iniciar el servicio local de Spark','Revisar permisos de red local, resolución del nombre del equipo y registro del error. Utilizar el ejemplo mínimo antes del proyecto.'),
('Resultados diferentes entre ejecuciones','Comprobar semilla, tamaño del archivo, versiones y si se reutilizaron salidas de otro experimento.')],[5.0,11.8])
text(guide,'''## Caso de pedidos y tiempos de entrega

Una organización ficticia desea analizar ventas por ciudad y anticipar pedidos cuya entrega superará 60 minutos. Cada fila describe un pedido terminado. El instante event_time representa la creación del pedido y delivery_minutes se conoce únicamente después de finalizar la entrega. Se asume hora local de Colombia sin cambio estacional en este conjunto didáctico.

La pregunta descriptiva es qué ciudades concentran pedidos e importes. La pregunta predictiva es si, en el momento de crear un pedido, puede anticiparse una entrega tardía. Esta distinción obliga a revisar qué variables están disponibles cuando se toma la decisión.

Los datos son sintéticos y contienen errores deliberados. Se introducen ciudades ausentes, cantidades cero, precios negativos y duplicados exactos. Las ciudades son etiquetas del ejemplo, no evidencia sobre sus condiciones reales. El importe se guarda en centavos de una moneda didáctica para evitar diferencias de redondeo entre motores.
''')
table(guide,['Campo','Tipo lógico','Interpretación y regla'],[
('id','Entero de 64 bits','Identificador único de pedido después de depurar.'),('event_time','Fecha y hora','Creación del pedido en hora local.'),('city','Texto','Tunja, Bogota, Medellin o Cali; obligatorio.'),('category','Texto','Hogar, Tecnologia o Alimentos.'),('units','Entero','Unidades; debe ser mayor que cero.'),('price_cents','Entero de 64 bits','Precio unitario en centavos; debe ser positivo.'),('delivery_minutes','Entero','Duración observada; no disponible al crear el pedido.'),('amount_cents','Entero derivado','units multiplicado por price_cents.'),('late','Binario derivado','1 si delivery_minutes es mayor que 60; objetivo del modelo.')],[3.8,3.4,9.6])
text(guide,'''## Generador y resultados controlados

El programa escribe el CSV de manera secuencial, usa semilla 64 y genera un archivo esperado.json con cantidades de control. Los registros cuyo identificador es múltiplo de 97 pierden la ciudad; los múltiplos de 113 reciben cantidad cero; los múltiplos de 157 reciben precio negativo. Los múltiplos de 199 se escriben una segunda vez, conservando exactamente sus valores.

Una fila puede incumplir más de una regla, por lo que no se deben sumar ciegamente los conteos de errores para estimar rechazados. El archivo de control calcula el conjunto válido después de aplicar todas las condiciones. La verificación se apoya en ese resultado, no en una cifra digitada manualmente por el estudiante.
''')
h(guide,'Programa 01 Generación de datos',3)
labcode(guide,'01_generar_datos.py')
code(guide,'''python 01_generar_datos.py --n 20000''')
p(guide,'Para ampliar la carga puede usarse --n 100000 o --n 1000000 después de verificar espacio y memoria. Cada nueva ejecución reemplaza pedidos.csv y esperado.json en la carpeta del ejercicio; también se deben regenerar las salidas siguientes para no mezclar experimentos. El generador no representa una distribución real ni contiene estacionalidad operacional validada.')
chapter(guide,'3 Fundamentos y formulación del problema')
text(guide,'''## Resultados y secuencia de la unidad

El estudiante distinguirá un problema de capacidad de un problema de calidad, propondrá una pregunta analítica y justificará una arquitectura inicial. El viernes se dedican 60 minutos a diagnóstico y caso, 60 a conceptos, 75 a formulación y 30 a discusión. El sábado se distribuyen 90 minutos en entorno y demostración, 135 en generación y perfilado, 120 en resolución del caso, 75 en revisión entre pares y 30 en cierre. Los recesos siguen el programa.

## Qué hace que un problema sea de Big Data

Big Data describe situaciones en las que las características de los datos y las exigencias de procesamiento superan de manera relevante las capacidades del enfoque disponible. No existe un número universal de filas que convierta una tabla en Big Data. Un archivo grande que se procesa una vez al mes puede ser viable en un equipo local; un flujo pequeño con exigencias estrictas de latencia puede requerir otra arquitectura.

El volumen afecta almacenamiento, lectura y memoria. La velocidad se refiere tanto a la llegada de datos como al tiempo permitido para responder. La variedad exige integrar estructuras y significados diferentes. La veracidad plantea si los datos son suficientemente confiables para el uso previsto. El valor depende de la decisión que se mejora y no de la cantidad de herramientas instaladas.

Ejemplo para discutir: una tabla de 20 millones de ventas se consulta una vez al día y el informe puede tardar diez minutos. Antes de proponer un clúster, se medirán tamaño en disco, columnas leídas, memoria necesaria y tiempo de consulta con un motor local. Si el problema es un código de cliente inconsistente, agregar nodos no resolverá ese defecto.

## Escalabilidad y límites del paralelismo

Escalar verticalmente consiste en aumentar recursos de una máquina. Escalar horizontalmente consiste en añadir máquinas y distribuir el trabajo. La primera opción puede simplificar la operación, pero encuentra límites físicos y económicos. La segunda permite repartir carga, aunque incorpora coordinación, movimiento de datos y manejo de fallos parciales.

El paralelismo divide tareas que pueden ejecutarse simultáneamente. La concurrencia permite mantener varias tareas en progreso, aunque no todas se ejecuten al mismo instante. Tener ocho núcleos no garantiza que un programa termine ocho veces más rápido: parte del trabajo puede ser secuencial o estar limitada por el disco.

Ejemplo de cálculo: si el 80 % de un trabajo es paralelizable y el 20 % permanece secuencial, el máximo teórico con cuatro procesadores, sin costos adicionales, es 1 dividido por (0,20 + 0,80/4), equivalente a 2,5 veces. Este cálculo sirve como límite ideal; una medición real puede ser menor por coordinación y transferencia.

## Latencia capacidad y crecimiento

La latencia es el tiempo que transcurre desde una solicitud hasta su respuesta. El throughput es la cantidad de trabajo terminada por unidad de tiempo. Ambos se necesitan: un sistema puede completar muchos eventos por segundo y aun así entregar respuestas tarde si existe una cola acumulada.

Ejercicio resuelto: una fuente produce 1 000 eventos por segundo de 500 bytes. Su volumen bruto es 500 000 bytes por segundo y 43,2 GB por día, utilizando unidades decimales. Tres copias completas ocuparían 129,6 GB diarios antes de compresión, índices y metadatos. El cálculo no equivale al costo total: faltan retención, redes, procesamiento y operación.

Si la llegada sostenida es de 1 000 eventos por segundo y el sistema solo procesa 800, la cola crece aproximadamente 200 eventos por segundo. Un sistema estable necesita capacidad suficiente y margen para picos y recuperación. Promediar la demanda de todo el día puede ocultar una hora de saturación.

## Componentes de una solución distribuida

Una solución puede separar captura, almacenamiento, procesamiento, catálogo y consumo. El catálogo describe qué datos existen y qué significan. El procesamiento transforma y agrega. El consumo ofrece consultas, modelos o productos de información. Cada frontera debe indicar entradas, salidas, responsables y condiciones de error.

La partición divide datos entre unidades de almacenamiento o cómputo. La replicación conserva copias para disponibilidad o recuperación. Una copia no sustituye una política de respaldo si un borrado lógico se propaga a todas las réplicas. La tolerancia a fallos requiere detectar y recuperar trabajo sin alterar su significado.

Una operación idempotente produce el mismo efecto final al repetirse con la misma entrada. Es importante cuando un mensaje o tarea se reintenta. Sumar dos veces un pedido no es idempotente; registrar su identificador y reemplazar una representación única puede serlo, según el diseño. La deduplicación necesita una definición explícita de identidad.

## Formulación de la pregunta

Una pregunta útil debe especificar unidad de análisis, período, población, variable de resultado y decisión. “Analizar Big Data de ventas” es demasiado amplio. “Comparar pedidos e importe por ciudad durante el período disponible para priorizar una revisión operacional” puede ejecutarse y verificarse con el caso.

Para la predicción, el instante de decisión debe quedar escrito. Anticipar una entrega tardía al crear el pedido excluye información observada al terminarla. La calidad del planteamiento se evalúa antes de medir la precisión del modelo, porque un objetivo mal definido puede producir un resultado técnicamente correcto e inútil.

## Laboratorio 1 Perfilado y ficha del problema

Objetivo: caracterizar los datos originales y establecer una pregunta verificable. Insumos: programa 01 y un conjunto de 20 000 registros únicos antes de duplicados. Duración sugerida de trabajo central: 135 minutos.

- Ejecutar el generador y registrar tamaño del CSV y conteos del archivo de control.
- Leer el CSV como texto o con pandas y revisar tipos, vacíos, rangos y duplicados.
- Diferenciar número de filas, pedidos distintos y filas válidas.
- Formular una pregunta descriptiva y una predictiva; identificar cuándo se conocen las variables.
- Redactar una ficha de una página y contrastarla con otro equipo.
''')
code(guide,'''import pandas as pd
df = pd.read_csv('datos/pedidos.csv')
print('Filas:', len(df))
print('Pedidos distintos:', df['id'].nunique())
print('Duplicados exactos:', df.duplicated().sum())
print(df.isna().sum())
print(df[['units', 'price_cents', 'delivery_minutes']].describe())''')
text(guide,'''Resultado esperado: el número de filas es mayor que el de identificadores distintos y aparecen ciudades vacías, cantidades cero y precios negativos. El estudiante deberá explicar por qué el archivo de control y la inspección de los datos constituyen evidencias diferentes que se deben conciliar.

Respuesta orientadora: la unidad es el pedido identificado por id. Una ciudad vacía afecta comparaciones geográficas; una cantidad cero afecta importes; un duplicado infla conteos y sumas. No se debe concluir que el archivo es útil para todas las preguntas solo porque puede leerse sin errores.

Trabajo autónomo de 45 minutos: 15 para precisar la pregunta, 15 para completar el diccionario y 15 para justificar criterios de éxito. Cierre oral: ¿qué medición haría cambiar la arquitectura propuesta? Una respuesta sólida nombra una restricción medible, como memoria, tiempo de respuesta o volumen diario.
''')
chapter(guide,'4 Arquitecturas almacenamiento y calidad')
text(guide,'''## Resultados y secuencia de la unidad

El estudiante seleccionará un esquema de almacenamiento, construirá controles de calidad y conciliará la transformación. El viernes se distribuyen 60 minutos en arquitecturas, 60 en formatos, 75 en reglas y 30 en defensa de decisiones. El sábado se destinan 90 a demostración, 135 al pipeline, 120 a consultas y formatos, 75 a revisión y 30 a cierre.

## Warehouse lake y lakehouse

Un data warehouse organiza datos integrados para consulta y análisis con estructuras y definiciones estables. Su valor está en ofrecer métricas consistentes, modelos documentados y controles de acceso. Un data lake conserva datos de diversos formatos y estados de procesamiento, por lo que necesita catálogo, convenciones y políticas de ciclo de vida para no perder trazabilidad.

El enfoque lakehouse combina almacenamiento de tipo lake con capacidades de gestión de tablas, como transacciones y evolución de esquemas, según la implementación. Guardar Parquet en una carpeta no proporciona por sí mismo todas esas propiedades. En este curso la carpeta local representa una organización por capas; no se presentará como una implementación completa de lakehouse.

Se usarán tres estados: datos originales inmutables, datos depurados y productos analíticos. Es posible nombrarlos bronze, silver y gold, pero el nombre no sustituye las reglas. Debe documentarse qué controles permiten promover datos de un estado a otro y cómo se reconstruye una salida.

## Hadoop HDFS y modelos NoSQL

Hadoop permite discutir el almacenamiento y procesamiento distribuido que antecede a muchas arquitecturas actuales. HDFS reparte archivos en bloques y conserva réplicas entre nodos; un servicio de metadatos coordina su ubicación. Este papel se estudia conceptualmente. No se instalará un clúster Hadoop para ejecutar los laboratorios locales.

Los modelos NoSQL abarcan familias distintas. Clave valor favorece acceso directo por una clave; documentos agrupa atributos que suelen consultarse juntos; columnas amplias organiza acceso distribuido según un diseño de claves; grafos representa relaciones y recorridos. Elegir una familia exige conocer patrones de consulta y consistencia, no únicamente la forma del archivo de entrada.

La consistencia fuerte, cuando un sistema la ofrece para una operación, permite razonar sobre observaciones coordinadas de los datos. La consistencia eventual admite divergencias temporales que pueden resolverse con el tiempo bajo ciertas condiciones. Ante una partición de red, garantizar a la vez todas las respuestas y una vista estrictamente consistente puede ser incompatible. La discusión debe precisar qué operación y qué garantía se están considerando; “NoSQL no tiene consistencia” es una generalización incorrecta.
''')
table(guide,['Necesidad','Alternativa a estudiar','Pregunta antes de elegir'],[
('Indicadores periódicos consistentes','Warehouse o modelo analítico relacional','¿Se han definido dimensiones y métricas comunes?'),('Conservar datos heterogéneos','Lake con catálogo y controles','¿Cómo se descubrirán y gobernarán los archivos?'),('Tablas analíticas sobre almacenamiento abierto','Lakehouse con formato de tabla apropiado','¿Qué transacciones y evolución necesita el caso?'),('Búsqueda por identificador','Relacional o clave valor según garantías','¿Qué consultas y transacciones deben soportarse?'),('Recorridos entre entidades','Modelo de grafos','¿Las relaciones son el centro de las preguntas?')],[4.7,5.9,6.2])
text(guide,'''## Formatos y lectura selectiva

CSV representa filas mediante texto delimitado y suele requerir inferir o declarar tipos. Es sencillo de inspeccionar, pero valores vacíos, separadores, codificación y fechas pueden ser ambiguos. JSON permite estructuras anidadas; su flexibilidad exige acordar cómo interpretar campos ausentes y cambios de estructura.

Parquet organiza el almacenamiento por columnas y admite compresión y codificaciones eficientes [R7]. En una consulta que usa pocas columnas, esa organización puede reducir lectura frente a un formato por filas. No garantiza mayor velocidad en toda carga: influyen tamaño, selectividad, compresión, metadatos y motor utilizado.

Particionar archivos por fecha puede permitir omitir directorios cuando se filtra un período. Particionar por id de pedido produciría demasiados archivos pequeños en este caso. Cada archivo añade costos de apertura y metadatos. La clave de partición debe responder a consultas frecuentes y a una granularidad razonable.

## ETL ELT y contratos

En ETL se extrae, transforma y después carga al destino elegido; en ELT se carga y luego se transforma dentro del sistema de destino. La distinción depende de cuál sea ese destino, no de una superioridad universal. En ambos casos se necesitan validación, observabilidad y una política para los registros que no cumplan las reglas.

Un contrato de datos define campos, tipos, significado, claves y condiciones de disponibilidad. También establece qué cambios son compatibles. Agregar una columna opcional puede ser tolerable; cambiar units de unidades a cajas sin aviso rompe el significado aunque el tipo siga siendo entero.

Las dimensiones de calidad deben vincularse al uso. Completitud mide presencia de valores requeridos; validez, cumplimiento de dominios; unicidad, ausencia de identidades repetidas; consistencia, compatibilidad entre campos o fuentes; oportunidad, disponibilidad a tiempo. Una puntuación global puede ocultar una falla grave en el campo que decide el análisis.

## Reglas de la práctica y conciliación

Se eliminan únicamente duplicados exactos. Después se asigna un motivo principal de rechazo con prioridad: ciudad ausente, cantidad inválida y precio inválido. La prioridad hace excluyentes los motivos reportados, pero no significa que una fila solo tenga un defecto. Los demás campos se generan válidos; una fuente real exigiría controles adicionales de tipos, dominios, fechas y rangos.

Un mismo id con valores distintos requiere una regla de negocio para resolver versiones o conflictos. No se elimina arbitrariamente con drop_duplicates sobre id. La práctica verifica unicidad al final para detectar ese caso si el estudiante modifica el generador.

La ecuación de conciliación es: filas originales = filas limpias + filas rechazadas después de deduplicar + duplicados exactos eliminados. El importe se calcula después de validar cantidad y precio. Los registros rechazados se conservan para explicar la diferencia entre la entrada y la salida.

## Laboratorio 2 Pipeline de calidad con DuckDB

Objetivo: producir datos depurados, exportarlos a Parquet y demostrar conservación de registros. DuckDB se ejecuta dentro del proceso de Python y permite consultas SQL sobre archivos [R5]. Insumos: CSV y esperado.json del laboratorio 1. Ejecute el programa completo y revise cada aserción.
''')
labcode(guide,'02_calidad_duckdb.py')
code(guide,'''python 02_calidad_duckdb.py''')
text(guide,'''Salidas: limpio.parquet, limpio.csv, rechazados.csv y resumen_duckdb.csv. Las aserciones deben terminar sin error. Si fallan, revise primero que esperado.json corresponda al mismo conjunto de entrada. Después compruebe la definición de duplicado y la prioridad de las reglas.

El reporte de calidad debe incluir fecha de ejecución, número de filas originales, duplicados, rechazados y válidos, porcentaje válido sobre pedidos únicos y suma de importes. No se acepta reportar un porcentaje sin denominador. También se adjuntará una muestra de errores y una explicación de su tratamiento.

## Ejercicios SQL y solución orientadora

Ejercicio A: calcular pedidos e importe por ciudad y categoría. Ejercicio B: identificar las ciudades con más de cien pedidos válidos. Ejercicio C: comparar el total antes y después de eliminar duplicados, explicando por qué los importes inválidos no son una línea base confiable.
''')
code(guide,'''-- Ejecutar con la conexión con del programa 02
SELECT city, category, count(*) AS pedidos,
       sum(amount_cents) AS importe_centavos
FROM clean
GROUP BY city, category
ORDER BY city, category;

SELECT city, count(*) AS pedidos
FROM clean
GROUP BY city
HAVING count(*) > 100
ORDER BY pedidos DESC;''')
text(guide,'''La respuesta C debe separar efecto de duplicados y efecto de valores inválidos. Comparar únicamente la suma de raw con la de clean mezcla ambos fenómenos. Una comparación válida para medir duplicados mantiene constantes las reglas de validez y cambia solo la deduplicación.

Reto de ampliación: añadir un pedido con id existente e importe distinto. El control de unicidad debe fallar. El equipo propondrá una regla documentada para decidir si es una corrección, una nueva versión o un conflicto. La solución no debe esconder el problema seleccionando una fila al azar.

Trabajo autónomo de 1 h 45 min: 35 minutos para describir reglas y conciliación, 35 para consultas y 35 para una decisión de arquitectura. Cierre: ¿qué información se perdería si se borraran los rechazados? Se espera mencionar trazabilidad, explicación de sesgos y posibilidad de corregir la fuente.
''')
chapter(guide,'5 Procesamiento con Apache Spark')
text(guide,'''## Resultados y secuencia de la unidad

El estudiante implementará agregaciones, joins y ventanas, comprobará equivalencia con DuckDB y explicará dónde ocurre movimiento de datos. El viernes dedica 60 minutos al modelo de ejecución, 60 a demostración, 75 a transformaciones y 30 a lectura de planes. El sábado emplea 90 minutos en consultas, 135 en el laboratorio, 120 en joins y ventanas, 75 en revisión y 30 en cierre.

## Modelo de ejecución

El driver coordina la aplicación, construye planes y programa tareas. Los ejecutores realizan trabajo sobre particiones y pueden mantener datos en memoria. En un clúster están distribuidos entre procesos y máquinas; en modo local se usa la capacidad de un solo equipo. La opción local[2] limita la ejecución local a dos hilos de trabajo y deja recursos para otras aplicaciones.

Una transformación describe un nuevo conjunto de datos. Una acción solicita un resultado y desencadena ejecución. La evaluación diferida permite reunir operaciones antes de ejecutar. Spark puede reconstruir particiones a partir de su linaje en los casos soportados; persistir datos puede evitar repetir trabajo [R2].

Ejemplo: seleccionar columnas y filtrar una ciudad no necesariamente lee todos los datos en el momento de escribir esas instrucciones. Cuando se pide count o se escribe una salida, el motor construye y ejecuta un plan. Medir solo el tiempo de crear un DataFrame no mide el costo de obtener el resultado.

Una partición es una unidad de distribución de datos; una tarea opera sobre una partición en una etapa. No debe confundirse con una carpeta de particionamiento de archivos: ambas divisiones pueden relacionarse, pero no son equivalentes. Un trabajo puede tener varias etapas separadas por redistribución.

## Transformaciones estrechas y shuffle

Un filtro puede procesarse dentro de cada partición. En una agregación por ciudad, los registros de la misma ciudad pueden encontrarse en varias particiones; el sistema necesita combinar resultados. La redistribución de datos se denomina shuffle y puede implicar transferencia, ordenamiento, serialización y uso de disco.

Un join puede beneficiarse de enviar una dimensión pequeña a los ejecutores mediante broadcast. Esa estrategia exige que la dimensión quepa de forma razonable en memoria. No debe forzarse con una tabla grande solo porque acelera un ejemplo pequeño. Además, antes del join se debe verificar la unicidad de la clave en la dimensión.

Si una dimensión contiene dos filas para Tunja, cada pedido de Tunja puede multiplicarse al unirla. La aplicación podría terminar sin errores y producir importes incorrectos. Por eso el laboratorio compara conteos antes y después y revisa claves sin correspondencia.

## DataFrames SQL y ventanas

Un DataFrame representa datos con esquema y permite expresar filtros, proyecciones y agregaciones. SQL y la API de DataFrames pueden describir operaciones equivalentes. Se elegirá la forma más legible para el equipo, sin asumir que escribir más código implica mayor rendimiento.

Una agregación reduce grupos a resultados resumidos. Una ventana permite calcular posiciones o acumulados preservando filas. Para seleccionar tres pedidos por ciudad se ordena por importe descendente y por id ascendente como desempate. Sin un desempate explícito, pedidos con el mismo importe podrían aparecer en distinto orden entre ejecuciones.

collect transfiere filas al driver. En el laboratorio se usa únicamente sobre el resumen de cuatro ciudades, cuyo tamaño es acotado. Usarlo sobre millones de pedidos puede agotar la memoria del proceso coordinador. show es apropiado para inspecciones pequeñas y write para resultados voluminosos.

## Laboratorio 3 Agregaciones joins y ventanas

Objetivo: obtener exactamente los mismos pedidos e importes por ciudad que DuckDB, enriquecer con una región y seleccionar los tres pedidos de mayor importe por ciudad. Insumos: limpio.parquet y resumen_duckdb.csv. El programa debe ejecutarse después del laboratorio 2.
''')
labcode(guide,'03_spark_lotes.py')
code(guide,'''python 03_spark_lotes.py''')
text(guide,'''Resultados esperados: cuatro ciudades en el resumen; equivalencia exacta de conteos e importes; ninguna región nula; mismo número de filas antes y después del join; tres pedidos por ciudad en la selección. Se comparan enteros en centavos para que una diferencia de coma flotante no oculte problemas de lógica.

El plan impreso permitirá identificar lectura de Parquet, agregación y, cuando corresponda, nodos Exchange asociados a redistribución. El nombre y la forma exacta del plan pueden cambiar según versión y ejecución adaptativa. El estudiante deberá interpretar el plan observado, no memorizar una captura.

## Ejercicio de traducción a SQL

Registre df como vista temporal con df.createOrReplaceTempView('pedidos'). Antes de detener Spark, ejecute esta consulta y compare con el resultado del DataFrame. Observe que la vista no es una copia persistente del archivo.
''')
code(guide,'''df.createOrReplaceTempView('pedidos')
spark.sql("""
  SELECT city, COUNT(*) AS orders, SUM(amount_cents) AS total_cents
  FROM pedidos
  GROUP BY city
  ORDER BY city
""").show()''')
text(guide,'''Reto: agregar una consulta que calcule importe promedio por categoría y explicar por qué el promedio global no suele ser el promedio simple de los promedios de cada ciudad. La solución debe ponderar por el número de pedidos si utiliza resultados previamente agregados.

Ejemplo resuelto: una ciudad tiene dos pedidos de importe medio 100 y otra tiene ocho de importe medio 50. El promedio global es (2 × 100 + 8 × 50) dividido por 10, igual a 60. Promediar 100 y 50 produce 75 y asigna el mismo peso a grupos de tamaños diferentes.

Trabajo autónomo de 1 h 45 min: 35 minutos para completar la consulta, 35 para comentar el plan y 35 para justificar join y controles. Cierre: ¿por qué Spark puede ser más lento que DuckDB en esta muestra? La respuesta debe considerar arranque, coordinación, tamaño de carga y recursos locales, sin concluir que un motor siempre es superior.
''')
chapter(guide,'6 Rendimiento y procesamiento de eventos')
text(guide,'''## Resultados y secuencia de la unidad

El estudiante diseñará una comparación controlada, interpretará una medición y explicará el tratamiento de eventos tardíos. El viernes dedica 60 minutos a hipótesis y medición, 60 a planes, 75 al benchmark y 30 a discusión. El sábado distribuye 90 minutos en tiempos y ventanas, 135 en streaming, 120 en experimentación, 75 en análisis del incidente y 30 en cierre.

## Diseñar un experimento de rendimiento

Una comparación comienza con una pregunta concreta: cuánto cambia el tiempo de una agregación cuando la misma tabla limpia se almacena en CSV o Parquet. Se mantiene constante la consulta, el resultado lógico, el motor, la cantidad de hilos y el equipo. Si también se cambian motor, tamaño y filtros, no podrá atribuirse la diferencia al formato.

Se debe medir hasta consumir el resultado, separar el calentamiento y repetir. La primera ejecución puede incluir apertura de bibliotecas, compilación o llenado de cachés. El orden alternado reduce un sesgo sistemático, pero no elimina todos los efectos del sistema operativo. La mediana es menos sensible a una ejecución excepcional que la media, aunque conviene reportar también dispersión y mediciones individuales.

El tiempo de arranque y el de ejecución responden preguntas distintas. Para un proceso que se inicia una sola vez al día, el arranque importa en el costo total. Para un servicio de consultas persistente, interesa además el tiempo de las consultas posteriores. El informe debe declarar qué parte del proceso está incluida.

Si una lectura CSV tarda 1,20 segundos y Parquet tarda 0,30, la razón de aceleración es 4 y la reducción del tiempo es 75 %. No son 400 % de reducción. Estas cifras son un ejemplo aritmético; los tiempos reales de la práctica se obtendrán en cada equipo y pueden no mostrar la misma relación.

## Palancas de optimización

La optimización debe comenzar por leer menos datos y evitar trabajo innecesario. Seleccionar columnas y aplicar filtros útiles puede reducir transferencia y memoria. Las posibilidades dependen del formato, los metadatos y el plan elegido. El motor puede omitir grupos de datos cuando las estadísticas lo permiten, pero no debe asumirse que todo filtro elimina lectura física.

En Spark, caché, estrategia de join y cantidad de particiones influyen en el plan; la ejecución adaptativa puede modificar decisiones a partir de estadísticas durante la consulta [R3]. Una caché puede ayudar cuando un resultado se reutiliza, pero almacenarlo consume recursos. La primera acción después de cache puede incluir el costo de llenarla.

El sesgo ocurre cuando algunas claves concentran mucho más trabajo que otras. Una partición grande puede determinar el tiempo final mientras otras terminan rápido. Aumentar indiscriminadamente particiones no divide necesariamente una clave dominante. Se debe identificar la distribución de claves antes de elegir una técnica de mitigación.

En DuckDB, el diseño de la consulta y el aprovechamiento de procesamiento en paralelo deben evaluarse junto con memoria y almacenamiento [R6]. Reducir hilos puede ser razonable en un portátil compartido con videoconferencia. La configuración adecuada para el curso no se convierte automáticamente en una recomendación para producción.

## Laboratorio 4 Medición de formatos

Insumos: limpio.csv y limpio.parquet, producidos por el mismo laboratorio de calidad. Ejecute el programa 04. Compruebe que los resultados son iguales antes de interpretar los tiempos. El programa realiza una verificación previa que también calienta cachés; por tanto, todas las mediciones se describen como ejecuciones con cachés calientes.
''')
labcode(guide,'04_benchmark.py')
code(guide,'''python 04_benchmark.py''')
text(guide,'''Producto: tiempos.csv y una tabla del informe con formato, bytes, cinco tiempos medidos después de descartar la iteración cero, mediana y rango. El programa no vacía la caché del sistema operativo y no mide consumo máximo de memoria. Si se desea estudiar memoria, debe añadirse un instrumento explícito y describir qué proceso observa.

Ejercicio de interpretación: repita con 100 000 filas después de regenerar 01 y 02. Compare tendencias sin combinar mediciones de tamaños distintos en una misma mediana. Si no se obtiene mejora, documente el resultado y proponga una explicación que pueda ponerse a prueba. No se calificará una mayor aceleración, sino la validez del experimento.

## Streaming y microbatches

En un procesamiento por lotes se dispone de un conjunto acotado. En streaming la entrada puede continuar indefinidamente y el sistema mantiene resultados a medida que llegan eventos. Un microbatch procesa una porción finita de esa entrada de forma periódica. El objetivo de streaming no es necesariamente responder en microsegundos; la latencia aceptable depende de la decisión.

El tiempo de evento indica cuándo ocurrió el hecho según la fuente. El tiempo de procesamiento indica cuándo lo atendió el sistema. Una desconexión puede hacer que un pedido de las 10:02 llegue después de uno de las 10:30. Agrupar únicamente por hora de llegada modifica el significado del indicador.

Una ventana fija agrupa eventos en intervalos no superpuestos, por ejemplo cada cinco minutos. Una ventana deslizante puede superponerse y un mismo evento puede contribuir a varias ventanas. Una sesión se define por períodos de actividad separados por inactividad. La elección debe corresponder a la pregunta analítica.

Structured Streaming permite expresar estas operaciones sobre DataFrames. El watermark ayuda a limitar estado y a manejar eventos tardíos; el checkpoint conserva información de progreso y estado según la consulta [R4]. La corrección de extremo a extremo también depende de la fuente y el destino. Un checkpoint no convierte cualquier efecto externo en una escritura exactamente una vez.

## Watermark y política de tardanza

Para el ejemplo se usa una tolerancia de diez minutos y ventanas de cinco. Conceptualmente, el watermark avanza a partir del máximo tiempo de evento observado, descontando la tolerancia; su aplicación ocurre entre microbatches. No es un temporizador que avanza automáticamente con el reloj de pared cuando no llegan eventos.

Un evento tardío puede actualizar una ventana todavía mantenida. Cuando esa ventana queda fuera del estado retenido, el motor puede descartar eventos demasiado antiguos según la operación. La garantía debe explicarse con el progreso observado y la configuración: no se debe tratar el watermark como una promesa de aceptar indefinidamente todo dato atrasado.

La práctica usa salida de consola en modo update para observar cambios. Esa salida es didáctica y no constituye un destino durable de producción. Para una solución real habría que diseñar escrituras idempotentes o transaccionales y comprobar recuperación del conjunto fuente, estado y destino.

## Laboratorio 5 Eventos y ventanas

El programa crea una carpeta distinta por ejecución. Los archivos se escriben primero en staging y se mueven completos a entrada para evitar que Spark lea un archivo a medio escribir. Después de cada publicación se procesan los datos disponibles y se imprime el progreso.
''')
labcode(guide,'05_streaming.py')
code(guide,'''python 05_streaming.py''')
table(guide,['Lote','Eventos publicados','Observación a verificar'],[
('1','10:01 por 1 000 y 10:03 por 2 000','Ventana 10:00 a 10:05 con 2 pedidos y 3 000 centavos.'),('2','10:02 por 1 500','Actualización de esa ventana a 3 pedidos y 4 500 centavos.'),('3','10:30 por 500','Nueva ventana y avance del máximo tiempo observado.'),('4','10:31 por 500','Actualización de la ventana 10:30 y aplicación del avance del watermark.'),('5','10:01 por 9 000','Evento muy antiguo respecto del watermark; revisar descarte y ausencia de actualización de la ventana cerrada.')],[1.4,5.6,9.8])
text(guide,'''El docente debe revisar eventTime y stateOperators en el progreso disponible, particularmente watermark y numRowsDroppedByWatermark cuando se reporten. El último progreso puede corresponder a un microbatch sin entradas; conviene conservar las salidas de todos los lotes. Si hay diferencias, se debe identificar primero la versión, el modo de salida y el momento en que avanzó el watermark.

El progreso puede mostrar marcas de tiempo en UTC con sufijo Z, aunque la tabla se muestre en America/Bogota. En este caso, 15:21 UTC corresponde a 10:21 en la hora local utilizada. Debe compararse el mismo instante y no interpretar la diferencia de representación como un retraso del sistema.

Actividad de recuperación: explicar qué ocurriría si se reiniciara con el mismo checkpoint y qué se pierde al crear otro. El programa usa un identificador nuevo para facilitar repeticiones independientes; por esa razón no demuestra recuperación de una consulta productiva. Un reinicio real exige conservar rutas, consulta compatible y destino recuperable.

Incidente para discutir: un dispositivo tiene su reloj adelantado dos días y envía un evento. ¿Qué riesgo aparece para los datos que llegan con la hora correcta? Respuesta orientadora: el máximo tiempo observado puede avanzar excesivamente y afectar la política de tardanza; se necesitan validaciones de reloj y reglas de cuarentena antes del cómputo temporal.

Trabajo autónomo de 1 h 45 min: 45 minutos para el informe experimental, 40 para la traza de streaming y 20 para proponer manejo del incidente. El informe debe distinguir hechos observados, hipótesis y experimentos que faltan.
''')
chapter(guide,'7 Analítica aplicada y gobernanza')
text(guide,'''## Resultados y secuencia de la unidad

El estudiante integrará un modelo sencillo, evaluará su utilidad frente a una línea base y documentará gobernanza. El viernes dedica 60 minutos a objetivo y variables, 60 a demostración, 75 a evaluación y gobernanza y 30 a preparación de defensa. El sábado reserva 90 minutos a integración, 135 a revisión de reproducibilidad y los bloques de tarde a resultados, sustentaciones y cierre. El trabajo autónomo de esta unidad debe realizarse antes de ese sábado.

## Del indicador al modelo

Un indicador describe un resultado observado; un modelo predictivo estima un resultado aún desconocido en el instante de uso. Para el caso se define late como entrega superior a 60 minutos. La elección de 60 es una convención didáctica y debería justificarse operacionalmente en una aplicación real.

Las variables candidatas son ciudad, categoría, unidades, precio y hora de creación. delivery_minutes define el objetivo y no puede ser predictor si se pretende decidir al crear el pedido. id se excluye porque representa una identificación y su secuencia podría codificar información temporal accidental. Cada variable debe pasar una revisión de disponibilidad y significado antes del entrenamiento.

La fuga de información ocurre cuando el entrenamiento o la evaluación utiliza datos que no estarían disponibles al predecir. Separar entrenamiento y prueba antes de ajustar transformaciones y encapsular el procesamiento en un pipeline ayuda a evitar ese problema [R8]. Un resultado muy alto puede ser una señal de fuga, no necesariamente de calidad.

## Separación temporal y línea base

Se ordenan los pedidos por tiempo y se usa aproximadamente el primer 80 % temporal para entrenamiento y el período posterior para prueba. La frontera se define con un tiempo de corte, manteniendo del mismo lado todos los pedidos con ese instante. Esta estrategia aproxima una evaluación hacia el futuro y evita mezclar libremente pasado y futuro.

La línea base predice la clase más frecuente del entrenamiento. Si las entregas tardías son minoritarias, puede alcanzar una exactitud elevada sin detectar ninguna. Por eso se reportan precisión, recall, F1 y matriz de confusión. El modelo introductorio usa regresión logística y el umbral predeterminado; cualquier ajuste de umbral debe realizarse con una partición de validación, no con la prueba final.

La estandarización y la codificación de categorías se ajustan con entrenamiento y se aplican a prueba. Las categorías nuevas se manejan sin producir una falla del codificador. En una aplicación operacional, la presencia de categorías desconocidas también debería generar observabilidad y revisión de calidad.

## Métricas con un ejemplo resuelto

Considere 100 pedidos: 20 son realmente tardíos. El modelo identifica 15 de esos 20 y marca además 10 pedidos puntuales como tardíos. Hay 15 verdaderos positivos, 10 falsos positivos, 5 falsos negativos y 70 verdaderos negativos. La precisión es 15/25 = 0,60; el recall es 15/20 = 0,75; F1 es 2 × 0,60 × 0,75 dividido por 1,35, aproximadamente 0,667. La exactitud es 85/100 = 0,85.

La métrica pertinente depende del costo de cada error. Si una alerta activa una llamada costosa, importan los falsos positivos. Si una omisión causa incumplimiento grave, importa detectar tardíos. El costo, la capacidad de intervención y las consecuencias de la decisión deben acompañar la métrica técnica.

## Laboratorio 6 Modelo introductorio

Ejecute con el conjunto inicial de 20 000 registros para mantener acotada la memoria. Esta fase utiliza pandas y scikit-learn; su propósito es enseñar evaluación y su conexión con el pipeline. No es una demostración de entrenamiento distribuido. La ingeniería previa prepara una tabla que puede consumirse por distintos motores analíticos.
''')
labcode(guide,'06_modelo.py')
code(guide,'''python 06_modelo.py''')
text(guide,'''La salida metricas.json contiene la línea base, el modelo y el tamaño de las particiones. La matriz usa etiquetas [0, 1]: la primera fila contiene verdaderos negativos y falsos positivos; la segunda, falsos negativos y verdaderos positivos. No se prescribe una puntuación fija como requisito de aprobación. Se verifica que la evaluación esté bien construida y que la interpretación respete sus límites.

En la ejecución de referencia con 20 000 pedidos antes de errores, quedaron 15 595 filas de entrenamiento y 3 899 de prueba; 583 casos de prueba fueron tardíos. La línea base no detectó ninguno. El modelo identificó 86 tardíos y produjo 84 falsas alertas: precisión aproximada de 0,506, recall de 0,148 y F1 de 0,228. Estos resultados ilustran una detección insuficiente al umbral predeterminado. Deben discutirse el costo de omitir casos, nuevas variables y una validación separada para ajustar el umbral, sin optimizar sobre la prueba final.

Los datos se generaron con una relación artificial entre ciudad, unidades y duración. Aprender esa relación es un ejercicio controlado; no demuestra utilidad predictiva en una empresa ni permite hacer afirmaciones sobre ciudades reales. El informe debe proponer qué datos y validaciones serían necesarios antes de un uso operacional.

## Visualización y comunicación

Una visualización debe responder una pregunta definida y declarar unidades y denominadores. Para comparar importe por ciudad puede usarse un gráfico de barras. Para el experimento conviene mostrar tiempos individuales además de la mediana. No se debe transformar una diferencia pequeña y variable en una afirmación categórica mediante ejes engañosos.
''')
code(guide,'''import pandas as pd
import matplotlib.pyplot as plt
summary = pd.read_csv('datos/resumen_duckdb.csv')
summary = summary.sort_values('total_cents')
fig, ax = plt.subplots(figsize=(7, 4))
ax.barh(summary['city'], summary['total_cents'] / 100)
ax.set_xlabel('Importe en unidades monetarias didacticas')
ax.set_title('Importe por ciudad en datos sinteticos')
fig.tight_layout()
fig.savefig('datos/importe_por_ciudad.png', dpi=150)
plt.close(fig)''')
text(guide,'''## Gobernanza y arquitectura de producción

La gobernanza asigna responsabilidades y reglas sobre los datos. El propietario del dato define usos y significado; quien lo custodia implementa controles; el equipo analítico documenta transformaciones y limitaciones. En organizaciones pequeñas una persona puede asumir varios papeles, pero las responsabilidades deben seguir siendo explícitas.

El linaje registra de qué entradas y transformaciones proviene un resultado. El proyecto debe permitir rastrear una cifra agregada hasta su archivo de entrada, versión del código y reglas. Un diccionario sin historial de transformaciones no constituye por sí solo linaje completo.

El diseño de privacidad empieza por minimizar los campos necesarios y restringir accesos por función. Reemplazar un nombre por un identificador no garantiza anonimato: otros atributos pueden permitir reidentificación. Las reglas de retención y borrado deben considerar copias, respaldos y productos derivados. En este curso se usan datos sintéticos; cualquier sustitución por datos reales debe revisar las obligaciones de la organización y la jurisdicción aplicable.

Para producción se propondrán captura, almacenamiento, procesamiento, consumo y monitoreo, indicando qué cambia respecto del portátil. El monitoreo debe incluir registros procesados, errores, frescura y latencia. Un plan de recuperación debe especificar qué se reejecuta, desde dónde y cómo se evitan efectos duplicados. Los costos se estimarán por almacenamiento, cómputo, transferencia y operación, sin inventar tarifas de nube.

Trabajo autónomo de 1 h 45 min: 35 minutos para resultados y métricas, 35 para la ficha de gobernanza y 35 para preparar el informe y la defensa. La presentación deberá reconocer al menos una limitación de calidad, una de rendimiento y una de generalización del análisis.
''')
chapter(guide,'8 Proyecto integrador y evaluación')
text(guide,'''## Consigna para el estudiante

Construya una solución reproducible para describir pedidos e importes por ciudad y evaluar una alerta de entrega tardía. Utilice el caso sintético o una fuente equivalente acordada con el docente. Integre ingesta, controles de calidad, almacenamiento Parquet, consultas con Spark, una medición de rendimiento y una demostración de procesamiento de eventos. Presente los resultados, sus limitaciones y una arquitectura razonada para producción.

El trabajo puede realizarse en equipos de dos o tres personas, con contribuciones declaradas y sustentación individual. No se exige un servicio desplegado en nube. El alcance debe permitir ejecutar el flujo en un portátil y explicar cada decisión en el tiempo disponible.

## Contenido del informe de 8 a 12 páginas

- Problema, decisión que se apoya y criterios de éxito.
- Fuente, unidad de análisis, diccionario y limitaciones de los datos.
- Arquitectura local y flujo de transformación con entradas y salidas.
- Reglas de calidad y conciliación de registros e importes.
- Consultas, joins y explicación de un plan de Spark.
- Diseño experimental, configuración, resultados y límites de rendimiento.
- Traza de eventos, ventanas, watermark y manejo de fallos.
- Modelo, línea base, métricas, disponibilidad de variables y límites.
- Gobernanza, propuesta de producción y costos por componentes.
- Instrucciones de reproducción y referencias.

El código y los archivos de resultados se entregan como anexos digitales y no cuentan dentro de esas páginas. El informe debe permitir seguir el argumento sin leer todo el código. Cada tabla y figura debe tener título, unidades y explicación de lo que permite concluir.

## Plantilla de ficha del problema

Complete en una página: título del caso; decisión a apoyar; usuario del resultado; unidad de análisis; período; pregunta descriptiva; pregunta predictiva; instante de decisión; fuentes; variables disponibles; restricción principal; criterio de éxito; riesgo de interpretación. Un criterio como “usar Spark” no es un resultado de negocio ni una medida de calidad.

## Plantilla de reporte experimental

Registre hipótesis, variable modificada, variables controladas, equipo, versiones, tamaño de entrada, formato, consulta exacta, procedimiento de calentamiento, número de repeticiones y forma de consumir el resultado. Incluya mediciones individuales, mediana y dispersión, verificación de equivalencia, conclusión limitada a la evidencia y siguiente experimento propuesto.

## Plantilla de gobernanza

Identifique responsable funcional, custodio técnico, clasificación de los datos, usos permitidos, roles de acceso, retención, tratamiento de errores, linaje, frecuencia de actualización, política de reejecución y procedimiento ante un incidente. En el caso sintético se documenta cómo cambiarían esos controles al incorporar información personal real.
''')
h(guide,'Criterios comunes de desempeño',2)
table(guide,['Nivel','Descriptor'],[
('4 Sobresaliente','Resultado correcto y reproducible, decisiones justificadas con evidencia y límites explícitos.'),('3 Logrado','Resultado correcto y reproducible con omisiones menores que no cambian la conclusión.'),('2 En desarrollo','Solución parcial, evidencia insuficiente o pasos manuales no documentados que dificultan reproducir.'),('1 Insuficiente','Errores que invalidan resultados, ausencia de justificación o imposibilidad de explicar la solución.'),('0 Sin evidencia','No se entrega o no existe evidencia evaluable del criterio.')],[3.5,13.3])
h(guide,'Rúbrica del proyecto integrador',2)
table(guide,['Criterio','Peso interno','Evidencia para nivel 4'],[
('Formulación y arquitectura','15 %','Pregunta verificable y elección de componentes ligada a restricciones.'),('Calidad y conciliación','20 %','Reglas explícitas, rechazados conservados y controles de filas e importes.'),('Procesamiento y corrección','20 %','Consultas correctas, join validado y equivalencia entre motores.'),('Evaluación analítica','15 %','Línea base, separación temporal, ausencia de fuga e interpretación de métricas.'),('Reproducibilidad y gobernanza','20 %','Ejecución desde cero, versiones, linaje, responsabilidades y recuperación.'),('Comunicación técnica','10 %','Argumento claro con evidencia, unidades y limitaciones.'),('Total','100 %','Este componente aporta 35 % de la nota del curso.')],[5.0,2.3,9.5])
p(guide,'Cálculo sugerido: para cada criterio se multiplica su peso por el nivel obtenido dividido por 4. La suma produce una puntuación de 0 a 100 para el proyecto; luego se multiplica por 0,35 para su contribución al curso. La escala final se convierte según la normativa institucional.')
h(guide,'Rúbricas de los otros componentes',2)
table(guide,['Componente','Distribución interna','Condición de logro'],[
('Laboratorios 30 % del curso','Corrección 50 %, controles 25 %, explicación 25 %.','Los tres laboratorios evaluados aportan 10 % cada uno; se comprueban ejecución y respuesta individual.'),
('Informe experimental 20 %','Diseño 30 %, medición 25 %, interpretación 25 %, eventos 20 %.','Se controla una variable, se consumen resultados, se reportan repeticiones y se interpreta la tardanza.'),
('Sustentación 15 %','Comprensión 40 %, defensa con evidencia 40 %, claridad 20 %.','Cada integrante explica una decisión, interpreta un resultado y responde una pregunta de modificación.')],[4.5,5.3,7.0])
text(guide,'''La misma escala de 0 a 4 se aplica a los subcriterios anteriores. Un resultado correcto sin explicación no obtiene el máximo de comprensión; una explicación convincente no compensa un total numérico incorrecto. La retroalimentación deberá indicar qué evidencia permitiría mejorar el nivel.

## Revisión de reproducibilidad

- Iniciar en una carpeta nueva con las versiones declaradas.
- Ejecutar 01 y 02; verificar controles y existencia de salidas.
- Ejecutar 03; comprobar equivalencia y reglas del join.
- Ejecutar 04; conservar datos de tiempo sin imponer una aceleración mínima.
- Ejecutar 05; conservar la traza y explicar las ventanas.
- Ejecutar 06 con el conjunto pequeño; comprobar corte temporal y métricas.
- Revisar que el informe utilice resultados del mismo conjunto de datos.

## Resultados de control del conjunto inicial
''')
table(guide,['Control con n igual a 20000','Valor esperado'],[
('Filas originales','20 100'),('Pedidos únicos antes de calidad','20 000'),('Duplicados exactos eliminados','100'),('Rechazados después de deduplicar','506'),('Pedidos válidos','19 494'),('Importe total válido en centavos','600 736 176')],[11.5,5.3])
table(guide,['Ciudad','Pedidos válidos','Importe en centavos'],[
('Bogota','4 860','151 535 646'),('Cali','4 859','146 420 815'),('Medellin','5 004','153 728 081'),('Tunja','4 771','149 051 634')],[5.5,5.0,6.3])
p(guide,'Estas cantidades corresponden al generador incluido, semilla 64 y n igual a 20 000. Al cambiar tamaño o lógica se utiliza el archivo esperado.json recién generado. Los tiempos y las métricas predictivas no son constantes de control universales.')
chapter(guide,'9 Banco de preguntas y solucionario docente')
p(guide,'Las preguntas 1 a 5 pueden usarse en el diagnóstico; las demás, en cierres y sustentaciones. Las respuestas son orientadoras. Se valora que el estudiante explique el mecanismo y sus condiciones, no que repita una frase exacta. Para diagnóstico, utilice 20 minutos de respuesta y 15 de discusión dentro de la primera sesión.')
questions=[
('1 Qué diferencia hay entre una fila y una entidad','Una fila es un registro físico o lógico de una tabla. Una entidad es el objeto del dominio. Un pedido duplicado puede ocupar dos filas y seguir representando una sola entidad. La clave y las reglas de identidad conectan ambos conceptos.'),
('2 Qué hace GROUP BY','Agrupa filas por valores de una o varias columnas para calcular agregados. Si se agrupa por ciudad y categoría, cada combinación observada forma un grupo.'),
('3 Cuándo conviene usar una mediana','Cuando interesa una medida central menos sensible a valores extremos, como tiempos de ejecución con ejecuciones excepcionalmente lentas. Debe acompañarse de dispersión y tamaño de muestra.'),
('4 Por qué un join puede aumentar filas','Una fila de la izquierda puede coincidir con varias de la derecha. Debe comprobarse la cardinalidad esperada y la unicidad de la dimensión antes de atribuir el aumento a datos nuevos.'),
('5 Para qué se separan entrenamiento y prueba','Para evaluar con datos no utilizados al ajustar el modelo y sus transformaciones. La separación debe reflejar el uso previsto, por ejemplo predecir períodos futuros.'),
('6 Un millón de filas siempre exige Spark','No. La necesidad depende de tamaño, ancho de filas, operaciones, memoria, latencia y concurrencia. Se debe medir una solución simple antes de añadir distribución.'),
('7 Cuánto produce una fuente de 1000 eventos por segundo y 500 bytes por evento','43,2 GB decimales diarios sin compresión. La respuesta debe mostrar 1000 × 500 × 86400 bytes y separar ese volumen de réplicas, índices y retención.'),
('8 Qué limitación tiene agregar procesadores','La fracción secuencial, el movimiento de datos y la coordinación limitan la aceleración. Con 80 % paralelizable y cuatro procesadores, el límite ideal del ejemplo es 2,5.'),
('9 Por qué no sumar todos los errores para contar rechazados','Una fila puede incumplir varias reglas. Se necesita la unión de filas inválidas o una clasificación excluyente, y debe declararse el denominador.'),
('10 Qué ocurre con dos filas de igual id y distinto importe','Existe un conflicto de identidad o versión. No se debe escoger una al azar. Se requiere una regla de negocio o cuarentena y evidencia del tratamiento.'),
('11 Parquet garantiza una consulta más rápida','No. Puede reducir lectura y aprovechar compresión, pero el resultado depende de consulta, tamaño, selectividad y motor. Se comprueba mediante un experimento controlado.'),
('12 Cuál es la diferencia entre transformación y acción','La transformación describe cómo obtener otro conjunto; la acción solicita un resultado o salida y desencadena ejecución. Por eso el cronómetro debe incluir una acción real.'),
('13 Cuándo es aceptable collect','Cuando el resultado que llega al driver está acotado y cabe con margen en memoria, como cuatro filas agregadas. No se usa indiscriminadamente sobre la tabla completa.'),
('14 Por qué una tarea puede tardar mucho más que las demás','Puede haber sesgo de claves o particiones, datos más costosos, recursos lentos o reintentos. Deben observarse métricas antes de elegir una explicación.'),
('15 Una consulta de 2 segundos pasa a 0 coma 5 segundos cuál es la mejora','La razón de aceleración es 4 y la reducción del tiempo es 75 %. Se debe aclarar si se comparan medianas equivalentes y qué componentes del tiempo se incluyeron.'),
('16 El watermark avanza si no llegan eventos','No avanza simplemente porque pase el tiempo de pared. Su progreso depende del tiempo de evento observado y de la ejecución de la consulta.'),
('17 Un checkpoint garantiza exactamente una vez en cualquier destino','No. La garantía depende también de fuente, operación, reintentos y semántica de escritura del destino. Un correo o una llamada a una API externa podría repetirse.'),
('18 Por qué delivery_minutes no debe ser predictor','Se conoce después de terminar la entrega y además define late. Usarlo al predecir en la creación del pedido constituye fuga de información.'),
('19 Qué significa recall igual a 0 coma 75','Que se identificó el 75 % de los positivos reales del conjunto evaluado. No significa que el 75 % de las alertas sea correcto; eso corresponde a precisión.'),
('20 Un modelo con buenos resultados sintéticos está listo para producción','No. Debe validarse representatividad, disponibilidad de variables, cambio temporal, costos de error y desempeño con datos del contexto real.'),
('21 Qué garantiza un identificador seudónimo','Permite sustituir una identificación directa, pero no garantiza anonimato. Otros atributos o cruces pueden permitir reidentificación y requieren controles.'),
('22 Qué evidencia pediría antes de migrar a un clúster','Volumen y crecimiento, latencia requerida, saturación medida, concurrencia, disponibilidad, costo operativo y un experimento representativo. Se comparan beneficios y complejidad añadida.')]
for question,answer in questions:
    h(guide,question,2);p(guide,answer)
text(guide,'''## Caso de defensa con cambio de requisito

La organización ahora recibe diez veces más pedidos y necesita un indicador cada dos minutos. Solicite al equipo que explique qué mediría, qué componente podría saturarse y cómo evaluaría un cambio. Una defensa sólida distingue aumento de volumen, frecuencia de actualización y latencia, propone observabilidad y evita rediseñar todo sin evidencia.

## Caso de control de calidad

Se observa que una ciudad concentra el 40 % de los rechazos, pero representa solo el 10 % de los pedidos. Pregunte si la comparación de ventas entre ciudades puede estar sesgada. La respuesta debe reconocer selección diferencial, revisar causas y mostrar tasas por ciudad antes de comparar importes. El total global conciliado no elimina ese riesgo.
''')
chapter(guide,'10 Guiones para preparar las presentaciones')
text(guide,'''Cada sesión se puede convertir en una presentación de ocho diapositivas centrales, complementada con demostración en vivo, instrucciones del taller y discusión. El código completo debe mantenerse en los archivos de práctica; las diapositivas mostrarán fragmentos breves y resultados legibles. Los guiones siguientes definen contenido, visual y pregunta, y remiten a las explicaciones de esta guía.

Una diapositiva debe comunicar una idea verificable. Las notas del presentador incorporarán la explicación de la sección correspondiente y la respuesta orientadora. Los tiempos del programa incluyen la práctica; no se debe llenar toda la jornada con exposición de diapositivas.
''')
decks=[
('Sesión 1 Problemas y fundamentos','Sección 3',[
'1 Objetivo del curso y pregunta del caso de pedidos.',
'2 Diagnóstico con un ejemplo de filas y entidades.',
'3 Volumen velocidad variedad y veracidad aplicados al caso.',
'4 Comparación de escalamiento vertical y horizontal.',
'5 Límite del paralelismo con el cálculo de aceleración 2,5.',
'6 Latencia y throughput con una cola de eventos.',
'7 Cálculo de 43,2 GB diarios y supuestos.',
'8 Consigna de ficha del problema y criterios de éxito.'
],'Diagrama de cola y esquema de componentes. Pregunta: ¿qué evidencia justificaría añadir máquinas?'),
('Sesión 2 Entorno y perfilado','Secciones 2 y 3',[
'1 Objetivo y archivos que se producirán.',
'2 Entorno local y verificación de versiones.',
'3 Diccionario de pedidos e instante de disponibilidad.',
'4 Errores deliberados y semilla del generador.',
'5 Diferencia entre filas pedidos únicos y válidos.',
'6 Demostración del programa 01 y perfilado.',
'7 Pregunta descriptiva y pregunta predictiva.',
'8 Evidencias de entrega y revisión entre pares.'
],'Captura de cinco filas y tabla de conteos. Pregunta: ¿por qué un archivo que abre correctamente puede ser inadecuado?'),
('Sesión 3 Arquitecturas y formatos','Sección 4',[
'1 Necesidades de consulta y almacenamiento del caso.',
'2 Warehouse lake y lakehouse con alcance explícito.',
'3 Rol de Hadoop y HDFS en un esquema distribuido.',
'4 Familias NoSQL y patrones de acceso.',
'5 Organización por filas y por columnas.',
'6 CSV JSON y Parquet con la misma información.',
'7 Particionamiento útil y problema de archivos pequeños.',
'8 Decisión de arquitectura con dos alternativas.'
],'Diagrama comparativo de almacenamiento. Pregunta: ¿por qué una carpeta Parquet no es por sí sola un lakehouse?'),
('Sesión 4 Calidad y pipeline','Sección 4',[
'1 Objetivo y ecuación de conciliación.',
'2 ETL ELT y estados de los datos.',
'3 Contrato de campos y reglas de validez.',
'4 Duplicado exacto frente a conflicto de id.',
'5 Cuarentena y prioridad de motivos.',
'6 Demostración del programa 02 y consultas.',
'7 Resultados de control y denominadores.',
'8 Reto de conflicto de versiones y cierre.'
],'Flujo entrada deduplicación validación salidas. Pregunta: ¿cómo se detecta que una fila incumple varias reglas?'),
('Sesión 5 Modelo de Spark','Sección 5',[
'1 Problema que se implementará en Spark.',
'2 Driver ejecutores y ejecución local.',
'3 Partición tarea etapa y trabajo.',
'4 Transformaciones y acciones.',
'5 Evaluación diferida con un ejemplo de filtro.',
'6 Shuffle en una agrupación por ciudad.',
'7 Lectura de un plan de ejecución.',
'8 Ejercicio de predicción antes de ejecutar count.'
],'Diagrama de particiones antes y después de agrupar. Pregunta: ¿qué está midiendo un cronómetro sin acción final?'),
('Sesión 6 Consultas joins y ventanas','Sección 5',[
'1 Equivalencia de consultas entre motores.',
'2 Agregaciones de conteos e importes.',
'3 Join con dimensión de ciudades.',
'4 Riesgo de multiplicar filas y controles.',
'5 Broadcast y condiciones de uso.',
'6 Ventana para tres pedidos por ciudad y desempate.',
'7 Demostración del programa 03 y comparación.',
'8 Promedio ponderado y entrega del laboratorio.'
],'Tabla pequeña de join y selección ordenada. Pregunta: ¿por qué el promedio de promedios puede ser incorrecto?'),
('Sesión 7 Rendimiento','Sección 6',[
'1 Hipótesis y variable que cambia.',
'2 Condiciones controladas y equivalencia de resultados.',
'3 Arranque calentamiento y cachés.',
'4 Repeticiones mediana y dispersión.',
'5 Aceleración frente a reducción porcentual.',
'6 Proyección filtros particiones y sesgo.',
'7 Demostración del programa 04.',
'8 Conclusión limitada al equipo y siguiente experimento.'
],'Gráfico de tiempos individuales por formato. Pregunta: ¿qué invalida comparar una consulta fría con otra caliente?'),
('Sesión 8 Eventos y tardanza','Sección 6',[
'1 Diferencia entre lote y flujo continuo.',
'2 Tiempo de evento y de procesamiento.',
'3 Ventanas fijas deslizantes y de sesión.',
'4 Estado y watermark con diez minutos de tolerancia.',
'5 Traza de los cinco lotes del laboratorio.',
'6 Demostración del programa 05 y progreso.',
'7 Checkpoint reintentos y destino de escritura.',
'8 Incidente del reloj adelantado y propuesta de control.'
],'Línea de tiempo con llegada desordenada. Pregunta: ¿cuándo deja de poder actualizarse una ventana antigua?'),
('Sesión 9 Analítica y gobernanza','Sección 7',[
'1 Objetivo de entrega tardía e instante de decisión.',
'2 Variables disponibles y fuga de información.',
'3 Corte temporal entrenamiento y prueba.',
'4 Línea base frente a regresión logística.',
'5 Matriz de confusión precisión recall y F1.',
'6 Demostración del programa 06.',
'7 Linaje privacidad acceso y retención.',
'8 Arquitectura de producción y preparación de defensa.'
],'Línea de tiempo de evaluación y matriz 2 por 2. Pregunta: ¿qué puede hacer sospechoso un modelo casi perfecto?'),
('Sesión 10 Integración y defensa','Secciones 7 y 8',[
'1 Criterios de éxito del proyecto.',
'2 Recorrido completo de entradas a resultados.',
'3 Conciliación y trazabilidad.',
'4 Evidencia de rendimiento y sus límites.',
'5 Evaluación analítica y decisiones posibles.',
'6 Revisión de reproducibilidad entre equipos.',
'7 Sustentación y cambio de requisito.',
'8 Retroalimentación y próximos experimentos.'
],'Diagrama de la solución con evidencias por etapa. Pregunta: ¿qué cambiaría si el flujo creciera diez veces?')]
for title,source,slides,note in decks:
    h(guide,title,2)
    p(guide,'Material base: '+source+'.')
    for slide in slides: guide.add_paragraph(slide,'List Bullet')
    p(guide,'Recurso visual y pregunta de discusión: '+note)
chapter(guide,'11 Glosario y referencias')
table(guide,['Término','Definición de trabajo'],[
('Batch','Procesamiento de una colección acotada de datos.'),('Checkpoint','Información persistida de progreso y estado para recuperación compatible.'),('DataFrame','Representación tabular con esquema y operaciones de transformación.'),('Driver','Proceso coordinador de una aplicación Spark.'),('ETL y ELT','Secuencias de extracción transformación y carga, según el orden respecto del destino.'),('Idempotencia','Propiedad de repetir una operación sin cambiar su efecto final respecto de una ejecución.'),('Latencia','Tiempo entre solicitud o evento y respuesta o resultado definido.'),('Linaje','Trazabilidad de entradas transformaciones y resultados.'),('Partición','Subdivisión utilizada para organizar almacenamiento o trabajo.'),('Pipeline','Secuencia explícita de pasos para producir un resultado.'),('Recall','Proporción de positivos reales identificados por el modelo.'),('Shuffle','Redistribución necesaria para ciertas operaciones entre particiones.'),('Skew','Distribución desigual de datos o carga de trabajo.'),('Throughput','Cantidad de trabajo completada por unidad de tiempo.'),('Watermark','Referencia de progreso temporal usada para gestionar tardanza y estado.')],[3.5,13.3])
h(guide,'Fuentes técnicas',2)
references(guide)
guide.save(ROOT/'02_Guia_academica_Big_Data_material_docente.docx')
print('Documentos creados en', ROOT)
