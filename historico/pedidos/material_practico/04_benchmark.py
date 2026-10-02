"""Comparación de formatos dentro de DuckDB; no compara clústeres."""
import csv
import statistics
import time
from pathlib import Path
import duckdb

con = duckdb.connect()
con.execute('SET threads=2')
con.execute("SET memory_limit='1GB'")
sources = {'csv': "read_csv_auto('datos/limpio.csv')",
           'parquet': "read_parquet('datos/limpio.parquet')"}
queries = {k: f"SELECT city, sum(amount_cents) FROM {v} GROUP BY city ORDER BY city"
           for k, v in sources.items()}
answers = {k: con.sql(q).fetchall() for k, q in queries.items()}
assert answers['csv'] == answers['parquet']
records = []
for iteration in range(6):
    order = ['csv', 'parquet'] if iteration % 2 == 0 else ['parquet', 'csv']
    for name in order:
        start = time.perf_counter()
        result = con.sql(queries[name]).fetchall()
        seconds = time.perf_counter() - start
        assert result == answers[name]
        records.append(dict(format=name, iteration=iteration, seconds=seconds))
with open('datos/tiempos.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['format', 'iteration', 'seconds'])
    writer.writeheader()
    writer.writerows(records)
for name in sources:
    values = [r['seconds'] for r in records if r['format'] == name and r['iteration'] > 0]
    print(name, 'mediana_s=', statistics.median(values),
          'bytes=', Path(f'datos/limpio.{name}').stat().st_size)
print('Son mediciones con cachés calientes; no se vació la caché del sistema.')
