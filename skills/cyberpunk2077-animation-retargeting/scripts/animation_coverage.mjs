// Compare native stored clip payloads and metadata independently of container layout.
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {resolve} from 'node:path';
import {canonical} from '../../cyberpunk2077-modding/scripts/native-animation/native-json-canonical.mjs';

const sha = value => createHash('sha256').update(value).digest('hex');
const ordered = value => Array.isArray(value) ? value.map(ordered) : value && typeof value === 'object'
  ? Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key])])) : value;

function decode(value) {
  assert(typeof value === 'string' && value.length > 0 && value.length % 4 === 0, 'Missing or invalid base64 payload');
  const bytes = Buffer.from(value, 'base64');
  assert.equal(bytes.toString('base64'), value, 'Invalid base64 payload');
  return bytes;
}

export function inventory(document) {
  const root = canonical(document).RootChunk, entries = new Map();
  assert(Array.isArray(root.animations) && root.animations.length, 'Expected native animations');
  for (const original of root.animations) {
    const entry = structuredClone(original), animation = entry.animation, buffer = animation.animBuffer;
    const name = animation.name.$value;
    assert(typeof name === 'string' && name && !entries.has(name), 'Missing or duplicate clip name');
    let bytes;
    if (buffer.inplaceCompressedBuffer?.Bytes) bytes = decode(buffer.inplaceCompressedBuffer.Bytes);
    else if (buffer.defferedBuffer?.Bytes) bytes = decode(buffer.defferedBuffer.Bytes);
    else {
      const address = buffer.dataAddress;
      assert(address && ['unkIndex', 'fsetInBytes', 'zeInBytes'].every(k => Number.isSafeInteger(address[k]) && address[k] >= 0), 'Invalid payload address');
      assert(address.zeInBytes > 0, 'Empty payload address');
      const chunk = decode(root.animationDataChunks?.[address.unkIndex]?.buffer?.Bytes);
      assert(address.fsetInBytes + address.zeInBytes <= chunk.length, 'Payload exceeds chunk');
      bytes = chunk.subarray(address.fsetInBytes, address.fsetInBytes + address.zeInBytes);
    }
    // Offsets and serializer copies change when other clips are repacked.
    for (const key of ['dataAddress', 'tempBuffer', 'inplaceCompressedBuffer', 'defferedBuffer']) delete buffer[key];
    entries.set(name, {name, codec: buffer.$type, duration: buffer.duration, payloadBytes: bytes.length,
      motionSHA256: sha(bytes), metadataSHA256: sha(JSON.stringify(ordered(entry)))});
  }
  return entries;
}

export function compare(baseline, candidate) {
  const old = inventory(baseline), current = inventory(candidate);
  const clips = [...new Set([...old.keys(), ...current.keys()])].sort().map(name => {
    const a = old.get(name), b = current.get(name);
    const status = !a ? 'added' : !b ? 'removed' : a.motionSHA256 !== b.motionSHA256 ? 'motion_changed'
      : a.metadataSHA256 !== b.metadataSHA256 ? 'metadata_only' : 'unchanged';
    return {name, status, baseline: a ?? null, candidate: b ?? null};
  });
  const counts = {};
  for (const clip of clips) counts[clip.status] = (counts[clip.status] ?? 0) + 1;
  return {status: 'CHECKED', counts, clips, runtimeVerified: false, sourceFidelityProven: false,
    limits: ['Stored payload identity detects retained donor data; metadata and native composition still affect evaluated motion.',
      'Changed bytes or codec do not prove new motion or source fidelity. Graph dispatch, contact, skin, sound and gameplay require separate evidence.']};
}

export function main(args) {
  if (args.length === 1 && args[0] === '--help') {
    console.log('Usage: node animation_coverage.mjs BASELINE.json CANDIDATE.json OUTPUT.json');
    return 0;
  }
  try {
    assert.equal(args.length, 3, 'Expected BASELINE.json CANDIDATE.json OUTPUT.json');
    const [baseline, candidate, output] = args;
    const result = compare(JSON.parse(fs.readFileSync(baseline)), JSON.parse(fs.readFileSync(candidate)));
    result.inputFiles = Object.fromEntries([baseline, candidate, fileURLToPath(import.meta.url)].map(p => [p, sha(fs.readFileSync(p))]));
    fs.writeFileSync(output, JSON.stringify(result, null, 2) + '\n', {flag: 'wx'});
    console.log(JSON.stringify({status: result.status, output, counts: result.counts, runtimeVerified: false}));
    return 0;
  } catch (error) {
    console.log(JSON.stringify({status: 'FAILED', error: error.message, runtimeVerified: false}));
    return 1;
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) process.exitCode = main(process.argv.slice(2));
