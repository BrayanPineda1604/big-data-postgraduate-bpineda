"""Prácticas de PQRS reales y reproducción NASA. Preparado por el PhD Esteban Hernández, CyberColombia."""
from pathlib import Path
import argparse, csv, hashlib, json, os, sys, time, tempfile, shutil, statistics, threading
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'pqrs_fuentes.json'
def guardar(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
def ruta_kit(value):
    path=Path(value).expanduser()
    return path if path.is_absolute() else ROOT/path
def fuentes():return json.loads(MANIFEST.read_text(encoding='utf-8'))
def seleccion(a):
    folder=ruta_kit(a.datos) if a.datos else ROOT/'data/pqrs_muestras'
    result=[]
    for f in fuentes():
        p=folder/(f['archivo'] if a.completo else 'Muestra_1000_'+f['periodo']+'.csv')
        if not p.exists():raise FileNotFoundError(f'Falta {p}. Indicar --datos o usar muestras incluidas.')
        result.append((f,p))
    return result
def hash_archivo(p):
    h=hashlib.sha256()
    with p.open('rb') as r:
        for b in iter(lambda:r.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def leer(f,p,bloque):return pd.read_csv(p,sep=f['separador'],encoding='utf-8-sig',dtype=str,keep_default_na=False,chunksize=bloque)
def perfil(a):
    result=[]
    for f,p in seleccion(a):
        n=0; vacios={};meses={};mem=0;anchos=0
        with p.open(encoding='utf-8-sig',newline='') as stream:
            r=csv.reader(stream,delimiter=f['separador']);header=next(r)
            if header!=f['columnas']:raise ValueError(f'Esquema distinto: {p.name}')
            for row in r:
                if len(row)!=len(header):anchos+=1
        for chunk in leer(f,p,a.bloque):
            n+=len(chunk);mem=max(mem,int(chunk.memory_usage(deep=True).sum()))
            for col in chunk:vacios[col]=vacios.get(col,0)+int(chunk[col].str.strip().eq('').sum())
            for month,count in chunk['mes'].value_counts().items():meses[month]=meses.get(month,0)+int(count)
        sha=hash_archivo(p);expected=f['sha256'] if a.completo else f['sha256_muestra']
        if sha!=expected:raise ValueError(f'Huella distinta en {p.name}: revisar el corte antes de usarlo')
        if a.completo and n!=f['filas']:raise ValueError('Conteo distinto del corte docente')
        if anchos:raise ValueError('Hay filas con ancho incorrecto')
        result.append({'archivo':p.name,'corte':f['periodo'],'filas':n,'columnas':len(header),'bytes':p.stat().st_size,'memoria_dataframe_bloque_max_bytes':mem,'ancho_incorrecto':anchos,'meses':meses,'vacios':vacios,'sha256_coincide':True,'alcance':'completo' if a.completo else 'primeras 1000 filas'})
    guardar(a.out/'perfil_pqrs.json',result);print([(r['corte'],r['filas'],r['bytes']) for r in result]);return result
SCHEMA=pa.schema([('corte_archivo',pa.string()),('fila_fuente',pa.int64()),('OBJECTID',pa.string()),('periodo',pa.string()),('mes',pa.string()),('afec_cod_depto',pa.string()),('afec_cod_mpio',pa.string()),('pet_cod_depto',pa.string()),('pet_cod_mpio',pa.string()),('ent_nombre',pa.string()),('afec_edad',pa.string()),('afec_genero',pa.string()),('anio',pa.int64()),('mes_num',pa.int64()),('edad_num',pa.float64()),('clave_candidata',pa.string())])
def normalizar(c,f,offset):
    required=set(f['columnas'])
    if set(c.columns)!=required:raise ValueError('Contrato de nombres incumplido: detener antes de publicar')
    q=c[['OBJECTID','periodo','mes','afec_cod_depto','afec_cod_mpio','pet_cod_depto','pet_cod_mpio','ent_nombre','afec_edad','afec_genero']].copy()
    q['corte_archivo']=f['periodo'];q['fila_fuente']=range(offset+2,offset+len(c)+2)
    q['anio']=pd.to_numeric(q['periodo'],errors='coerce').astype('Int64');q['mes_num']=pd.to_numeric(q['mes'],errors='coerce').astype('Int64');q['edad_num']=pd.to_numeric(q['afec_edad'],errors='coerce')
    q['clave_candidata']=q['corte_archivo']+'|'+q['OBJECTID']
    return pa.Table.from_pandas(q,schema=SCHEMA,preserve_index=False,safe=True)
def formatos(a):
    # Publicación completa por reemplazo: una reejecución no añade registros al producto anterior.
    perfil(a);a.out.mkdir(parents=True,exist_ok=True);stage=Path(tempfile.mkdtemp(prefix='pqrs_',dir=a.out));count=0
    try:
        dest=stage/'pqrs.parquet'
        with pq.ParquetWriter(dest,SCHEMA,compression='zstd') as w:
            for f,p in seleccion(a):
                offset=0
                for c in leer(f,p,a.bloque):
                    table=normalizar(c,f,offset);w.write_table(table);offset+=len(c);count+=len(c)
        con=duckdb.connect();con.execute("SET threads=2");con.execute("SET memory_limit='1GB'")
        con.execute('CREATE TABLE q AS SELECT * FROM read_parquet(?)',[str(dest)])
        # La partición se usa para estudiar consultas; el año procede de periodo, no del nombre del semestre.
        partition=stage/'pqrs_particionado'
        literal=str(partition).replace("'","''")
        con.execute(f"COPY q TO '{literal}' (FORMAT PARQUET, PARTITION_BY (anio,mes_num), COMPRESSION ZSTD)")
        rows=con.execute('SELECT count(*) FROM read_parquet(?)',[str(partition/'**/*.parquet')]).fetchone()[0]
        if rows!=count:raise AssertionError('La partición cambió el conteo')
        signature=con.execute('SELECT sum(hash(corte_archivo,fila_fuente,OBJECTID,periodo,mes,afec_cod_depto,ent_nombre,afec_edad)) FROM q').fetchone()[0]
        con.close()
        # CSV normalizado conserva exactamente la proyección usada por Parquet, para el benchmark.
        normalized=stage/'pqrs_proyeccion.csv'
        with normalized.open('w',encoding='utf-8',newline='') as stream:
            for i,b in enumerate(pq.ParquetFile(dest).iter_batches(batch_size=a.bloque)):
                b.to_pandas().to_csv(stream,index=False,header=i==0)
        for name in ['pqrs.parquet','pqrs_particionado','pqrs_proyeccion.csv']:
            target=a.out/name
            if target.is_dir():shutil.rmtree(target)
            elif target.exists():target.unlink()
            shutil.move(stage/name,target)
        report={'filas':count,'columnas_producto':len(SCHEMA),'columnas_original':38,'bytes_parquet':(a.out/'pqrs.parquet').stat().st_size,'bytes_csv_proyeccion':(a.out/'pqrs_proyeccion.csv').stat().st_size,'particiones_archivos':len(list((a.out/'pqrs_particionado').rglob('*.parquet'))),'firma_contenido':str(signature),'bloque':a.bloque,'alcance':'completo' if a.completo else 'muestra','particion':['anio','mes_num'],'originales_modificados':False}
        guardar(a.out/'control_formatos_pqrs.json',report);print(report);return report
    finally:shutil.rmtree(stage,ignore_errors=True)
def calidad(a):
    con=duckdb.connect();con.execute("SET threads=2");con.execute("SET memory_limit='1GB'")
    con.execute('CREATE TABLE q AS SELECT * FROM read_parquet(?)',[str(a.out/'pqrs.parquet')])
    result=con.execute('''SELECT count(*) filas, count(DISTINCT clave_candidata) claves_candidatas,
       count(*) FILTER(WHERE OBJECTID='') id_vacio,
       count(*) FILTER(WHERE anio IS NULL OR mes_num IS NULL OR mes_num NOT BETWEEN 1 AND 12) periodo_en_revision,
       count(*) FILTER(WHERE edad_num IS NULL OR edad_num<0) edad_en_revision,
       count(*) FILTER(WHERE edad_num>90) mayores_90,
       count(*) FILTER(WHERE pet_cod_depto='' OR pet_cod_mpio='') ubicacion_peticionario_vacia FROM q''').df().iloc[0].to_dict()
    # No deduplicar una proyección: filas que difieren en las otras 28 columnas pueden coincidir aquí.
    dim=ROOT/'data/raw/divipola.csv'
    if dim.exists():
        d=pd.read_csv(dim,dtype=str);d['municipio']=d['Código Municipio'].str.zfill(5);con.register('dim',d)
        result['afectados_sin_municipio_divipola']=con.execute('SELECT count(*) FROM q LEFT JOIN dim ON q.afec_cod_mpio=dim.municipio WHERE dim.municipio IS NULL').fetchone()[0]
    result={k:int(v) for k,v in result.items()};result['exclusiones_automaticas']=0
    guardar(a.out/'control_calidad_pqrs.json',result)
    con.execute('SELECT corte_archivo,anio,mes_num,afec_cod_depto,count(*) reportes FROM q GROUP BY ALL ORDER BY ALL').df().to_csv(a.out/'reportes_por_grupo.csv',index=False)
    con.close();print(result);return result
QUERY='''SELECT corte_archivo,anio,mes_num,afec_cod_depto,count(*) AS reportes FROM q GROUP BY corte_archivo,anio,mes_num,afec_cod_depto ORDER BY corte_archivo,anio,mes_num,afec_cod_depto'''
def trabajador(motor,folder):
    folder=Path(folder);p=folder/'pqrs.parquet'
    if motor=='pandas':
        d=pd.read_parquet(p,columns=['corte_archivo','anio','mes_num','afec_cod_depto']);r=d.groupby(['corte_archivo','anio','mes_num','afec_cod_depto'],dropna=False).size().reset_index(name='reportes')
    elif motor=='polars':
        import polars as pl
        q=pl.scan_parquet(p).group_by(['corte_archivo','anio','mes_num','afec_cod_depto']).agg(pl.len().alias('reportes'));r=q.collect(engine='streaming').to_pandas()
    else:
        c=duckdb.connect();c.execute("SET threads=2");c.execute("SET memory_limit='1GB'")
        if motor=='duckdb_csv':c.read_csv(str(folder/'pqrs_proyeccion.csv'), header=True, all_varchar=True).create_view('q')
        else:c.read_parquet(str(p if motor=='duckdb' else folder/'pqrs_particionado/**/*.parquet'),hive_partitioning=(motor=='duckdb_particionado')).create_view('q')
        r=c.sql(QUERY).df();c.close()
    for col in ['anio','mes_num','reportes']:r[col]=r[col].astype('int64')
    r['afec_cod_depto']=r['afec_cod_depto'].astype(str).str.zfill(2)
    r=r.sort_values(['corte_archivo','anio','mes_num','afec_cod_depto']).reset_index(drop=True)
    return r
def benchmark(a):
    import subprocess,psutil
    control=json.loads((a.out/'control_formatos_pqrs.json').read_text())
    scope='completo' if a.completo else 'muestra'
    if control['alcance']!=scope:
        raise ValueError('El producto no coincide con --completo: ejecutar formatos con el alcance y --salidas correctos')
    expected_rows=sum(f['filas'] for f in fuentes()) if a.completo else 3000
    if control['filas']!=expected_rows:
        raise ValueError('Conteo del producto distinto del corte de referencia')
    motors=['pandas','polars','duckdb','duckdb_particionado','duckdb_csv'];reports=[];baseline=None
    for motor in motors:
        # Calentamiento explícito. Cada medición se realiza en un proceso nuevo.
        for trial in range(-1,a.repeticiones):
            fd=Path(tempfile.mktemp(prefix='resultado_',suffix='.csv',dir=a.out))
            start=time.perf_counter();e=os.environ.copy();e.update(POLARS_MAX_THREADS='2',OMP_NUM_THREADS='2',OPENBLAS_NUM_THREADS='2')
            proc=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'_worker',motor,str(a.out),str(fd)],env=e,stdout=subprocess.DEVNULL)
            monitor=psutil.Process(proc.pid);rss=0
            while proc.poll() is None:
                try:rss=max(rss,monitor.memory_info().rss+sum(c.memory_info().rss for c in monitor.children(recursive=True)))
                except (psutil.NoSuchProcess,psutil.AccessDenied,PermissionError):pass
                time.sleep(.01)
            elapsed=time.perf_counter()-start
            if proc.returncode:raise RuntimeError(f'Falló {motor}')
            result=pd.read_csv(fd,dtype={'afec_cod_depto':str});fd.unlink()
            if int(result['reportes'].sum())!=expected_rows:raise AssertionError('El motor no conservó el conteo de entrada')
            if baseline is None:baseline=result
            pd.testing.assert_frame_equal(baseline,result,check_dtype=False)
            if trial>=0:reports.append({'motor':motor,'repeticion':trial+1,'segundos_extremo_a_extremo':elapsed,'rss_max_muestreado_bytes':rss,'filas_entrada':int(result['reportes'].sum()),'grupos':len(result),'intervalo_sondeo_ms':10,'alcance':'completo' if a.completo else 'muestra','equivalente':True})
    pd.DataFrame(reports).to_csv(a.out/'benchmark_pqrs.csv',index=False)
    summary=pd.DataFrame(reports).groupby('motor').agg(mediana_segundos=('segundos_extremo_a_extremo','median'),rss_max_muestreado_bytes=('rss_max_muestreado_bytes','max')).reset_index()
    summary.to_csv(a.out/'benchmark_pqrs_resumen.csv',index=False);print(summary.to_string(index=False));return reports

