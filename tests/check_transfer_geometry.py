"""Independent geometric validation of recorded poses (no browser or simulated ticks)."""
import json,math,argparse
from pathlib import Path
from run_baseline import ROOT
p=argparse.ArgumentParser();p.add_argument('report',nargs='?',default='test-results/transfer/results.json');a=p.parse_args()
r=json.loads((ROOT/a.report).read_text());home=r['states']['rest'];checks=[]
pivot=[s for s in r['samples'] if s['phase']==6 and s['mode']=='OK' and s['elapsed']/1.1<=.25]
slide=[s for s in r['samples'] if s['phase']==6 and s['mode']=='OK' and s['elapsed']/1.1>.25]
def bottom(s,z):
 pitch=s['pitch'];return s['piece'][1]-.0675*math.cos(pitch)-z*math.sin(pitch),s['piece'][2]-.0675*math.sin(pitch)+z*math.cos(pitch)
fixed=bool(pivot) and all(abs(bottom(s,.19)[0]-1.2925)<1e-6 and abs(bottom(s,.19)[1]-home['startZ'])<1e-6 for s in pivot)
aligned=bool(slide) and all(abs(s['pitch']+home['slope'])<1e-6 and all(abs(bottom(s,z)[0]-(home['rampTop']['y']+math.tan(home['slope'])*(bottom(s,z)[1]-home['rampTop']['z'])))<1e-6 for z in [-.19,.19]) for s in slide)
for name,ok,n in [('rear bottom corner fixed during tilt',fixed,len(pivot)),('both lower edges aligned during slide',aligned,len(slide))]:checks.append({'name':name,'status':'PASS' if ok else 'FAIL','samples':n})
out={'source_sha256':r['source_sha256'],'scope':'Post-validation of retained real-clock pose samples; does not rerun the simulation.','checks':checks}
path=ROOT/'test-results/transfer/pose-validation.json';path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
raise SystemExit(int(any(c['status']=='FAIL' for c in checks)))
