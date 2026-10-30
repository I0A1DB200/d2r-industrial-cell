import json,math,time,hashlib
from browser_lab import ROOT,lab
from protected_contract import protected_checks
out=ROOT/'test-results/transfer';out.mkdir(parents=True,exist_ok=True)
source=(ROOT/'D2R-3D-001_Prototipo_Funcional_v11.html').read_text()
r={'checks':protected_checks(source),'states':{},'terminals':[],'samples':[],'errors':[],'source_sha256':hashlib.sha256(source.encode()).hexdigest()}
def check(name,ok,detail=None):
 r['checks'].append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail});print(r['checks'][-1],flush=True)
try:
 with lab(256,192,'tests/transfer-observer.js') as (page,read,wait,errors):
  def click(id):page.locator('#'+id).click()
  page.locator('[data-focus="sort"]').click()
  def capture(name):
   page.set_viewport_size({'width':800,'height':600});page.screenshot(path=str(out/f'{name}.png'));page.set_viewport_size({'width':256,'height':192})
  s=read();r['states']['rest']=s
  check('rails/glass clear full ramp exterior',len(s['passage'])==8 and all(p['hi']<=.78001 or p['lo']>=1.71999 for p in s['passage']),s['passage'])
  check('fixed caps at both cylinder ends',s['caps']==[[0,1.385,1.3],[0,1.385,3.1]])
  check('plate outside belt and above it at rest',s['homeFace']>.55 and s['plateBottom']>1.2925 and s['armZ']==0);capture('rest')
  click('auto')
  for name,predicate in [
   ('arrival',lambda s:s['phase']==4),
   ('approach',lambda s:s['phase']==5 and -.25<s['armZ']<-.04),
   ('contact',lambda s:s['phase']==5 and s['piece'][2]<-.10 and s['armZ']> -1.35),
   ('return',lambda s:s['phase']==6 and .35<s['elapsed']/1.1<.60)]:
   wait(predicate,name);click('pause');s=read();r['states'][name]=s
   check(name+' target captured',predicate(s))
   if name=='arrival':check('SORT_STOP piece fixed and pusher home',s['piece']==[1.25,1.36,0] and s['armZ']==0)
   if name=='approach':check('approach does not move piece',s['piece']==[1.25,1.36,0] and s['face']>.19)
   if name=='contact':check('contact faces coincide',abs(s['face']-(s['piece'][2]+.19))<1e-6)
   if name=='return':check('return separates plate, does not drag piece',s['face']>max(p[2] for p in s['corners']) and s['piece'][2]<-.9)
   capture(name);click('pause')
  # Capture first terminal and all subsequent transfers from the untouched clock.
  ok_contact=True;approach_still=True;return_clear=True;ramp_clear=True;outside=True;rod_ok=True;nok_home=True;body_fixed=True
  seen=set();last_return={};deadline=time.monotonic()+1500
  while time.monotonic()<deadline:
   s=read();r['samples'].append({k:s[k] for k in ['phase','elapsed','partIndex','mode','piece','pitch','armZ','face','visible']})
   body_fixed=body_fixed and s['body']==[0,1.385,2.2]
   rod_ok=rod_ok and abs(s['rod'][0]-s['plateBack'])<1e-6 and abs(s['rod'][1]-1.35)<1e-6
   if s['mode']=='NOK':nok_home=nok_home and abs(s['armZ'])<1e-8
   if s['phase']==5 and s['mode']=='OK':
    if s['face']>.19:approach_still=approach_still and abs(s['piece'][2])<1e-7
    else:ok_contact=ok_contact and abs(s['face']-(s['piece'][2]+.19))<1e-6
   if s['phase']==6 and s['mode']=='OK':
    outside=outside and max(p[2] for p in s['corners'])<-.55
    return_clear=return_clear and s['face']>=max(p[2] for p in s['corners'])-1e-6
    for p in s['corners']:
     surface=1.2925 if p[2]>=s['startZ'] else s['rampTop']['y']+math.tan(-s['rampTop']['pitch'])*(p[2]-s['rampTop']['z'])
     ramp_clear=ramp_clear and p[1]>=surface-1e-6
    prev=last_return.get(s['partIndex'])
    if prev:return_clear=return_clear and s['armZ']>=prev['armZ']-1e-6 and s['piece'][2]<=prev['piece'][2]+1e-6
    last_return[s['partIndex']]=s
   if not s['visible'] and s['partIndex'] not in seen:
    seen.add(s['partIndex']);r['terminals'].append(s);print('terminal',s['partIndex'],s['mode'],flush=True)
   if s['partIndex']==7 and not s['running']:break
   page.wait_for_timeout(80)
  check('four OK three NOK complete',s['partIndex']==7 and s['okCount']==4 and s['nokCount']==3)
  check('all seven terminal poses observed',len(r['terminals'])==7)
  oks=[s for s in r['terminals'] if s['mode']=='OK'];noks=[s for s in r['terminals'] if s['mode']=='NOK']
  check('four OK exact terminal pose before hiding',len(oks)==4 and all(abs(s['piece'][2]+2.25)<1e-7 and abs(s['pitch']+s['slope'])<1e-7 and abs(s['piece'][1]-(1.2925+math.tan(s['slope'])*(-2.25-s['startZ'])+.0675/math.cos(s['slope'])))<1e-7 for s in oks))
  check('three NOK original terminal',len(noks)==3 and all(s['piece']==[4.15,.81,0] and s['pitch']==0 for s in noks))
  for name,ok in [('contact without penetration',ok_contact),('approach without displacement',approach_still),('return without drag',return_clear),('piece wholly off belt during OK return',outside),('bottom corners never through bridge/ramp plane',ramp_clear),('rod connected with fixed internal rear',rod_ok),('body and caps fixed',body_fixed),('all NOK keep arm home',nok_home)]:check(name,ok)
  # Existing fault diagnostics after the reconstructed graphics.
  for fault,diag in [('vision','Diag_VisionTimeout'),('pusher','Diag_PusherMismatch')]:
   click('reset');page.locator('[data-panel="faults"]').click();page.locator('#faultSelect').select_option(fault);click('panelClose');click('auto')
   s=wait(lambda s:s['faultLatched'],fault);r['states']['fault_'+fault]=s
   check(fault+' snapshot retained',s['io'][diag] and s['numericFrozen'] and s['partIndex']==0)
   page.set_viewport_size({'width':390,'height':844});click('hmiReset');check(fault+' reset releases fault and reloads seven',not read()['faultLatched'] and read()['visible'] and read()['upperCount']==6);page.set_viewport_size({'width':256,'height':192})
  r['errors']=errors;check('no JS errors including between cycles',not errors,errors)
except Exception as e:check('scenario completed',False,repr(e))
finally:
 r['sample_count']=len(r['samples']);r['samples']=r['samples'][::max(1,len(r['samples'])//150)]
 (out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
raise SystemExit(int(any(c['status']=='FAIL' for c in r['checks'])))