def eventos(a):
    # Reproducción finita de valores NASA reales, con un reintento y un día que llega tarde.
    nasa=ROOT/'data/raw/nasa.json'
    values=json.loads(nasa.read_text())['properties']['parameter']['PRECTOTCORR']
    days=list(range(1,5))+list(range(6,13))+[6,5];seen=set();latest=None;trace=[];accepted=[]
    from datetime import datetime,timedelta
    for day in days:
        key=f'202501{day:02d}';date=datetime.strptime(key,'%Y%m%d');wm=latest-timedelta(days=3) if latest else None
        if key in seen:status='duplicado'
        elif wm and date<wm:status='tardio'
        else:status='aceptado';seen.add(key);accepted.append(float(values[key]))
        latest=max(latest or date,date)
        trace.append({'event_id':key,'fecha_evento':date.date().isoformat(),'lluvia_mm':values[key],'watermark_antes':wm.date().isoformat() if wm else None,'estado':status})
    pd.DataFrame(trace).to_csv(a.out/'traza_eventos_nasa.csv',index=False)
    r={'entregas':len(trace),'registros_reales_distintos':len(set(t['event_id'] for t in trace)),'aceptados':sum(t['estado']=='aceptado' for t in trace),'duplicados':sum(t['estado']=='duplicado' for t in trace),'tardios':sum(t['estado']=='tardio' for t in trace),'suma_aceptada_mm':sum(accepted),'regla':'demora de 3 días; traza simplificada para discusión, no implementación de Spark','reintento':'día 6','tardio':'día 5'}
    guardar(a.out/'control_eventos_intro.json',r);print(r);return r

