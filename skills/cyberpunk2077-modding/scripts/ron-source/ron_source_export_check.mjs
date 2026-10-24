// Fresh-export checks for the pinned RoN HK416 reload pair and full body skeleton.
// Historical failed-export fixtures are deliberately not required.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
assert(process.argv.length >= 3, 'Usage: node ron_source_export_check.mjs EXPORT_DIRECTORY [DEPENDENCY_DUMP_DIRECTORY ...]');
const root = path.resolve(process.argv[2]);
class Reader {
  constructor(b) { this.b=b; this.p=0; }
  take(n) { assert(n>=0 && this.p+n<=this.b.length,'truncated UEFormat'); const r=this.b.subarray(this.p,this.p+n);this.p+=n;return r; }
  i() { return this.take(4).readInt32LE(); }
  f() { const f=this.take(4).readFloatLE(); assert(Number.isFinite(f));return f; }
  s() { return this.take(this.i()).toString('utf8'); }
  u8() { return this.take(1)[0]; }
  end() { assert.equal(this.p,this.b.length,'unconsumed UEFormat bytes'); }
}
function attrs(r) { const out=new Map();const n=r.i();assert(n>=0);for(let i=0;i<n;i++){const name=r.s();assert(!out.has(name));out.set(name,r.take(r.i()));}return out; }
function read(rel) {
  const r=new Reader(fs.readFileSync(path.join(root,rel)));
  assert.equal(r.take(8).toString(),'UEFORMAT');const kind=r.s(),version=r.u8(),name=r.s(),objectPath=r.s();
  assert.equal(r.u8(),0,'this check expects uncompressed export');const data=attrs(r);r.end();return {kind,version,name,objectPath,data};
}
const base='assets/ReadyOrNot/Content/ReadyOrNot/';
function animation(rel,expectedTracks,{fixture=false}={}) {
  const asset=read(rel);assert.equal(asset.kind,'UEANIM');
  const m=new Reader(asset.data.get('METADATA'));
  const frames=m.i(),fps=m.f(),reference=m.s(),additive=m.u8(),referenceType=m.u8(),referenceFrame=m.i();m.end();
  assert.equal(frames,121);assert.equal(fps,60);assert.equal(additive,0,'converted clips must be full poses');
  const t=new Reader(asset.data.get('TRACKS')),trackCount=t.i();assert.equal(trackCount,expectedTracks);
  const names=[],tracks=[];let maxQuaternionError=0;const badQuaternions=[];
  for(let i=0;i<trackCount;i++){
    names.push(t.s());
    const channels=[];tracks.push(channels);
    for(const width of [3,4,3]){const channel=[];channels.push(channel);const n=t.i();assert(n>0);let last=-1;for(let j=0;j<n;j++){
      const frame=t.i();assert(frame>=0&&frame<frames&&frame>last);last=frame;
      const v=Array.from({length:width},()=>t.f());
      channel.push({frame,v});
      if(width===4){const error=Math.abs(Math.hypot(...v)-1);maxQuaternionError=Math.max(maxQuaternionError,error);if(error>=0.001&&badQuaternions.length<10)badQuaternions.push({bone:names.at(-1),frame,v,error});}
    }}
  }
  t.end();assert.equal(new Set(names).size,names.length);if(!fixture)assert(maxQuaternionError<1e-6,JSON.stringify({maxQuaternionError,badQuaternions}));
  const curves=[];
  if(asset.data.has('CURVES')){const c=new Reader(asset.data.get('CURVES'));const n=c.i();for(let i=0;i<n;i++){const name=c.s(),keys=[];const count=c.i();for(let k=0;k<count;k++)keys.push({frame:c.i(),value:c.f()});curves.push({name,keys});}c.end();}
  return {name:asset.name,frames,fps,duration:(frames-1)/fps,trackCount,names,tracks,reference,additive,referenceType,referenceFrame,curves,maxQuaternionError,trackBytes:asset.data.get('TRACKS')};
}
const body=animation(base+'Animations/FP/HK416/body/fp_hk416_add_spd_reload_empty.ueanim',292);
const weapon=animation(base+'Animations/FP/HK416/weapon/fp_hk416_add_spd_reload_empty_weapon.ueanim',23);
assert(body.names.includes('weapon_right'));assert(body.names.includes('fp_camera'));
const source=JSON.parse(fs.readFileSync(path.join(root,'properties/ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/body/fp_hk416_add_spd_reload_empty.uasset.json'))).find(x=>x.Type==='AnimSequence');
const sourceCurves=source.CompressedCurveData.FloatCurves;
assert.equal(body.curves.length,sourceCurves.length);
for(const curve of sourceCurves){const actual=body.curves.find(x=>x.name===curve.CurveName);assert(actual);assert.equal(actual.keys.length,curve.FloatCurve.Keys.length);curve.FloatCurve.Keys.forEach((key,i)=>{assert.equal(actual.keys[i].frame,Math.round(key.Time*60));assert(Math.abs(actual.keys[i].value-key.Value)<1e-6);});}
function sample(keys,frame) {let a=keys[0],b=keys.at(-1);for(const key of keys){if(key.frame<=frame)a=key;if(key.frame>=frame){b=key;break;}}const t=b.frame===a.frame?0:(frame-a.frame)/(b.frame-a.frame);return a.v.map((x,i)=>x+(b.v[i]-x)*t);}
const manifest=JSON.parse(fs.readFileSync(path.join(root,'manifest.json')));
const bodyRecord=manifest.flatMap(x=>x.Exports).find(x=>x.Name===body.name && x.animation);
assert(bodyRecord, 'body animation metadata missing');
assert.equal(bodyRecord.animation.Compression.KeyEncodingFormat,2,'expected per-track codec');
assert.equal(bodyRecord.animation.SourceWasAdditive,true);
assert.equal(bodyRecord.animation.ExportedPoseSpace,'full-local-transforms');
let omittedScaleTracks=0;
for (const track of bodyRecord.animation.Compression.BoneTracks) {
  if(track.TrackIndex>=0 && bodyRecord.animation.Compression.ScaleOffsets[track.TrackIndex]===-1) omittedScaleTracks++;
}
assert(omittedScaleTracks>0,'must exercise omitted additive scale channels');
for(const channels of body.tracks)for(const key of channels[2])
  assert(key.v.every(v=>Math.abs(v-1)<1e-6),'this source reload must retain unit scale');
