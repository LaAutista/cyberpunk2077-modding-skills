#!/usr/bin/env node
// Agent-neutral, isolated provisioning. All external sources are pinned in local manifests.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {Readable} from 'node:stream';
import {pipeline} from 'node:stream/promises';

export const here=path.dirname(fileURLToPath(import.meta.url));
const skill=fs.existsSync(path.join(here,'../../SKILL.md'))?path.resolve(here,'../..'):path.join(path.dirname(here),'skills/cyberpunk2077-modding');
const repo=path.dirname(skill);
const downloads=JSON.parse(fs.readFileSync(path.join(here,'downloads.json')));
const hosts=new Set(['github.com','release-assets.githubusercontent.com','objects.githubusercontent.com','builds.dotnet.microsoft.com','download.blender.org','registry.npmjs.org']);
export function checkedURL(value){const u=new URL(value);if(u.protocol!=='https:'||!hosts.has(u.hostname)||u.username||u.password)throw Error('Unrecognized source: '+value);return u;}
export function hash(file,algorithm='sha256'){return crypto.createHash(algorithm).update(fs.readFileSync(file)).digest('hex');}
const json=file=>JSON.parse(fs.readFileSync(file,'utf8'));
const writeJSON=(file,value)=>fs.writeFileSync(file,JSON.stringify(value,null,2)+'\n',{flag:'wx'});
const quote=value=>"'"+String(value).replaceAll("'","'\\''")+"'";
const exists=file=>{try{fs.lstatSync(file);return true;}catch(e){if(e.code==='ENOENT')return false;throw e;}};
const canonical=value=>JSON.stringify(value&&typeof value==='object'?(Array.isArray(value)?value.map(v=>JSON.parse(canonical(v))):Object.fromEntries(Object.keys(value).sort().map(k=>[k,JSON.parse(canonical(value[k]))]))):value);

export function privateDirectory(root,relative,create=false){
 const target=path.resolve(root,relative),rel=path.relative(root,target);
 if(rel.startsWith('..')||path.isAbsolute(rel))throw Error('Directory escapes tool root');
 let current=root;
 for(const part of rel.split(path.sep).filter(Boolean)){
  current=path.join(current,part);
  if(exists(current)){const s=fs.lstatSync(current);if(s.isSymbolicLink()||!s.isDirectory())throw Error('Private directory replaced; preserved: '+current);}
  else if(create)fs.mkdirSync(current);
 }
 return target;
}
export function noLinks(directory){
 if(fs.lstatSync(directory).isSymbolicLink())throw Error('Symlink in private library/skill; preserved: '+directory);
 for(const entry of fs.readdirSync(directory,{withFileTypes:true})){
  const file=path.join(directory,entry.name);
  if(entry.isSymbolicLink())throw Error('Symlink in private library/skill; preserved: '+file);
  if(entry.isDirectory())noLinks(file);
 }
}
export function trustedLibrary(library){
 noLinks(library);
 for(const name of fs.readdirSync(path.join(here,'library/tools'))){
  if(!name.endsWith('.py'))continue;
  const actual=path.join(library,'tools',name);
  if(!exists(actual)||!fs.lstatSync(actual).isFile()||hash(actual)!==hash(path.join(here,'library/tools',name)))throw Error('Modified documentation tool preserved; refusing execution: '+actual);
 }
 const expected=new Map(json(path.join(here,'library/docs/repository-manifest.json')).map(r=>[r.name,r]));
 for(const record of json(path.join(library,'docs/repository-manifest.json'))){
  const original=expected.get(record.name);
  if(!original||['remote','commit','path'].some(k=>record[k]!==original[k]))throw Error('Modified repository locator preserved; refusing acquisition: '+record.name);
 }
}
export function missingSkill(source,dest,name){
 privateDirectory(path.dirname(dest),path.basename(dest),true);
 const target=path.join(dest,name);
 if(exists(target)){console.log('preserved existing skill',name);return;}
 noLinks(source);
 const stage=fs.mkdtempSync(path.join(path.dirname(dest),'.stage-skill-'));
 try{const copy=path.join(stage,name);fs.cpSync(source,copy,{recursive:true,filter:p=>path.basename(p)!=='__pycache__'});if(exists(target))throw Error('Concurrent skill install; preserved');fs.renameSync(copy,target);}
 finally{fs.rmSync(stage,{recursive:true,force:true});}
}

