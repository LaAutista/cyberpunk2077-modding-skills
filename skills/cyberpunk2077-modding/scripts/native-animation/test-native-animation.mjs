#!/usr/bin/env node
// Synthetic regression inputs contain no game data. Native integration needs owned assets.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {inspectCompressedKeys,auditCompressedKeys} from './audit-compressed-keys.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const work=fs.mkdtempSync(path.join(os.tmpdir(),'native-animation-selftest-'));
function run(script,args,ok=true){
  const p=spawnSync(process.execPath,[path.join(here,script),...args],{encoding:'utf8'});
  assert.equal(p.status===0,ok,p.stderr||p.stdout);
  return p;
}
function writeGlb(dest,j,bin){
  let json=Buffer.from(JSON.stringify(j));
  json=Buffer.concat([json,Buffer.alloc((4-json.length%4)%4,32)]);
  const b=Buffer.alloc(28+json.length+bin.length);
  b.writeUInt32LE(0x46546c67);b.writeUInt32LE(2,4);b.writeUInt32LE(b.length,8);
  b.writeUInt32LE(json.length,12);b.writeUInt32LE(0x4e4f534a,16);json.copy(b,20);
  b.writeUInt32LE(bin.length,20+json.length);b.writeUInt32LE(0x004e4942,24+json.length);bin.copy(b,28+json.length);
  fs.writeFileSync(dest,b);
}
try {
  const bin=Buffer.alloc(36);
  [0.33333334,1,0,0,0,1,0,0,0].forEach((v,i)=>bin.writeFloatLE(v,i*4));
  const j={asset:{version:'2.0'},buffers:[{byteLength:bin.length}],
    bufferViews:[{buffer:0,byteOffset:0,byteLength:4},{buffer:0,byteOffset:4,byteLength:4},{buffer:0,byteOffset:8,byteLength:16},{buffer:0,byteOffset:24,byteLength:12}],
    accessors:[{bufferView:0,componentType:5126,count:1,type:'SCALAR',min:[0.33333334],max:[0.33333334]},
      {bufferView:1,componentType:5126,count:1,type:'SCALAR',min:[1],max:[1]},
      {bufferView:2,componentType:5126,count:1,type:'VEC4'},
      {bufferView:3,componentType:5126,count:1,type:'VEC3'}],nodes:[{name:'bone'}],
    animations:[{name:'fixture',extras:{schema:{type:'wkit.cp2077.gltf.anims'},animationType:'Normal',rootMotionType:'None',
      optimizationHints:{preferSIMD:true},trackKeys:[{time:0.33333334,trackIndex:0,value:0.25}],constTrackKeys:[],animEvents:[]},
      channels:[{sampler:0,target:{node:0,path:'rotation'}},{sampler:1,target:{node:0,path:'translation'}}],
      samplers:[{input:0,output:2,interpolation:'STEP'},{input:1,output:3,interpolation:'LINEAR'}]}]};
  const source=path.join(work,'source.glb'),prepared=path.join(work,'prepared.glb');
  writeGlb(source,j,bin);
  run('check-animation.mjs',['prepare',source,prepared,'--preserve-key-sampling']);
  const result=fs.readFileSync(prepared),json=JSON.parse(result.subarray(20,20+result.readUInt32LE(12)));
  const stored=result.readFloatLE(28+result.readUInt32LE(12));
  assert.equal(json.accessors[0].min[0],stored);assert.equal(json.accessors[0].max[0],stored);
  assert.equal(Math.floor(stored*65535),Math.round(bin.readFloatLE(0)*65535));
  assert.equal(json.animations[0].samplers[0].interpolation,'STEP');
  assert.equal(json.animations[0].extras.optimizationHints.preferSIMD,false);
  run('check-animation.mjs',['prepare',source,prepared],false);
  // Many individually valid channels must not overflow JavaScript's argument stack.
  const dense=structuredClone(j),count=40000,tracks=5,denseBin=Buffer.alloc(count*(tracks*4+16));
  dense.nodes=Array.from({length:tracks},(_,i)=>({name:'dense'+i}));dense.bufferViews=[];dense.accessors=[];
  dense.animations[0].channels=[];dense.animations[0].samplers=[];
  for(let channel=0;channel<tracks;channel++){
    const offset=channel*count*4;
    for(let i=0;i<count;i++)denseBin.writeFloatLE(i/(count-1),offset+i*4);
    dense.bufferViews.push({buffer:0,byteOffset:offset,byteLength:count*4});
    dense.accessors.push({bufferView:channel,componentType:5126,count,type:'SCALAR',min:[0],max:[1]});
    dense.animations[0].channels.push({sampler:channel,target:{node:channel,path:'rotation'}});
    dense.animations[0].samplers.push({input:channel,output:tracks,interpolation:'LINEAR'});
  }
  for(let i=0;i<count;i++)denseBin.writeFloatLE(1,tracks*count*4+i*16+12);
  dense.bufferViews.push({buffer:0,byteOffset:tracks*count*4,byteLength:count*16});
  dense.accessors.push({bufferView:tracks,componentType:5126,count,type:'VEC4'});dense.buffers[0].byteLength=denseBin.length;
  const denseSource=path.join(work,'dense-source.glb'),denseOutput=path.join(work,'dense-prepared.glb');writeGlb(denseSource,dense,denseBin);
  const denseBefore=fs.readFileSync(denseSource);
  run('check-animation.mjs',['prepare',denseSource,denseOutput,'--preserve-key-sampling']);
  assert.deepEqual(fs.readFileSync(denseSource),denseBefore);
  const denseBytes=fs.readFileSync(denseOutput),denseJson=JSON.parse(denseBytes.subarray(20,20+denseBytes.readUInt32LE(12)));
  for(const accessor of denseJson.accessors.slice(0,tracks)){assert.equal(accessor.count,count);assert.deepEqual(accessor.min,[0]);assert.deepEqual(accessor.max,[1]);}
  // Null and the native null-handle are valid; missing or live extraction must fail closed.
  const motionAuthor=structuredClone(j);
  Object.assign(motionAuthor.animations[0].extras,{frameClamping:false,frameClampingStartFrame:0,frameClampingEndFrame:0});
  const motionReadback=structuredClone(motionAuthor);motionReadback.animations[0].extras.rootMotionType='Unknown';
  const motionSource=path.join(work,'motion-source.glb'),motionOutput=path.join(work,'motion-readback.glb'),motionJson=path.join(work,'motion.json');
  writeGlb(motionSource,motionAuthor,bin);writeGlb(motionOutput,motionReadback,bin);
  for(const [motionExtraction,ok] of [[null,true],[{HandleRefId:'-1'},true],[{HandleRefId:'2'},false],[undefined,false]]){
    const motion={Data:{RootChunk:{animationDataChunks:[],animations:[{Data:{animation:{Data:{name:{$value:'fixture'},animationType:'Normal',duration:1,
      frameClamping:false,frameClampingStartFrame:0,frameClampingEndFrame:0,motionExtraction,animBuffer:{Data:{$type:'animAnimationBufferSimd'}}}}}}]}}};
    fs.writeFileSync(motionJson,JSON.stringify(motion));
    run('check-animation.mjs',['verify-authored',motionJson,motionJson,motionSource,motionOutput],ok);
  }
  j.animations[0].extras.animationType='Unsupported';writeGlb(path.join(work,'unsupported.glb'),j,bin);
  run('check-animation.mjs',['prepare',path.join(work,'unsupported.glb'),path.join(work,'rejected.glb')],false);
  j.animations[0].extras.animationType='Normal';
  j.animations[0].channels.length=1;j.animations[0].samplers.length=1;
  const rig=path.join(work,'rig.json');fs.writeFileSync(rig,JSON.stringify({Data:{RootChunk:{boneNames:[{$value:'bone'}],boneTransforms:[{Rotation:{i:0,j:0,k:0,r:1}}]}}}));
  for(const constant of [false,true]){
    const name=constant?'step':'linear',native=path.join(work,name+'.json'),cli=path.join(work,name+'.glb'),out=path.join(work,name+'-readback.glb');
    j.animations[0].samplers[0].interpolation=constant?'STEP':'LINEAR';bin.writeFloatLE(1,0);
    writeGlb(cli,j,bin);
    const key=Buffer.alloc(16);key.writeUInt16LE(65535,constant?2:0);key.writeUInt16LE(0x2000,constant?0:2);key.writeFloatLE(1e-5,4);
    const doc={Data:{RootChunk:{animations:[{Data:{animation:{Data:{name:{$value:'fixture'},animationType:'Normal',duration:1,
      animBuffer:{Data:{$type:'animAnimationBufferCompressed',hasRawRotations:1,numAnimKeys:0,numAnimKeysRaw:constant?0:1,numConstAnimKeys:constant?1:0,
        dataAddress:{unkIndex:0,fsetInBytes:0,zeInBytes:16}}}}}}}],animationDataChunks:[{buffer:{Bytes:key.toString('base64')}}]}}};
    fs.writeFileSync(native,JSON.stringify(doc));
    const args=[native,rig,cli,out,'--required-clips','fixture'];
    run('readback-animation.mjs',args);
    const report=JSON.parse(fs.readFileSync(out+'.raw-readback.json'));
    assert.equal(report.corrections.length,1);assert.equal(report.clips[0].nativeRotationKeys,1);
    run('readback-animation.mjs',args,false);
    key.writeUInt16LE(0x2000,constant?2:0);key.writeUInt16LE(65535,constant?0:2);
    doc.Data.RootChunk.animationDataChunks[0].buffer.Bytes=key.toString('base64');fs.writeFileSync(native,JSON.stringify(doc));
    run('readback-animation.mjs',[native,rig,cli,path.join(work,name+'-bad.glb'),'--required-clips','fixture'],false);
  }
  // Multiple corrections must keep distinct offsets and preserve the original binary prefix.
  const multi=structuredClone(j),multiBin=Buffer.from(bin),keys=Buffer.alloc(32);
  multi.nodes=[{name:'bone'},{name:'second'}];
  multi.animations=['first','second'].map(name=>({name,extras:{animationType:'Normal'},
    channels:[{sampler:0,target:{node:0,path:'rotation'}},{sampler:1,target:{node:1,path:'rotation'}}],
    samplers:[{input:0,output:2,interpolation:'LINEAR'},{input:0,output:2,interpolation:'LINEAR'}]}));
  for(let bone=0;bone<2;bone++){
    keys.writeUInt16LE(65535,bone*16);keys.writeUInt16LE(0x2000|bone,bone*16+2);
    keys.writeFloatLE(1e-5,bone*16+4+bone*4);
  }
  fs.writeFileSync(rig,JSON.stringify({Data:{RootChunk:{boneNames:multi.nodes.map(n=>({$value:n.name})),
    boneTransforms:multi.nodes.map(()=>({Rotation:{i:0,j:0,k:0,r:1}}))}}}));
  const multiNative=path.join(work,'multi.json'),multiCli=path.join(work,'multi.glb'),multiOut=path.join(work,'multi-readback.glb');
  fs.writeFileSync(multiNative,JSON.stringify({Data:{RootChunk:{animations:multi.animations.map(a=>({Data:{animation:{Data:{
    name:{$value:a.name},animationType:'Normal',duration:1,animBuffer:{Data:{$type:'animAnimationBufferCompressed',
      numAnimKeys:0,numAnimKeysRaw:2,numConstAnimKeys:0,inplaceCompressedBuffer:{Bytes:keys.toString('base64')}}}}}}}))}}}));
  writeGlb(multiCli,multi,multiBin);
  run('readback-animation.mjs',[multiNative,rig,multiCli,multiOut,'--required-clips','first,second']);
  const multiBytes=fs.readFileSync(multiOut),multiJsonLength=multiBytes.readUInt32LE(12);
  const multiJson=JSON.parse(multiBytes.subarray(20,20+multiJsonLength)),multiOutputBin=multiBytes.subarray(28+multiJsonLength);
  assert.deepEqual(multiOutputBin.subarray(0,multiBin.length),multiBin);
  assert.equal(multiOutputBin.length,multiBin.length+4*16);
  assert.equal(multiJson.buffers[0].byteLength,multiOutputBin.length);
  const views=multiJson.animations.flatMap(a=>a.samplers.map(s=>multiJson.bufferViews[multiJson.accessors[s.output].bufferView]));
  assert.deepEqual(views.map(v=>v.byteOffset),[0,1,2,3].map(i=>multiBin.length+i*16));
  for(let i=0;i<views.length;i++){
    const actual=[0,1,2,3].map(k=>multiOutputBin.readFloatLE(views[i].byteOffset+k*4));
    const v=keys.readFloatLE((i%2)*16+4+(i%2)*4),s=Math.sqrt(2-v*v);
    const expected=i%2?[0,0,-v*s,1-v*v]:[v*s,0,0,1-v*v];
    actual.forEach((x,k)=>assert(Math.abs(x-Math.fround(expected[k]))<1e-9));
  }
  const multiReport=JSON.parse(fs.readFileSync(multiOut+'.raw-readback.json'));
  assert.equal(multiReport.corrections.length,4);assert.equal(multiReport.runtimeVerified,false);
  const unchanged=JSON.parse(fs.readFileSync(multiNative));
  for(let bone=0;bone<2;bone++)keys.fill(0,bone*16+4,bone*16+16);
  for(const a of unchanged.Data.RootChunk.animations)a.Data.animation.Data.animBuffer.Data.inplaceCompressedBuffer.Bytes=keys.toString('base64');
  fs.writeFileSync(multiNative,JSON.stringify(unchanged));
  const unchangedOut=path.join(work,'unchanged-readback.glb');
  run('readback-animation.mjs',[multiNative,rig,multiCli,unchangedOut,'--required-clips','first,second']);
  const unchangedBytes=fs.readFileSync(unchangedOut);
  assert.deepEqual(unchangedBytes.subarray(28+unchangedBytes.readUInt32LE(12)),multiBin);
  assert.equal(JSON.parse(fs.readFileSync(unchangedOut+'.raw-readback.json')).corrections.length,0);
  // The decoder used to sort rotations after reading, hiding a broken native
  // stream whose T/Q/S records had been regrouped by channel instead of time.
  function record(bone,tick,kind,{quantized=false,constant=false}={}){
    const bytes=Buffer.alloc(quantized?10:16);
    bytes.writeUInt16LE(bone|(kind<<13),constant?0:2);bytes.writeUInt16LE(tick,constant?2:0);
    return bytes;
  }
  const orderedKeys=[];
  for(const bone of [0,1])for(const tick of [0,65535])for(const kind of [0,1,2])orderedKeys.push({bone,tick,kind});
  function orderFixture(quantized=false,storage='external'){
    const dynamic=Buffer.concat(orderedKeys.map(k=>record(k.bone,k.tick,k.kind,{quantized})));
    // No evidence requires constant keys to follow the dynamic comparator.
    const constants=Buffer.concat([record(1,200,1,{constant:true}),record(0,100,1,{constant:true})]);
    const payload=Buffer.concat([dynamic,constants,Buffer.alloc(8)]);
    const buffer={$type:'animAnimationBufferCompressed',numAnimKeys:quantized?12:0,numAnimKeysRaw:quantized?0:12,numConstAnimKeys:2,numTrackKeys:1,numConstTrackKeys:0,numJoints:2};
    const root={animations:[{Data:{animation:{Data:{name:{$value:'ordered'},animBuffer:{Data:buffer}}}}}]};
    if(storage==='external'){
      root.animationDataChunks=[{buffer:{Bytes:Buffer.concat([Buffer.alloc(4),payload,Buffer.alloc(4)]).toString('base64')}}];
      buffer.dataAddress={unkIndex:0,fsetInBytes:4,zeInBytes:payload.length};
    }else buffer[storage]={Bytes:payload.toString('base64')};
    return {root,buffer,payload,dynamicLength:dynamic.length};
  }
  for(const quantized of [false,true])for(const storage of ['external','inplaceCompressedBuffer','defferedBuffer']){
    const fixture=orderFixture(quantized,storage),before=JSON.stringify(fixture.root);
    assert.deepEqual(inspectCompressedKeys(fixture.root,fixture.buffer).bytes,fixture.payload);
    assert.equal(auditCompressedKeys(fixture.root).clips.length,1);assert.equal(JSON.stringify(fixture.root),before);
    const bad=orderedKeys.toSorted((a,b)=>a.bone-b.bone||a.kind-b.kind||a.tick-b.tick);
    const badBytes=Buffer.concat([Buffer.concat(bad.map(k=>record(k.bone,k.tick,k.kind,{quantized}))),fixture.payload.subarray(fixture.dynamicLength)]);
    if(storage==='external')fixture.root.animationDataChunks[0].buffer.Bytes=Buffer.concat([Buffer.alloc(4),badBytes,Buffer.alloc(4)]).toString('base64');
    else fixture.buffer[storage].Bytes=badBytes.toString('base64');
    assert.throws(()=>inspectCompressedKeys(fixture.root,fixture.buffer),/noncanonical dynamic key order/);
  }
  for(const mutate of [
    f=>{f.buffer.dataAddress.fsetInBytes=-1;},
    f=>{f.buffer.dataAddress.unkIndex=1;},
    f=>{f.buffer.dataAddress.zeInBytes+=5;},
    f=>{f.buffer.numAnimKeysRaw=-1;},
    f=>{f.buffer.numAnimKeysRaw=0.5;},
    f=>{f.buffer.numAnimKeysRaw++;},
    f=>{f.buffer.numTrackKeys++;},
    f=>{f.buffer.numJoints=1;},
    f=>{const data=Buffer.from(f.root.animationDataChunks[0].buffer.Bytes,'base64');data.writeUInt16LE(0x6000,6);f.root.animationDataChunks[0].buffer.Bytes=data.toString('base64');}
  ]){const f=orderFixture();mutate(f);assert.throws(()=>inspectCompressedKeys(f.root,f.buffer));}
  const independent=orderFixture();
  const separate=Buffer.concat([record(1,65535,1,{quantized:true}),independent.payload]);
  independent.buffer.numAnimKeys=1;independent.buffer.inplaceCompressedBuffer={Bytes:separate.toString('base64')};
  assert.doesNotThrow(()=>inspectCompressedKeys(independent.root,independent.buffer),'Ordering restarts for each dynamic section');
  const auditPath=path.join(work,'order-audit.json');fs.writeFileSync(auditPath,JSON.stringify({Data:{RootChunk:independent.root}}));
  assert.equal(JSON.parse(run('audit-compressed-keys.mjs',[auditPath]).stdout).clips.length,1);
  run('audit-compressed-keys.mjs',[auditPath,'--required-clips','missing'],false);
  const unsupported=structuredClone(independent.root);unsupported.animations.push({Data:{animation:{Data:{name:{$value:'simd'},animBuffer:{Data:{$type:'animAnimationBufferSimd'}}}}}});
  assert.equal(auditCompressedKeys(unsupported).skippedClips[0].name,'simd');
  assert.throws(()=>auditCompressedKeys(unsupported,new Set(['simd'])),/unsupported native buffer/);
  // Exercise the production readback entry point: malformed ordering must fail
  // before a new GLB/report exists, even though the rotation values are unchanged.
  const orderBin=Buffer.alloc(40);orderBin.writeFloatLE(1,4);orderBin.writeFloatLE(1,20);orderBin.writeFloatLE(1,36);
  const orderGlb={asset:{version:'2.0'},buffers:[{byteLength:40}],
    bufferViews:[{buffer:0,byteOffset:0,byteLength:8},{buffer:0,byteOffset:8,byteLength:32}],
    accessors:[{bufferView:0,componentType:5126,count:2,type:'SCALAR',min:[0],max:[1]},{bufferView:1,componentType:5126,count:2,type:'VEC4'}],
    nodes:[{name:'bone'}],animations:[{name:'ordered',extras:{animationType:'Normal'},channels:[{sampler:0,target:{node:0,path:'rotation'}}],samplers:[{input:0,output:1,interpolation:'LINEAR'}]}]};
  const orderNative=path.join(work,'ordered-native.json'),orderCli=path.join(work,'ordered-cli.glb');writeGlb(orderCli,orderGlb,orderBin);
  const orderRecords=[record(0,0,0),record(0,0,1),record(0,65535,0),record(0,65535,1)];
  const orderBuffer={$type:'animAnimationBufferCompressed',numAnimKeys:0,numAnimKeysRaw:4,numConstAnimKeys:0,numJoints:2,inplaceCompressedBuffer:{Bytes:Buffer.concat(orderRecords).toString('base64')}};
  const orderAnimation={name:{$value:'ordered'},animationType:'Normal',duration:1,animBuffer:{Data:orderBuffer}};
  const orderDoc={Data:{RootChunk:{animations:[{Data:{animation:{Data:orderAnimation}}}]}}};
  fs.writeFileSync(orderNative,JSON.stringify(orderDoc));
  run('readback-animation.mjs',[orderNative,rig,orderCli,path.join(work,'ordered-ok.glb'),'--required-clips','ordered']);
  orderDoc.Data.RootChunk.animations[0].Data.animation.Data.animBuffer.Data.inplaceCompressedBuffer.Bytes=Buffer.concat([orderRecords[0],orderRecords[2],orderRecords[1],orderRecords[3]]).toString('base64');
  fs.writeFileSync(orderNative,JSON.stringify(orderDoc));
  const rejectedOut=path.join(work,'ordered-rejected.glb');
  assert.match(run('readback-animation.mjs',[orderNative,rig,orderCli,rejectedOut,'--required-clips','ordered'],false).stderr,/noncanonical dynamic key order/);
  assert(!fs.existsSync(rejectedOut)&&!fs.existsSync(rejectedOut+'.raw-readback.json'));
  console.log('PASS: native ticks/bounds, STEP retention, mode/header/overwrite and root-extraction refusals, tiny-quaternion readback, canonical raw/quantized order with channel-major negative controls, native slice/count/bone bounds and failure before GLB publication.');
} finally {console.log('Fixture evidence retained:',work);}
