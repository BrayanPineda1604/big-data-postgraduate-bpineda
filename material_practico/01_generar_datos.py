"""Datos sintéticos educativos. Ejecutar desde la carpeta material_practico."""
import argparse
import csv
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--n', type=int, default=20000)
args = parser.parse_args()
if args.n < 1000:
    parser.error('Utilice al menos 1000 registros')
rng = random.Random(64)
root = Path('datos')
root.mkdir(exist_ok=True)
cities = ['Tunja', 'Bogota', 'Medellin', 'Cali']
categories = ['Hogar', 'Tecnologia', 'Alimentos']
fields = ['id', 'event_time', 'city', 'category', 'units',
          'price_cents', 'delivery_minutes']
valid_count = duplicates = 0
amount_total = 0
with (root / 'pedidos.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    for i in range(1, args.n + 1):
        city = rng.choice(cities)
        category = rng.choice(categories)
        units = rng.randint(1, 5)
        price = rng.randint(500, 20000)
        dt = datetime(2026, 1, 1) + timedelta(minutes=i)
        duration = max(5, round(25 + cities.index(city) * 7
                       + units * 3 + rng.gauss(0, 12)))
        row = dict(id=i, event_time=dt.isoformat(), city=city,
                   category=category, units=units, price_cents=price,
                   delivery_minutes=duration)
        if i % 97 == 0:
            row['city'] = ''
        if i % 113 == 0:
            row['units'] = 0
        if i % 157 == 0:
            row['price_cents'] = -10
        valid = bool(row['city']) and row['units'] > 0 and row['price_cents'] > 0
        if valid:
            valid_count += 1
            amount_total += row['units'] * row['price_cents']
        writer.writerow(row)
        if i % 199 == 0:
            writer.writerow(row)
            duplicates += 1
expected = dict(unique_input=args.n, raw_rows=args.n + duplicates,
                duplicates=duplicates, rejected=args.n-valid_count,
                clean_rows=valid_count, total_cents=amount_total)
(root / 'esperado.json').write_text(json.dumps(expected, indent=2))
print(json.dumps(expected, indent=2))
