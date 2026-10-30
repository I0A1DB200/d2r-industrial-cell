import json, threading, functools, tempfile, urllib.request, shutil
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright, expect
root=Path(__file__).resolve().parents[2]
scratch=Path(tempfile.mkdtemp(prefix='d2r-audit-'))
try:
 urllib.request.urlretrieve('https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js',scratch/'three.module.js')
except Exception:
 shutil.rmtree(scratch);raise
html=root/'D2R-3D-001_Prototipo_Funcional_v11.html'
server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/{html.name}'
results={}
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 page=browser.new_page(viewport={'width':1440,'height':900})
 errors=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.route('https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js',lambda r:r.fulfill(path=str(scratch/'three.module.js'),content_type='application/javascript'))
 page.goto(url);page.wait_for_selector('canvas');page.wait_for_timeout(1000)
 results['unmodified_boot']={'errors':errors.copy(),'canvas':page.locator('body > canvas').count(),'watch_rows':page.locator('[data-io]').count(),'numeric_rows':page.locator('[data-numeric]').count()}
 assert not errors
 page.locator('#hmiStart').click();page.wait_for_timeout(250)
 page.locator('#pause').click();expect(page.locator('#topState')).to_have_text('● PAUSED',timeout=15000)
 page.locator('#pause').click();expect(page.locator('#topState')).to_have_text('● RUN',timeout=15000)
 page.locator('#reset').click();expect(page.locator('#totalNum')).to_have_text('0/7',timeout=15000)
 for name in ['feed','inspect','sort','cab','all']:page.locator(f'[data-focus="{name}"]').click()
 page.locator('[data-panel="watch"]').click();assert page.locator('#sidepanel').is_visible()
 page.screenshot(path=str(scratch/'baseline.png'))
 results['unmodified_ui_smoke']='PASS: START, pausa/reanudación, SIM RESET, 5 vistas y panel Watch'
 # Instrument only the HTTP response: original file remains byte-identical.
 page.close();page=browser.new_page(viewport={'width':1440,'height':900})
 page.route('https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js',lambda r:r.fulfill(path=str(scratch/'three.module.js'),content_type='application/javascript'))
 source=html.read_text().replace('reset(true);const time=', '''window.qa={reset,runAutomatic,update,refreshUX,processValues,io,phases,workpieceBatch,scene,renderer,
 state:()=>({running,paused,betweenCycles,stopAfterCycle,phase,elapsed,partIndex,okCount,nokCount,faultLatched,numericFrozen,visionResult,automaticMode,piece:piece.position.toArray(),arm:arm.position.z}),
 tick:(n)=>{for(let i=0;i<n;i++)update(.02);refreshUX();}};
reset(true);const time=''')
 page.route(url,lambda r:r.fulfill(body=source,content_type='text/html'))
 page.add_init_script('window.requestAnimationFrame=()=>0')
 page.goto(url);page.wait_for_function('!!window.qa')
 def ev(s):return page.evaluate(s)
 ev('qa.runAutomatic();qa.tick(4000)')
 s=ev('qa.state()');assert (s['okCount'],s['nokCount'],s['partIndex'],s['running'])==(4,3,7,False)
 results['auto_batch']=s
 ev('qa.reset();document.getElementById("hmiAuto").click();qa.runAutomatic();qa.tick(700)')
 s=ev('qa.state()');assert s['partIndex']==1 and not s['running'];results['single_piece']=s
 ev('qa.reset();document.getElementById("hmiAuto").click();qa.runAutomatic();qa.tick(100);document.getElementById("hmiStop").click();qa.tick(700)')
 s=ev('qa.state()');assert s['partIndex']==1 and not s['running'];results['stop_after_piece']=s
 ev('qa.reset();qa.runAutomatic();qa.tick(100);document.getElementById("pause").click()')
 before=ev('qa.state()');ev('qa.tick(100)');after=ev('qa.state()');assert before==after
 ev('document.getElementById("pause").click();qa.tick(20)');assert ev('qa.state().elapsed')!=before['elapsed'];results['pause_freezes_state']='PASS'
 for kind,diag in [('vision','Diag_VisionTimeout'),('pusher','Diag_PusherMismatch')]:
  ev(f'qa.reset();document.getElementById("faultSelect").value="{kind}";qa.runAutomatic();qa.tick(700)')
  s=ev('qa.state()');assert s['faultLatched'] and s['numericFrozen'] and s['partIndex']==0 and ev(f'qa.io.{diag}')
  snapshot=ev('({io:{...qa.io},values:Array.from(document.querySelectorAll("[data-numeric]")).map(e=>e.textContent)})')
  ev('qa.tick(100);qa.runAutomatic()');assert snapshot==ev('({io:{...qa.io},values:Array.from(document.querySelectorAll("[data-numeric]")).map(e=>e.textContent)})')
  results[kind]={'state':s,'snapshot':snapshot}
  ev('document.getElementById("faultReset").click()');assert not ev('qa.state().faultLatched')
  ev('document.getElementById("faultSelect").value="none";qa.runAutomatic();qa.tick(4000)');assert ev('qa.state().partIndex')==7
 results['recovery']='PASS for F01 and F02 after rearm and selecting none'
 results['render_info']=ev('({calls:qa.renderer.info.render.calls,triangles:qa.renderer.info.render.triangles,geometries:qa.renderer.info.memory.geometries,textures:qa.renderer.info.memory.textures,objects:qa.scene.children.length})')
 print(json.dumps(results,indent=2));browser.close()
server.shutdown()
shutil.rmtree(scratch)
