"""Genera el fixture RAW del grupo 1 (contrato de 01_RAW_Ruben.md).

Ejecutar desde la raíz del repositorio:  python soluciones/plan_grupo_1/fixtures/generar_fixture_raw.py
Escribe soluciones/plan_grupo_1/fixtures/raw/. Los casos y resultados esperados están en fixtures/README.md.
"""
from datetime import date
from importlib.metadata import version
from pathlib import Path
import json
import platform

import numpy as np
import pandas as pd

DESTINO = Path(__file__).resolve().parent / 'raw'
DESTINO.mkdir(parents=True, exist_ok=True)
NA = np.nan

# --- EVA: 8 filas aceptadas (fila_fuente con saltos: las que faltan fueron rechazadas en RAW) ---
COLUMNAS_EVA = ['codigo_departamento', 'codigo_municipio', 'departamento', 'municipio', 'grupo_cultivo', 'cultivo',
                'anio', 'periodo', 'area_sembrada_ha', 'area_cosechada_ha', 'produccion_t',
                'rendimiento_publicado_t_ha', 'ciclo', 'estado_fisico', 'codigo_cultivo', 'fila_fuente']
eva = pd.DataFrame([
    ('15', '15001', 'Boyacá', 'Tunja', 'Tubérculos y plátanos', 'Papa', 2021, '2021A', 12.0, 10.0, 200.0, 20.0, 'Transitorio', 'En fresco', '1070100', 2),
    ('15', '15001', 'Boyacá', 'Tunja', 'Tubérculos y plátanos', 'Papa', 2021, '2021B', 30.0, 30.0, 900.0, 30.0, 'Transitorio', 'En fresco', '1070100', 3),
    ('15', '15001', 'Boyacá', 'Tunja', 'Leguminosas', 'Arveja', 2021, '2021A', 6.0, 5.0, 25.0, 5.0, 'Transitorio', 'En fresco', '1060200', 4),
    ('15', '15001', 'Boyacá', 'Tunja', 'Tubérculos y plátanos', 'Papa', 2022, '2022A', 5.0, 0.0, 0.0, NA, 'Transitorio', 'En fresco', '1070100', 5),
    ('54', '54001', 'Norte de Santander', 'Cúcuta', 'Cereales', 'Arroz', 2021, '2021A', 100.0, 100.0, 500.0, 5.0, 'Transitorio', 'Paddy o cascara verde', '1010100', 7),
    ('15', '15248', 'Boyacá', 'El Espino', 'Cereales', 'Maíz', 2022, '2022A', 8.0, 8.0, 16.0, 2.0, 'Transitorio', 'Grano seco', '1010300', 8),
    ('05', '05001', 'Antioquia', 'Medellín', 'Hortalizas', 'Apio', 2021, '2021A', 8.0, 8.0, 128.0, 16.0, 'Transitorio', 'En fresco', '1050600', 9),
    ('25', '25999', 'Cundinamarca', 'Inexistente', 'Tubérculos y plátanos', 'Papa', 2021, '2021A', 4.0, 4.0, 40.0, 10.0, 'Transitorio', 'En fresco', '1070100', 10),
], columns=COLUMNAS_EVA)

# --- DIVIPOLA: 4 municipios ---
COLUMNAS_DIVIPOLA = ['codigo_departamento', 'codigo_municipio', 'departamento', 'municipio', 'tipo',
                     'longitud', 'latitud', 'clave_territorial']
divipola = pd.DataFrame([
    ('15', '15001', 'BOYACÁ', 'TUNJA', 'Municipio', -73.355539, 5.53988, 'BOYACA|TUNJA'),
    ('15', '15248', 'BOYACÁ', 'EL ESPINO', 'Municipio', -72.497007, 6.483027, 'BOYACA|EL ESPINO'),
    ('54', '54001', 'NORTE DE SANTANDER', 'SAN JOSÉ DE CÚCUTA', 'Municipio', -72.508178, 7.905725, 'NORTE DE SANTANDER|SAN JOSE DE CUCUTA'),
    ('05', '05001', 'ANTIOQUIA', 'MEDELLÍN', 'Municipio', -75.581775, 6.246631, 'ANTIOQUIA|MEDELLIN'),
], columns=COLUMNAS_DIVIPOLA)

# --- AGROSAVIA: 7 muestras aceptadas ---
COLUMNAS_AGROSAVIA = ['id_muestra', 'fila_fuente', 'fecha', 'anio', 'departamento', 'municipio', 'clave_territorial',
                      'cultivo', 'ph', 'materia_organica', 'fosforo', 'aluminio', 'calcio', 'magnesio', 'potasio',
                      'cic', 'conductividad']
