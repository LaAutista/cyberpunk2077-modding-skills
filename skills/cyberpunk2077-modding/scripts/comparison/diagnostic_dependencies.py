"""Read-only identity gate before importing optional diagnostic helpers."""
import hashlib
import json
from pathlib import Path
import types

MANIFEST=Path(__file__).with_name('diagnostic-dependencies.json')

def preflight(diagnostic,skills_root=None,helper_paths=None,blender=None,numpy=None):
    manifest=json.loads(MANIFEST.read_text())
    rows=[]
    for key in manifest['diagnostics'][diagnostic]:
        expected=manifest['helpers'][key]
        path=(helper_paths or {}).get(key)
        if path is None and skills_root is not None:path=Path(skills_root)/expected['relativePath']
        row={'dependency':key,'path':str(path) if path is not None else None,'status':'missing','expectedRevision':expected['revision'],'expectedSHA256':expected['sha256']}
        if path is not None and Path(path).is_file():
            row['sha256']=hashlib.sha256(Path(path).read_bytes()).hexdigest()
            row['status']='tested-revision' if row['sha256']==expected['sha256'] else 'mismatch'
        rows.append(row)
    for key in manifest['runtimeRequirements'][diagnostic]:
        actual={'blender':blender,'numpy':numpy}[key]
        version=str(actual).split()[0] if actual is not None else None
        rows.append({'dependency':key,'version':version,'testedVersions':manifest['runtimes'][key],'status':'unknown' if version is None else ('tested-revision' if version in manifest['runtimes'][key] else 'mismatch')})
    return {'schema':1,'diagnostic':diagnostic,'dependencies':rows,'ready':all(r['status']=='tested-revision' for r in rows),'scope':'Identity gate only; not an export/native/gameplay pass'}

def require(report):
    if not report['ready']:
        raise ValueError('Diagnostic dependency preflight refused import; review/update pins and validate the new revision first: '+json.dumps(report))
    return report

def load_helper(key,path):
    """Execute exactly the verified bytes, bypassing cached/shadowed modules."""
    expected=json.loads(MANIFEST.read_text())['helpers'][key]
    data=Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest()!=expected['sha256']:
        raise ValueError('Helper changed before import; preserved: '+str(path))
    module=types.ModuleType('verified_'+key);module.__file__=str(Path(path).resolve())
    exec(compile(data,module.__file__,'exec'),module.__dict__)
    return module
