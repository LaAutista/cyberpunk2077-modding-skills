#!/usr/bin/env node
// Independent raw-key repair of the demonstrated WKit9.0.1 compressed reader snap.
// Reads ACTUAL serialized native bytes; never receives the authored expectation.
import {supportedTypes,normalize,bindRotation,multiply} from './additive-math.mjs';
import fs from 'node:fs';import assert from 'node:assert/strict';import {createHash} from 'node:crypto';
const [nativePath,rigPath,cliPath,outPath,flag,requiredText]=process.argv.slice(2);assert(outPath&&flag==='--required-clips'&&requiredText,'Usage: NATIVE.json RIG.json CLI.glb NEW.glb --required-clips NAME,NAME');const required=new Set(requiredText.split(','));assert(required.size>0&&![...required].some(x=>!x));assert(!fs.existsSync(outPath)&&!fs.existsSync(outPath+'.raw-readback.json'),'Refusing to replace readback or report');
const hash=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex'),root=JSON.parse(fs.readFileSync(nativePath)).Data.RootChunk,rig=JSON.parse(fs.readFileSync(rigPath)).Data.RootChunk,names=rig.boneNames.map(n=>n.$value),source=fs.readFileSync(cliPath);assert.equal(source.readUInt32LE(0),0x46546c67,'Invalid GLB magic');assert.equal(source.readUInt32LE(4),2);assert.equal(source.readUInt32LE(8),source.length,'Invalid declared GLB length');let j,bin;for(let p=12;p<source.length;){assert(p+8<=source.length);const n=source.readUInt32LE(p),type=source.readUInt32LE(p+4);assert(p+8+n<=source.length&&n%4===0);if(type===0x4e4f534a){assert(!j,'Duplicate JSON chunk');j=JSON.parse(source.subarray(p+8,p+8+n));}else if(type===0x004e4942){assert(!bin,'Duplicate BIN chunk');bin=Buffer.from(source.subarray(p+8,p+8+n));}else throw new Error('Unsupported extra GLB chunk');p+=8+n;}assert(j&&bin);
function array(id){const a=j.accessors[id],v=j.bufferViews[a.bufferView],width={SCALAR:1,VEC4:4}[a.type];assert(width&&a.componentType===5126);return Array.from({length:a.count},(_,i)=>Array.from({length:width},(_,k)=>bin.readFloatLE((v.byteOffset??0)+(a.byteOffset??0)+i*(v.byteStride??width*4)+k*4)));}
function append(rows){const data=Buffer.alloc(rows.length*16);rows.forEach((r,i)=>r.forEach((v,k)=>data.writeFloatLE(v,i*16+k*4)));const view=j.bufferViews.length;j.bufferViews.push({buffer:0,byteOffset:bin.length,byteLength:data.length});bin=Buffer.concat([bin,data]);const id=j.accessors.length;j.accessors.push({bufferView:view,componentType:5126,count:rows.length,type:'VEC4',min:[0,1,2,3].map(k=>Math.min(...rows.map(r=>r[k]))),max:[0,1,2,3].map(k=>Math.max(...rows.map(r=>r[k])))});return id;}
const report={passed:false,requiredClips:[...required],runtimeVerified:false,scope:'Native compressed quantized/raw/constant rotation bytes and original rig bind-relative composition; only demonstrated CLI identity snapping corrected',inputSHA256:{nativeJson:hash(nativePath),rigJson:hash(rigPath),standardCliGlb:hash(cliPath)},clips:[],skippedClips:[],corrections:[],maxUncorrectedResidual:0};
for(const entry of root.animations){const a=entry.Data.animation.Data,b=a.animBuffer.Data,name=a.name.$value;if(!required.has(name))continue;assert(supportedTypes.has(a.animationType));assert.equal(b.$type,'animAnimationBufferCompressed');const additive=a.animationType!=='Normal';
 const address=b.dataAddress,inline=b.inplaceCompressedBuffer?.Bytes??b.defferedBuffer?.Bytes;
 const chunk=Buffer.from(inline??root.animationDataChunks[address.unkIndex].buffer.Bytes,'base64');
 const bytes=inline?chunk:chunk.subarray(address.fsetInBytes,address.fsetInBytes+address.zeInBytes);
 assert(bytes.length>=b.numAnimKeys*10+(b.numAnimKeysRaw+b.numConstAnimKeys)*16);
 const tracks=new Map();let count=0,p=0;
 for(const[length,size,isConst,quantized]of[[b.numAnimKeys,10,false,true],[b.numAnimKeysRaw,16,false,false],[b.numConstAnimKeys,16,true,false]]){
  for(let i=0;i<length;i++,p+=size){
   const header=bytes.readUInt16LE(p+(isConst?0:2)),kind=(header&0x6000)>>13;assert(kind<=2,'Unsupported transform key kind');if(kind!==1)continue;
   const bone=header&0x1fff;assert(bone<names.length);
   const v=quantized?[4,6,8].map(o=>bytes.readUInt16LE(p+o)/65535*2-1):[4,8,12].map(o=>bytes.readFloatLE(p+o));
   const dot=v.reduce((sum,x)=>sum+x*x,0);assert(dot<=2&&v.every(Number.isFinite),'Invalid stored quaternion');
   const scale=Math.sqrt(2-dot),delta=normalize([v[0]*scale,v[2]*scale,-v[1]*scale,(1-dot)*(header&0x8000?-1:1)]);
   const bind=additive?bindRotation([0,0,0,1],rig.boneTransforms[bone]):[0,0,0,1];
   const q=additive?bindRotation(delta,rig.boneTransforms[bone]):delta;
   // WKit applies its W==1 shortcut to the rig bind and to both rotation stages.
   const f=Math.fround;
   const stockNormalize=x=>{x=x.map(f);if(x[3]===1)return[0,0,0,1];const d=f(f(f(x[0]*x[0])+f(x[1]*x[1]))+f(f(x[2]*x[2])+f(x[3]*x[3])));const n=f(Math.sqrt(d));return x.map(v=>f(v/n));};
   const vf=quantized?[4,6,8].map(o=>f(f(f(f(1/65535)*bytes.readUInt16LE(p+o))*2)-1)):v;
   const df=f(f(f(vf[0]*vf[0])+f(vf[1]*vf[1]))+f(vf[2]*vf[2]));
   const sf=f(Math.sqrt(f(2-df))),rawStock=[f(vf[0]*sf),f(vf[2]*sf),-f(vf[1]*sf),f((1-df)*(header&0x8000?-1:1))];
   const rb=rig.boneTransforms[bone].Rotation,stockBind=stockNormalize([rb.i,rb.k,-rb.j,rb.r]),stockDelta=stockNormalize(rawStock);
   const stock=additive?stockNormalize(multiply(stockBind,stockDelta).map(f)):stockDelta;
   if(!tracks.has(bone))tracks.set(bone,[]);
   tracks.get(bone).push({time:bytes.readUInt16LE(p+(isConst?2:0))/65535*a.duration,q,delta,bind,stock,tick:bytes.readUInt16LE(p+(isConst?2:0)),interpolation:isConst?'STEP':'LINEAR'});count++;
  }
 }
 const animation=j.animations.find(x=>x.name===name);assert(animation);assert.equal(animation.extras?.animationType??a.animationType,a.animationType);assert.equal(animation.channels.filter(c=>c.target.path==='rotation').length,tracks.size,'Native rotation channel coverage');let corrected=0;
 for(const [bone,keys]of tracks){keys.sort((a,b)=>a.time-b.time);const channel=animation.channels.find(c=>j.nodes[c.target.node].name===names[bone]&&c.target.path==='rotation');assert(channel);const sampler=animation.samplers[channel.sampler],times=array(sampler.input).flat(),values=array(sampler.output);assert(keys.every(k=>k.interpolation===(sampler.interpolation??"LINEAR")),`${name}/${names[bone]}: constant/linear key mismatch`);assert.equal(keys.length,values.length);let changed=false;
 const align=(q,v)=>q.reduce((sum,x,k)=>sum+x*v[k],0)<0?q.map(x=>-x):q;
 const error=(q,v)=>Math.max(...align(q,v).map((x,k)=>Math.abs(x-v[k])));
 const tiny=q=>q.slice(0,3).some(x=>x!==0)&&Math.fround(q[3])===1;
 for(let i=0;i<keys.length;i++){
  const key=keys[i];assert(Math.abs(times[i]-key.time)<1e-6,`${name}/${names[bone]}: native/CLI key time mismatch`);
  const q=align(key.q,values[i]),delta=error(q,values[i]);
  const decodeSnap=(tiny(key.delta)||(additive&&tiny(key.bind))||tiny(key.q)||error(key.q,key.stock)>1e-5)&&error(key.stock,values[i])<1e-6;
  const exportSnap=false;
  if((decodeSnap||exportSnap)&&delta>1e-12){
   report.corrections.push({clip:name,bone:names[bone],key:i,tick:key.tick,time:key.time,source:'actual native bytes plus original rig bind',cli:values[i],native:q});values[i]=q;changed=true;corrected++;
  }else{assert(delta<=1e-5,`${name}/${names[bone]}/${i}: unexplained native/CLI quaternion delta ${delta}; native=${JSON.stringify(key.q)} stock=${JSON.stringify(key.stock)} CLI=${JSON.stringify(values[i])} bind=${JSON.stringify(key.bind)} raw=${JSON.stringify(key.delta)}`);report.maxUncorrectedResidual=Math.max(report.maxUncorrectedResidual,delta);}
 }
 if(changed){assert.equal(animation.channels.filter(c=>c.sampler===channel.sampler).length,1,'Shared sampler cannot be patched in place');sampler.output=append(values);}}
 report.clips.push({name,animationType:a.animationType,nativeRotationKeys:count,quantizedRecords:b.numAnimKeys,correctedKeys:corrected});}
for(const name of required)assert(report.clips.some(c=>c.name===name),`Required clip not independently decoded: ${name}`);
j.buffers[0].byteLength=bin.length;let jb=Buffer.from(JSON.stringify(j));jb=Buffer.concat([jb,Buffer.alloc((4-jb.length%4)%4,32)]);const out=Buffer.alloc(28+jb.length+bin.length);out.writeUInt32LE(0x46546c67);out.writeUInt32LE(2,4);out.writeUInt32LE(out.length,8);out.writeUInt32LE(jb.length,12);out.writeUInt32LE(0x4e4f534a,16);jb.copy(out,20);out.writeUInt32LE(bin.length,20+jb.length);out.writeUInt32LE(0x004e4942,24+jb.length);bin.copy(out,28+jb.length);fs.writeFileSync(outPath,out,{flag:'wx'});report.passed=true;report.outputSHA256=hash(outPath);fs.writeFileSync(outPath+'.raw-readback.json',JSON.stringify(report,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify({passed:true,clips:report.clips.length,nativeRotationKeys:report.clips.reduce((s,c)=>s+c.nativeRotationKeys,0),correctedReaderKeys:report.corrections.length,maxUncorrectedResidual:report.maxUncorrectedResidual}));
