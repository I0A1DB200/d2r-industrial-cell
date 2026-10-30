() => ({running,paused,phase,elapsed,betweenCycles,partIndex,okCount,nokCount,faultLatched,
 piece:piece.position.toArray(),armZ:arm.position.z,gateX:gate.position.x,
 hmi:document.getElementById('hmiState').textContent,
 body:barrel.position.toArray(),feedBody:feedBarrel.position.toArray(),
 feedRod:[feedRod.position.x-feedRod.scale.y/2,feedRod.position.x+feedRod.scale.y/2],
 rod:[arm.position.z+rod.position.z-rod.scale.y/2,arm.position.z+rod.position.z+rod.scale.y/2],
 plateBack:arm.position.z+pl.position.z+.0375,
 controls:Object.fromEntries(['auto','stopAfter','pause','reset','hmiStart','hmiStop','hmiPause','hmiReset','hmiAuto'].map(id=>{const b=document.getElementById(id);return [id,{disabled:b.disabled,text:b.textContent,title:b.title,aria:b.getAttribute('aria-label'),pressed:b.getAttribute('aria-pressed'),ariaDisabled:b.getAttribute('aria-disabled')}]}))})
