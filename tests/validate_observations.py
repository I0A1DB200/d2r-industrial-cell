"""Checks observations, never calculates or controls the simulator's next state."""
import math

def validate(report):
 checks=[]
 current=report['states'].get('ready',{}).get('mechanics')=='contact-transfer'
 def add(name,ok,detail=None):checks.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
 samples=[s for s in report['samples'] if s['running'] and not s['betweenCycles'] and s['phase']<7]
 add('positions finite',bool(samples) and all(all(math.isfinite(x) for x in s['piece']+[s['armZ'],s['gateX']]) for s in samples))
 add('piece vertical envelope',bool(samples) and all(.809<=s['piece'][1]<=1.361 for s in samples))
 add('actuator travel bounds',bool(samples) and all(-1.481<=s['armZ']<=.001 and ((-1.321<=s['gateX']<=-.319) if current else (.289<=s['gateX']<=.521)) for s in samples))
 for phase in range(7):
  rows=[s for s in samples if s['phase']==phase]
  add(f'phase {phase} positions observed',bool(rows))
  if not rows:continue
  if phase==0:ok=all(((-4.001<=s['piece'][0]<=-2.999) if current else abs(s['piece'][0]+3)<.001) and abs(s['armZ'])<.001 for s in rows)
  elif phase==1:ok=all(-3.001<=s['piece'][0]<=-.649 and abs(s['piece'][2])<.001 for s in rows)
  elif phase==2:ok=all(abs(s['piece'][0]+.65)<.001 and abs(s['piece'][2])<.001 for s in rows)
  elif phase==3:ok=all(-.651<=s['piece'][0]<=1.251 and abs(s['piece'][2])<.001 for s in rows)
  elif phase==4:ok=all(abs(s['piece'][0]-1.25)<.001 and abs(s['piece'][2])<.001 for s in rows)
  elif phase==5:ok=all((abs(s['piece'][0]-1.25)<.001 and -2.251<=s['piece'][2]<=.001) if s['mode']=='OK' else (1.249<=s['piece'][0]<=4.151 and abs(s['armZ'])<.001) for s in rows)
  else:ok=all(((-2.251<=s['piece'][2]<=-.9065) if current else abs(s['piece'][2]+2.25)<.001) if s['mode']=='OK' else abs(s['piece'][0]-4.15)<.001 for s in rows)
  add(f'phase {phase} position envelope',ok)
 monotonic=True
 for a,b in zip(samples,samples[1:]):
  if a['partIndex']!=b['partIndex'] or a['phase']!=b['phase'] or b['elapsed']<a['elapsed']:continue
  if a['phase'] in [1,3]:monotonic=monotonic and b['piece'][0]>=a['piece'][0]-.001
  if a['phase']==5 and a['mode']=='OK':monotonic=monotonic and b['piece'][2]<=a['piece'][2]+.001 and b['armZ']<=a['armZ']+.001
  if a['phase']==6 and a['mode']=='OK':monotonic=monotonic and b['armZ']>=a['armZ']-.001
 add('observed travel directions',monotonic)
 expected=['OK','NOK','OK','NOK','OK','OK','NOK']
 ready=report['states']['ready']
 add('batch order and phase durations preserved',ready['batch']==expected and [x[1] for x in ready['phases']]==[.8,2.2,1.5,1.9,.5,2.2,1.1])
 observed=list(report['states'].values())
 typed=[s for s in observed if 'numeric' in s]
 valid=bool(typed)
 for s in typed:
  for tag,kind in s['types']:
   value=s['numeric'][tag]
   try:
    if kind=='REAL':float(value.split()[0]);valid=valid and len(value.split()[0].split('.')[-1])==2
    elif kind=='TIME':valid=valid and value.endswith(' ms');int(value.split()[0].replace('.',''))
    else:int(value.replace('.',''))
   except (ValueError,IndexError):valid=False
 add('INT DINT REAL TIME displayed values parse',valid)
 report['checks'].extend(checks)
 return checks
