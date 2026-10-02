"""Spark local: consultas equivalentes o reproducción de observaciones NASA abiertas."""
from pathlib import Path
import argparse,json,os,tempfile
ROOT=Path(__file__).resolve().parent; OUT=ROOT/'salidas'
def session():
    from pyspark.sql import SparkSession
    return SparkSession.builder.master('local[2]').appName('SueloSabio').config('spark.sql.shuffle.partitions','4').config('spark.sql.session.timeZone','UTC').getOrCreate()
def lotes(spark):
    import duckdb
    e=spark.read.parquet(str(OUT/'eva.parquet'));d=spark.read.parquet(str(OUT/'dim_municipio.parquet'))
    e.createOrReplaceTempView('eva');d.createOrReplaceTempView('municipios')
    sql='''SELECT codigo_municipio,cultivo,estado_fisico,anio,
      sum(produccion_t) AS produccion_t, sum(area_ha) AS area_ha,
      sum(produccion_t)/sum(area_ha) AS rendimiento_t_ha
      FROM eva WHERE apto_rendimiento
      GROUP BY codigo_municipio,cultivo,estado_fisico,anio'''
    result=spark.sql(sql);result.explain('formatted')
    result.write.mode('overwrite').parquet(str(OUT/'spark_rendimiento'))
    con=duckdb.connect();con.execute('CREATE TABLE a AS SELECT * FROM read_parquet(?)',[str(OUT/'rendimiento.parquet')]);con.execute('CREATE TABLE b AS SELECT * FROM read_parquet(?)',[str(OUT/'spark_rendimiento/*.parquet')])
    differences=con.execute('''SELECT count(*) FROM a FULL OUTER JOIN b
      USING(codigo_municipio,cultivo,estado_fisico,anio)
      WHERE a.rendimiento_t_ha IS NULL OR b.rendimiento_t_ha IS NULL
      OR abs(a.rendimiento_t_ha-b.rendimiento_t_ha)>0.000001''').fetchone()[0]
    assert differences==0
    result.createOrReplaceTempView('rendimiento')
    spark.sql('''SELECT * FROM (SELECT *, row_number() OVER
      (PARTITION BY cultivo,estado_fisico,anio ORDER BY rendimiento_t_ha DESC,codigo_municipio) AS posicion
      FROM rendimiento) WHERE posicion<=3''').write.mode('overwrite').parquet(str(OUT/'spark_top3'))
    (OUT/'control_spark.json').write_text(json.dumps({'grupos':result.count(),'diferencias_duckdb':differences},indent=2));print('Equivalencia verificada.')
def eventos(spark):
    from pyspark.sql import functions as F,types as T
    # Solo cambia el orden de llegada. No se inventan observaciones ni se duplican eventos.
    raw=json.loads((ROOT/'data/raw/nasa.json').read_text())['properties']['parameter']['PRECTOTCORR']
    folder=Path(tempfile.mkdtemp(prefix='replay_',dir=OUT));source=folder/'entrada';source.mkdir()
    schema=T.StructType([T.StructField('event_id',T.StringType()),T.StructField('fecha',T.TimestampType()),T.StructField('lluvia_mm',T.DoubleType())])
    stream=spark.readStream.schema(schema).json(str(source))
    agg=stream.withWatermark('fecha','3 days').groupBy(F.window('fecha','7 days')).agg(F.sum('lluvia_mm').alias('lluvia_mm'),F.count('*').alias('observaciones'))
    query=agg.writeStream.format('json').outputMode('append').option('path',str(folder/'resultado')).option('checkpointLocation',str(folder/'checkpoint')).start()
    groups=[list(range(1,5))+list(range(6,11)),list(range(11,21)),list(range(21,32)),[5]]
    progress={}
    try:
        for i,days in enumerate(groups):
            lines=[]
            for day in days:
                date=f'202501{day:02d}';value=raw[date]
                if value==-999:continue
                lines.append(json.dumps({'event_id':date,'fecha':f'2025-01-{day:02d}T00:00:00','lluvia_mm':float(value)}))
            temp=folder/'lote.tmp';temp.write_text('\n'.join(lines)+'\n');temp.replace(source/f'lote_{i}.json')
            query.processAllAvailable()
            for p in query.recentProgress:progress[p['batchId']]=p
    finally:query.stop()
    summary={'carpeta':folder.name,'registros_fuente':len(raw),'reproduccion':'día 5 llega al final','progreso':list(progress.values())}
    (OUT/'control_eventos.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Evidencia:',folder,'Consultar numRowsDroppedByWatermark en control_eventos.json.')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('modo',choices=['lotes','eventos']);a=p.parse_args();spark=session()
    try: globals()[a.modo](spark)
    finally:spark.stop()
