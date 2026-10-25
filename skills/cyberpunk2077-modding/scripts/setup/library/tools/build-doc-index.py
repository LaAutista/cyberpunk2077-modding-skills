#!/usr/bin/env python3
"""Build an offline, searchable reader for the local reference snapshots."""
import html,json,pathlib,re,subprocess,hashlib
from urllib.parse import urljoin,urlparse,unquote,quote
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup
ROOT=pathlib.Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'docs/source-manifest.json').read_text(encoding='utf-8'))
items=list(manifest['pages']);repos=[]
repository_manifest=ROOT/'docs/repository-manifest.json'
saved_repos={p['name']:p for p in json.loads(repository_manifest.read_text(encoding='utf-8'))} if repository_manifest.exists() else {}
portable_map=ROOT/'docs/portable-path-map.json'
portable_originals={v:k for k,v in json.loads(portable_map.read_text(encoding='utf-8')).get('paths',{}).items()} if portable_map.exists() else {}
extras=ROOT/'docs/supplemental-sources.json'
if extras.exists():items.extend(json.loads(extras.read_text(encoding='utf-8'))['pages'])
for p in sorted((ROOT/'docs/guides').glob('*.md')):
 items.append({'title':p.read_text(encoding='utf-8').splitlines()[0].lstrip('# '),'path':p.relative_to(ROOT).as_posix(),'url':p.as_uri(),'group':'Start here'})
