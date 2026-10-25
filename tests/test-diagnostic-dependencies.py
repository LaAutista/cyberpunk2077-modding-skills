import importlib.util,json,hashlib,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'skills/cyberpunk2077-modding/scripts/comparison/diagnostic_dependencies.py'
spec=importlib.util.spec_from_file_location('deps',SCRIPT);deps=importlib.util.module_from_spec(spec);spec.loader.exec_module(deps)
with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);helper=root/'helper.py';helper.write_text("raise RuntimeError('must never be imported by preflight')\n")
    manifest=root/'manifest.json';record=json.loads(deps.MANIFEST.read_text());record['helpers']['scenario_export']['sha256']=hashlib.sha256(helper.read_bytes()).hexdigest();manifest.write_text(json.dumps(record));deps.MANIFEST=manifest
    report=deps.preflight('scenario',helper_paths={'scenario_export':helper},blender='5.2.3 LTS',numpy='2.5.4');assert deps.require(report)['ready']
    helper.write_text(helper.read_text()+'# changed revision\n')
    changed=deps.preflight('scenario',helper_paths={'scenario_export':helper},blender='5.2.3 LTS',numpy='2.5.4');assert changed['dependencies'][0]['status']=='mismatch'
    try:deps.require(changed);raise AssertionError('mismatch allowed')
    except ValueError:pass
    try:deps.load_helper('scenario_export',helper);raise AssertionError('changed bytes executed')
    except ValueError:pass
    unknown=deps.preflight('scenario');assert unknown['dependencies'][0]['status']=='missing' and unknown['dependencies'][1]['status']=='unknown'
    versions=deps.preflight('scenario',helper_paths={'scenario_export':helper},blender='6.0.0',numpy='9.0');assert not versions['ready'] and versions['dependencies'][1]['status']=='mismatch'
print('PASS: tested helper identity, changed/missing helpers and unknown/mismatched runtime versions; no helper code imported.')
