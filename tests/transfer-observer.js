() => {
 const corners=[];
 for(const x of [-.26,.26])for(const z of [-.19,.19]){
  const p=new THREE.Vector3(x,-.0675,z).applyEuler(piece.rotation).add(piece.position);corners.push(p.toArray());
 }
 const passage=machine.children.filter(o=>o.isMesh&&(o.material===glass||(o.material===aluminum&&Math.abs(o.position.y-1.31)<1e-8&&Math.abs(Math.abs(o.position.z)-.72)<1e-8))).map(o=>{const a=o.geometry.attributes.position;let lo=Infinity,hi=-Infinity;for(let i=0;i<a.count;i++){lo=Math.min(lo,a.getX(i)+o.position.x);hi=Math.max(hi,a.getX(i)+o.position.x)}return {glass:o.material===glass,lo,hi};});
 const caps=sort.children.filter(o=>o.isMesh&&o.geometry.type==='CylinderGeometry'&&o.geometry.parameters.radiusTop===.15).map(o=>o.position.toArray());
 return {passage,caps,running,paused,phase,elapsed,betweenCycles,partIndex,okCount,nokCount,mode,faultLatched,numericFrozen,
  visible:piece.visible,piece:piece.position.toArray(),pitch:piece.rotation.x,corners,
  armZ:arm.position.z,face:pl.position.z-.0375+arm.position.z,plateBottom:pl.position.y-.08,
  rod:[arm.position.z+rod.position.z-rod.scale.y/2,arm.position.z+rod.position.z+rod.scale.y/2],plateBack:arm.position.z+pl.position.z+.0375,
  body:barrel.position.toArray(),homeFace:pusherHomeFace,travel:pusherTravel,exitZ:pusherExitZ,startZ:pusherRampStart,slope:pusherSlope,
  rampTop:{y:r.position.y+.02*Math.cos(r.rotation.x),z:r.position.z+.02*Math.sin(r.rotation.x),pitch:r.rotation.x},
  io:{...io},numeric:Object.fromEntries(Array.from(document.querySelectorAll('[data-numeric]'),e=>[e.dataset.numeric,e.textContent])),
  upperCount:upperPieces.filter(o=>o.visible).length,hmi:document.getElementById('hmiState').textContent};
}
