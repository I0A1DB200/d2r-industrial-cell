"""Protect unchanged functional regions while allowing authorized graphic/UI work."""
from browser_lab import ROOT

def protected_checks(source):
 original=(ROOT/'tests/baseline/V0.html').read_text()
 blocks=[('batch',"const workpieceBatch=",';let partIndex'),('phases','const phases=[','];'),
 ('registry','const registry={','// Valores tipados'),
 ('typed registry','const processRegistry=[','];'),
 ('Watch conversions','function processValues(){','function publishNumerics'),
 ('fault snapshots','function latchFault(','function refreshIO'),
 ('I/O conditions','function refreshIO(){','function update'),
 ('update timing/fault gates','function update(dt){',' let ph=phases[phase]'),
 ('counters and transitions',' piece.visible=false;arm.position.z=0;partIndex++;',' const q=ease(elapsed/ph.t)')]
 checks=[]
 for name,start,end in blocks:
  def region(s):a=s.index(start);return s[a:s.index(end,a)]
  checks.append({'name':name+' unchanged','status':'PASS' if region(source)==region(original) else 'FAIL'})
 nok="p.x=1.25+2.9*q;p.z=0;p.y=1.36-.55*Math.max(0,(q-.7)/.3);arm.position.z=0"
 checks.append({'name':'NOK discharge trajectory unchanged','status':'PASS' if nok in source and nok in original else 'FAIL'})
 return checks