agrosavia = pd.DataFrame([
    ('101', 2, date(2021, 3, 4), 2021, 'BOYACÁ', 'TUNJA', 'BOYACA|TUNJA', 'Papa', 5.0, 4.0, 10.0, 0.5, 4.1, 1.2, 0.30, 8.1, 0.20),
    ('102', 3, date(2021, 6, 9), 2021, 'BOYACÁ', 'TUNJA', 'BOYACA|TUNJA', 'Papa', 6.0, 6.0, 30.0, 0.1, 6.3, 1.8, 0.45, 9.4, 0.31),
    ('103', 4, date(2022, 2, 1), 2022, 'BOYACÁ', 'TUNJA', 'BOYACA|TUNJA', 'Arveja', NA, 5.0, 20.0, NA, 5.0, 1.5, 0.40, 8.8, NA),
    ('104', 5, date(2021, 8, 15), 2021, 'NORTE DE SANTANDER', 'CÚCUTA', 'NORTE DE SANTANDER|CUCUTA', 'Arroz', 7.0, 2.0, 15.0, 0.0, 9.0, 3.0, 0.50, 14.0, 0.80),
    ('105', 6, date(2022, 5, 20), 2022, 'BOYACÁ', 'ESPINO', 'BOYACA|ESPINO', 'Maíz', 4.5, 3.0, 8.0, 1.4, 2.2, 0.7, 0.20, 6.0, 0.10),
    ('106', 7, date(2021, 1, 10), 2021, 'CAUCA', 'BORRAR', 'CAUCA|BORRAR', 'No Indica', 5.5, 7.0, 12.0, 0.8, 3.0, 1.0, 0.25, 7.5, 0.15),
    ('107', 9, date(2019, 11, 30), 2019, 'BOYACÁ', 'TUNJA', 'BOYACA|TUNJA', 'Papa', 5.2, 4.5, 18.0, 0.3, 4.8, 1.3, 0.35, 8.5, 0.22),
], columns=COLUMNAS_AGROSAVIA)

# --- Rechazados de ejemplo (explican los saltos de fila_fuente) ---
rechazados = pd.DataFrame([
    ('eva', 6, 'AREA_INVALIDA', json.dumps({'Área cosechada': '-3'}, ensure_ascii=False)),
    ('agrosavia', 8, 'DUPLICADO_EXACTO', json.dumps({'Secuencial': '107'}, ensure_ascii=False)),
], columns=['fuente', 'fila_fuente', 'motivos', 'registro_original'])

for nombre, tabla in [('eva', eva), ('divipola', divipola), ('agrosavia', agrosavia), ('rechazados', rechazados)]:
    tabla.to_parquet(DESTINO / f'{nombre}.parquet', index=False)

manifiesto = [{'id': fuente, 'ruta': f'fixture:{fuente}', 'bytes': None, 'bytes_esperados': None, 'sha256': None,
               'sha256_esperado': None, 'coincide': True, 'filas_leidas': filas, 'columnas': []}
              for fuente, filas in [('eva', 9), ('divipola', 4), ('agrosavia', 8)]]
(DESTINO / 'manifiesto_entradas.json').write_text(json.dumps(manifiesto, ensure_ascii=False, indent=2), encoding='utf-8')

controles_raw = {
    'run_id': 'fixture', 'firma_entrada': 'fixture', 'estado': 'valida',
    'fuentes': {
        'eva': {'leidas': 9, 'aceptadas': 8, 'rechazadas': 1, 'motivos': {'AREA_INVALIDA': 1}},
        'divipola': {'leidas': 4, 'aceptadas': 4, 'rechazadas': 0, 'motivos': {}},
        'agrosavia': {'leidas': 8, 'aceptadas': 7, 'rechazadas': 1, 'motivos': {'DUPLICADO_EXACTO': 1}},
    },
    'firmas_contenido': {},
    'errores': [],
    # Bloque reducido de entorno: SILVER lo compara con el suyo (convención de versionamiento).
    'entorno': {
        'capa': 'raw', 'responsable': 'fixture', 'version_notebook': 'generar_fixture_raw.py',
        'python': {'version': platform.python_version()},
        'librerias': {nombre: {'instalada': version(nombre)} for nombre in ['pandas', 'numpy', 'pyarrow']},
    },
}
(DESTINO / 'controles_raw.json').write_text(json.dumps(controles_raw, ensure_ascii=False, indent=2), encoding='utf-8')

# Resultado esperado de SILVER calculado a mano (ver README.md).
esperado_silver = {
    'filas_eva_entrada': 8, 'filas_unificado': 8, 'filas_aptas_rendimiento': 7, 'eva_sin_divipola': 1,
    'agrosavia_enlazadas': 6, 'agrosavia_sin_enlace': 1, 'agrosavia_por_alias': 2,
    'filas_suelo': 5, 'filas_sin_correspondencia': 2, 'particiones': 5,
    'cobertura_suelo_pct': 75.0, 'produccion_total_t': 1809.0, 'area_cosechada_total_ha': 165.0,
    'suelo': [
        {'codigo_municipio': '15001', 'anio': 2021, 'muestras': 2, 'mediana_ph': 5.5},
        {'codigo_municipio': '15001', 'anio': 2022, 'muestras': 1, 'mediana_ph': None},
        {'codigo_municipio': '54001', 'anio': 2021, 'muestras': 1, 'mediana_ph': 7.0},
    ],
    'area_cosechada_m2_fila_2': 100000.0,
}
(DESTINO / 'esperado_silver.json').write_text(json.dumps(esperado_silver, ensure_ascii=False, indent=2), encoding='utf-8')

print('Fixture RAW escrito en', DESTINO.relative_to(Path.cwd()) if DESTINO.is_relative_to(Path.cwd()) else DESTINO)
print({'eva': len(eva), 'divipola': len(divipola), 'agrosavia': len(agrosavia), 'rechazados': len(rechazados)})
