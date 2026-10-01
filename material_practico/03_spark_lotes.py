"""Agregación, join, ventana y comparación exacta entre motores."""
import csv
import json
from pathlib import Path
from pyspark.sql import SparkSession, functions as F, Window

spark = (SparkSession.builder.master('local[2]').appName('Curso64')
 .config('spark.sql.shuffle.partitions', '4')
 .config('spark.sql.session.timeZone', 'America/Bogota').getOrCreate())
df = spark.read.parquet('datos/limpio.parquet')
expected = json.loads(Path('datos/esperado.json').read_text())
assert df.count() == expected['clean_rows']
summary = (df.groupBy('city').agg(F.count('*').alias('orders'),
 F.sum('amount_cents').alias('total_cents')).orderBy('city'))
actual = {r.city: (r.orders, r.total_cents) for r in summary.collect()}
with open('datos/resumen_duckdb.csv', encoding='utf-8') as f:
    reference = {r['city']: (int(r['orders']), int(r['total_cents']))
                 for r in csv.DictReader(f)}
assert actual == reference
dim = spark.createDataFrame([('Tunja', 'Centro'), ('Bogota', 'Centro'),
 ('Medellin', 'Noroccidente'), ('Cali', 'Suroccidente')], ['city', 'region'])
joined = df.join(F.broadcast(dim), 'city', 'left')
assert joined.count() == df.count()
assert joined.filter(F.col('region').isNull()).count() == 0
window = Window.partitionBy('city').orderBy(F.desc('amount_cents'), F.asc('id'))
top = (joined.withColumn('position', F.row_number().over(window))
 .filter(F.col('position') <= 3))
summary.show()
top.select('city', 'id', 'amount_cents', 'position').show()
summary.explain('formatted')
summary.write.mode('overwrite').parquet('datos/resumen_spark')
spark.stop()
