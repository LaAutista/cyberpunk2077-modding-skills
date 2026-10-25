import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {inspect,discover,peVersion} from '../setup/preflight.mjs';
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'cp-preflight-fixture-'));
try{
 const file=path.join(temp,'tool');assert.equal(inspect('tool',file).status,'missing');
 fs.writeFileSync(file,'fixture');assert.equal(inspect('tool',file).status,'unknown');
 const expected=crypto.createHash('sha256').update('fixture').digest('hex');assert.equal(inspect('tool',file,expected).status,'present');assert.equal(inspect('tool',file,'0'.repeat(64)).status,'incompatible');
 assert.equal(peVersion(file),null);const pe=Buffer.alloc(160);pe.write('MZ');pe.writeUInt32LE(64,60);pe.writeUInt32LE(0x4550,64);Buffer.from([0xbd,4,0xef,0xfe,0,0,1,0]).copy(pe,80);pe.writeUInt32LE((1<<16)|2,88);pe.writeUInt32LE((3<<16)|4,92);fs.writeFileSync(file,pe);assert.equal(peVersion(file),'1.2.3.4');
 const before=fs.readdirSync(temp);assert.deepEqual(discover({},temp),discover({},temp));assert.deepEqual(fs.readdirSync(temp),before);
 const source=discover({},undefined,undefined,'ron-hk416');assert.equal(source.sourceAdapter.destination,'cyberpunk2077');assert.match(source.sourceReadiness,/missing or unverified/);
 console.log('PASS: four identity statuses, read-only repeat discovery and task-scoped source requirements.');
}finally{fs.rmSync(temp,{recursive:true,force:true});}
