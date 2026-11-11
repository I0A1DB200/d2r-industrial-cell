import json,hashlib,argparse
from pathlib import Path
from browser_lab import lab,ROOT
parser=argparse.ArgumentParser();parser.add_argument('--ui-only',action='store_true');args=parser.parse_args()
out=ROOT/('test-results/controls-final' if args.ui_only else 'test-results/controls');out.mkdir(parents=True,exist_ok=True)
r={'checks':[],'sizes':{},'errors':[],'source_sha256':hashlib.sha256((ROOT/'D2R-3D-001_Prototipo_Funcional_v11.html').read_bytes()).hexdigest()}
def check(name,ok,detail=None):
 r['checks'].append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail});print(r['checks'][-1],flush=True)
try:
 with lab(observer_file='tests/controls-observer.js') as (page,read,wait,errors):
  def click(id):page.locator('#'+id).click()
  for width,height in [(390,844),(960,600),(640,360)]:
   page.set_viewport_size({'width':width,'height':height})
   page.locator('[data-panel="watch"]').click();page.wait_for_timeout(200)
   if width==390:
    s=read();watch=page.evaluate('''() => ({di:document.querySelectorAll('#diRows tr').length,dq:document.querySelectorAll('#dqRows tr').length,logic:document.querySelectorAll('#logicRows tr').length,process:document.querySelectorAll('#numericRows tr').length,types:[...document.querySelectorAll('#numericRows tr')].map(r=>[r.querySelector('.type-cell').textContent,r.querySelector('.numeric-val').textContent])})''')
    check('PLC Watch normal BOOL registry',len(s['io'])==16 and all(type(value) is bool for value in s['io'].values()) and [watch['di'],watch['dq'],watch['logic']]==[7,4,5])
    counts={kind:sum(1 for _,t in s['types'] if t==kind) for kind in ['INT','DINT','REAL','TIME']}
    check('PLC Watch INT DINT REAL TIME types and values',counts=={'INT':2,'DINT':3,'REAL':3,'TIME':1} and watch['process']==9 and any(t=='TIME' and value.endswith(' ms') for t,value in watch['types']) and all('.' in value.split()[0] and len(value.split()[0].split('.')[-1])==2 for t,value in watch['types'] if t=='REAL'))
    page.locator('[data-filter="DI"]').click();filtered=page.evaluate("() => [getComputedStyle(document.getElementById('diRows').closest('table')).display,getComputedStyle(document.getElementById('numericRows').closest('table')).display]")
    check('PLC Watch filters remain operational',filtered[0]!='none' and filtered[1]=='none')
    page.locator('[data-filter="all"]').click();page.locator('#diRows tr[data-sensor="DI_InspectionPresent"]').click();s=read()
    check('3D sensor selection highlights row and focuses camera',s['selectedSensor']=='DI_InspectionPresent' and page.locator('#diRows tr.sensor-selected').get_attribute('data-sensor')==s['selectedSensor'] and all(abs(s['cameraTarget'][i]-s['sensorTarget'][i])<1e-6 for i in range(3)))
   click('reset');check(f'{width} SIM RESET leaves Watch open',page.locator('#panelTitle').inner_text()=='PLC Watch' and 'open' in page.locator('#sidepanel').get_attribute('class'))
   r['sizes'][f'{width}x{height}']=page.evaluate('''() => Object.fromEntries(['machine-hmi','simbar','sidepanel'].map(id=>{const b=document.getElementById(id).getBoundingClientRect();return [id,{x:b.x,y:b.y,w:b.width,h:b.height}]}))''')
   def overlap(a,b):return min(a['x']+a['w'],b['x']+b['w'])>max(a['x'],b['x']) and min(a['y']+a['h'],b['y']+b['h'])>max(a['y'],b['y'])
   boxes=r['sizes'][f'{width}x{height}'];check(f'{width}x{height} panel excludes HMI/SIM',not overlap(boxes['sidepanel'],boxes['machine-hmi']) and not overlap(boxes['sidepanel'],boxes['simbar']),boxes)
   click('hmiStart');s=read();check(f'{width} HMI START immediate',s['running'] and s['controls']['hmiReset']['disabled'] and s['controls']['pause']['disabled']==False)
   click('hmiPause');a=read();page.wait_for_timeout(250);b=read()
   check(f'{width} HMI pause freezes real clock',a['paused'] and a['elapsed']==b['elapsed'] and a['piece']==b['piece'])
   check(f'{width} paired pause metadata',all(b['controls'][id]['title']==b['controls'][id]['aria']=='Reanudar simulación' and b['controls'][id]['pressed']=='true' for id in ['pause','hmiPause']))
   page.screenshot(path=str(out/f'watch-{width}x{height}.png'))
   click('pause');check(f'{width} SIM resumes immediate',not read()['paused'])
   click('reset');check(f'{width} SIM RESET in motion',not read()['running'] and read()['partIndex']==0)
   check(f'{width} SIM RESET keeps Watch open',page.locator('#panelTitle').inner_text()=='PLC Watch' and 'open' in page.locator('#sidepanel').get_attribute('class'))
   click('hmiReset') # allowed only stopped; closes the current panel
   check(f'{width} HMI RESET closes Watch without opening diagnostics',not page.locator('#sidepanel').evaluate("e=>e.classList.contains('open')") and page.locator('[data-panel="faults"]').count()==0)
   check(f'{width} idle pause/reset metadata',read()['controls']['hmiPause']['disabled'] and not read()['controls']['hmiReset']['disabled'])
   page.locator('[data-panel="alarms"]').click();click('hmiStart');click('hmiPause');check(f'{width} alarms allow HMI actions',read()['paused']);click('reset')
   check(f'{width} SIM RESET leaves Alarmas open',page.locator('#panelTitle').inner_text()=='Alarmas' and 'open' in page.locator('#sidepanel').get_attribute('class'))
   click('panelClose')
  if not args.ui_only:
   page.set_viewport_size({'width':320,'height':240})
   click('auto');wait(lambda s:s['phase']==5 and s['elapsed']>.6,'pusher moving')
   s=read();r['moving']=s
   check('C02 rod attached and anchored inside fixed body',abs(s['rod'][0]-s['plateBack'])<1e-7 and abs(s['rod'][1]-1.35)<1e-7 and s['body']==[0,1.385,2.2])
   check('feed rod anchored inside body and attached',abs(s['feedRod'][0]-s['feedAnchor'])<1e-7 and abs(s['feedRod'][1]-s['feedTip'])<1e-7)
   s=wait(lambda s:s['betweenCycles']>0,'between cycles');r['between']=s;check('ENTRE PIEZAS, no phases[7] access',s['phase']==7 and s['hmi']=='ENTRE PIEZAS')
   click('hmiStop');s=read();check('HMI STOP requests end, not immediate',s['running'])
   wait(lambda s:not s['running'],'end piece');check('HMI STOP completed current next piece',read()['partIndex']==2)
   click('hmiReset');click('auto');wait(lambda s:s['phase']==1,'SIM run');click('stopAfter');check('SIM STOP not immediate',read()['running']);wait(lambda s:not s['running'],'SIM end');check('SIM STOP one piece',read()['partIndex']==1)
   page.set_viewport_size({'width':640,'height':480});click('reset');click('hmiAuto');check('HMI selects PIEZA mode',page.locator('#machine-hmi .ux-heading .short').inner_text()=='· PIEZA' and not read()['automaticMode'])
   click('hmiStart');wait(lambda s:not s['running'],'PIEZA first order');s=read();check('PIEZA executes exactly one piece per START',s['partIndex']==1 and s['okCount']==1 and s['nokCount']==0)
   page.wait_for_timeout(500);check('PIEZA waits for the next START',not read()['running'] and read()['partIndex']==1)
   click('hmiStart');wait(lambda s:not s['running'] and s['partIndex']==2,'PIEZA second order');s=read();check('second PIEZA START advances only one piece',s['partIndex']==2 and s['okCount']==1 and s['nokCount']==1)
  r['errors']=errors;check('no JS errors',not errors,errors)
except Exception as e:check('scenario completed',False,repr(e))
finally:(out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
raise SystemExit(int(any(c['status']=='FAIL' for c in r['checks'])))
