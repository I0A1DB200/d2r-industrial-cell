import json,hashlib,time
from browser_lab import ROOT,lab
out=ROOT/'test-results/feeder';out.mkdir(parents=True,exist_ok=True)
r={'checks':[],'states':{},'counts':[],'errors':[],'source_sha256':hashlib.sha256((ROOT/'D2R-3D-001_Prototipo_Funcional_v11.html').read_bytes()).hexdigest()}
def check(name,ok,detail=None):
 r['checks'].append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail});print(r['checks'][-1],flush=True)
try:
 with lab(640,480,'tests/feeder-observer.js') as (page,read,wait,errors):
  def click(id):page.locator('#'+id).click()
  page.locator('[data-focus="feed"]').click()
  s=read();check('seven initially, active at -4',len(s['uppers'])==6 and s['active'] and s['piece']==[-4,1.36,0])
  page.screenshot(path=str(out/'loaded.png'))
  click('auto')
  for name,lo,hi in [('advance',.12,.35),('return',.48,.68),('drop',.81,.96)]:
   wait(lambda s:s['phase']==0 and lo<=s['elapsed']/.8<=hi,name)
   click('pause');s=read();r['states'][name]=s
   check(name+' captured FEED',s['phase']==0)
   if name=='advance':check('piece and orange pusher stay in contact',abs(s['piece'][0]-.26-(-2.98+s['gateX']+.04))<1e-6)
   if name=='return':check('piece waits at belt during return',abs(s['piece'][0]+3)<1e-6 and -1.32<s['gateX']<-.32)
   if name=='drop':check('drop only after carriage retracted',abs(s['gateX']+1.32)<1e-6 and 1.36<s['uppers'][0][1]<1.495)
   check(name+' rod connected/anchored',abs(s['rod'][0]+1.70)<1e-6 and abs(s['rod'][1]-(s['gateX']-.04))<1e-6 and s['barrel']==[-2.25,1.1,0])
   page.wait_for_timeout(200);check(name+' pause freezes',read()==s)
   page.screenshot(path=str(out/f'{name}.png'));click('pause')
  # All seven actual cycles, no clock changes; smaller render surface for software.
  page.set_viewport_size({'width':256,'height':192})
  seen=set();deadline=time.monotonic()+1500;valid=True
  while time.monotonic()<deadline:
   s=read();remaining=int(s['active'])+len(s['uppers'])
   valid=valid and remaining==7-s['partIndex']
   if (s['partIndex'],remaining) not in seen:
    seen.add((s['partIndex'],remaining));r['counts'].append({'index':s['partIndex'],'visible':remaining});print('remaining',remaining,flush=True)
   if s['partIndex']==7 and not s['running']:break
   page.wait_for_timeout(100)
  r['states']['empty']=s
  check('no duplicate/missing workpiece at any sampled instant',valid)
  check('full batch 4 OK 3 NOK and zero visible',s['partIndex']==7 and s['okCount']==4 and s['nokCount']==3 and not s['active'] and not s['uppers'])
  page.set_viewport_size({'width':640,'height':480});page.screenshot(path=str(out/'empty.png'))
  click('reset');s=read();r['states']['reset']=s
  check('RESET reloads exactly seven at home',s['partIndex']==0 and s['active'] and len(s['uppers'])==6 and s['piece']==[-4,1.36,0] and abs(s['gateX']+1.32)<1e-6)
  page.screenshot(path=str(out/'reset.png'));r['errors']=errors;check('no JS errors',not errors,errors)
except Exception as e:check('scenario completed',False,repr(e))
finally:(out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
raise SystemExit(int(any(c['status']=='FAIL' for c in r['checks'])))
