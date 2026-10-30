"""Focused v1.2 visual configuration checks; unmodified HTTP HTML, read-only CDP."""
import hashlib,json,os,re,threading,time,functools,urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
from run_baseline import ROOT,CDN,SHA,QuietHandler
from protected_contract import protected_checks
from http.server import ThreadingHTTPServer

def main():
 out=ROOT/'test-results/visual-config';out.mkdir(parents=True,exist_ok=True)
 original=(ROOT/'tests/baseline/V0.html').read_text()
 target=ROOT/'D2R-3D-001_Prototipo_Funcional_v11.html';source=target.read_text()
 report={'checks':[],'errors':[],'states':{},'source_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
 def check(name,ok,detail=None):
  report['checks'].append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail});print(report['checks'][-1],flush=True)
 check('V0 original SHA256',hashlib.sha256((ROOT/'tests/baseline/V0.html').read_bytes()).hexdigest()==SHA)
 marker='// D2R-3D-001: deterministic';end='reset(true);const time='
 for c in protected_checks(source):check(c['name'],c['status']=='PASS')
 check('required UI remains',all(('id="'+id+'"') in source for id in ['machine-hmi','simbar','faultSelect','pane-watch','pane-alarms','hmiPause']))
 check('no new imports',re.findall(r'^import .+$',source,re.M)==re.findall(r'^import .+$',original,re.M))
 check('label helper and calls removed','function label(' not in source and 'label(' not in source)
 tail=source[source.index(end):].replace('syncFeederVisual();updateActuatorRods();','').replace('camera.updateProjectionMatrix();renderer.setPixelRatio(Math.min(devicePixelRatio,2));','camera.updateProjectionMatrix();')
 check('clock and camera loop preserved',tail==original[original.index(end):])
 module=urllib.request.urlopen(CDN).read()
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'),headless=True,args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
   page=browser.new_page(viewport={'width':800,'height':600},device_scale_factor=1)
   page.on('pageerror',lambda e:report['errors'].append(str(e)))
   page.route(CDN,lambda r:r.fulfill(body=module,content_type='application/javascript'))
   cdp=page.context.new_cdp_session(page);cdp.send('Debugger.enable')
   url=f'http://127.0.0.1:{server.server_port}/{target.name}'
   line=next(i for i,s in enumerate(source.splitlines()) if end in s)
   bp=cdp.send('Debugger.setBreakpointByUrl',{'url':url,'lineNumber':line});observer={}
   def capture(event):
    try:
     r=cdp.send('Debugger.evaluateOnCallFrame',{'callFrameId':event['callFrames'][0]['callFrameId'],'expression':(ROOT/'tests/visual-observer.js').read_text()})
     observer['id']=r['result']['objectId'];cdp.send('Debugger.removeBreakpoint',{'breakpointId':bp['breakpointId']})
    finally:cdp.send('Debugger.resume')
   cdp.on('Debugger.paused',capture);page.goto(url,wait_until='commit')
   deadline=time.monotonic()+60
   while 'id' not in observer and time.monotonic()<deadline:page.wait_for_timeout(100)
   def read():
    r=cdp.send('Runtime.callFunctionOn',{'objectId':observer['id'],'functionDeclaration':'function(){return this();}','returnByValue':True})
    return r['result']['value']
   page.wait_for_timeout(300);s=read();report['states']['ready']=s
   check('ACES exposure 1.12 and local environment',s['aces'] and s['exposure']==1.12 and s['environment'])
   check('one 2048 shadow light',s['shadowLights']==1 and s['shadowMap']==[2048,2048])
   check('cell caster vertices inside shadow camera',not s['shadowFrustumOutside'],s['shadowFrustumOutside'])
   check('bevel exterior dimensions',all(all(abs(b['hi'][i]-b['expected'][i]/2)<1e-5 and abs(b['lo'][i]+b['expected'][i]/2)<1e-5 for i in range(3)) for b in s['boxes']))
   check('bevels used on thick boxes',any(b['type']=='ExtrudeGeometry' for b in s['boxes']))
   check('32 cylinder segments',s['cylinderSegments']==[32])
   check('glass casts no shadows',s['glassCastShadows']==0)
   check('256 textures no bump',s['textures']==[{'width':256,'height':256}]*2 and s['bumpMaps']==0)
   check('no zone sprites and five views',s['sprites']==0 and s['viewButtons']==5)
   check('subtle grid',s['gridOpacity']==.16)
   for dpr in [3,1.25]:
    cdp.send('Emulation.setDeviceMetricsOverride',{'width':810 if dpr==3 else 820,'height':610,'deviceScaleFactor':dpr,'mobile':False})
    deadline=time.monotonic()+30
    while True:
     s=read()
     if (s['pixelRatio']==min(dpr,2) and s['size']==[810 if dpr==3 else 820,610]) or time.monotonic()>deadline:break
     page.wait_for_timeout(100)
    report['states'][f'resize_{dpr}']=s
    check(f'resize DPR {dpr} capped and recalculated',s['pixelRatio']==min(dpr,2) and s['size']==[810 if dpr==3 else 820,610])
   check('no JS errors during visual config/resize',not report['errors'],report['errors']);browser.close()
 except Exception as e:
  check('visual infrastructure completed',False,repr(e))
 finally:
  server.shutdown();server.server_close();(out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
 return int(any(c['status']=='FAIL' for c in report['checks']))
if __name__=='__main__':raise SystemExit(main())