let sourceSamplesChecked=0;
for(const now of [body,weapon]){
  const group=now===body?'body':'weapon';
  const decoded=JSON.parse(fs.readFileSync(path.join(root,`decoded/ReadyOrNot/Content/ReadyOrNot/Animations/FP/HK416/${group}/${now.name}.uasset.json`)));
  assert.equal(decoded.length,now.trackCount);
  for(let bone=0;bone<now.trackCount;bone++){
    assert.equal(now.names[bone],decoded[bone].Bone);
    assert.equal(decoded[bone].Frames.length,121);
    decoded[bone].Frames.forEach((pose,i)=>assert.equal(pose.Frame,i));
    for(let channel=0;channel<3;channel++)assert.equal(now.tracks[bone][channel].length,121,'all sampled frames must be retained');
    for(const pose of decoded[bone].Frames)for(let channel=0;channel<3;channel++){
      const a=[pose.Position,pose.Quaternion,pose.Scale][channel],b=sample(now.tracks[bone][channel],pose.Frame);
      if(channel===1){const dot=a.reduce((s,v,i)=>s+v*b[i],0)/(Math.hypot(...a)*Math.hypot(...b));assert(Math.abs(dot)>1-1e-7);}
      else assert(a.every((v,i)=>Math.abs(v-b[i])<1e-5),'UEFormat differs from decoded local sample');
      sourceSamplesChecked++;
    }
  }
}
const magIndex=weapon.names.indexOf('tag_mag_01');assert(magIndex>=0);
const fixedHold=sample(weapon.tracks[magIndex][1],28);
assert(Math.hypot(...fixedHold.slice(0,3))<1e-7,'magazine rotation must retain the decoded hold at frame 28');
const rig=read(base+'Character/SWAT/Character_SWAT_3P/Shared/SKL_RoN_Player_Master_Shared.uemodel');
const skeleton=attrs(new Reader(rig.data.get('SKELETON'))),bones=new Reader(skeleton.get('BONES'));
const boneCount=bones.i();assert.equal(boneCount,292);const boneNames=[];
for(let i=0;i<boneCount;i++){boneNames.push(bones.s());const parent=bones.i();assert(parent>=-1&&parent<i);for(let k=0;k<10;k++)bones.f();}bones.end();
assert.deepEqual(boneNames,body.names,'export track order differs from full skeleton');
const results=JSON.parse(fs.readFileSync(path.join(root,'export-results.json')));
assert(results.length>=3);assert(results.every(x=>x.Success));
const exportedFiles=[];
for(const r of results)for(const p of r.DiskFilePaths){assert(path.resolve(p).startsWith(root+path.sep));const data=fs.readFileSync(p);assert(data.length>0);exportedFiles.push({path:path.relative(root,p),bytes:data.length,sha256:createHash('sha256').update(data).digest('hex')});}
const packages=new Map();
for(const packageRoot of [root,...process.argv.slice(3).map(p=>path.resolve(p))]) {
  for(const record of JSON.parse(fs.readFileSync(path.join(packageRoot,'manifest.json'))))
    packages.set(record.Path,{record,packageRoot});
}
let rawCompanionsChecked=0;
for(const {record,packageRoot} of packages.values())for(const raw of record.RawFiles){const rawPath=path.resolve(packageRoot,'raw',raw.Path);assert(rawPath.startsWith(path.join(packageRoot,'raw')+path.sep));const data=fs.readFileSync(rawPath);assert.equal(data.length,raw.Size);assert.equal(createHash('sha256').update(data).digest('hex'),raw.Sha256);rawCompanionsChecked++;}
for(const a of [body,weapon]){delete a.names;delete a.tracks;delete a.trackBytes;}
console.log(JSON.stringify({passed:true,body,weapon,fullSkeletonBones:boneCount,exportObjects:results.length,sourceSamplesChecked,omittedScaleTracks,sourcePackagesChecked:packages.size,rawCompanionsChecked,exportedFiles,checks:['finite keys and unit quaternions','121 endpoint samples at 60 fps','body tracks match full skeleton order','source curve values and frames retained','omitted additive scale channels retain unit idle scale','every exchanged local sample agrees with saved decoder output','magazine rotation hold retained at frame 28','export files exist and raw companions match hashes'],limits:['HK416 empty reload pair on the recorded build only','readback shares the CUE4Parse source decoder','historical failed-export fixtures are not rerun','not Blender visual inspection, Unreal runtime behavior or Cyberpunk native export']},null,2));
