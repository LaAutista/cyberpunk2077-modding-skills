import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {compare} from '../skills/cyberpunk2077-animation-retargeting/scripts/animation_coverage.mjs';

function fixture(bytes = [1, 2, 3], offset = 0) {
  return {Data: {RootChunk: {
    animationDataChunks: [{buffer: {Bytes: Buffer.from([...Array(offset).fill(99), ...bytes]).toString('base64')}}],
    animations: [{animation: {name: {$value: 'idle'}, animationType: 'Normal', animBuffer: {
      $type: 'synthetic', duration: 1, dataAddress: {unkIndex: 0, fsetInBytes: offset, zeInBytes: bytes.length}}}, events: []}]
  }}};
}
const base = fixture(), original = JSON.stringify(base);
assert.deepEqual(compare(base, fixture()).counts, {unchanged: 1});
assert.deepEqual(compare(base, fixture([1, 2, 3], 17)).counts, {unchanged: 1});
assert.deepEqual(compare(base, fixture([1, 2, 4])).counts, {motion_changed: 1});
const event = fixture();event.Data.RootChunk.animations[0].events = [{startFrame: 3}];
assert.deepEqual(compare(base, event).counts, {metadata_only: 1});
const renamed = fixture();renamed.Data.RootChunk.animations[0].animation.name.$value = 'draw';
assert.deepEqual(compare(base, renamed).counts, {added: 1, removed: 1});
for (const key of ['inplaceCompressedBuffer', 'defferedBuffer']) {
  const inline = fixture();inline.Data.RootChunk.animations[0].animation.animBuffer[key] = {Bytes: 'AQID'};
  delete inline.Data.RootChunk.animations[0].animation.animBuffer.dataAddress;
  assert.deepEqual(compare(base, inline).counts, {unchanged: 1});
}
const duplicate = fixture();duplicate.Data.RootChunk.animations.push(duplicate.Data.RootChunk.animations[0]);
assert.throws(() => compare(base, duplicate), /duplicate/);
for (const address of [{unkIndex: 0, fsetInBytes: .5, zeInBytes: 2}, {unkIndex: 0, fsetInBytes: 2, zeInBytes: 2},
                       {unkIndex: 0, fsetInBytes: 0, zeInBytes: 0}]) {
  const bad = fixture();bad.Data.RootChunk.animations[0].animation.animBuffer.dataAddress = address;
  assert.throws(() => compare(base, bad));
}
assert.equal(JSON.stringify(base), original);assert.equal(compare(base, event).sourceFidelityProven, false);
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'coverage '));
try {
  const source = path.join(temp, 'source.json'), output = path.join(temp, 'report.json');
  fs.writeFileSync(source, original);
  const cli = fileURLToPath(new URL('../skills/cyberpunk2077-animation-retargeting/scripts/animation_coverage.mjs', import.meta.url));
  const run = () => spawnSync(process.execPath, [cli, source, source, output], {encoding: 'utf8'});
  assert.equal(run().status, 0);const report = fs.readFileSync(output);
  assert.equal(run().status, 1);assert.deepEqual(fs.readFileSync(output), report);
  assert.equal(JSON.parse(report).runtimeVerified, false);
} finally {fs.rmSync(temp, {recursive: true, force: true});}
console.log('PASS native clip coverage: identity, relocation, payload/metadata changes, missing/duplicate clips, bounds and receipt preservation');
