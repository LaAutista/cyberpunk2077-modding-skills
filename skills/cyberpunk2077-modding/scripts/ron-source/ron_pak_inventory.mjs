// Read-only inventory for the observed UE5 V11 PAK layout. Not a payload decoder.
// Layout reference: trumank/repak, repak/src/{footer,pak}.rs.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';

const [pakDir, output] = process.argv.slice(2);
assert(pakDir && output, 'Usage: node ron_pak_inventory.mjs PAK_DIRECTORY OUTPUT_JSON');
function reader(bytes) {
  let offset = 0;
  const take = n => { assert(n >= 0 && offset + n <= bytes.length); const b = bytes.subarray(offset, offset + n); offset += n; return b; };
  return {
    u32: () => take(4).readUInt32LE(), i32: () => take(4).readInt32LE(),
    u64: () => { const v = take(8).readBigUInt64LE(); assert(v <= BigInt(Number.MAX_SAFE_INTEGER)); return Number(v); },
    bytes: take,
    string: () => {
      const n = take(4).readInt32LE();
      assert(n !== 0 && Math.abs(n) < 1000000, 'Invalid FString size');
      const b = take(Math.abs(n) * (n < 0 ? 2 : 1));
      assert(n < 0 ? b.readUInt16LE(b.length - 2) === 0 : b[b.length - 1] === 0);
      return b.subarray(0, b.length - (n < 0 ? 2 : 1)).toString(n < 0 ? 'utf16le' : 'utf8');
    },
    remaining: () => bytes.length - offset,
  };
}
const digest = b => crypto.createHash('sha1').update(b).digest('hex');
const result = { scope: 'Index-only; no payload decryption, decompression or UObject/animation decoding', paks: [], hk416: [], armCandidates: [] };
for (const name of fs.readdirSync(pakDir).filter(n => n.endsWith('.pak')).sort()) {
  const filename = path.join(pakDir, name), stat = fs.statSync(filename), fd = fs.openSync(filename, 'r');
  try {
    function read(at, length) {
      assert(Number.isSafeInteger(at) && Number.isSafeInteger(length) && length > 0 && length < 128 * 1024 * 1024 && at >= 0 && at + length <= stat.size);
      const b = Buffer.alloc(length); assert.equal(fs.readSync(fd, b, 0, length, at), length); return b;
    }
    const footer = read(stat.size - 221, 221);
    assert.equal(footer.readUInt32LE(17), 0x5a6f12e1, name);
    assert.equal(footer.readUInt32LE(21), 11, name);
    assert.equal(footer[16], 0, 'Encrypted index unsupported');
    const index = read(Number(footer.readBigUInt64LE(25)), Number(footer.readBigUInt64LE(33)));
    assert.equal(digest(index), footer.subarray(41, 61).toString('hex'), 'Index SHA1');
    const r = reader(index), mount = r.string(), entries = r.u32(); r.u64();
    if (r.u32()) { r.u64(); r.u64(); r.bytes(20); }
    assert.equal(r.u32(), 1, 'Full directory index required');
    const directory = read(r.u64(), r.u64()), expected = r.bytes(20).toString('hex');
    assert.equal(digest(directory), expected, 'Directory SHA1');
    const d = reader(directory), folders = d.u32(); let listed = 0, deleted = 0;
    for (let f = 0; f < folders; f++) {
      const folder = d.string().replace(/^\//, ''), count = d.u32();
      for (let j = 0; j < count; j++) {
        const asset = folder + d.string(), encodedOffset = d.i32();
        if (encodedOffset === -2147483648) { deleted++; continue; }
        listed++;
        if (/416/i.test(asset)) result.hk416.push({ pak: name, asset });
        if (/\.uasset$/i.test(asset) && /\/(SK|SKL|SKM)_[^/]*(arm|body.*fp|fp.*body)/i.test(asset)) result.armCandidates.push({ pak: name, asset });
      }
    }
    assert.equal(d.remaining(), 0, 'Unparsed directory bytes');
    assert.equal(listed, entries, 'Declared/listed entry count');
    result.paks.push({ name, bytes: stat.size, mtime: stat.mtime.toISOString(), version: 11, indexEncrypted: false, mount, entries, deleted, indexSha1: digest(index), directorySha1: expected, compression: footer.subarray(61).toString('ascii').split('\0').filter(Boolean) });
  } finally { fs.closeSync(fd); }
}
assert(result.paks.length > 0);
result.totalEntries = result.paks.reduce((n, p) => n + p.entries, 0);
fs.writeFileSync(output, JSON.stringify(result, null, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify({ paks: result.paks.length, entries: result.totalEntries, hk416Paths: result.hk416.length, armCandidates: result.armCandidates.length, output }));
