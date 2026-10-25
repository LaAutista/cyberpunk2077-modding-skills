#!/usr/bin/env python3
"""Restore missing authoritative reference repositories at recorded commits."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--apply',action='store_true')
    ap.add_argument('--name',action='append',required=True,help='explicit repository name from manifest')
    args=ap.parse_args()
    records=json.loads((ROOT/'docs/repository-manifest.json').read_text())
    if set(args.name)-{r['name'] for r in records}: ap.error('Unknown repository name')
    for record in records:
        if record['name'] not in args.name: continue
        target=(ROOT/record['path']).resolve()
        target.relative_to((ROOT/'docs/upstream').resolve())
        if target.exists():
            if not (target/'.git').is_dir() or (target/'.git').is_symlink():
                raise ValueError('Unknown existing snapshot preserved: '+str(target))
            def git(*args):
                return subprocess.check_output(['git','-c','core.fsmonitor=false','-c','core.hooksPath=/dev/null','-c','credential.helper=','-C',str(target),*args],text=True).strip()
            if git('rev-parse','HEAD')!=record['commit'] or git('remote','get-url','origin')!=record['remote'] or git('status','--porcelain'):
                raise ValueError('Changed existing snapshot preserved: '+str(target))
            print('verified existing snapshot:',target)
            continue
        print(record['remote'],record['commit'],'->',target)
        if not args.apply: continue
        if not record['remote'].startswith('https://github.com/'):
            raise ValueError('Unrecognized repository source')
        target.parent.mkdir(parents=True,exist_ok=True)
        with tempfile.TemporaryDirectory(dir=target.parent) as temp:
            stage=Path(temp)/'snapshot'
            subprocess.run(['git','clone','--no-checkout',record['remote'],str(stage)],check=True)
            subprocess.run(['git','-C',str(stage),'checkout','--detach',record['commit']],check=True)
            actual=subprocess.check_output(['git','-C',str(stage),'rev-parse','HEAD'],text=True).strip()
            if actual!=record['commit']: raise ValueError('Commit mismatch')
            stage.rename(target)
if __name__=='__main__': main()
