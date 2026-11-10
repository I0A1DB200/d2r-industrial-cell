"""Protect normal sequence and PLC data against the immutable V0 baseline.

Only F01/F02 injection-specific differences are normalized out of V0 before
comparison. The historical V0 test runner remains untouched.
"""
from browser_lab import ROOT


def _region(source, start, end):
    begin = source.index(start)
    return source[begin:source.index(end, begin)]


def _remove_once(source, text, label):
    if source.count(text) != 1:
        raise AssertionError(f"expected one historical {label} fragment")
    return source.replace(text, "", 1)


def _current_equivalent(name, historical):
    if name == "registry":
        historical = _remove_once(
            historical,
            ",['F01 · Vision timeout','Diag_VisionTimeout'],['F02 · Pusher feedback','Diag_PusherMismatch']",
            "diagnostic BOOL pair",
        )
    elif name == "typed registry":
        historical = _remove_once(
            historical,
            " ['Timeout visión','DB_VisionTimeout','TIME','ms']\n",
            "DB_VisionTimeout row",
        )
    elif name == "Watch conversions":
        historical = _remove_once(historical, ",DB_VisionTimeout:1500", "timeout Watch value")
    elif name == "I/O conditions":
        historical = _remove_once(
            historical,
            " if(faultLatched)return; // Retain fault evidence in PLC Watch until reset.\n",
            "snapshot early return",
        )
        extension_gate = "const extended= !faultLatched && ((pushing&&q>=.95)||(retracting&&q<.05));"
        if historical.count(extension_gate) != 1:
            raise AssertionError("expected one historical snapshot extension gate")
        historical = historical.replace(extension_gate, "const extended=(pushing&&q>=.95)||(retracting&&q<.05);", 1)
        historical = historical.replace("&&!faultLatched", "")
        historical = _remove_once(
            historical,
            ",Diag_VisionTimeout:false,Diag_PusherMismatch:false",
            "injection BOOL values",
        )
    elif name == "update timing/fault gates":
        historical = _remove_once(
            historical,
            " // Simulate missing vision handshake after trigger timeout; do not count the part.\n"
            " if(fault==='vision'&&phase===2&&elapsed>=phases[2].t){latchFault('F01 · Timeout de visión: InspectionDone no recibido. Comprobar trigger, alimentación y comunicación.');return}\n"
            " // Simulate failed extension confirmation without moving the pusher past its travel limit.\n"
            " if(fault==='pusher'&&mode==='OK'&&phase===5&&elapsed>=phases[5].t){latchFault('F02 · C02: falta DI_PusherExtended. Comprobar sensor, cableado, carrera y condiciones neumáticas.');return}\n",
            "injection branches",
        )
    return historical


def protected_checks(source):
    original = (ROOT / 'tests/baseline/V0.html').read_text()
    blocks = [
        ('batch', 'const workpieceBatch=', ';let partIndex'),
        ('phases', 'const phases=[', '];'),
        ('registry', 'const registry={', '// Valores tipados'),
        ('typed registry', 'const processRegistry=[', '];'),
        ('Watch conversions', 'function processValues(){', 'function publishNumerics'),
        ('I/O conditions', 'function refreshIO(){', 'function update'),
        ('update timing/fault gates', 'function update(dt){', ' let ph=phases[phase]'),
        ('counters and transitions', ' piece.visible=false;arm.position.z=0;partIndex++;', ' const q=ease(elapsed/ph.t'),
    ]
    checks = []
    for name, start, end in blocks:
        current = _region(source, start, end)
        baseline = _current_equivalent(name, _region(original, start, end))
        checks.append({'name': name + ' unchanged from V0 (injection removed)', 'status': 'PASS' if current == baseline else 'FAIL'})
    nok = "p.x=1.25+2.9*q;p.z=0;p.y=1.36-.55*Math.max(0,(q-.7)/.3);arm.position.z=0"
    checks.append({'name': 'NOK discharge trajectory unchanged', 'status': 'PASS' if nok in source and nok in original else 'FAIL'})
    removed = ['faultSelect', 'pane-faults', 'faultReset', 'F01', 'F02', 'Diag_VisionTimeout', 'Diag_PusherMismatch', 'DB_VisionTimeout', 'faultLatched', 'numericFrozen', 'latchFault']
    leftovers = [token for token in removed if token in source]
    checks.append({'name': 'F01/F02 injection controls and code removed', 'status': 'PASS' if not leftovers else 'FAIL', 'detail': leftovers})
    retained = ['id="pane-watch"', 'id="pane-alarms"', 'function alarm(msg,isFault=false)', "['Permiso de seguridad*','SafetyReady']"]
    checks.append({'name': 'Watch, alarms and Safety annunciation retained', 'status': 'PASS' if all(token in source for token in retained) else 'FAIL'})
    return checks
