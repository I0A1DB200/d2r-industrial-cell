// Created through Debugger.evaluateOnCallFrame in module scope. Read-only:
// no assignment to simulator variables, calls to its functions or clock replacement.
() => ({
 mechanics:typeof pusherTravel==='undefined'?'v0':'contact-transfer',pitch:piece.rotation.x,
 running, paused, betweenCycles, stopAfterCycle, automaticMode, phase, elapsed,
 partIndex, okCount, nokCount, fault, faultLatched, numericFrozen, mode, visionResult,
 piece: piece.position.toArray(), pieceVisible: piece.visible,
 armZ: arm.position.z, gateX: gate.position.x,
 io: {...io},
 numeric: Object.fromEntries(Array.from(document.querySelectorAll('[data-numeric]'),
   e => [e.dataset.numeric, e.textContent])),
 types: processRegistry.map(r => [r[1], r[2]]),
 phases: phases.map(p => [p.id, p.t]), batch: [...workpieceBatch],
 camera: camera.position.toArray(), target: target.toArray(),
 render: {calls: renderer.info.render.calls, triangles: renderer.info.render.triangles,
   textures: renderer.info.memory.textures, geometries: renderer.info.memory.geometries},
 alarm: document.getElementById('alarm').textContent,
 topState: document.getElementById('topState').textContent
})
