import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {checkedURL,hash,tree,verify,initialize,acquire,here,privateDirectory,trustedLibrary,missingSkill} from '../setup/provision.mjs';
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'cp-provision-fixture-'));
try{
 for(const url of ['http://github.com/a','https://evil.test/a','https://github.com@evil.test/a'])assert.throws(()=>checkedURL(url));
 assert.throws(()=>initialize(temp));
 const root=path.join(temp,'isolated');initialize(root);initialize(root);
 const outside=path.join(temp,'outside');fs.mkdirSync(outside);fs.renameSync(path.join(root,'tools'),path.join(root,'tools-original'));fs.symlinkSync(outside,path.join(root,'tools'));assert.throws(()=>initialize(root),/directory replaced/);assert.deepEqual(fs.readdirSync(outside),[]);fs.unlinkSync(path.join(root,'tools'));fs.renameSync(path.join(root,'tools-original'),path.join(root,'tools'));
 const component=path.join(root,'tools/fixture');fs.mkdirSync(component);fs.writeFileSync(path.join(component,'a'),'fixture');
 const receipt={recipe:'fixture',files:tree(component)};fs.writeFileSync(path.join(component,'.component-receipt.json'),JSON.stringify(receipt));verify(component,'fixture');
 fs.writeFileSync(path.join(component,'a'),'modified');assert.throws(()=>verify(component,'fixture'),/Local modifications/);assert.equal(fs.readFileSync(path.join(component,'a'),'utf8'),'modified');
 const cache=path.join(root,'cache'),item={id:'fixture.zip',url:'https://github.com/official/fixture',algorithm:'sha256',hash:'0'.repeat(64)};
 const originalFetch=globalThis.fetch;globalThis.fetch=async()=>new Response(new Uint8Array([1,2,3]));
 try{await assert.rejects(acquire(item,cache),/hash mismatch/);assert.deepEqual(fs.readdirSync(cache),[]);
 const file=path.join(temp,'bytes');fs.writeFileSync(file,Buffer.from([1,2,3]));item.hash=hash(file);
 await acquire(item,cache);await acquire(item,cache);assert.deepEqual(fs.readdirSync(cache),['fixture.zip']);
 fs.writeFileSync(path.join(cache,item.id),'local');await assert.rejects(acquire(item,cache),/preserved/);}
 finally{globalThis.fetch=originalFetch;}
 const archives=spawnSync('python3',['-c',`import zipfile,tarfile,io,pathlib
r=pathlib.Path(${JSON.stringify(temp)})
with zipfile.ZipFile(r/'good.zip','w') as z:z.writestr('one/file.txt','ok')
with zipfile.ZipFile(r/'bad.zip','w') as z:z.writestr('../escape','bad')
with tarfile.open(r/'bad.tar','w') as t:
 e=tarfile.TarInfo('link');e.type=tarfile.SYMTYPE;e.linkname='../escape';t.addfile(e)
`],{encoding:'utf8'});assert.equal(archives.status,0,archives.stderr);
 for(const [name,success] of [['good.zip',true],['bad.zip',false],['bad.tar',false]]){
 const dest=path.join(temp,name+'-out');fs.mkdirSync(dest);
 const r=spawnSync('python3',[path.join(here,'extract-archive.py'),path.join(temp,name),dest],{encoding:'utf8'});assert.equal(r.status===0,success,r.stderr);
 if(!success)assert.deepEqual(fs.readdirSync(dest),[]);
 }
 assert.equal(fs.existsSync(path.join(temp,'escape')),false);
 const library=path.join(root,'library');fs.cpSync(path.join(here,'library'),library,{recursive:true});trustedLibrary(library);
 const script=path.join(library,'tools/find-docs.py');fs.appendFileSync(script,'\nraise RuntimeError("must not execute")\n');assert.throws(()=>trustedLibrary(library),/Modified documentation tool/);assert.match(fs.readFileSync(script,'utf8'),/must not execute/);
 fs.symlinkSync(outside,path.join(root,'agent-skills'));assert.throws(()=>privateDirectory(root,'agent-skills',true),/Private directory replaced/);fs.unlinkSync(path.join(root,'agent-skills'));
 const source=path.join(temp,'source-skill');fs.mkdirSync(source);fs.writeFileSync(path.join(source,'SKILL.md'),'fixture');
 const dest=path.join(root,'agent-skills'),copy=fs.cpSync;
 fs.cpSync=()=>{throw Error('simulated copy interruption');};try{assert.throws(()=>missingSkill(source,dest,'fixture'),/copy interruption/);}finally{fs.cpSync=copy;}
 assert.equal(fs.existsSync(path.join(dest,'fixture')),false);missingSkill(source,dest,'fixture');fs.writeFileSync(path.join(dest,'fixture/local'),'preserve');missingSkill(source,dest,'fixture');assert.equal(fs.readFileSync(path.join(dest,'fixture/local'),'utf8'),'preserve');
 console.log('PASS: official source boundary, owned-root guard, repeat verification, local changes preserved, atomic hash-failure cleanup, ZIP traversal and tar symlink escape refusal.');
}finally{fs.rmSync(temp,{recursive:true,force:true});}
