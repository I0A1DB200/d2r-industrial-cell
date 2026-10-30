// Read-only visual checks, evaluated in module scope through CDP.
() => {
 const meshes=[];scene.traverse(o=>{if(o.isMesh)meshes.push(o)});
 const bounds=[];
 for(const [key,g] of boxGeometries){
  const expected=key.split(':').map(Number);const a=g.attributes.position;
  const lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
  for(let i=0;i<a.count;i++){const v=[a.getX(i),a.getY(i),a.getZ(i)];for(let j=0;j<3;j++){lo[j]=Math.min(lo[j],v[j]);hi[j]=Math.max(hi[j],v[j]);}}
  bounds.push({key,type:g.type,expected,lo,hi});
 }
 const frustum=[];const cam=sun.shadow.camera;
 for(const o of meshes.filter(o=>o.castShadow)){
  const a=o.geometry.attributes.position;let outside=0;
  for(let i=0;i<a.count;i++){
   const p=new THREE.Vector3(a.getX(i),a.getY(i),a.getZ(i)).applyMatrix4(o.matrixWorld).applyMatrix4(cam.matrixWorldInverse);
   if(p.x<cam.left-.001||p.x>cam.right+.001||p.y<cam.bottom-.001||p.y>cam.top+.001||-p.z<cam.near||-p.z>cam.far)outside++;
  }
  if(outside)frustum.push({type:o.geometry.type,position:o.position.toArray(),outside});
 }
 return {
  aces:renderer.toneMapping===THREE.ACESFilmicToneMapping,exposure:renderer.toneMappingExposure,
  environment:!!scene.environment,environmentSize:scene.environment?.image?{width:scene.environment.image.width,height:scene.environment.image.height}:null,
  shadowLights:scene.children.filter(o=>o.isLight&&o.castShadow).length,
  shadowMap:sun.shadow.mapSize.toArray(),shadowFrustumOutside:frustum,
  boxes:bounds,cylinderSegments:[...new Set(meshes.filter(o=>o.geometry.type==='CylinderGeometry').map(o=>o.geometry.parameters.radialSegments))],
  glassCastShadows:meshes.filter(o=>o.material===glass&&o.castShadow).length,
  textures:[floorMaterial.map,belt.map].map(t=>({width:t.image.width,height:t.image.height})),
  bumpMaps:meshes.filter(o=>o.material.bumpMap).length,
  sprites:scene.children.filter(o=>o.isSprite).length,viewButtons:document.querySelectorAll('#viewbar [data-focus]').length,
  pixelRatio:renderer.getPixelRatio(),devicePixelRatio:window.devicePixelRatio,size:renderer.getSize(new THREE.Vector2()).toArray(),
  gridOpacity:grid.material.opacity,render:{...renderer.info.render},memory:{...renderer.info.memory}
 };
}
