"""Shared real-clock HTTP/CDP fixture. Never changes HTML, functions or clocks."""
import functools,json,os,threading,time,urllib.request
from contextlib import contextmanager
from http.server import ThreadingHTTPServer
from playwright.sync_api import sync_playwright
from run_baseline import ROOT,CDN,QuietHandler

@contextmanager
def lab(width=320,height=240,observer_file='tests/observer.js'):
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=str(ROOT)))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 module=urllib.request.urlopen(CDN).read();source=(ROOT/'D2R-3D-001_Prototipo_Funcional_v11.html').read_text()
 try:
  with sync_playwright() as pw:
   browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH'),headless=True,args=['--use-angle=swiftshader','--enable-unsafe-swiftshader'])
   page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
   errors=[];page.on('pageerror',lambda e:errors.append({'message':str(e),'stack':e.stack}))
   page.route(CDN,lambda r:r.fulfill(body=module,content_type='application/javascript'))
   cdp=page.context.new_cdp_session(page);cdp.send('Debugger.enable')
   url=f'http://127.0.0.1:{server.server_port}/D2R-3D-001_Prototipo_Funcional_v11.html'
   line=next(i for i,s in enumerate(source.splitlines()) if 'reset(true);const time=' in s)
   bp=cdp.send('Debugger.setBreakpointByUrl',{'url':url,'lineNumber':line});observer={}
   def capture(e):
    try:
     r=cdp.send('Debugger.evaluateOnCallFrame',{'callFrameId':e['callFrames'][0]['callFrameId'],'expression':(ROOT/observer_file).read_text()})
     observer['id']=r['result']['objectId'];cdp.send('Debugger.removeBreakpoint',{'breakpointId':bp['breakpointId']})
    finally:cdp.send('Debugger.resume')
   cdp.on('Debugger.paused',capture);page.goto(url,wait_until='commit')
   deadline=time.monotonic()+90
   while 'id' not in observer and time.monotonic()<deadline:page.wait_for_timeout(100)
   if 'id' not in observer:raise RuntimeError('CDP scope not captured')
   def read():
    r=cdp.send('Runtime.callFunctionOn',{'objectId':observer['id'],'functionDeclaration':'function(){return this();}','returnByValue':True})
    if 'exceptionDetails' in r:raise RuntimeError(r['exceptionDetails'])
    return r['result']['value']
   def wait(predicate,label,timeout=1200):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
     s=read()
     if predicate(s):return s
     page.wait_for_timeout(80)
    raise TimeoutError(label)
   yield page,read,wait,errors
   browser.close()
 finally:server.shutdown();server.server_close()