export function tree(directory){
 const result={};
 function walk(dir){for(const name of fs.readdirSync(dir).sort()){
  if(name==='.git'||name==='__pycache__'||name==='.component-receipt.json')continue;
  const p=path.join(dir,name),s=fs.lstatSync(p),key=path.relative(directory,p);
  if(s.isSymbolicLink()){const target=fs.readlinkSync(p),resolved=path.resolve(path.dirname(p),target);if(path.relative(directory,resolved).startsWith('..')||path.isAbsolute(target))throw Error('Escaping symlink: '+key);result[key]={link:target};}
  else if(s.isDirectory())walk(p);
  else if(s.isFile())result[key]={sha256:hash(p),executable:!!(s.mode&0o111)};
  else throw Error('Unsupported installed file: '+key);
 }}walk(directory);return result;
}
export function verify(directory,recipe){
 if(fs.lstatSync(directory).isSymbolicLink()||!fs.lstatSync(directory).isDirectory())throw Error('Component directory was replaced; preserved: '+directory);
 const receipt=json(path.join(directory,'.component-receipt.json'));
 if(receipt.recipe!==recipe)throw Error('Existing component belongs to a different recipe; preserved: '+directory);
 if(canonical(tree(directory))!==canonical(receipt.files))throw Error('Local modifications or missing files; preserved: '+directory);
 return receipt;
}
function finish(stage,target,recipe,details){
 const receipt={schema:1,recipe,details,files:tree(stage)};
 writeJSON(path.join(stage,'.component-receipt.json'),receipt);
 if(exists(target))throw Error('Concurrent destination appeared; preserved: '+target);
 fs.renameSync(stage,target);return target;
}
function command(exe,args,env={},options={}){
 const result=spawnSync(exe,args,{cwd:options.cwd??repo,env:{...process.env,...env},encoding:'utf8',timeout:options.timeout??600000,maxBuffer:32*1024*1024});
 if(options.log)fs.writeFileSync(options.log,(result.stdout??'')+(result.stderr??''));
 if(result.error||result.status!==0)throw Error(`${exe} ${args[0]??''} failed (${result.status}): ${(result.stderr??result.stdout??'').slice(-3500)} ${result.error??''}`);
 return result.stdout.trim();
}
export async function acquire(item,cache){
 checkedURL(item.url);fs.mkdirSync(cache,{recursive:true});const target=path.join(cache,item.id);
 if(exists(target)){if(fs.lstatSync(target).isSymbolicLink()||!fs.statSync(target).isFile()||hash(target,item.algorithm)!==item.hash)throw Error('Existing archive differs; preserved: '+target);return target;}
 const temp=path.join(cache,'.download-'+crypto.randomUUID());
 try{
  let url=item.url,response;
  for(let redirects=0;redirects<8;redirects++){
   checkedURL(url);response=await fetch(url,{redirect:'manual',signal:AbortSignal.timeout(120000)});
   if(response.status>=300&&response.status<400){const next=response.headers.get('location');await response.body?.cancel();url=new URL(next,url).href;continue;}
   if(!response.ok)throw Error('Download HTTP '+response.status+': '+url);break;
  }
  if(!response?.ok)throw Error('Too many redirects');
  await pipeline(Readable.fromWeb(response.body),fs.createWriteStream(temp,{flags:'wx',mode:0o600}));
  if(hash(temp,item.algorithm)!==item.hash)throw Error('Downloaded archive hash mismatch: '+item.id);
  try{fs.linkSync(temp,target);}catch(e){if(e.code!=='EEXIST')throw e;if(fs.lstatSync(target).isSymbolicLink()||!fs.statSync(target).isFile()||hash(target,item.algorithm)!==item.hash)throw Error('Concurrent archive differs; preserved');}
  return target;
 }finally{fs.rmSync(temp,{force:true});}
}
async function archive(root,id,component){
 const item=downloads.find(x=>x.id===id);if(!item)throw Error('Unknown pinned archive '+id);
 const target=path.join(root,'tools',component),recipe='archive:'+item.algorithm+':'+item.hash+':strip'+(item.strip??0);
 if(exists(target)){verify(target,recipe);console.log('verified existing',component);return target;}
 const source=await acquire(item,path.join(root,'cache'));const stage=fs.mkdtempSync(path.join(root,'.stage-'+component+'-'));
 try{
  command('python3',[path.join(here,'extract-archive.py'),source,stage,'--strip',String(item.strip??0)]);
  return finish(stage,target,recipe,{url:item.url,archiveHash:item.hash});
 }finally{fs.rmSync(stage,{recursive:true,force:true});}
}
function environment(root){
 for(const dir of ['state/dotnet','state/nuget/packages','state/nuget/http','state/nuget/plugins','state/pip-cache','state/git-template'])privateDirectory(root,dir,true);
 if(fs.readdirSync(path.join(root,'state/git-template')).length)throw Error('Private Git template modified; preserved');
 return {
 DOTNET_ROOT:path.join(root,'tools/dotnet-sdk'),DOTNET_MULTILEVEL_LOOKUP:'0',DOTNET_ROLL_FORWARD:'LatestPatch',DOTNET_CLI_TELEMETRY_OPTOUT:'1',DOTNET_SKIP_FIRST_TIME_EXPERIENCE:'1',DOTNET_NOLOGO:'1',
 DOTNET_CLI_HOME:path.join(root,'state/dotnet'),NUGET_PACKAGES:path.join(root,'state/nuget/packages'),NUGET_HTTP_CACHE_PATH:path.join(root,'state/nuget/http'),NUGET_PLUGINS_CACHE_PATH:path.join(root,'state/nuget/plugins'),NUGET_PLUGIN_PATHS:'',NUGET_CREDENTIALPROVIDER_SESSIONTOKENCACHE_ENABLED:'false',NETRC:path.join(root,'state/empty-netrc'),
 GIT_CONFIG_GLOBAL:'/dev/null',GIT_CONFIG_NOSYSTEM:'1',GIT_TERMINAL_PROMPT:'0',GIT_CONFIG_COUNT:'0',GIT_CONFIG_PARAMETERS:'',GIT_TEMPLATE_DIR:path.join(root,'state/git-template'),
 PYTHONDONTWRITEBYTECODE:'1',PIP_CONFIG_FILE:'/dev/null',PIP_EXTRA_INDEX_URL:'',PIP_INDEX_URL:'https://pypi.org/simple',PIP_TRUSTED_HOST:'',PIP_CACHE_DIR:path.join(root,'state/pip-cache'),PIP_NO_INPUT:'1',PIP_DISABLE_PIP_VERSION_CHECK:'1',PYTHONNOUSERSITE:'1',
};}
const git=(args,env,cwd)=>command('git',['-c','credential.helper=','-c','core.hooksPath=/dev/null',...args],env,{cwd});
async function source(root,name,remote,commit,patch){
 const recipe='git:'+remote+'@'+commit+(patch?':'+hash(patch):'');const target=path.join(root,'tools',name),env=environment(root);
 if(exists(target)){verify(target,recipe);if(git(['-C',target,'rev-parse','HEAD'],env)!==commit)throw Error('Source HEAD changed; preserved');return target;}
 const parent=fs.mkdtempSync(path.join(root,'.stage-source-'));const stage=path.join(parent,'source');
 try{
  git(['clone','--no-checkout',remote,stage],env);
  git(['-C',stage,'checkout','--detach',commit],env);
  if(name==='cue4parse')git(['-C',stage,'submodule','update','--init','--recursive'],env);
  if(git(['-C',stage,'rev-parse','HEAD'],env)!==commit)throw Error('Wrong source commit');
  if(patch){git(['-C',stage,'apply','--check',patch],env);git(['-C',stage,'apply',patch],env);}
  return finish(stage,target,recipe,{remote,commit,patchSHA256:patch?hash(patch):null,submodules:name==='cue4parse'?git(['-C',stage,'submodule','status','--recursive'],env):null});
 }finally{fs.rmSync(parent,{recursive:true,force:true});}
}
function generated(file,text,mode=0o644){
 if(exists(file)){if(fs.readFileSync(file,'utf8')!==text)throw Error('Existing generated configuration differs; preserved: '+file);return;}
 fs.writeFileSync(file,text,{flag:'wx',mode});
}
async function foundation(root){
 for(const [id,name] of [['dotnet-sdk-10.0.400-linux-x64.tar.gz','dotnet-sdk'],['dotnet-runtime-10.0.12-linux-x64.tar.gz','dotnet-runtime'],['WolvenKit.ConsoleLinux-9.0.1.zip','wk-linux']])await archive(root,id,name);
 const env=environment(root),sdk=path.join(root,'tools/dotnet-sdk/dotnet'),runtime=path.join(root,'tools/dotnet-runtime/dotnet');
 if(command(sdk,['--version'],env)!=='10.0.400')throw Error('SDK identity mismatch');
 if(!command(runtime,['--list-runtimes'],env).includes('Microsoft.NETCore.App 10.0.12 '))throw Error('Runtime identity mismatch');
 generated(path.join(root,'bin/wolvenkit-cli'),'#!/usr/bin/env bash\nset -euo pipefail\nexport DOTNET_ROOT='+quote(path.join(root,'tools/dotnet-runtime'))+'\nexec '+quote(runtime)+' '+quote(path.join(root,'tools/wk-linux/WolvenKit.CLI.dll'))+' "$@"\n',0o755);
 command(path.join(root,'bin/wolvenkit-cli'),['--help'],env,{log:path.join(root,'state/wolvenkit-help.log')});
}
async function ron(root){
 await foundation(root);
 const cue=await source(root,'cue4parse','https://github.com/FabianFG/CUE4Parse.git','990d4d7d4e0340a75a14323436d55568f1415e00',path.join(skill,'scripts/ron-source/cue4parse-local-corrections.patch'));
 const oodle=await archive(root,'oodle-gcc-x64-release.zip','oodle');
 if(hash(path.join(oodle,'lib/liboodle-data-shared.so'))!=='f21d70299bbe873f63e8aef778b30f4dee6dec1fc09140c185caf1f8d153f771')throw Error('Oodle library hash mismatch');
 const helper=path.join(root,'tools/ron-extract'),recipe='ron-build:'+hash(path.join(cue,'.component-receipt.json'))+':'+hash(path.join(skill,'scripts/ron-source/Program.cs'))+':project'+hash(path.join(skill,'scripts/ron-source/RonExtract.csproj'))+':locks'+hash(path.join(here,'ron-locks/helper.json'));
 if(exists(helper))verify(helper,recipe);
 else{
 // Build only in private state: keep immutable source snapshots and install receipts stable.
 const work=fs.mkdtempSync(path.join(root,'state/ron-build-'));
 const buildCue=path.join(work,'CUE4Parse');fs.cpSync(cue,buildCue,{recursive:true,filter:p=>path.basename(p)!=='.git'&&path.basename(p)!=='.component-receipt.json'});
 const src=path.join(work,'helper');fs.mkdirSync(src);
 for(const name of ['Program.cs','RonExtract.csproj'])fs.copyFileSync(path.join(skill,'scripts/ron-source',name),path.join(src,name));
 fs.writeFileSync(path.join(work,'global.json'),JSON.stringify({sdk:{version:'10.0.400',rollForward:'disable'}}));
 const config=path.join(work,'NuGet.Config');fs.writeFileSync(config,'<configuration><packageSources><clear/><add key="nuget.org" value="https://api.nuget.org/v3/index.json"/></packageSources><packageSourceCredentials/><disabledPackageSources><clear/></disabledPackageSources></configuration>');
 fs.copyFileSync(path.join(here,'ron-locks/helper.json'),path.join(src,'packages.lock.json'));
 for(const project of ['CUE4Parse','CUE4Parse-Conversion'])fs.copyFileSync(path.join(here,'ron-locks',project+'.json'),path.join(buildCue,project,'packages.lock.json'));
 const env=environment(root),sdk=path.join(root,'tools/dotnet-sdk/dotnet');
 command(sdk,['restore',path.join(src,'RonExtract.csproj'),'--configfile',config,'--use-lock-file','--locked-mode','-p:Cue4ParseRoot='+buildCue],env,{cwd:work,log:path.join(root,'state/ron-restore.log')});
 command(sdk,['build',path.join(src,'RonExtract.csproj'),'-c','Release','--no-restore','-m:1','-nr:false','-p:Cue4ParseRoot='+buildCue],env,{cwd:work,log:path.join(root,'state/ron-build.log')});
 const output=path.join(src,'bin/Release/net10.0');
 if(!fs.existsSync(path.join(output,'CUE4Parse-Natives.so')))throw Error('Native ACL build missing; see isolated build log');
 command(sdk,[path.join(output,'RonExtract.dll'),'--help'],{...env,RON_OODLE:path.join(oodle,'lib/liboodle-data-shared.so')},{cwd:work,log:path.join(root,'state/ron-help.log')});
 fs.copyFileSync(path.join(src,'packages.lock.json'),path.join(output,'packages.lock.json'));
 finish(output,helper,recipe,{cueCommit:'990d4d7d4e0340a75a14323436d55568f1415e00',sdk:'10.0.400',hostToolchain:{cmake:command('cmake',['--version']).split('\n')[0],cxx:command('c++',['--version']).split('\n')[0]},nativeACL:'built; source ACL clip not tested',nugetLock:hash(path.join(src,'packages.lock.json'))});
 }
 const sdk=path.join(root,'tools/dotnet-sdk/dotnet');
 generated(path.join(root,'bin/ron-extract'),'#!/usr/bin/env bash\nset -euo pipefail\nexport RON_OODLE='+quote(path.join(oodle,'lib/liboodle-data-shared.so'))+'\nexec '+quote(sdk)+' '+quote(path.join(helper,'RonExtract.dll'))+' "$@"\n',0o755);
}
async function wine(root){
 await foundation(root);
 await archive(root,'WolvenKit.Console-9.0.1.zip','wk-console');await archive(root,'WolvenKit-9.0.1.zip','wk-desktop');
 const manifest=json(path.join(here,'wine-assembly.json')),target=path.join(root,'tools/wk-wine'),recipe='wine-assembly:'+hash(path.join(here,'wine-assembly.json'));
 if(exists(target))verify(target,recipe);
 else{
  const stage=fs.mkdtempSync(path.join(root,'.stage-wine-'));
  try{
   for(const [name,entry] of Object.entries(manifest.files)){const file=path.join(root,'tools',entry.source==='WolvenKit-9.0.1'?'wk-desktop':'wk-console',name);if(hash(file)!==entry.sha256)throw Error('Assembly source hash mismatch: '+name);fs.copyFileSync(file,path.join(stage,name));}
   for(const [name,entry] of Object.entries(manifest.metadata)){
    const file=path.join(root,'tools/wk-console',name);if(hash(file)!==entry.sourceSHA256)throw Error('Metadata source mismatch');let document=json(file);
    for(const change of entry.delta){let ref=document;for(const key of change.path.slice(0,-1))ref=ref[key];ref[change.path.at(-1)]=change.value;}
    for(const parts of entry.delete){let ref=document;for(const key of parts.slice(0,-1))ref=ref[key];delete ref[parts.at(-1)];}
    if(crypto.createHash('sha256').update(canonical(document)).digest('hex')!==entry.targetCanonicalSHA256)throw Error('Metadata reconstruction mismatch');
    fs.writeFileSync(path.join(stage,name),JSON.stringify(document,null,2)+'\n');
   }finish(stage,target,recipe,{assemblies:456});
  }finally{fs.rmSync(stage,{recursive:true,force:true});}
 }
 // Prefixes are mutable runtime state, never mixed with the user's existing prefixes.
 const prefix=path.join(root,'state/wine-prefix-headless-v2'),marker=path.join(root,'state/wine-prefix-ready.json');
 const env={...environment(root),WINEPREFIX:prefix,WINEARCH:'win64',WINEDEBUG:'-all',WINEDLLOVERRIDES:'winemenubuilder.exe=d',DISPLAY:'',WAYLAND_DISPLAY:'',DOTNET_PROCESSOR_COUNT:'2',ALSOFT_DRIVERS:'null'};
 if(!exists(marker)){
  if(exists(prefix))throw Error('Incomplete/unknown prefix preserved: '+prefix+'; inspect and move aside before retry');
  command('wineboot',['--init'],env,{log:path.join(root,'state/wineboot.log'),timeout:180000});command('wineserver',['--wait'],env,{timeout:60000});
  command('wine',['reg','add','HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem','/v','LongPathsEnabled','/t','REG_DWORD','/d','1','/f'],env,{log:path.join(root,'state/wine-long-paths.log')});
  command('wine',[path.join(target,'WolvenKit.CLI.exe'),'--help'],env,{log:path.join(root,'state/wine-wolvenkit-help.log'),timeout:120000});
  writeJSON(marker,{prefix,arch:'win64',wine:command('wine',['--version'],env),recipe,helpPassed:true});
 }else{
  const record=json(marker);
  if(fs.lstatSync(marker).isSymbolicLink()||record.recipe!==recipe||record.prefix!==prefix||record.arch!=='win64')throw Error('Prefix marker differs; preserved');
  privateDirectory(root,path.relative(root,prefix));
  if(!exists(prefix))throw Error('Recorded prefix is missing; select a new root or inspect recovery state');
 }
 generated(path.join(root,'bin/wolvenkit-wine'),'#!/usr/bin/env bash\nset -euo pipefail\nexport WINEPREFIX='+quote(prefix)+' WINEARCH=win64 WINEDEBUG=-all WINEDLLOVERRIDES="winemenubuilder.exe=d"\nexec wine '+quote(path.join(target,'WolvenKit.CLI.exe'))+' "$@"\n',0o755);
}
async function blender(root){
 const binary=await archive(root,'blender-5.2.3-linux-x64.tar.xz','blender');
 const ue=await source(root,'ueformat','https://github.com/h4lfheart/UEFormat.git','d858fe38b2b5b8c63ac4b7481b4386ebfabbf935');
 const pythons=fs.readdirSync(binary).filter(x=>/^\d+\.\d+$/.test(x)).flatMap(v=>{const p=path.join(binary,v,'python/bin');return fs.existsSync(p)?fs.readdirSync(p).filter(n=>/^python3\.\d+$/.test(n)).map(n=>path.join(p,n)):[];});
 if(pythons.length!==1)throw Error('Cannot identify bundled Blender Python');
 const target=path.join(root,'tools/blender-python'),recipe='ueformat-python:'+hash(path.join(here,'blender-requirements.txt'));
 if(exists(target))verify(target,recipe);
 else{
  const stage=fs.mkdtempSync(path.join(root,'.stage-blender-python-')),env=environment(root);
  try{
   command('python3',['-m','pip','--python',pythons[0],'install','--no-user','--no-deps','--only-binary=:all:','--require-hashes','--index-url','https://pypi.org/simple','--target',stage,'-r',path.join(here,'blender-requirements.txt')],env,{log:path.join(root,'state/blender-pip.log')});
   finish(stage,target,recipe,{zstandard:'0.25.0',ueformat:'d858fe38b2b5b8c63ac4b7481b4386ebfabbf935'});
  }finally{fs.rmSync(stage,{recursive:true,force:true});}
 }
 generated(path.join(root,'bin/blender'),'#!/usr/bin/env bash\nset -euo pipefail\nexport BLENDER_USER_CONFIG='+quote(path.join(root,'state/blender/config'))+' BLENDER_USER_SCRIPTS='+quote(path.join(root,'state/blender/scripts'))+' ALSOFT_DRIVERS=null\nexec '+quote(path.join(binary,'blender'))+' "$@"\n',0o755);
 const smoke=path.join(root,'state/blender-smoke.py');
 generated(smoke,'import sys, json, bpy, numpy\nsys.path[:0]='+JSON.stringify([target,path.join(ue,'plugins/blender')])+'\nimport zstandard\nfrom io_scene_ueformat.importer.import_context import UEFormatImport\nfrom io_scene_ueformat.options import UEModelOptions, UEAnimOptions\nprint("CP_SETUP_BLENDER_OK", json.dumps({"blender":bpy.app.version_string,"python":sys.version,"zstandard":zstandard.__version__}))\n');
 command(path.join(root,'bin/blender'),['--background','--factory-startup','--python-exit-code','1','--python',smoke],environment(root),{timeout:120000,log:path.join(root,'state/blender-smoke.log')});
}
async function audio(root){
 await wine(root);
 const compiler=await archive(root,'llvm-mingw-20260922-ucrt-ubuntu-22.04-x86_64.tar.xz','llvm-mingw');
 const source=path.join(skill,'scripts/source-audio/fmod-events.c'),target=path.join(root,'tools/source-fmod'),recipe='source-fmod:'+hash(source)+':'+hash(path.join(compiler,'.component-receipt.json'));
 if(exists(target)){verify(target,recipe);return;}
 const stage=fs.mkdtempSync(path.join(root,'.stage-fmod-'));
 try{
  command(path.join(compiler,'bin/x86_64-w64-mingw32-gcc'),['-O2','-Wall',source,'-o',path.join(stage,'fmod-events.exe')],environment(root),{log:path.join(root,'state/fmod-build.log')});
  finish(stage,target,recipe,{sourceSHA256:hash(source),fmodAPI:'2.03.10',toolchain:'llvm-mingw20260922; public Windows C API; no FMOD SDK/DLL included'});
 }finally{fs.rmSync(stage,{recursive:true,force:true});}
}
async function docs(root){
 const env=environment(root),requirements=path.join(here,'library/requirements.txt');
 const library=privateDirectory(root,'library');
 if(!exists(library))fs.cpSync(path.join(here,'library'),library,{recursive:true,filter:p=>path.basename(p)!=='__pycache__'});
 trustedLibrary(library);
 const venv=path.join(root,'state/docs-venv'),recipe='docs-parser:'+hash(requirements);
 if(exists(venv))verify(venv,recipe);
 else{
  command('python3',['-m','venv','--copies',venv],env);
  command(path.join(venv,'bin/python'),['-m','pip','install','--no-deps','--only-binary=:all:','--require-hashes','--index-url','https://pypi.org/simple','-r',requirements],env,{log:path.join(root,'state/docs-pip.log')});
  writeJSON(path.join(venv,'.component-receipt.json'),{schema:1,recipe,files:tree(venv)});
 }
 const python=path.join(venv,'bin/python'),tool=name=>path.join(library,'tools',name);
 if(exists(path.join(library,'docs/source-manifest.json')))command(python,[tool('verify-docs.py')],env);
 command(python,[tool('sync-docs.py'),'--sections','wolvenkit'],env,{log:path.join(root,'state/docs-sync.log')});
 command(python,[tool('verify-docs.py')],env,{log:path.join(root,'state/docs-verify.log')});
 command(python,[tool('restore-repositories.py'),'--name','RED4ext','--name','RED4ext.SDK','--apply'],env,{log:path.join(root,'state/docs-repositories.log')});
 command(python,[tool('build-doc-index.py')],env,{log:path.join(root,'state/docs-index.log')});
 command(python,[tool('find-docs.py'),'animation','--json'],env,{log:path.join(root,'state/docs-search.json')});
}
async function skills(root){
 const dest=privateDirectory(root,'agent-skills',true);
 for(const name of ['cyberpunk2077-modding','weapon-animation-inspection']){
  missingSkill(path.join(path.dirname(skill),name),dest,name);
 }
 const target=path.join(dest,'reverse-engineer-anything');
 if(exists(target)){console.log('preserved existing REA skill');return;}
 const rea=await archive(root,'rea-agents-6.4.0.tgz','rea-package');
 const source=path.join(rea,'skills/reverse-engineer-anything');if(!fs.existsSync(path.join(source,'SKILL.md')))throw Error('Pinned REA package lacks skill');
 missingSkill(source,dest,'reverse-engineer-anything');
 console.log('installed missing REA skill; package code, MCP and engines were not executed/configured');
}
function configuration(root){
 const values={CP2077_TOOL_ROOT:root,DOTNET_SDK:path.join(root,'tools/dotnet-sdk/dotnet'),DOTNET_RUNTIME:path.join(root,'tools/dotnet-runtime/dotnet'),WOLVENKIT_ROOT:path.join(root,'tools/wk-linux'),WK_CLI:path.join(root,'bin/wolvenkit-cli'),RON_SDK:path.join(root,'tools/dotnet-sdk/dotnet'),RON_CUE:path.join(root,'tools/cue4parse'),RON_EXTRACT:path.join(root,'tools/ron-extract/RonExtract.dll'),RON_OODLE:path.join(root,'tools/oodle/lib/liboodle-data-shared.so'),BLENDER:path.join(root,'bin/blender'),UEFORMAT_ROOT:path.join(root,'tools/ueformat/plugins/blender'),BLENDER_PYTHON_DEPS:path.join(root,'tools/blender-python')};
 generated(path.join(root,'env.sh'),Object.entries(values).map(([k,v])=>'export '+k+'='+quote(v)).join('\n')+'\nexport PATH='+quote(path.join(root,'bin'))+':"$PATH"\n');
 generated(path.join(root,'paths.json'),JSON.stringify(values,null,2)+'\n');
}
export function initialize(root){
 if(!path.isAbsolute(root)||root===path.parse(root).root||fs.realpathSync(path.dirname(root))!==path.dirname(root))throw Error('Use an absolute isolated root beneath a real directory');
 if(exists(root)){
  if(fs.lstatSync(root).isSymbolicLink()||!exists(path.join(root,'.cp2077-setup.json')))throw Error('Existing unowned root preserved: '+root);
  const marker=path.join(root,'.cp2077-setup.json');
  if(fs.lstatSync(marker).isSymbolicLink()||!fs.lstatSync(marker).isFile())throw Error('Root marker replaced; preserved');
  const record=json(marker);
  if(record.schema!==1||record.root!==root||record.purpose!=='isolated Cyberpunk tools')throw Error('Unknown/moved setup root; preserved');
 }else{fs.mkdirSync(root);writeJSON(path.join(root,'.cp2077-setup.json'),{schema:1,purpose:'isolated Cyberpunk tools',root});}
 for(const dir of ['tools','cache','state','bin']){const target=path.join(root,dir);if(exists(target)&&(fs.lstatSync(target).isSymbolicLink()||!fs.lstatSync(target).isDirectory()))throw Error('Owned-root directory replaced; preserved: '+target);fs.mkdirSync(target,{recursive:true});}
 generated(path.join(root,'state/empty-netrc'),'');
}
export async function main(){
 const args=process.argv.slice(2),action=args.shift();let root,components=['foundation'],apply=false;
 while(args.length){const flag=args.shift();if(flag==='--root')root=args.shift();else if(flag==='--components')components=args.shift().split(',');else if(flag==='--apply')apply=true;else throw Error('Unknown option '+flag);}
 const allowed={foundation,ron,wine,blender,audio,docs,skills};
 if(!root||!['plan','install','verify'].includes(action)||components.some(c=>!allowed[c]))throw Error('Usage: node setup/provision.mjs plan|install|verify --root /new/private/tools [--components foundation,ron,wine,blender] [--apply]');
 if(process.platform!=='linux'||process.arch!=='x64')throw Error('Provisioning supports Linux x86_64 only; other platforms are discovery/manual routes');
 root=path.resolve(root);console.log(JSON.stringify({root,components,actions:components.map(c=>({foundation:'pinned SDK/runtime and WolvenKit native CLI',ron:'patched source + recursive dependencies, isolated NuGet/native build and Oodle',wine:'pinned console/desktop merge plus new win64 prefix and CLI smoke',blender:'portable Blender + pinned UEFormat and zstandard wheel',audio:'pinned MinGW compiler and offline source FMOD helper; game DLLs/banks remain supplied',docs:'isolated pinned parser, authoritative WolvenKit wiki and independent RED4ext/SDK snapshots',skills:'missing-only sibling skills plus official REA skill; no agent settings or MCP edits'}[c])),manual:['OS shared libraries, Wine, CMake/C++/Git/Node/Python as reported by preflight','owned game assets, matching mappings and game/SDK DLLs','game-version-specific runtime frameworks; no live profile installation'],applies:apply},null,2));
 if(action==='plan'||(action==='install'&&!apply))return;
 if(action==='verify'){
  if(!exists(path.join(root,'.cp2077-setup.json')))throw Error('No owned setup root');
  for(const name of fs.readdirSync(path.join(root,'tools'))){const target=path.join(root,'tools',name);verify(target,json(path.join(target,'.component-receipt.json')).recipe);console.log('verified',name);}return;
 }
 initialize(root);const lock=path.join(root,'.install-lock');fs.mkdirSync(lock);
 try{for(const component of components){console.log('provisioning',component);await allowed[component](root);}configuration(root);console.log('Ready: source '+path.join(root,'env.sh'));}
 finally{fs.rmdirSync(lock);}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url))main().catch(e=>{console.error(e.message);process.exitCode=1;});
