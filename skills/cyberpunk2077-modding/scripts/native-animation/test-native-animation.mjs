#!/usr/bin/env node
// Synthetic regression inputs contain no game data. Native integration needs owned assets.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
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
  j.animations[0].extras.animationType='Additive';writeGlb(path.join(work,'unsupported.glb'),j,bin);
  run('check-animation.mjs',['prepare',path.join(work,'unsupported.glb'),path.join(work,'rejected.glb')],false);
  j.animations[0].extras.animationType='Normal';
  j.animations[0].channels.length=1;j.animations[0].samplers.length=1;
  const rig=path.join(work,'rig.json');fs.writeFileSync(rig,JSON.stringify({Data:{RootChunk:{boneNames:[{$value:'bone'}]}}}));
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
  console.log('PASS: nearest native ticks, float32 accessor bounds, STEP retention, unsupported mode refusal, independent LINEAR/STEP tiny-quaternion decoding, reversed-header rejection, and overwrite refusal.');
} finally {fs.rmSync(work,{recursive:true,force:true});}
