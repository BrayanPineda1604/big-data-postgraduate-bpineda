"""Descargador PQRS de tamaño acotado. Preparado por el PhD Esteban Hernández, CyberColombia."""
from pathlib import Path
import argparse,json,hashlib,urllib.request
ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--listar',action='store_true');p.add_argument('--descargar',nargs='+');p.add_argument('--verificar',action='store_true');p.add_argument('--datos',type=Path,default=ROOT/'data/pqrs_completos');a=p.parse_args()
f=json.loads((ROOT/'pqrs_fuentes.json').read_text());a.datos.mkdir(parents=True,exist_ok=True)
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as r:
  for b in iter(lambda:r.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
if a.listar:
 for x in f:print(x['periodo'],x['archivo'],round(x['bytes']/1e6,2),'MB',x['filas'],'filas',x['url'])
if a.descargar:
 if set(a.descargar)-{x['periodo'] for x in f}:raise SystemExit('Cortes admitidos: 2023_II, 2024_I, 2024_II')
 for x in f:
  if x['periodo'] not in a.descargar:continue
  path=a.datos/x['archivo'];part=path.with_suffix('.csv.part')
  if path.exists():print('Se conserva:',path.name);continue
  try:
   req=urllib.request.Request(x['url'],headers={'User-Agent':'Curso-BigData/1.0'})
   with urllib.request.urlopen(req,timeout=60) as r,part.open('wb') as w:
    if 'text/html' in r.headers.get('Content-Type','').lower():raise ValueError('Respuesta HTML en vez de CSV')
    n=0
    while True:
     block=r.read(1024*1024)
     if not block:break
     n+=len(block)
     if n>x['bytes']*1.5:raise ValueError('Tamaño supera 1,5 veces el corte de referencia; revisar fuente')
     w.write(block)
   if sha(part)!=x['sha256']:
    part.replace(path.with_suffix('.csv.nueva'));raise ValueError('Hash cambió. Conservar .nueva y revisar corte antes de usarlo')
   part.replace(path);print('Descargado:',path.name)
  except Exception as e:part.unlink(missing_ok=True);raise SystemExit(str(e))
if a.verificar:
 for x in f:
  path=a.datos/x['archivo']
  if not path.exists():raise SystemExit('Ausente: '+str(path))
  if sha(path)!=x['sha256']:raise SystemExit('Hash distinto: '+path.name)
  print(path.name,'coincide',path.stat().st_size,'bytes')
if not any([a.listar,a.descargar,a.verificar]):p.print_help()
