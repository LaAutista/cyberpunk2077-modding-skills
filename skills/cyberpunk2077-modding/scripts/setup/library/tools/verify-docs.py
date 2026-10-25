#!/usr/bin/env python3
"""Rehash acquired wiki pages before indexing or searching cached snapshots."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'docs/source-manifest.json').read_text())
errors=[];count=0
for record in manifest['pages']:
    path=(ROOT/record['path']).resolve()
    try:
        path.relative_to(ROOT/'docs')
        actual=hashlib.sha256(path.read_bytes()).hexdigest()
        if actual!=record['sha256']: raise ValueError('hash mismatch')
        count+=1
    except (OSError,ValueError) as error:errors.append(f"{record['path']}: {error}")
if errors:raise SystemExit('\n'.join(errors))
print('Verified',count,'page hashes; does not establish content review')
