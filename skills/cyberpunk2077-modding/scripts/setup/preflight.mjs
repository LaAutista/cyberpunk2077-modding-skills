#!/usr/bin/env node
// Read-only discovery: inspect bytes/receipts, never execute discovered candidates.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {hash,verify} from './provision.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const exists=p=>{try{return fs.statSync(p).isFile();}catch{return false;}};
export function inspect(component,file,expected){
 const row={component,path:file??null,status:'missing',compatibility:'unknown'};
 if(file&&exists(file)){row.sha256=hash(file);row.status=expected?(row.sha256===expected?'present':'incompatible'):'unknown';row.compatibility=row.status==='present'?'recorded identity':'requires validation';}
 return row;
}
function executable(name){return (process.env.PATH??'').split(path.delimiter).map(d=>path.join(d,name)).find(p=>exists(p));}
export function peVersion(file){
 const bytes=fs.readFileSync(file);if(bytes.length<64||bytes.toString('ascii',0,2)!=='MZ')return null;const pe=bytes.readUInt32LE(60);if(pe+4>bytes.length||bytes.readUInt32LE(pe)!==0x4550)return null;const signature=Buffer.from([0xbd,0x04,0xef,0xfe,0x00,0x00,0x01,0x00]);
 const offset=bytes.indexOf(signature);if(offset<0||offset+16>bytes.length)return null;
 const ms=bytes.readUInt32LE(offset+8),ls=bytes.readUInt32LE(offset+12);return [ms>>>16,ms&65535,ls>>>16,ls&65535].join('.');
}
function gameCandidates(){
 const home=os.homedir(),steam=[path.join(home,'.local/share/Steam'),path.join(home,'.steam/steam')];
 if(process.env['ProgramFiles(x86)'])steam.push(path.join(process.env['ProgramFiles(x86)'],'Steam'));
 const libraries=new Set(steam);
 for(const root of steam){const vdf=path.join(root,'steamapps/libraryfolders.vdf');if(!exists(vdf))continue;for(const m of fs.readFileSync(vdf,'utf8').matchAll(/"path"\s+"([^"\n]+)"/g))libraries.add(m[1].replaceAll('\\\\','\\'));}
 const candidates=[process.env.CP2077_GAME,...[...libraries].map(p=>path.join(p,'steamapps/common/Cyberpunk 2077'))].filter(Boolean);
 return [...new Set(candidates)].filter(p=>exists(path.join(p,'bin/x64/Cyberpunk2077.exe')));
}
export function diagnosticDependencies(skillsRoot){
 const manifest=JSON.parse(fs.readFileSync(path.join(here,'../comparison/diagnostic-dependencies.json')));
 const helpers=Object.entries(manifest.helpers).map(([name,expected])=>{
  const file=path.join(skillsRoot,expected.relativePath),actual=exists(file)?hash(file):null;
  return {dependency:name,path:file,status:actual===null?'missing':actual===expected.sha256?'tested-revision':'mismatch',sha256:actual,expectedSHA256:expected.sha256,expectedRevision:expected.revision};
 });
 return {helpers,runtimes:Object.entries(manifest.runtimes).map(([name,versions])=>({dependency:name,status:'unknown',testedVersions:versions})),scope:'Read-only helper identities; the diagnostic itself checks actual Blender/NumPy before import'};
}
export function discover(config={},project,root,source,diagnosticsRoot){
 const evidence=JSON.parse(fs.readFileSync(path.join(here,'evidence.json'))).observedFiles,rows=[];
 const add=(key,group,fallback,expected)=>{const row=inspect(key,config[key]??fallback,expected);row.group=group;rows.push(row);return row;};
 for(const tool of ['node','git','bash','jq','magick','python3','cmake','c++','make','wine','wineserver'])add(tool,['cmake','c++','make','wine','wineserver'].includes(tool)?'host-task-specific':'baseline',executable(tool));
 for(const key of ['wk-linux','wk-wine','wk-red4','runtime']){
  const e=evidence[key];if(project&&e)add(key,'observed-existing',path.join(project,e.source),e.sha256);
 }
 if(root){
  for(const [component,name,file] of [['sdk','dotnet-sdk','dotnet'],['runtime','dotnet-runtime','dotnet'],['wk-linux','wk-linux','WolvenKit.CLI.dll'],['wk-wine','wk-wine','WolvenKit.CLI.exe'],['cue4parse','cue4parse','CUE4Parse/CUE4Parse.csproj'],['ron-extract','ron-extract','RonExtract.dll'],['oodle','oodle','lib/liboodle-data-shared.so'],['ueformat','ueformat','plugins/blender/io_scene_ueformat/__init__.py'],['blender','blender','blender'],['blender-python','blender-python','zstandard/__init__.py']]){
   const target=path.join(root,'tools',name),row=add(component,'isolated-tools',path.join(target,file));
   if(fs.existsSync(target))try{const r=JSON.parse(fs.readFileSync(path.join(target,'.component-receipt.json')));verify(target,r.recipe);row.status='present';row.compatibility='verified recipe file tree; workflow smoke separate';row.recipe=r.recipe;}catch(error){row.status='incompatible';row.reason=error.message;}
  }
  add('reverse-engineer-anything','optional',path.join(root,'agent-skills/reverse-engineer-anything/SKILL.md'));
 }else add('reverse-engineer-anything','optional',path.join(os.homedir(),'.agents/skills/reverse-engineer-anything/SKILL.md'));
 for(const key of ['mapping','game-executable','fmod-dll','fmodstudio-dll','windows-sdk','redscript-compiler'])add(key,'supplied-or-task-specific',undefined,key==='mapping'&&source?JSON.parse(fs.readFileSync(path.join(here,'evidence.json'))).dependencies.mapping.sha256:undefined);
 for(const key of ['RED4ext','redscript','Codeware','ArchiveXL','TweakXL','CET','AudioXL'])add(key,'runtime-framework');
 add('blender-mcp','optional');
 const installations=gameCandidates();
 if(config['game-executable']&&exists(config['game-executable']))installations.push(path.resolve(config['game-executable'],'../../..'));
 const games=[...new Set(installations)].map(directory=>{const file=path.join(directory,'bin/x64/Cyberpunk2077.exe');return {directory,executable:file,version:peVersion(file),sha256:hash(file),compatibility:'not inferred from version alone'};});
 const osRelease=fs.existsSync('/etc/os-release')?Object.fromEntries(fs.readFileSync('/etc/os-release','utf8').split('\n').filter(l=>/^(ID|ID_LIKE|PRETTY_NAME)=/.test(l)).map(l=>{const i=l.indexOf('=');return [l.slice(0,i),l.slice(i+1).replaceAll('\"','')];})):{};
 const report={schema:2,gameInstallations:games,distribution:osRelease,platform:process.platform,architecture:process.arch,support:process.platform==='linux'&&process.arch==='x64'?'Linux x86_64 provisioning supported; see validation limits':'discovery only; provisioning unsupported',components:rows,notes:['Unknown means a file was found without a verified identity.','No candidate executable ran. Receipt checks are read-only; mutable Wine state and gameplay need separate tests.','Only select frameworks and source dependencies required by the task. Blender MCP is optional.']};
 if(source){const adapter=JSON.parse(fs.readFileSync(path.join(here,'sources',source+'.json')));report.sourceAdapter=adapter;report.sourceReadiness=adapter.required.every(key=>rows.some(r=>r.component===key&&r.status==='present'))?'required identities verified; execution gates separate':'requirements missing or unverified';}
 if(diagnosticsRoot)report.diagnosticDependencies=diagnosticDependencies(diagnosticsRoot);
 return report;
}
export function main(){
 const args=process.argv.slice(2);let config={},project,root,source,diagnosticsRoot,strict=false;
 while(args.length){const flag=args.shift();if(flag==='--config')config=JSON.parse(fs.readFileSync(args.shift()));else if(flag==='--project')project=args.shift();else if(flag==='--root')root=args.shift();else if(flag==='--source')source=args.shift();else if(flag==='--diagnostics-root')diagnosticsRoot=args.shift();else if(flag==='--strict')strict=true;else throw Error('Unknown option '+flag);}
 if(!config||Array.isArray(config)||!Object.values(config).every(x=>typeof x==='string'))throw Error('Config must map component names to file paths');
 if(source&&!['ron-hk416'].includes(source))throw Error('Unknown source adapter');
 const report=discover(config,project,root,source,diagnosticsRoot);console.log(JSON.stringify(report,null,2));
 const required=source?report.sourceAdapter.required:['sdk','runtime','wk-linux'];
 if(strict&&required.some(key=>!report.components.some(r=>r.component===key&&r.status==='present')))process.exitCode=1;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))try{main();}catch(e){console.error(e.message);process.exitCode=2;}
