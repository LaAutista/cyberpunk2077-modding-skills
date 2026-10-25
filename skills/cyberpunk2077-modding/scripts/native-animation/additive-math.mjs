import assert from 'node:assert/strict';

export const supportedTypes = new Set(['Normal', 'Additive', 'AdditiveWithoutFirstFrame']);
export function normalize(q) {
  assert(q.length === 4 && q.every(Number.isFinite));
  const n = Math.hypot(...q); assert(n > 1e-12, 'Singular quaternion');
  return q.map(x => x / n);
}
export function multiply(a, b) {
  const [x,y,z,w]=a,[X,Y,Z,W]=b;
  return [w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W,w*W-x*X-y*Y-z*Z];
}
export function unbind(path, value, node) {
  assert(!node.matrix, 'Additive authoring requires original TRS rig nodes');
  assert(value.every(Number.isFinite));
  if(path === 'rotation') {
    const b=normalize(node.rotation ?? [0,0,0,1]);
    return normalize(multiply([-b[0],-b[1],-b[2],b[3]],normalize(value)));
  }
  if(path === 'translation') return value.map((v,k)=>v-(node.translation??[0,0,0])[k]);
  assert.equal(path,'scale'); const b=node.scale??[1,1,1];
  assert(b.every(x=>Number.isFinite(x)&&x>1e-12), 'Singular/reflected additive bind scale');
  assert(value.every(x=>x>0), 'Singular/reflected additive authored scale');
  return value.map((v,k)=>v/b[k]);
}
export function bindRotation(delta, boneTransform) {
  const b=boneTransform.Rotation;
  return normalize(multiply(normalize([b.i,b.k,-b.j,b.r]),delta));
}
