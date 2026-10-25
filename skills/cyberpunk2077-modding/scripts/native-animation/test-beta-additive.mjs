import assert from 'node:assert/strict';
import {unbind,multiply,normalize,bindRotation} from './additive-math.mjs';

const close=(a,b)=>a.forEach((x,i)=>assert(Math.abs(x-b[i])<1e-12,`${a} != ${b}`));
const half=Math.sqrt(0.5),bind=[half,0,0,half],delta=[0,half,0,half];
// 90 degrees about X followed by Y has a positive Z quaternion component.
close(multiply(bind,delta),[0.5,0.5,0.5,0.5]);
close(unbind('rotation',[0.5,0.5,0.5,0.5],{rotation:bind}),delta);
assert(Math.abs(multiply([0.5,0.5,0.5,0.5],[-half,0,0,half])[2])>0.7,'Fixture must expose right-division error');
close(unbind('translation',[4,6,8],{translation:[1,2,3]}),[3,4,5]);
close(unbind('scale',[4,9,16],{scale:[2,3,4]}),[2,3,4]);
const tiny=normalize([1e-5,0,0,1]);assert(tiny[0]>0);
close(bindRotation(delta,{Rotation:{i:half,j:0,k:0,r:half}}),[0.5,0.5,0.5,0.5]);
assert.throws(()=>unbind('scale',[1,1,1],{scale:[1,0,1]}));
assert.throws(()=>unbind('rotation',[0,0,0,1],{matrix:Array(16).fill(0)}));
assert.throws(()=>unbind('rotation',[0,0,0,0],{}));
console.log('PASS: noncommuting left unbind, native/glTF bind composition, translation/scale deltas, tiny quaternion preservation, invalid bind rejection.');
