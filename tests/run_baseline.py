"""Read-only CDP observer + real UI actions. Never rewrites served HTML or clock."""
import argparse, functools, hashlib, json, os, statistics, threading, time, urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright
from validate_observations import validate

ROOT=Path(__file__).resolve().parents[1]
SHA='fb09ee9b8ef9ee635ea138283f1faaaf2d75b0ad9025a05395d77715948a76b3'
CDN='https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js'
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args): pass

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--target',default='tests/baseline/V0.html',help='V0 by default; select current HTML explicitly')
 ap.add_argument('--output',default='test-results/baseline')
 ap.add_argument('--timeout',type=float,default=600,help='wall seconds per wait, software rendering can be slow')
 args=ap.parse_args()
 target=(ROOT/args.target).resolve();target.relative_to(ROOT)
 out=(ROOT/args.output).resolve();out.mkdir(parents=True,exist_ok=True)
 if hashlib.sha256((ROOT/'tests/baseline/V0.html').read_bytes()).hexdigest()!=SHA:
  raise RuntimeError('V0 changed: restore the immutable original; do not update its expected hash')
 source=target.read_text();line=next(i for i,s in enumerate(source.splitlines()) if 'reset(true);const time=' in s)
 module=urllib.request.urlopen(CDN).read()
 report={'target':str(target.relative_to(ROOT)),'target_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
  'v0_sha256':SHA,'three_sha256':hashlib.sha256(module).hexdigest(),'checks':[], 'errors':[],
  'error_count':0,'states':{},'samples':[], 'environment':{}}
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 def check(name,ok,detail=None):
  report['checks'].append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
  print(('PASS ' if ok else 'FAIL ')+name,flush=True)
 try:
  with sync_playwright() as pw:
   executable=os.environ.get('CHROMIUM_PATH')
   browser=pw.chromium.launch(**({'executable_path':executable} if executable else {}),headless=True,
    args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
   report['environment']={'chromium':browser.version,'rendering':'headless SwiftShader; not user GPU',
    'viewport':[960,640],'deviceScaleFactor':1}
   page=browser.new_page(viewport={'width':960,'height':640},device_scale_factor=1)
   def error(e):
    report['error_count']+=1
    if len(report['errors'])<12: report['errors'].append({'message':str(e),'stack':e.stack,'last_sample':report['samples'][-1] if report['samples'] else None})
   page.on('pageerror',error)
   page.route(CDN,lambda r:r.fulfill(body=module,content_type='application/javascript'))
   cdp=page.context.new_cdp_session(page);cdp.send('Debugger.enable')
   url=f'http://127.0.0.1:{server.server_port}/{target.relative_to(ROOT).as_posix()}'
   bp=cdp.send('Debugger.setBreakpointByUrl',{'url':url,'lineNumber':line})
   observer={}
   def capture(event):
    try:
     result=cdp.send('Debugger.evaluateOnCallFrame',{'callFrameId':event['callFrames'][0]['callFrameId'],
      'expression':(ROOT/'tests/observer.js').read_text(),'returnByValue':False})
     observer['id']=result['result']['objectId']
     cdp.send('Debugger.removeBreakpoint',{'breakpointId':bp['breakpointId']})
    finally: cdp.send('Debugger.resume')
   cdp.on('Debugger.paused',capture)
   page.goto(url,wait_until='commit')
   limit=time.monotonic()+30
   while 'id' not in observer and time.monotonic()<limit: page.wait_for_timeout(50)
   assert 'id' in observer,'CDP could not attach read-only observer'
   def read():
    result=cdp.send('Runtime.callFunctionOn',{'objectId':observer['id'],'functionDeclaration':'function(){return this();}', 'returnByValue':True})
    if 'exceptionDetails' in result: raise RuntimeError(result['exceptionDetails'])
    return result['result']['value']
   def sample():
    s=read()
    report['samples'].append({k:s[k] for k in ['phase','elapsed','partIndex','betweenCycles','running','paused','mode','piece','armZ','gateX']})
    return s
   def wait(predicate,label):
    deadline=time.monotonic()+args.timeout
    while time.monotonic()<deadline:
     s=sample()
     if predicate(s): return s
     page.wait_for_timeout(100)
    raise TimeoutError(label)
   def click(id): page.locator('#'+id).click(timeout=10000)
   def fault_select(value):
    page.locator('[data-panel="faults"]').click();page.locator('#faultSelect').select_option(value)
    click('panelClose')
   def reset(): click('reset');wait(lambda s:not s['running'] and s['partIndex']==0,'SIM reset')
   # Independent rAF observer, no changes to animate, update, THREE.Clock or dt.
   page.evaluate('''() => {window.__d2rFrames=[];let last;
    function observe(t){if(last!==undefined && window.__d2rFrames.length<20000)window.__d2rFrames.push(t-last);last=t;requestAnimationFrame(observe)}
    requestAnimationFrame(observe);}''')
   check('boot',page.locator('body > canvas').count()==1)
   initial=read();report['states']['ready']=initial
   check('BOOL registry',len(initial['io'])==18 and all(type(v)==bool for v in initial['io'].values()))
   check('numeric types',set(t[1] for t in initial['types'])=={'INT','DINT','REAL','TIME'} and len(initial['numeric'])==10)
   for view in ['all','feed','inspect','sort','cab']:
    page.locator(f'[data-focus="{view}"]').click();page.wait_for_timeout(200)
    s=read();report['states']['view_'+view]={'camera':s['camera'],'target':s['target']}
    page.screenshot(path=str(out/f'view-{view}.png'))
   check('five view targets',len({tuple(report['states']['view_'+v]['target']) for v in ['all','feed','inspect','sort','cab']})==5)
   page.locator('[data-focus="all"]').click()
   # AUTO: real clock, sample actual routes and every phase.
   click('auto');routes={};phases_seen=set();captured=set()
   deadline=time.monotonic()+args.timeout
   last_progress=None
   while time.monotonic()<deadline:
    s=sample();phases_seen.add(s['phase'])
    progress=(s['partIndex'],s['phase'])
    if progress!=last_progress:
     print(f'AUTO piece={s["partIndex"]+1} phase={s["phase"]} elapsed={s["elapsed"]:.2f}',flush=True);last_progress=progress
    if s['phase'] in [2,5] and s['phase'] not in captured:
     report['states']['phase_'+str(s['phase'])]=s;page.screenshot(path=str(out/f'phase-{s["phase"]}.png'));captured.add(s['phase'])
    if s['phase']==6 and s['running']:
     routes[str(s['partIndex']+1)]={'mode':s['mode'],'piece':s['piece'],'exitA':s['io']['DI_ExitA'],'exitB':s['io']['DI_ExitB']}
    if not s['running'] and s['partIndex']==7:break
    page.wait_for_timeout(100)
   report['states']['auto_complete']=s;report['routes']=routes
   check('AUTO seven / four OK / three NOK',s['partIndex']==7 and s['okCount']==4 and s['nokCount']==3 and not s['running'])
   check('routes A/B for all seven',len(routes)==7 and all((v['exitA'] and not v['exitB'] and abs(v['piece'][2]+2.25)<.001) if v['mode']=='OK' else (v['exitB'] and not v['exitA'] and abs(v['piece'][0]-4.15)<.001) for v in routes.values()),routes)
   check('all seven phases sampled',set(range(7)).issubset(phases_seen))
   bad=[s for s in report['samples'] if s['betweenCycles']>0 and s['phase']==7]
   report['interval_phase7_samples']=bad[:3]
   check('no JavaScript errors in AUTO',report['error_count']==0,{'errors':report['error_count']})
   page.screenshot(path=str(out/'auto-complete.png'))
   reset();check('SIM RESET clears batch',read()['okCount']==0 and read()['nokCount']==0)
   click('hmiAuto');click('hmiStart');wait(lambda s:not s['running'] and s['partIndex']==1,'PIEZA')
   check('HMI PIEZA',read()['okCount']==1 and not read()['automaticMode'])
   click('hmiReset');check('HMI RESET',read()['partIndex']==0)
   click('hmiAuto');click('hmiStart');wait(lambda s:s['phase']==1,'transport')
   click('pause');a=read();page.wait_for_timeout(400);b=read()
   check('SIM pause freezes positions/time',a['paused'] and (a['elapsed'],a['piece'],a['armZ'])==(b['elapsed'],b['piece'],b['armZ']))
   click('pause');wait(lambda s:s['elapsed']!=b['elapsed'],'resume');check('SIM resume',not read()['paused'])
   click('hmiStop');wait(lambda s:not s['running'],'HMI STOP')
   check('HMI START/STOP finishes piece',read()['partIndex']==1)
   reset();click('auto');wait(lambda s:s['phase']==1,'SIM START');click('stopAfter');wait(lambda s:not s['running'],'SIM STOP')
   check('SIM START/STOP finishes piece',read()['partIndex']==1)
   reset();click('auto');wait(lambda s:s['running'],'active');reset();check('SIM RESET during run',not read()['running'] and read()['partIndex']==0)
   for kind,diag in [('vision','Diag_VisionTimeout'),('pusher','Diag_PusherMismatch')]:
    fault_select(kind);click('hmiStart');s=wait(lambda s:s['faultLatched'],kind)
    report['states']['fault_'+kind]=s;page.screenshot(path=str(out/f'fault-{kind}.png'))
    check(kind+' alarm/snapshot',s['io'][diag] and s['numericFrozen'] and s['partIndex']==0 and ('F01' if kind=='vision' else 'F02') in s['alarm'])
    page.wait_for_timeout(300);b=read();check(kind+' frozen BOOL and numerics',s['io']==b['io'] and s['numeric']==b['numeric'])
    page.locator('[data-panel="faults"]').click();click('faultReset');page.locator('#faultSelect').select_option('none');click('panelClose')
    check(kind+' rearm',not read()['faultLatched'] and not read()['numericFrozen'])
    click('hmiAuto');click('hmiStart');wait(lambda s:not s['running'] and s['partIndex']==1,'recovery piece')
    check(kind+' recovery completes piece',read()['okCount']==1)
    reset();click('hmiAuto')
   frames=page.evaluate('window.__d2rFrames')
   if frames:
    ordered=sorted(frames);report['performance']={'samples':len(frames),'fps_from_mean_interval':1000/statistics.mean(frames),'frame_ms_mean':statistics.mean(frames),'frame_ms_p50':statistics.median(frames),'frame_ms_p95':ordered[int((len(ordered)-1)*.95)],'frame_ms_max':max(frames),'renderer_info':read()['render'],'scope':'whole run incl UI, screenshots, pause, CDP; SwiftShader; not GPU benchmark'}
   check('no JavaScript errors overall',report['error_count']==0,{'errors':report['error_count']})
   browser.close()
 except Exception as exc:
  report['checks'].append({'name':'infrastructure / scenario completion','status':'FAIL','detail':repr(exc)})
  print(repr(exc),flush=True)
 finally:
  server.shutdown();server.server_close()
  
  if 'ready' in report['states']:
   for result in validate(report):print(result['status']+' '+result['name'],flush=True)
  report['samples_count']=len(report['samples']);report['samples']=report['samples'][::max(1,len(report['samples'])//150)]
  (out/'results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 return 1 if any(c['status']=='FAIL' for c in report['checks']) else 0
if __name__=='__main__': raise SystemExit(main())
