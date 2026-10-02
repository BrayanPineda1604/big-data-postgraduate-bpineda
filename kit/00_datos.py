"""Descarga o verifica las 12 fuentes fechadas del curso. Solo biblioteca estándar."""
from pathlib import Path
import argparse, csv, hashlib, json, shutil, urllib.request, zipfile
ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'data' / 'raw'
P = argparse.ArgumentParser(description=__doc__)
P.add_argument('--listar', action='store_true')
P.add_argument('--descargar', nargs='+', metavar='ID')
P.add_argument('--respaldo', type=Path, help='Carpeta raw de una copia del kit')
P.add_argument('--verificar', action='store_true')
args = P.parse_args()
fuentes = json.loads((ROOT/'fuentes.json').read_text(encoding='utf-8'))['fuentes']
RAW.mkdir(parents=True, exist_ok=True)
if args.listar:
    for f in fuentes:
        print(f"{f['id']:20} {f['bytes']/1e6:8.3f} MB  {f['alcance']:8} {f['metodo']}")
if args.respaldo:
    for f in fuentes:
        src = args.respaldo/f['archivo']; dst = RAW/f['archivo']
        if src.resolve() == dst.resolve(): continue
        if not src.exists(): raise SystemExit(f'Falta {src}')
        if hashlib.sha256(src.read_bytes()).hexdigest() != f['sha256']:
            raise SystemExit(f'El respaldo no coincide con la versión docente: {src}')
        if dst.exists():
            if hashlib.sha256(dst.read_bytes()).hexdigest() != f['sha256']:
                raise SystemExit(f'No se sobrescribe una versión diferente: {dst}')
        else: shutil.copy2(src, dst)
if args.descargar:
    unknown = set(args.descargar)-{f['id'] for f in fuentes}
    if unknown: raise SystemExit(f'IDs desconocidos: {unknown}')
    for f in fuentes:
        if f['id'] not in args.descargar: continue
        dst = RAW/f['archivo']
        if dst.exists():
            print(f"Ya existe {dst.name}; use --verificar. No se sobrescribe."); continue
        if f['metodo'] == 'manual':
            print(f"Descarga DANE mediante navegador; guardar como {dst}\n{f['url']}"); continue
        temp = dst.with_suffix(dst.suffix+'.part')
        limit = max(f['bytes']*3, 2_000_000)
        try:
            with urllib.request.urlopen(f['url'], timeout=60) as response, temp.open('wb') as w:
                ct = response.headers.get('Content-Type','').lower(); n=0
                if 'text/html' in ct: raise ValueError('El servidor entregó HTML en lugar de datos')
                while True:
                    chunk = response.read(1024*1024)
                    if not chunk: break
                    n += len(chunk)
                    if n > limit: raise ValueError(f'Descarga supera el límite docente de {limit/1e6:.1f} MB')
                    w.write(chunk)
            if hashlib.sha256(temp.read_bytes()).hexdigest() != f['sha256']:
                changed=dst.with_suffix(dst.suffix+'.nueva'); temp.replace(changed)
                raise ValueError(f'La fuente cambió; se conserva en {changed.name}. Revisar esquema y controles antes de sustituir el corte docente.')
            temp.replace(dst); print('Descargado:',dst.name)
        except Exception as e:
            temp.unlink(missing_ok=True)
            print(f"No se incorporó {f['id']}: {e}\nUsar el respaldo fechado; no reintentar en bucle.")
if args.verificar:
    report=[]
    for f in fuentes:
        file=RAW/f['archivo']; r={'id':f['id'],'archivo':f['archivo']}
        if not file.exists(): r['estado']='ausente'
        else:
            r['bytes']=file.stat().st_size
            r['sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
            r['estado']='coincide' if r['sha256']==f['sha256'] else 'version_distinta'
            if file.suffix=='.csv':
                with file.open(encoding='utf-8-sig',newline='') as stream:
                    reader=csv.reader(stream); r['columnas']=len(next(reader)); r['filas']=sum(1 for _ in reader)
            elif file.suffix=='.zip':
                with zipfile.ZipFile(file) as z:
                    r['zip_integro']=z.testzip() is None
                    r['componentes']=sorted({Path(n).suffix for n in z.namelist()})
            elif file.suffix=='.json':
                d=json.loads(file.read_text()); r['error_api']=d.get('error')
                if 'features' in d:r['elementos']=len(d['features'])
        report.append(r); print(r['id'],r['estado'],r.get('filas',r.get('elementos','')))
    out=ROOT/'salidas';out.mkdir(exist_ok=True)
    (out/'verificacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    if any(r['estado']!='coincide' or r.get('error_api') or r.get('zip_integro') is False for r in report):
        raise SystemExit('Verificación incompleta: consultar salidas/verificacion.json')
if not any([args.listar,args.descargar,args.respaldo,args.verificar]): P.print_help()
