"""Microbatches por archivos. Cada ejecución conserva sus propios resultados."""
import json
import uuid
from pathlib import Path
from pyspark.sql import SparkSession, functions as F

spark = (SparkSession.builder.master('local[2]').appName('Eventos64')
 .config('spark.sql.shuffle.partitions', '2')
 .config('spark.sql.session.timeZone', 'America/Bogota').getOrCreate())
root = Path('datos') / ('stream_' + uuid.uuid4().hex[:8])
incoming, stage = root / 'entrada', root / 'staging'
incoming.mkdir(parents=True)
stage.mkdir()
schema = 'id LONG, event_time TIMESTAMP, city STRING, amount_cents LONG'
events = spark.readStream.schema(schema).json(str(incoming))
counts = (events.withWatermark('event_time', '10 minutes')
 .groupBy(F.window('event_time', '5 minutes'), 'city')
 .agg(F.count('*').alias('orders'), F.sum('amount_cents').alias('total_cents')))
query = (counts.writeStream.format('console').option('truncate', 'false')
 .outputMode('update').option('checkpointLocation', str(root / 'checkpoint')).start())

def publish(index, rows):
    temp = stage / f'batch_{index}.json'
    temp.write_text('\n'.join(json.dumps(r) for r in rows) + '\n', encoding='utf-8')
    temp.replace(incoming / temp.name)
    query.processAllAvailable()
    print('Progreso:', query.lastProgress)

def event(i, minute, amount):
    return dict(id=i, event_time=f'2026-01-01T10:{minute}:00',
                city='Tunja', amount_cents=amount)
try:
    publish(1, [event(1, '01', 1000), event(2, '03', 2000)])
    publish(2, [event(3, '02', 1500)])
    publish(3, [event(4, '30', 500)])
    publish(4, [event(5, '31', 500)])
    publish(5, [event(6, '01', 9000)])
    print('Progreso de la última ejecución:', query.lastProgress)
    print('Carpeta de la ejecución:', root)
finally:
    query.stop()
    spark.stop()
