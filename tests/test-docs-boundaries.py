"""Offline source/failure/preservation checks for the reused documentation tooling."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]/'skills/cyberpunk2077-modding/scripts/setup/library'
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'tools'/name);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
sync=load('sync-docs.py');restore=load('restore-repositories.py')
for value in ['http://wiki.redmodding.org/x','https://example.invalid/x',''.join(('https','://','user',':','secret','@','wiki.redmodding.org/x'))]:
    try:sync.checked_url(value);raise AssertionError('source accepted')
    except ValueError:pass
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);sync.ROOT=root
    def fail(url):raise OSError('fixture retrieval failed')
    sync.fetch=fail;sys.argv=['sync','--sections','wolvenkit']
    try:sync.main();raise AssertionError('failed acquisition reported success')
    except SystemExit as error:assert error.code==1
    manifest=json.loads((root/'docs/source-manifest.json').read_text());assert len(manifest['errors'])==2
    target=root/'docs/upstream/fixture';target.mkdir(parents=True)
    def git(*args):return subprocess.check_output(['git','-C',str(target),*args],text=True).strip()
    git('init','--quiet');(target/'README.md').write_text('# Fixture\n');git('add','README.md');git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--quiet','-m','fixture');git('remote','add','origin','https://github.com/WopsS/RED4ext.git');head=git('rev-parse','HEAD')
    records=[{'name':'fixture','remote':'https://github.com/WopsS/RED4ext.git','commit':head,'path':'docs/upstream/fixture'},{'name':'later','remote':'https://github.com/WopsS/RED4ext.SDK.git','commit':'0'*40,'path':'docs/upstream/later'}]
    (root/'docs/repository-manifest.json').write_text(json.dumps(records));restore.ROOT=root;sys.argv=['restore','--name','fixture','--apply'];restore.main()
    (target/'README.md').write_text('# Local change\n')
    try:restore.main();raise AssertionError('dirty snapshot accepted')
    except ValueError as error:assert 'preserved' in str(error)
    assert (target/'README.md').read_text()=='# Local change\n'
    (target/'README.md').write_text('# Fixture\n');(root/'docs/source-manifest.json').write_text(json.dumps({'pages':[],'errors':[],'snapshot_at':'fixture','sections':[]}));(root/'docs/guides').mkdir();(root/'tools').mkdir();shutil.copy2(ROOT/'tools/build-doc-index.py',root/'tools/build-doc-index.py')
    subprocess.run([sys.executable,str(root/'tools/build-doc-index.py')],check=True)
    remaining=json.loads((root/'docs/repository-manifest.json').read_text());assert {r['name'] for r in remaining}=={'fixture','later'} and next(r for r in remaining if r['name']=='later')['snapshot_present'] is False
print('PASS: authoritative HTTPS boundaries, failure exit with retained diagnostics, dirty snapshot preservation and unacquired repository locator retention.')
