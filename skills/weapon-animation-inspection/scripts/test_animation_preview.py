"""Asset-free checks, optionally followed by read-only checks of external GLBs.

blender -b --factory-startup --python-exit-code 1 --python THIS_FILE -- [--asset FILE ...]
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import traceback
import numpy as np
from mathutils import Quaternion

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from weapon_animation_gltf import GltfAnimation, CONVERSION
from ron_additive_preview import additive_pose


def write_glb(path, doc, binary):
    doc = copy.deepcopy(doc)
    doc['buffers'] = [{'byteLength': len(binary)}]
    text = json.dumps(doc).encode()
    text += b' ' * (-len(text) % 4)
    binary += b'\0' * (-len(binary) % 4)
    path.write_bytes(struct.pack('<4sII', b'glTF', 2, 28 + len(text) + len(binary)) +
                     struct.pack('<II', len(text), 0x4E4F534A) + text +
                     struct.pack('<II', len(binary), 0x004E4942) + binary)


def matrix(t, q, s):
    # Independent direct quaternion-to-matrix formula, not helper decomposition.
    x, y, z, w = np.asarray(q) / np.linalg.norm(q)
    r = np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                  [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                  [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])
    result = np.eye(4)
    result[:3, :3], result[:3, 3] = r @ np.diag(s), t
    return result


def xyzw(q):
    return [q.x, q.y, q.z, q.w]


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset', action='append', default=[], type=Path)
    args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
    report = {'passed': False, 'visuallyInspected': False, 'runtimeVerified': False, 'externalAssets': []}
    with tempfile.TemporaryDirectory(prefix='animation-preview-test-') as directory:
        p = Path(directory) / 'synthetic.glb'
        bind_q = Quaternion((1, 0, 0), np.pi / 2)
        base_q = Quaternion((0, 1, 0), np.pi / 2)
        delta_q = Quaternion((0, 0, 1), np.pi / 2)
        nodes = [{'name': 'parent', 'children': [1], 'translation': [1, 2, 3], 'rotation': xyzw(bind_q), 'scale': [2, 3, 4]},
                 {'name': 'child', 'translation': [0, 1, 0], 'scale': [1, .999960, 1]}]
        doc = {'asset': {'version': '2.0'}, 'nodes': nodes, 'accessors': [], 'bufferViews': [], 'animations': []}
        binary = bytearray()

        def acc(rows, kind):
            start = len(binary)
            for row in rows:
                binary.extend(struct.pack('<' + 'f' * len(row), *row))
            vi = len(doc['bufferViews'])
            doc['bufferViews'].append({'buffer': 0, 'byteOffset': start, 'byteLength': len(binary) - start})
            doc['accessors'].append({'bufferView': vi, 'componentType': 5126, 'count': len(rows), 'type': kind})
            return len(doc['accessors']) - 1

        def clip(name, kind, channels):
            a = {'name': name, 'extras': {'animationType': kind}, 'channels': [], 'samplers': []}
            for node, target, times, values, mode in channels:
                a['channels'].append({'sampler': len(a['samplers']), 'target': {'node': node, 'path': target}})
                a['samplers'].append({'input': acc([[t] for t in times], 'SCALAR'),
                                      'output': acc(values, 'VEC4' if target == 'rotation' else 'VEC3'), 'interpolation': mode})
            doc['animations'].append(a)

        clip('base', 'Normal', [(0, 'translation', [0], [[10, 20, 30]], 'LINEAR'),
                               (0, 'rotation', [0], [xyzw(base_q)], 'LINEAR'),
                               (0, 'scale', [0], [[1.5, 2, 2.5]], 'LINEAR')])
        channels = [(0, 'translation', [0, 1], [[1.25, 2, 3.75]] * 2, 'LINEAR'),
                    (0, 'rotation', [0, 1], [xyzw(bind_q @ delta_q)] * 2, 'LINEAR'),
                    (0, 'scale', [0, 1], [[2 * .999960, 3.3, 3.6]] * 2, 'LINEAR')]
        clip('add', 'Additive', channels)
        clip('without', 'AdditiveWithoutFirstFrame', channels)
        clip('identity', 'Additive', [])
        clip('step', 'Normal', [(0, 'translation', [0, .5, 1], [[0, 0, 0], [1, 0, 0], [2, 0, 0]], 'STEP')])
        clip('linear', 'Normal', [(0, 'translation', [0, 1], [[0, 0, 0], [2, 0, 0]], 'LINEAR')])
        write_glb(p, doc, bytes(binary))
        a = GltfAnimation(p, normalize_rotations=True)
        conversion = np.asarray(CONVERSION)
        parent = matrix([10.25, 20, 30.75], xyzw(base_q @ delta_q), [1.5 * .999960, 2.2, 2.25])
        child = parent @ matrix(nodes[1]['translation'], [0, 0, 0, 1], nodes[1]['scale'])
        for kind in ('add', 'without'):
            for t in (-1, 0, .5, 1, 2):
                actual = additive_pose(a, kind, t, 'base')
                for name, expected in [('parent', parent), ('child', child)]:
                    assert np.max(np.abs(np.asarray(actual[name]) - conversion @ expected @ conversion.T)) < 4e-6
        for name, expected in a.pose('base', 0).items():
            assert np.max(np.abs(np.asarray(additive_pose(a, 'identity', 0, 'base')[name]) - expected)) < 4e-6
        for time, value in [(-1, 0), (0, 0), (.49, 0), (.5, 1), (.99, 1), (1, 2), (2, 2)]:
            assert a.local_values('step', time)[0]['translation'][0] == value
        assert a.local_values('linear', .25)[0]['translation'][0] == .5

        rejected = []

        def reject(label, action):
            try:
                action()
            except (ValueError, KeyError, IndexError):
                rejected.append(label)
            else:
                raise AssertionError('Accepted ' + label)

        reject('normal as additive', lambda: additive_pose(a, 'base', 0, 'base'))
        reject('additive base', lambda: additive_pose(a, 'add', 0, 'add'))
        reject('nonfinite time', lambda: a.pose('base', float('nan')))
        for scale in ([0, 1, 1], [-1, 1, 1]):
            saved = a.nodes[1]['scale']
            a.nodes[1]['scale'] = scale
            reject('singular/reflected scale', lambda: additive_pose(a, 'add', 0, 'base'))
            a.nodes[1]['scale'] = saved
        fixtures = [('duplicate node name', lambda d: d['nodes'][1].update(name='parent')),
                    ('cyclic hierarchy', lambda d: d['nodes'][1].update(children=[0])),
                    ('matrix node', lambda d: d['nodes'][0].update(matrix=list(np.eye(4).ravel()))),
                    ('CUBICSPLINE', lambda d: d['animations'][0]['samplers'][0].update(interpolation='CUBICSPLINE')),
                    ('accessor overrun', lambda d: d['accessors'][0].update(count=999)),
                    ('sparse accessor', lambda d: d['accessors'][0].update(sparse={})),
                    ('duplicate clip name', lambda d: d['animations'][1].update(name='base'))]
        for label, mutate in fixtures:
            broken = copy.deepcopy(doc)
            mutate(broken)
            write_glb(p, broken, bytes(binary))
            reject(label, lambda: GltfAnimation(p))
        write_glb(p, doc, bytes(binary))
        p.write_bytes(p.read_bytes()[:-1])
        reject('truncated GLB', lambda: GltfAnimation(p))
        report['negativeFixtures'] = rejected
        report['syntheticChecks'] = ['noncommuting additive rotations', 'positive nonuniform scales', 'local hierarchy composition',
                                     'identity delta', 'AdditiveWithoutFirstFrame has no invented skipped frame',
                                     'LINEAR interpolation', 'STEP exact endpoint and out-of-range clamping']
    for p in args.asset:
        before = hashlib.sha256(p.read_bytes()).hexdigest()
        a = GltfAnimation(p, normalize_rotations=True)
        samples = 0
        for clip, channels in a.clips.items():
            times = sorted(set(float(t) for _, _, keys, _, _ in channels for t in keys))
            for time in times:
                assert all(np.isfinite(np.asarray(m)).all() for m in a.pose(clip, time).values())
                samples += 1
        composed = []
        for posture in ('shoulder', 'ironsight'):
            clip, base = 'add_recoil_single_shot_' + posture, 'idlepose_' + posture
            if clip not in a.clips or base not in a.clips:
                continue
            times = sorted(set(float(t) for _, _, keys, _, _ in a.clips[clip] for t in keys))
            times = sorted(set(times + [(x + y) / 2 for x, y in zip(times, times[1:])]))
            for time in times:
                assert all(np.isfinite(np.asarray(m)).all() for m in additive_pose(a, clip, time, base).values())
            composed.append({'clip': clip, 'base': base, 'samplesIncludingMidpoints': len(times)})
        assert hashlib.sha256(p.read_bytes()).hexdigest() == before
        report['externalAssets'].append({'path': str(p.resolve()), 'sha256': before, 'clips': len(a.clips), 'sampledTimes': samples,
                                        'explicitAdditivePreviews': composed,
                                        'scope': 'Parsing and finite named transforms/full-weight additive composition only; no graph, native or visual acceptance'})
    report['passed'] = True
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    try:
        run()
    except BaseException:
        traceback.print_exc()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(1)
    # Blender's background audio cleanup can hang in a sandbox; all checks ran above.
    sys.stdout.flush()
    os._exit(0)
