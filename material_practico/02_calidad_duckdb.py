"""Tipado, deduplicación exacta, cuarentena y agregación."""
import json
from pathlib import Path
import duckdb

root = Path('datos')
con = duckdb.connect()
con.execute("SET threads=2")
con.execute("SET memory_limit='1GB'")
con.execute("""
CREATE TABLE raw AS SELECT * FROM read_csv('datos/pedidos.csv',
 header=true, columns={
 'id':'BIGINT', 'event_time':'TIMESTAMP', 'city':'VARCHAR',
 'category':'VARCHAR', 'units':'INTEGER', 'price_cents':'BIGINT',
 'delivery_minutes':'INTEGER'})
""")
con.execute("CREATE TABLE unique_rows AS SELECT DISTINCT * FROM raw")
con.execute("""
CREATE TABLE checked AS SELECT *, CASE
 WHEN city IS NULL OR trim(city) = '' THEN 'ciudad_ausente'
 WHEN units IS NULL OR units <= 0 THEN 'cantidad_invalida'
 WHEN price_cents IS NULL OR price_cents <= 0 THEN 'precio_invalido'
 ELSE 'OK' END AS quality_status
FROM unique_rows
""")
con.execute("""
CREATE TABLE clean AS SELECT id, event_time, city, category, units,
 price_cents, delivery_minutes, units * price_cents AS amount_cents
FROM checked WHERE quality_status = 'OK'
""")
assert con.sql('SELECT count(*)=count(DISTINCT id) FROM clean').fetchone()[0]
con.execute("COPY clean TO 'datos/limpio.parquet' (FORMAT PARQUET)")
con.execute("COPY clean TO 'datos/limpio.csv' (HEADER, DELIMITER ',')")
con.execute("""COPY (SELECT * FROM checked WHERE quality_status <> 'OK')
 TO 'datos/rechazados.csv' (HEADER, DELIMITER ',')""")
gold = con.sql("""SELECT city, count(*) AS orders,
 sum(amount_cents) AS total_cents FROM clean GROUP BY city ORDER BY city""")
con.execute("""COPY (SELECT city, count(*) AS orders,
 sum(amount_cents) AS total_cents FROM clean GROUP BY city ORDER BY city)
 TO 'datos/resumen_duckdb.csv' (HEADER, DELIMITER ',')""")
observed = dict(
 raw_rows=con.sql('SELECT count(*) FROM raw').fetchone()[0],
 clean_rows=con.sql('SELECT count(*) FROM clean').fetchone()[0],
 rejected=con.sql("SELECT count(*) FROM checked "
                  "WHERE quality_status <> 'OK'").fetchone()[0],
 total_cents=con.sql('SELECT sum(amount_cents) FROM clean').fetchone()[0])
expected = json.loads((root / 'esperado.json').read_text())
for key, value in observed.items():
    assert value == expected[key], (key, value, expected[key])
assert observed['raw_rows'] == (observed['clean_rows']
    + observed['rejected'] + expected['duplicates'])
print(gold.fetchall())
print('Controles aprobados:', observed)