for directory in sorted((ROOT/'docs/upstream').iterdir()):
 if not directory.is_dir():continue
 if (directory/'.git').exists():
  def git(*args):return subprocess.check_output(['git','-C',str(directory),*args],text=True).strip()
  repo={'name':directory.name,'remote':git('remote','get-url','origin'),'commit':git('rev-parse','HEAD'),'path':directory.relative_to(ROOT).as_posix()}
 elif directory.name in saved_repos:
  repo=saved_repos[directory.name]
 else:continue
 repos.append(repo)
 for p in sorted(directory.rglob('*.md')):
  if '.git' in p.parts:continue
  original=ROOT/portable_originals.get(p.relative_to(ROOT).as_posix(),p.relative_to(ROOT).as_posix())
  relative=original.relative_to(directory).as_posix();repo_url=repos[-1]['remote'].removesuffix('.git')
  if repo_url.endswith('.wiki'):url=repo_url.removesuffix('.wiki')+'/wiki/'+original.stem
  else:url=repo_url+'/blob/'+repos[-1]['commit']+'/'+relative
  items.append({'title':directory.name+' / '+relative,'path':p.relative_to(ROOT).as_posix(),'url':url,'status':'git-snapshot','sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
repository_records={**saved_repos,**{r['name']:r for r in repos}}
for record in repository_records.values():record['snapshot_present']=(ROOT/record['path']).is_dir()
(ROOT/'docs/repository-manifest.json').write_text(json.dumps(list(repository_records.values()),indent=2),encoding='utf-8')
lookup={p['url'].removesuffix('.md'):i for i,p in enumerate(items)}
local_lookup={(ROOT/p['path']).resolve().as_uri():i for i,p in enumerate(items)}
renderer=MarkdownIt('commonmark',{'html':True}).enable('table')
records=[]
for i,p in enumerate(items):
 text=(ROOT/p['path']).read_text(encoding='utf-8',errors='replace')
 text=re.split(r'^# Agent Instructions\s*$',text,flags=re.M)[0]
 text=re.sub(r'^> For the complete documentation index,.*\n\n','',text,count=1)
 body=re.sub(r'\{%.*?%\}', '',text,flags=re.S)
 if p['path'].endswith('.txt'):body='<pre>'+html.escape(body)+'</pre>'
 soup=BeautifulSoup(renderer.render(body),'html.parser')
 heading_ids={}
 for heading in soup.find_all(re.compile('^h[1-6]$')):
  slug=re.sub(r'[^\w -]','',heading.get_text().lower()).replace(' ','-')
  count=heading_ids.get(slug,0);heading_ids[slug]=count+1
  heading['id']=slug+('-'+str(count) if count else '')
 for tag in soup(['script','style','iframe','object','embed','form']):tag.decompose()
 for tag in soup.find_all(True):
  for attr in list(tag.attrs):
   if attr.lower().startswith('on') or attr.lower() in ['srcdoc','style']:del tag[attr]
  for attr in ['href','src']:
   if attr in tag.attrs:
    val=tag[attr]
    if val.strip().lower().startswith(('javascript:','data:','vbscript:')):del tag[attr];continue
    if attr=='href' and val.startswith('#'):
     tag[attr]='#p='+str(i)+'&a='+quote(val[1:])
    elif attr=='href':
     full=urljoin(p['url'],val);parsed=urlparse(full)
     key=full.split('#')[0].removesuffix('.md')
     page_id=lookup.get(key,local_lookup.get(full.split('#')[0]))
     if page_id is not None:tag[attr]='#p='+str(page_id)+('&a='+quote(parsed.fragment) if parsed.fragment else '')
     else:tag[attr]=full
    elif attr=='src':
     full=urljoin(p['url'],val)
     if full.startswith('https://github.com/') and '/blob/' in full:
      full=full.replace('https://github.com/','https://raw.githubusercontent.com/',1).replace('/blob/','/',1)
     tag[attr]=full
  if tag.name=='img':tag['loading']='lazy';tag['referrerpolicy']='no-referrer'
 group=p.get('group') or (p['path'].split('/')[3] if '/redmodding/' in p['path'] else p['path'].split('/')[2])
 # Local guide links must survive copying the whole workspace to another machine.
 for tag in soup.find_all(True):
  for attr in ['href','src']:
   val=tag.get(attr,'')
   if val.startswith(ROOT.as_uri()+'/'):tag[attr]='../'+val[len(ROOT.as_uri())+1:]
 source='../'+quote(p['path']) if p['url'].startswith(ROOT.as_uri()+'/') else p['url']
 records.append({'id':i,'title':p['title'],'group':group,'url':source,'file':'../'+p['path'],'text':text,'body':str(soup)})
errors=[e for e in manifest['errors'] if not e.get('resolved_by')]
data=json.dumps(records,ensure_ascii=False).replace('<','\\u003c')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>2077Dev Reference Library</title><style>
:root{color-scheme:dark;--bg:#11141a;--panel:#191e27;--fg:#e7ebf3;--muted:#a4b0c4;--link:#69d7e7}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui}header{padding:18px 25px;background:var(--panel);border-bottom:1px solid #344050}h1{font-size:1.7rem;margin:.2em 0}a{color:var(--link)}input,select{padding:10px;border:1px solid #46536a;border-radius:6px;color:var(--fg);background:var(--bg);font:inherit}input{width:min(550px,70%)}.layout{display:grid;grid-template-columns:340px 1fr;height:calc(100vh - 166px)}aside{overflow:auto;border-right:1px solid #344050;padding:14px}aside a{display:block;padding:8px;text-decoration:none;overflow-wrap:anywhere}aside a:hover{background:var(--panel)}article{overflow:auto;padding:25px;max-width:1100px}article img{max-width:100%;height:auto}pre{overflow:auto;background:#080b10;padding:14px;border-radius:6px}code{font-family:ui-monospace,monospace}table{border-collapse:collapse;display:block;overflow:auto}th,td{border:1px solid #455069;padding:8px}blockquote{border-left:3px solid #536985;padding-left:16px;color:var(--muted)}small,.muted{color:var(--muted)}@media(max-width:800px){.layout{grid-template-columns:1fr;height:auto}aside{max-height:250px}article{overflow:visible}} </style>
<header><h1>2077Dev Reference Library</h1><div class="muted">Offline documentation text and code · Images and external references may require internet · Current scripting home: Scripting Cyberpunk</div><input id="q" placeholder="Search titles and full text…" aria-label="Search documentation"><select id="group" aria-label="Documentation collection"><option value="">All collections</option></select> <small id="status"></small></header><div class="layout"><aside id="results"></aside><article id="page"><h2>Start here</h2><p>Select a page or search the complete local text. This reader opens directly from disk; no server is needed.</p><p><a href="source-manifest.json">Sources and coverage</a> · <a href="repository-manifest.json">Repository locators and snapshot status</a></p><p>__COUNT__ reference pages. __ERRORS__ indexed pages could not be retrieved; see source manifest. Downloading and indexing are separate from reading and understanding.</p></article></div><script>const pages=__DATA__;
const search=document.querySelector('#q'),groups=document.querySelector('#group'),results=document.querySelector('#results'),view=document.querySelector('#page');
[...new Set(pages.map(p=>p.group))].sort().forEach(g=>{let o=document.createElement('option');o.value=g;o.textContent=g;groups.append(o)});
function filter(){let terms=search.value.toLowerCase().trim().split(/\\s+/).filter(Boolean),g=groups.value;let found=pages.filter(p=>(!g||p.group===g)&&terms.every(t=>(p.title+' '+p.text).toLowerCase().includes(t)));results.replaceChildren();found.slice(0,250).forEach(p=>{let a=document.createElement('a');a.href='#p='+p.id;a.textContent=p.title;results.append(a)});document.querySelector('#status').textContent=found.length+' matches'+(found.length>250?' (first 250 shown)':'')}
function show(){let m=location.hash.match(/^#p=(\\d+)/);if(!m)return;let p=pages[Number(m[1])];if(!p)return;view.innerHTML='';let h=document.createElement('p');for(let [title,url]of [['Source',p.url],['Local Markdown',encodeURI(p.file)]]){let a=document.createElement('a');a.href=url;a.textContent=title;h.append(a,document.createTextNode(' · '))}view.append(h);let b=document.createElement('div');b.innerHTML=p.body;view.append(b);view.scrollTop=0;let anchor=new URLSearchParams(location.hash.slice(1)).get('a');if(anchor){let target=document.getElementById(anchor);if(target&&view.contains(target))target.scrollIntoView()}document.title=p.title+' — 2077Dev'}search.addEventListener('input',filter);groups.addEventListener('change',filter);window.addEventListener('hashchange',show);filter();show();</script></html>'''
page=page.replace('__COUNT__',str(len(records))).replace('__ERRORS__',str(len(errors))).replace('__DATA__',data)
(ROOT/'docs/index.html').write_text(page,encoding='utf-8')
(ROOT/'docs/catalog.json').write_text(json.dumps([{k:v for k,v in p.items() if k not in ['text','body']} for p in records],indent=2),encoding='utf-8')
print('Built',len(records),'pages;',len(errors),'unavailable indexed pages; HTML bytes',len(page.encode()))
