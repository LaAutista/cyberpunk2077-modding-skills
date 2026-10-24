// Additional native-event/float-tail/codec-flag gate; independent of the GLB exporter.
import fs from'node:fs';import assert from'node:assert/strict';import{createHash}from'node:crypto';
import{canonical}from'./native-json-canonical.mjs';
const [oldPath,newPath,rigPath,authoredPath,originalPath]=process.argv.slice(2);
assert(originalPath,'Usage: ORIGINAL_NATIVE.json NEW_NATIVE.json RIG.json AUTHORED.glb ORIGINAL.glb');
const read=p=>JSON.parse(fs.readFileSync(p)),sha=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const report={schema:1,passed:false,runtimeVerified:false,inputFiles:{},clips:[],scope:'Selected Normal/raw compressed float tracks, scale flags, rig counts, original fallback rows, full preserved events or explicit empty events'};
const bind=p=>{report.inputFiles[p]=sha(p);return p};
function glb(p){const b=fs.readFileSync(bind(p));assert.equal(b.readUInt32LE(0),0x46546c67);return JSON.parse(b.subarray(20,20+b.readUInt32LE(12)))}
function eventList(e){const c=e.events;if(c===null||c===undefined)return[];assert.equal(c.$type,'animEventsContainer');assert.deepEqual(Object.keys(c).sort(),['$type','events']);return c.events;}
{
 const oldDoc=read(bind(oldPath)),newDoc=read(bind(newPath)),old=canonical(oldDoc).RootChunk,now=canonical(newDoc).RootChunk,raw=newDoc.Data.RootChunk,rig=read(bind(rigPath)).Data.RootChunk;
 const incoming=glb(authoredPath),original=glb(originalPath);
 for(const a of incoming.animations){
  const oldEntry=old.animations.find(e=>e.animation.name.$value===a.name),entry=now.animations.find(e=>e.animation.name.$value===a.name),r=raw.animations.find(e=>e.Data.animation.Data.name.$value===a.name).Data.animation.Data,b=r.animBuffer.Data;
  assert(oldEntry&&entry);assert.equal(r.animationType,'Normal');assert.equal(a.extras.rootMotionType,'None');assert.equal(b.$type,'animAnimationBufferCompressed');assert.equal(b.numAnimKeys,0);assert.equal(b.hasRawRotations,1);assert.equal(b.numJoints,rig.boneNames.length);assert.equal(b.numTracks,rig.referenceTracks.length);assert.equal(b.numExtraJoints,a.extras.numExtraJoints);assert.equal(b.numExtraTracks,a.extras.numExtraTracks);assert.equal(b.numFrames,Math.ceil(r.duration*30));
  assert.deepEqual(b.fallbackFrameIndices,oldEntry.animation.animBuffer.fallbackFrameIndices,a.name+': preserve alias fallback lookup');
  const empty=Array.isArray(a.extras.animEvents)&&a.extras.animEvents.length===0,prev=original.animations.find(x=>x.name===a.name);assert(prev);
  if(empty)assert.deepEqual(eventList(entry),[],a.name+': authored empty events');else{assert.deepEqual(eventList(entry),eventList(oldEntry),a.name+': full original native event payload');}
  const addr=b.dataAddress,bytes=Buffer.from(raw.animationDataChunks[addr.unkIndex].buffer.Bytes,'base64').subarray(addr.fsetInBytes,addr.fsetInBytes+addr.zeInBytes);assert.equal(bytes.length,(b.numAnimKeysRaw+b.numConstAnimKeys)*16+(b.numTrackKeys+b.numConstTrackKeys)*8);
  let allScalesUnit=true,scaleKeys=0;for(let i=0;i<b.numAnimKeysRaw+b.numConstAnimKeys;i++){const p=i*16,isConst=i>=b.numAnimKeysRaw,h=bytes.readUInt16LE(p+(isConst?0:2)),kind=(h&0x6000)>>13;assert((h&0x1fff)<b.numJoints);assert(kind<=2);if(kind===2){scaleKeys++;for(const o of[4,8,12])if(bytes.readFloatLE(p+o)!==1)allScalesUnit=false;}}
  if(scaleKeys===0){assert.equal(a.channels.filter(c=>c.target.path==='scale').length,0,a.name+': missing native scale keys require absent authored scale channels');assert.equal(prev.channels.filter(c=>c.target.path==='scale').length,0,a.name+': absent scale channels preserve original clip behavior');assert.deepEqual(incoming.nodes.map(n=>n.scale??[1,1,1]),original.nodes.map(n=>n.scale??[1,1,1]),a.name+': original rest scales preserved');}assert.equal(Boolean(b.isScaleConstant),allScalesUnit,a.name+': native scale flag versus actual keys');
  let offset=(b.numAnimKeysRaw+b.numConstAnimKeys)*16;for(const[k,count,isConst]of[['trackKeys',b.numTrackKeys,false],['constTrackKeys',b.numConstTrackKeys,true]]){const expected=a.extras[k]??[];assert.equal(count,expected.length,a.name+': float key count');for(let i=0;i<count;i++,offset+=8){const tick=bytes.readUInt16LE(offset+(isConst?2:0)),index=bytes.readUInt16LE(offset+(isConst?0:2)),value=bytes.readFloatLE(offset+4),e=expected[i];assert.equal(index,e.trackIndex);assert(index<b.numTracks);assert.equal(tick,Math.round(e.time/r.duration*65535),a.name+': stored float time');assert.equal(value,Math.fround(e.value),a.name+': exact stored float value');}}
  report.clips.push({name:a.name,nativeEvents:eventList(entry).length,originalEventsPreserved:!empty,trackKeys:b.numTrackKeys,constTrackKeys:b.numConstTrackKeys,scaleKeys,isScaleConstant:Boolean(b.isScaleConstant),numFrames:b.numFrames,numJoints:b.numJoints,numTracks:b.numTracks,fallbackRowsPreserved:true});
 }
}
report.passed=true;console.log(JSON.stringify(report,null,2));
