#!/usr/bin/env python3
"""Snapshot official REDmodding documentation. Never writes to the game installation."""
import argparse, concurrent.futures, datetime, hashlib, json, pathlib, re, time, urllib.request
from urllib.parse import urlparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
SECTIONS=['home','cyberpunk-2077-modding','wolvenkit','scripting-cyberpunk','redscript','cyber-engine-tweaks','red4ext']
BASE='https://wiki.redmodding.org/'
def checked_url(url):
 parsed=urlparse(url)
 if parsed.scheme!='https' or parsed.hostname not in {'wiki.redmodding.org','docs.red4ext.com'} or parsed.username or parsed.password:
  raise ValueError('Unexpected documentation source: '+url)
 return url
class Redirects(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  checked_url(newurl)
  return super().redirect_request(req,fp,code,msg,headers,newurl)
def page_path(url):
 checked_url(url)
 parsed=urlparse(url)
 if parsed.netloc=='wiki.redmodding.org':rel=parsed.path.lstrip('/')
 elif parsed.netloc=='docs.red4ext.com':rel='red4ext/'+parsed.path.lstrip('/')
 else:raise ValueError('Unexpected documentation host: '+parsed.netloc)
 if '..' in pathlib.PurePosixPath(rel).parts:raise ValueError('Unsafe documentation path')
 return ROOT/'docs/upstream/redmodding'/rel
def fetch(url):
 checked_url(url)
 for attempt in range(4):
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'2077Dev-local-documentation/1.0'})
   with urllib.request.build_opener(Redirects()).open(req,timeout=70) as r:
    checked_url(r.geturl())
    b=r.read(); content_type=r.headers.get('Content-Type','')
    if 'text/html' in content_type and url.endswith(('.md','.txt')):raise ValueError('Unexpected HTML response')
    return b,r.geturl()
  except Exception:
   if attempt==3:raise
   time.sleep(1+attempt*2)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sections',nargs='+',choices=SECTIONS,default=SECTIONS);ap.add_argument('--refresh',action='store_true');args=ap.parse_args()
 dest=ROOT/'docs/upstream/redmodding';dest.mkdir(parents=True,exist_ok=True)
 mf=ROOT/'docs/source-manifest.json';old=json.loads(mf.read_text()) if mf.exists() else {'pages':[]}
 records={r['url']:r for r in old['pages']};tasks=[];fail=[];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 for section in args.sections:
  folder=dest/section;folder.mkdir(exist_ok=True)
  for endpoint in ['llms.txt','llms-full.txt']:
   url=BASE+section+'/'+endpoint
   try:
    b,final=fetch(url);(folder/endpoint).write_bytes(b)
    if endpoint=='llms.txt':
     for title,url in re.findall(r'\[([^\]]+)\]\((https://(?:wiki\.redmodding\.org|docs\.red4ext\.com)/[^)]+\.md)\)',b.decode()):
      tasks.append((title,url))
   except Exception as e:fail.append({'url':url,'error':str(e)})
  print('Indexed',section,flush=True)
 tasks=list(dict.fromkeys(tasks))
 def download(task):
  title,url=task;path=page_path(url)
  if url in records and path.exists() and not args.refresh:return records[url]
  b,final=fetch(url);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(b)
  return {'title':title,'url':url,'resolved_url':final,'path':str(path.relative_to(ROOT)),'fetched_at':now,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'status':'downloaded','reviewed':False}
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  futures={pool.submit(download,t):t for t in tasks}
  for i,f in enumerate(concurrent.futures.as_completed(futures),1):
   title,url=futures[f]
   try:records[url]=f.result()
   except Exception as e:fail.append({'url':url,'error':str(e)})
   if i%50==0:print('Pages',i,'/',len(tasks),flush=True)
   if i%100==0:mf.write_text(json.dumps({'snapshot_at':now,'sections':args.sections,'pages':list(records.values()),'errors':fail},indent=2))
 attempted={url for _,url in tasks}|{BASE+s+'/'+e for s in args.sections for e in ['llms.txt','llms-full.txt']}
 fail=[e for e in old.get('errors',[]) if e['url'] not in attempted]+fail
 sections=sorted(set(old.get('sections',[]))|set(args.sections))
 result={'snapshot_at':now,'sections':sections,'pages':sorted(records.values(),key=lambda x:x['url']),'errors':fail,'coverage':'All retrievable pages in the named official llms.txt indexes; failures are recorded. Embedded media and external sites remain linked; not an offline media mirror.'}
 mf.write_text(json.dumps(result,indent=2));print('DONE',len(records),'pages;',len(fail),'errors',flush=True)
 if fail:
  print(json.dumps(fail,indent=2))
  raise SystemExit(1)
if __name__=='__main__':main()