def main():
    if len(sys.argv)>1 and sys.argv[1]=='_worker':trabajador(sys.argv[2],sys.argv[3]).to_csv(sys.argv[4],index=False);return
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('modo',choices=['perfil','formatos','calidad','benchmark','eventos']);p.add_argument('--config',type=Path);p.add_argument('--datos');p.add_argument('--completo',action='store_true');p.add_argument('--bloque',type=int,default=25000);p.add_argument('--salidas',type=Path);p.add_argument('--repeticiones',type=int,default=3);a=p.parse_args()
    if a.config:
        cfg=json.loads(ruta_kit(a.config).read_text(encoding='utf-8'))
        if set(cfg)-{'datos','completo','bloque','repeticiones'}:raise ValueError('Claves de configuración no admitidas')
        for key,value in cfg.items():
            if '--'+key not in sys.argv:setattr(a,key,value)
    if not 100<=a.bloque<=100000:raise ValueError('Elegir bloque entre 100 y 100000 filas')
    if not 1<=a.repeticiones<=10:raise ValueError('Elegir entre 1 y 10 repeticiones')
    a.out=ruta_kit(a.salidas or 'salidas/pqrs').resolve();a.out.mkdir(parents=True,exist_ok=True);globals()[a.modo](a)
if __name__=='__main__':main()
