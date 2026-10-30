() => ({running,paused,phase,elapsed,betweenCycles,partIndex,okCount,nokCount,active:piece.visible,
 piece:piece.position.toArray(),pitch:piece.rotation.x,gateX:gate.position.x,
 uppers:upperPieces.filter(o=>o.visible).map(o=>o.position.toArray()),
 feedX:feed.position.x,carriageX:feedCarriage.position.x,
 rod:[feedRod.position.x-feedRod.scale.y/2,feedRod.position.x+feedRod.scale.y/2],
 barrel:feedBarrel.position.toArray(),io:{...io},hmi:document.getElementById('hmiState').textContent})
