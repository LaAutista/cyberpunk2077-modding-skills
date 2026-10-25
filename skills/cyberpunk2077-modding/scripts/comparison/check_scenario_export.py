"""Probe Scenario's glTF weight preservation on a copied, owned mesh.

Run in factory-startup Blender. No native cooking or gameplay claim is made.
Bounded to >4-influence copied skins with the tested pre-existing multi-root warning.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import traceback

import bpy
import numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parent))
from diagnostic_dependencies import preflight, require, load_helper
from skin_deformation import compare as compare_skin


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def glb_weights(path):
    data = Path(path).read_bytes()
    magic, version, total = struct.unpack_from('<4sII', data)
    assert magic == b'glTF' and version == 2 and total == len(data)
    size, kind = struct.unpack_from('<I4s', data, 12)
    assert kind == b'JSON'
    doc = json.loads(data[20:20 + size])
    bsize, kind = struct.unpack_from('<I4s', data, 20 + size)
    assert kind == b'BIN\0'
    binary = data[28 + size:28 + size + bsize]
    formats = {5121: ('B', 1, 255), 5123: ('H', 2, 65535), 5125: ('I', 4, 4294967295), 5126: ('f', 4, None)}

    def values(index):
        acc = doc['accessors'][index]
        view = doc['bufferViews'][acc['bufferView']]
        assert view.get('buffer', 0) == 0 and 'sparse' not in acc
        fmt, width, divisor = formats[acc['componentType']]
        count = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}[acc['type']]
        start = view.get('byteOffset', 0) + acc.get('byteOffset', 0)
        rows = [struct.unpack_from('<' + fmt * count, binary, start + i * view.get('byteStride', count * width)) for i in range(acc['count'])]
        return [[v / divisor for v in row] for row in rows] if acc.get('normalized') else rows

    result = {}
    attrs = []
    total_vertices = 0
    points = {}
    for node in doc['nodes']:
        if 'mesh' not in node or 'skin' not in node:
            continue
        names = [doc['nodes'][i]['name'] for i in doc['skins'][node['skin']]['joints']]
        for primitive_index, prim in enumerate(doc['meshes'][node['mesh']]['primitives']):
            a = prim['attributes']
            attrs.append(sorted(k for k in a if k.startswith(('JOINTS_', 'WEIGHTS_'))))
            pos = values(a['POSITION'])
            weights = [{} for _ in pos]
            for key in sorted(k for k in a if k.startswith('JOINTS_')):
                jrows, wrows = values(a[key]), values(a[key.replace('JOINTS_', 'WEIGHTS_')])
                for row, js, ws in zip(weights, jrows, wrows):
                    for j, w in zip(js, ws):
                        if w > 1e-8:
                            row[names[j]] = row.get(names[j], 0) + w
            for vertex_index, (point, row) in enumerate(zip(pos, weights)):
                key = (node['name'], primitive_index, vertex_index)
                assert key not in result, 'Duplicate mesh primitive vertex key'
                result[key] = row
                points[key] = point
            total_vertices += len(pos)
    assert result
    return (result, points), {'vertexRows': total_vertices, 'uniqueVertexKeys': len(result), 'attributes': attrs,
                    'maxInfluences': max(map(len, result.values())), 'maxWeightSumError': max(abs(sum(w.values()) - 1) for w in result.values())}


def compare_weights(before_data, after_data):
    before, old_positions = before_data
    after, new_positions = after_data
    assert before.keys() == after.keys(), 'Mesh/primitive/vertex counts differ; cannot infer correspondence'
    position_error = max(abs(x - y) for key in old_positions for x, y in zip(old_positions[key], new_positions[key]))
    assert position_error < 1e-6, 'Vertex order/coordinates changed; cannot infer weight preservation'
    changed = missing = 0
    max_l1 = max_component = 0.0
    examples = []
    max_bone = None
    for key, old in before.items():
        new = after[key]
        ds = {n: abs(old.get(n, 0) - new.get(n, 0)) for n in old.keys() | new.keys()}
        max_l1 = max(max_l1, sum(ds.values()))
        bone = max(ds, key=ds.get)
        if ds[bone] > max_component:
            max_component, max_bone = ds[bone], bone
        changed += max(ds.values()) > 1e-6
        missing += len(old.keys() - new.keys())
        if old.keys() - new.keys() and len(examples) < 4:
            examples.append({'vertex': key, 'before': old, 'after': new, 'beforeSum': sum(old.values()), 'afterSum': sum(new.values())})
    # One known 10 mm post-bind translation changes the LBS result by weight * 10 mm.
    # This independent matrix-delta probe is not a native clip or gameplay simulation.
    pose = None if max_bone is None else {'joint': max_bone, 'jointMatrixTranslationDeltaMm': 10,
        'maxVertexDisplacementErrorMm': max(abs(old.get(max_bone, 0) - after[key].get(max_bone, 0)) * 10 for key, old in before.items()),
        'kind': 'Synthetic single-joint post-bind translation, analytical linear-blend-skinning response; no native pose claim'}
    return {'changedVertexRows': changed, 'missingNamedInfluences': missing, 'maxL1': max_l1,
            'maxComponentError': max_component, 'maxCorrespondingPositionComponentErrorM': position_error,
            'syntheticPoseSensitivity': pose, 'changedExamples': examples}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--skills-root', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--inspect-only', action='store_true')
    p.add_argument('--animation', type=Path, help='optional copied, bind-compatible Normal animation GLB')
    p.add_argument('--animation-clip', action='append', help='explicit representative Normal clip; repeatable')
    a = p.parse_args(sys.argv[sys.argv.index('--') + 1:])
    a.input = a.input.resolve()
    a.output = a.output.resolve()
    assert a.output != a.input, 'Output must not overwrite input'
    helper = a.skills_root / 'scenario-blender-export/scripts/bx_export.py'
    dependencies=require(preflight('scenario',a.skills_root,blender=bpy.app.version_string,numpy=np.__version__))
    bxe=load_helper('scenario_export',helper)
    if a.inspect_only:
        with a.output.open('x') as target:
            target.write(json.dumps(bxe.inspect_file(str(a.input)), indent=2) + '\n')
        return
    a.output.mkdir(parents=True, exist_ok=False)
    original_hash = sha(a.input)
    source, source_info = glb_weights(a.input)
    assert source_info['maxInfluences'] > 4, 'This probe needs an actual >4 influence asset'
    report = {'passed': False, 'runtimeVerified': False, 'dependencyPreflight':dependencies, 'blenderVersion': bpy.app.version_string, 'inputFiles': {str(a.input): original_hash, str(helper): sha(helper), str(Path(__file__).resolve()): sha(__file__)}, 'source': source_info, 'variants': {}}
    for name in ('skin_deformation.py','diagnostic_dependencies.py','diagnostic-dependencies.json'):
        file=Path(__file__).with_name(name);report['inputFiles'][str(file.resolve())]=sha(file)
    for name, overrides in [('default', {}), ('all-influences', {'export_all_influences': True})]:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(a.input))
        objects = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE' or (o.type == 'MESH' and o.find_armature() is not None)]
        assert {o.name for o in objects if o.type == 'MESH'} == {key[0] for key in source[0]}, 'Unexpected skinned mesh selection'
        out = a.output / (name + '.glb')
        exported = bxe.export(str(out), 'gltf', objects, **overrides)
        # The stock child hangs on shutdown here; use its same inspect/compare with explicit exit.
        before = bxe.inspect_scene(objects, all_actions=True)
        inspected = a.output / (name + '-inspection.json')
        run = subprocess.run([bpy.app.binary_path, '-t', '2', '-noaudio', '-b', '--factory-startup', '--python-exit-code', '1', '--python', str(Path(__file__).resolve()), '--', '--input', str(out), '--skills-root', str(a.skills_root), '--output', str(inspected), '--inspect-only'], capture_output=True, text=True, timeout=60)
        (a.output / (name + '-inspection.log')).write_text(run.stdout + run.stderr)
        assert run.returncode == 0, run.stdout[-2000:] + run.stderr[-2000:]
        after = json.loads(inspected.read_text())
        diffs = bxe.compare(before, after, bxe.CARRIES['gltf'])
        baseline_diffs = bxe.compare(before, before, bxe.CARRIES['gltf'])
        roots_equal = all(set(o.get('roots', [])) == set(after['objects'][n].get('roots', [])) for n, o in before['objects'].items() if o['type'] == 'ARMATURE')
        root_order_changed = any(o.get('roots', []) != after['objects'][n].get('roots', []) for n, o in before['objects'].items() if o['type'] == 'ARMATURE')
        gate = {'pass': not diffs, 'diffs': diffs, 'selfComparisonDiffs': baseline_diffs, 'rootNameSetsUnchanged': roots_equal, 'rootOrderChanged': root_order_changed, 'additionalDiffsBeyondSourcePolicy': [x for x in diffs if not (roots_equal and 'root bones' in x and 'engines want one' in x)], 'before': before, 'after': after, 'execution': 'Unchanged Scenario inspect_scene/inspect_file/compare, explicit-exit child wrapper'}
        result, info = glb_weights(out)
        delta = compare_weights(source, result)
        skin=compare_skin(a.input,out)
        if a.animation:
            skin['suppliedAnimationComparison']=compare_skin(a.input,out,a.animation,a.animation_clip)
        report['variants'][name] = {'export': exported, 'roundTrip': gate, 'readback': info, 'independentNamedWeightDelta': delta, 'copiedSkinEquivalence':skin, 'sha256': sha(out), 'summary': bxe.glb_summary(out)}
    plain, full = report['variants']['default'], report['variants']['all-influences']
    (a.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    for v in (plain, full):
        gate = v['roundTrip']
        assert gate['rootNameSetsUnchanged'], 'Root-name hierarchy changed'
        assert len(gate['selfComparisonDiffs']) == 1 and 'root bones' in gate['selfComparisonDiffs'][0]
        assert len(gate['diffs']) == 1 and 'root bones' in gate['diffs'][0], 'Expected native mesh multi-root policy warning'
        assert not gate['additionalDiffsBeyondSourcePolicy']
    assert plain['readback']['maxInfluences'] == 4 and plain['independentNamedWeightDelta']['missingNamedInfluences'] > 0
    assert full['readback']['maxInfluences'] == source_info['maxInfluences']
    assert full['independentNamedWeightDelta']['missingNamedInfluences'] == 0 and full['independentNamedWeightDelta']['maxComponentError'] < 1e-6
    assert full['copiedSkinEquivalence']['passed'], 'All-influence copied bind/deformation contract failed'
    assert not plain['copiedSkinEquivalence']['sampledDeformationPassed'], 'Lossy default must fail the sampled deformation control'
    report['inputHashAfter'] = sha(a.input)
    report['helperHashAfter'] = sha(helper)
    assert report['inputHashAfter'] == original_hash
    assert report['helperHashAfter'] == report['inputFiles'][str(helper)]
    report['passed'] = True
    report['limits'] = ['Copied named mapping, inverse-bind and nine sampled multi-joint stress poses supplement weight equality. Synthetic stress is not native animation; optional supplied Normal clips require complete joint coverage and matching bind frames.', 'Correspondence requires identical mesh/primitive/vertex keys and every corresponding local-position component within 1e-6 m; the probe fails otherwise.', 'Scenario compare still rejects both exports for pre-existing multi-root hierarchy. Joint permutations are reported/remapped by name, not certified as native index preservation. No materials, native mesh cooking, graph/IK, visual or gameplay acceptance.']
    (a.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'passed': True, 'blenderVersion': report['blenderVersion'], 'variants': {k: v['independentNamedWeightDelta'] for k, v in report['variants'].items()}}), flush=True)


if __name__ == '__main__':
    try:
        main()
    except BaseException:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)
