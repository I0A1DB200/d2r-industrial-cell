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
   click('hmiReset') # allowed only stopped; also closes Watch
   check(f'{width} idle pause/reset metadata',read()['controls']['hmiPause']['disabled'] and not read()['controls']['hmiReset']['disabled'])
   page.locator('[data-panel="alarms"]').click();click('hmiStart');click('hmiPause');check(f'{width} alarms allow HMI actions',read()['paused']);click('reset');click('panelClose')
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
  r['errors']=errors;check('no JS errors',not errors,errors)
except Exception as e:check('scenario completed',False,repr(e))
finally:(out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
raise SystemExit(int(any(c['status']=='FAIL' for c in r['checks'])))
