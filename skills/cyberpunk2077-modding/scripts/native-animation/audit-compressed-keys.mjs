#!/usr/bin/env node
// Read-only validation shared with the independent native rotation reader.
// WolvenKit 9.0.1 CompressedBuffer.AnimKeySort orders dynamic keys by bone,
// time, then position/rotation/scale. Constant-key ordering is not asserted.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';

function uint(value,label){
  assert(Number.isSafeInteger(value)&&value>=0,`${label}: expected a nonnegative safe integer`);
  return value;
}

export function inspectCompressedKeys(root,buffer,{label='compressed animation',rigJointCount}={}){
  assert.equal(buffer.$type,'animAnimationBufferCompressed',`${label}: unsupported native buffer`);
  const definitions=[['numAnimKeys',10,false,true],['numAnimKeysRaw',16,false,false],['numConstAnimKeys',16,true,false]];
  let byteLength=0;
  const sections=definitions.map(([field,size,isConst,quantized])=>{
    const count=uint(buffer[field],`${label}/${field}`),offset=byteLength;
    byteLength+=count*size;
    assert(Number.isSafeInteger(byteLength),`${label}: transform byte count overflow`);
    return {field,count,size,isConst,quantized,offset};
  });
  // Some minimal serialized fixtures omit empty float-track arrays/counts.
  const floatTracks=uint(buffer.numTrackKeys??0,`${label}/numTrackKeys`)+uint(buffer.numConstTrackKeys??0,`${label}/numConstTrackKeys`);
  const expectedLength=byteLength+floatTracks*8;
  assert(Number.isSafeInteger(expectedLength),`${label}: payload byte count overflow`);
  const inline=buffer.inplaceCompressedBuffer?.Bytes??buffer.defferedBuffer?.Bytes;
  let bytes;
  if(inline!==undefined){
    assert.equal(typeof inline,'string',`${label}: invalid inline buffer`);
    bytes=Buffer.from(inline,'base64');
  }else{
    const address=buffer.dataAddress;
    assert(address&&Array.isArray(root.animationDataChunks),`${label}: missing external data address/chunks`);
    const index=uint(address.unkIndex,`${label}/dataAddress.unkIndex`);
    const offset=uint(address.fsetInBytes,`${label}/dataAddress.fsetInBytes`);
    const size=uint(address.zeInBytes,`${label}/dataAddress.zeInBytes`);
    assert(index<root.animationDataChunks.length,`${label}: external chunk index out of bounds`);
    const encoded=root.animationDataChunks[index]?.buffer?.Bytes;
    assert.equal(typeof encoded,'string',`${label}: missing external buffer bytes`);
    const chunk=Buffer.from(encoded,'base64');
    assert(offset<=chunk.length&&size<=chunk.length-offset,`${label}: external byte range out of bounds`);
    bytes=chunk.subarray(offset,offset+size);
  }
  assert.equal(bytes.length,expectedLength,`${label}: native key/float-track counts do not match payload length`);
  const jointBounds=[];
  if(buffer.numJoints!==undefined)jointBounds.push(uint(buffer.numJoints,`${label}/numJoints`));
  if(rigJointCount!==undefined)jointBounds.push(uint(rigJointCount,`${label}/rigJointCount`));
  for(const section of sections){
    let previous;
    for(let i=0,p=section.offset;i<section.count;i++,p+=section.size){
      const header=bytes.readUInt16LE(p+(section.isConst?0:2));
      const bone=header&0x1fff,kind=(header&0x6000)>>13,tick=bytes.readUInt16LE(p+(section.isConst?2:0));
      assert(kind<=2,`${label}/${section.field}[${i}]: unsupported transform key kind`);
      assert(jointBounds.every(count=>bone<count),`${label}/${section.field}[${i}]: bone index out of bounds`);
      if(!section.isConst){
        const key=[bone,tick,kind];
        assert(!previous||bone>previous[0]||(bone===previous[0]&&(tick>previous[1]||(tick===previous[1]&&kind>=previous[2]))),
          `${label}/${section.field}[${i}]: noncanonical dynamic key order; expected (bone,tick,kind), previous=${JSON.stringify(previous)}, current=${JSON.stringify(key)}`);
        previous=key;
      }
    }
  }
  return {bytes,sections,transformBytes:byteLength,floatTrackKeys:floatTracks,jointBoundsChecked:jointBounds.length>0};
}

export function auditCompressedKeys(root,required){
  assert(Array.isArray(root.animations),'Missing animation entries');
  const clips=[],skippedClips=[];
  for(const entry of root.animations){
    const animation=entry.Data.animation.Data,name=animation.name.$value;
    if(required&&!required.has(name))continue;
    const buffer=animation.animBuffer.Data;
    if(buffer.$type!=='animAnimationBufferCompressed'){
      assert(!required,`${name}: required clip has unsupported native buffer ${buffer.$type}`);
      skippedClips.push({name,bufferType:buffer.$type});continue;
    }
    const inspected=inspectCompressedKeys(root,buffer,{label:name});
    clips.push({name,payloadBytes:inspected.bytes.length,dynamicKeys:buffer.numAnimKeys+buffer.numAnimKeysRaw,constantKeys:buffer.numConstAnimKeys,floatTrackKeys:inspected.floatTrackKeys,jointBoundsChecked:inspected.jointBoundsChecked});
  }
  if(required)for(const name of required)assert(clips.some(clip=>clip.name===name),`Required clip not audited: ${name}`);
  assert(clips.length>0,'No supported compressed clips audited');
  return {passed:true,runtimeVerified:false,scope:'Compressed key layout/bounds and canonical dynamic key order; constants retain their existing order; pose values and runtime behavior are not validated',clips,skippedClips};
}

if(process.argv[1]&&pathToFileURL(process.argv[1]).href===import.meta.url){
  const [nativePath,flag,requiredText,...rest]=process.argv.slice(2);
  assert(nativePath&&rest.length===0&&((flag===undefined&&requiredText===undefined)||(flag==='--required-clips'&&requiredText)),
    'Usage: audit-compressed-keys.mjs NATIVE.json [--required-clips NAME,NAME]');
  const required=requiredText===undefined?undefined:new Set(requiredText.split(','));
  assert(!required||![...required].some(name=>!name),'Empty required clip name');
  const input=fs.readFileSync(nativePath),report=auditCompressedKeys(JSON.parse(input).Data.RootChunk,required);
  console.log(JSON.stringify({...report,inputSHA256:createHash('sha256').update(input).digest('hex')},null,2));
}
