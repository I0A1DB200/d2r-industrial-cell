import json,hashlib,argparse,subprocess,sys
from pathlib import Path
from browser_lab import lab,ROOT
parser=argparse.ArgumentParser();parser.add_argument('--ui-only',action='store_true');args=parser.parse_args()
out=ROOT/('test-results/controls-final' if args.ui_only else 'test-results/controls');out.mkdir(parents=True,exist_ok=True)
r={'checks':[],'sizes':{},'errors':[],'source_sha256':hashlib.sha256((ROOT/'D2R-3D-001_Prototipo_Funcional_v11.html').read_bytes()).hexdigest()}
def check(name,ok,detail=None):
 r['checks'].append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail});print(r['checks'][-1],flush=True)
generated=subprocess.run([sys.executable,str(ROOT/'scripts/render_engineering_brief.py'),'--check'],capture_output=True,text=True)
check('Engineering brief HTML is generated from the Markdown source',generated.returncode==0,generated.stdout.strip() or generated.stderr.strip())
try:
 with lab(observer_file='tests/controls-observer.js') as (page,read,wait,errors):
  def click(id):page.locator('#'+id).click()
  for width,height in [(390,844),(960,600),(640,360)]:
   page.set_viewport_size({'width':width,'height':height})
   page.locator('[data-panel="watch"]').click();page.wait_for_timeout(200)
   if width==390:
    page.locator('[data-panel="docs"]').click();check('DOCUMENTOS opens project roadmap and first draft',page.locator('#panelTitle').inner_text()=='Documentación del proyecto' and page.locator('#pane-docs article').count()==8 and page.locator('#pane-docs').is_visible() and page.locator('#briefOpenLink').get_attribute('href')=='docs/engineering/00-BRIEF-CLIENTE.html' and page.locator('#briefOpenLink').get_attribute('target') is None)
    page.locator('#briefOpenLink').click();brief=page.frame_locator('#documentFrame');page.wait_for_function("document.getElementById('documentOverlay').hidden===false && document.getElementById('documentFrame').contentDocument?.querySelector('#es-brief-title')")
    embedded=page.locator('#documentFrame').get_attribute('src').endswith('00-BRIEF-CLIENTE.html?embedded=1') and page.locator('#documentOverlay').is_visible() and len(page.context.pages)==1
    embedded_header=brief.locator('.topbar').evaluate("e=>getComputedStyle(e).display")=='none' and brief.locator('#es-brief-title').is_visible() and brief.locator('#document-es h2').count()==8
    spanish_default=page.evaluate("document.getElementById('documentFrame').contentDocument.documentElement.lang==='es'") and page.locator('#docLangEs').get_attribute('aria-pressed')=='true'
    page.locator('#docLangEn').click();english_selected=page.evaluate("document.getElementById('documentFrame').contentDocument.documentElement.lang==='en'") and brief.locator('#en-brief-title').is_visible() and page.locator('#docLangEn').get_attribute('aria-pressed')=='true'
    page.locator('#docLangEs').click();spanish_restored=page.evaluate("document.getElementById('documentFrame').contentDocument.documentElement.lang==='es'") and brief.locator('#es-brief-title').is_visible()
    check('Internal document language selector switches ES and EN',spanish_default and english_selected and spanish_restored and page.locator('#docLangEn').get_attribute('aria-pressed')=='false')
    page.evaluate("const f=document.getElementById('documentFrame').contentWindow;f.print=()=>f.__pdfRequested=true")
    page.locator('#docPrint').click();print_called=page.evaluate("document.getElementById('documentFrame').contentWindow.__pdfRequested===true")
    pdfpage=page.context.new_page();pdfpage.goto(page.locator('#documentFrame').get_attribute('src').split('?')[0],wait_until='domcontentloaded')
    pdfpage.locator('[data-language-button="en"]').click();english_direct=pdfpage.locator('#en-brief-title').is_visible() and pdfpage.evaluate("document.documentElement.lang==='en'");pdfpage.emulate_media(media='print')
    print_layout=pdfpage.locator('.tools').evaluate("e=>getComputedStyle(e).display")=='none' and pdfpage.locator('#document-en .toc').evaluate("e=>getComputedStyle(e).display")=='none'
    pdfpage.emulate_media(media='screen');pdfpage.set_viewport_size({'width':390,'height':844})
    mobile_table=pdfpage.locator('#document-en .table-wrap').evaluate("e=>e.scrollWidth<=e.clientWidth+1 && [...e.querySelectorAll('tbody tr')].every(row=>getComputedStyle(row).display==='block')")
    pdfpage.set_viewport_size({'width':1280,'height':900});pdfpage.screenshot(path=str(out/'brief-html.png'),full_page=True)
    pdf_bytes=pdfpage.pdf(path=str(out/'brief-preview.pdf'),format='A4',print_background=True)
    check('Brief opens as an internal responsive tab and prints to PDF',embedded and embedded_header and english_direct and page.locator('#docBack').is_visible() and page.locator('#docPrint').is_enabled() and print_called and print_layout and mobile_table and pdf_bytes.startswith(b'%PDF-'))
    pdfpage.close();page.locator('#docBack').click();check('Brief tab returns to the same simulator state',page.locator('#documentOverlay').is_hidden() and page.locator('#pane-docs').is_visible() and read()['partIndex']==0 and len(page.context.pages)==1)
    page.locator('#briefOpenLink').click();page.frame_locator('#documentFrame').locator('#es-brief-title').click();page.keyboard.press('Escape');check('Escape closes the internal document tab from the reader',page.locator('#documentOverlay').is_hidden() and page.evaluate("document.activeElement===document.getElementById('briefOpenLink')"))
    click('navSimulator');check('SIMULADOR returns to machine without altering state',not page.locator('#sidepanel').evaluate("e=>e.classList.contains('open')") and read()['partIndex']==0)
    page.locator('[data-panel="watch"]').click()
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
   boxes=r['sizes'][f'{width}x{height}'];check(f'{width}x{height} panel excludes HMI/SIM',not overlap(boxes['sidepanel'],boxes['machine-hmi']) and not overlap(boxes['sidepanel'],boxes['simbar']),boxes);check(f'{width}x{height} HMI excludes navigation',not overlap(boxes['machine-hmi'],boxes['simbar']),boxes)
   click('hmiStart');s=read();check(f'{width} HMI START immediate',s['running'] and s['controls']['hmiReset']['disabled'] and s['controls']['hmiPause']['disabled']==False and s['hmiDetail']=='Liberación controlada')
   click('hmiPause');a=read();page.wait_for_timeout(250);b=read()
   check(f'{width} HMI pause freezes real clock',a['paused'] and a['elapsed']==b['elapsed'] and a['piece']==b['piece'])
   check(f'{width} pause metadata stays synchronized',b['controls']['hmiPause']['title']==b['controls']['hmiPause']['aria']=='Reanudar simulación' and b['controls']['hmiPause']['pressed']=='true')
   if width==390:page.screenshot(path=str(out/f'watch-{width}x{height}.png'))
   click('hmiPause');check(f'{width} HMI resumes immediate',not read()['paused'])
   click('reset');check(f'{width} SIM RESET in motion',not read()['running'] and read()['partIndex']==0)
   check(f'{width} SIM RESET keeps Watch open',page.locator('#panelTitle').inner_text()=='PLC Watch' and 'open' in page.locator('#sidepanel').get_attribute('class'))
   click('hmiReset') # allowed only stopped; closes the current panel
   check(f'{width} HMI RESET closes Watch without opening diagnostics',not page.locator('#sidepanel').evaluate("e=>e.classList.contains('open')") and page.locator('[data-panel="faults"]').count()==0)
   check(f'{width} idle pause/reset metadata',read()['controls']['hmiPause']['disabled'] and not read()['controls']['hmiReset']['disabled'])
   page.locator('[data-panel="watch"]').click();page.locator('[data-view="alarms"]').click();check(f'{width} Alarmas tab available within diagnosis',page.locator('#panelTitle').inner_text()=='Alarmas' and page.locator('#pane-alarms').is_visible());click('hmiStart');click('hmiPause');check(f'{width} alarms allow HMI actions',read()['paused']);click('reset')
   check(f'{width} SIM RESET leaves Alarmas open',page.locator('#panelTitle').inner_text()=='Alarmas' and 'open' in page.locator('#sidepanel').get_attribute('class'))
   click('panelClose')
  if not args.ui_only:
   page.set_viewport_size({'width':320,'height':240})
   click('hmiStart');wait(lambda s:s['phase']==5 and s['elapsed']>.6,'pusher moving')
   s=read();r['moving']=s
   check('C02 rod attached and anchored inside fixed body',abs(s['rod'][0]-s['plateBack'])<1e-7 and abs(s['rod'][1]-1.35)<1e-7 and s['body']==[0,1.385,2.2])
   check('feed rod anchored inside body and attached',abs(s['feedRod'][0]-s['feedAnchor'])<1e-7 and abs(s['feedRod'][1]-s['feedTip'])<1e-7)
   s=wait(lambda s:s['betweenCycles']>0,'between cycles');r['between']=s;check('ENTRE PIEZAS, no phases[7] access',s['phase']==7 and s['hmi']=='ENTRE PIEZAS')
   click('hmiStop');s=read();check('HMI STOP requests end, not immediate',s['running'])
   wait(lambda s:not s['running'],'end piece');check('HMI STOP completed current next piece',read()['partIndex']==2)
   click('hmiReset');click('hmiStart');wait(lambda s:s['phase']==1,'HMI run');click('hmiStop');check('HMI STOP not immediate',read()['running']);wait(lambda s:not s['running'],'HMI end');check('HMI STOP one piece',read()['partIndex']==1)
   page.set_viewport_size({'width':640,'height':480});click('reset');click('hmiAuto');check('HMI selects PIEZA mode',page.locator('#machine-hmi .ux-heading .short').inner_text()=='· PIEZA' and not read()['automaticMode'])
   click('hmiStart');wait(lambda s:not s['running'],'PIEZA first order');s=read();check('PIEZA executes exactly one piece per START',s['partIndex']==1 and s['okCount']==1 and s['nokCount']==0)
   page.wait_for_timeout(500);check('PIEZA waits for the next START',not read()['running'] and read()['partIndex']==1)
   click('hmiStart');wait(lambda s:not s['running'] and s['partIndex']==2,'PIEZA second order');s=read();check('second PIEZA START advances only one piece',s['partIndex']==2 and s['okCount']==1 and s['nokCount']==1)
  r['errors']=errors;check('no JS errors',not errors,errors)
except Exception as e:check('scenario completed',False,repr(e))
finally:(out/'results.json').write_text(json.dumps(r,indent=2)+'\n')
raise SystemExit(int(any(c['status']=='FAIL' for c in r['checks'])))
