"""Bounded Blender playback of embedded WolvenKit GLB local TRS channels.

Requires Blender's mathutils and NumPy. This is not an animation-graph evaluator.
"""
import json
from pathlib import Path
import struct
import numpy as np
from mathutils import Matrix, Quaternion, Vector

CONVERSION = Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))


def glb(path):
    """Read one embedded JSON/BIN GLB; reject unsupported/ambiguous storage."""
    data = Path(path).read_bytes()
    if len(data) < 28 or struct.unpack_from('<4sII', data) != (b'glTF', 2, len(data)):
        raise ValueError('Invalid GLB header')
    chunks, offset = [], 12
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError('Truncated GLB chunk header')
        length, kind = struct.unpack_from('<II', data, offset)
        if length % 4 or offset + 8 + length > len(data):
            raise ValueError('Invalid GLB chunk length')
        chunks.append((kind, data[offset + 8:offset + 8 + length]))
        offset += 8 + length
    if [kind for kind, _ in chunks] != [0x4E4F534A, 0x004E4942]:
        raise ValueError('Expected exactly one JSON then one BIN chunk')
    document, binary = json.loads(chunks[0][1]), chunks[1][1]
    buffers = document.get('buffers', [])
    if len(buffers) != 1 or 'uri' in buffers[0] or not 0 <= len(binary) - buffers[0]['byteLength'] <= 3:
        raise ValueError('Expected one embedded buffer with valid padding')

    def accessor(index):
        a = document['accessors'][index]
        if 'sparse' in a or a.get('normalized', False):
            raise ValueError('Sparse/normalized accessors need a separate reader')
        view = document['bufferViews'][a['bufferView']]
        if view.get('buffer', 0) != 0:
            raise ValueError('External accessor buffer')
        width = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}[a['type']]
        fmt = '<' + {5121: 'B', 5123: 'H', 5125: 'I', 5126: 'f'}[a['componentType']] * width
        size, count = struct.calcsize(fmt), a['count']
        stride, start = view.get('byteStride', size), a.get('byteOffset', 0)
        view_start, view_length = view.get('byteOffset', 0), view['byteLength']
        if count <= 0 or stride < size or start < 0 or start + (count - 1) * stride + size > view_length:
            raise ValueError('Accessor exceeds its buffer view')
        if view_start < 0 or view_start + view_length > buffers[0]['byteLength']:
            raise ValueError('Buffer view exceeds embedded buffer')
        result = np.array([struct.unpack_from(fmt, binary, view_start + start + i * stride) for i in range(count)])
        if not np.isfinite(result).all():
            raise ValueError('Non-finite accessor')
        return result

    return document, accessor


class GltfAnimation:
    def __init__(self, path, normalize_rotations=False):
        self.normalize_rotations = normalize_rotations
        self.path = Path(path)
        self.doc, self.accessor = glb(self.path)
        self.nodes, self.parents, self.clips = self.doc['nodes'], {}, {}
        names = [n.get('name') for n in self.nodes]
        if any(not isinstance(n, str) or not n for n in names) or len(set(names)) != len(names):
            raise ValueError('Preview requires unique names for all nodes')
        for i, node in enumerate(self.nodes):
            if 'matrix' in node:
                raise ValueError('Matrix nodes require an explicit decomposition contract')
            for field, default in [('translation', [0, 0, 0]), ('rotation', [0, 0, 0, 1]), ('scale', [1, 1, 1])]:
                value = node.get(field, default)
                if len(value) != len(default) or not np.isfinite(value).all() or (field == 'rotation' and np.linalg.norm(value) == 0):
                    raise ValueError('Invalid node TRS')
            for child in node.get('children', []):
                if not 0 <= child < len(self.nodes) or child in self.parents:
                    raise ValueError('Invalid or multiply-parented node')
                self.parents[child] = i
        for i in range(len(self.nodes)):
            seen = set()
            while i in self.parents:
                if i in seen:
                    raise ValueError('Cyclic node hierarchy')
                seen.add(i)
                i = self.parents[i]
        for animation in self.doc.get('animations', []):
            name, channels, seen = animation['name'], [], set()
            if name in self.clips:
                raise ValueError('Duplicate animation name')
            for channel in animation['channels']:
                sampler = animation['samplers'][channel['sampler']]
                interpolation = sampler.get('interpolation', 'LINEAR')
                node, target = channel['target']['node'], channel['target']['path']
                if interpolation not in ('LINEAR', 'STEP') or target not in ('translation', 'rotation', 'scale'):
                    raise ValueError('Only LINEAR/STEP local TRS animation is supported')
                if not 0 <= node < len(self.nodes) or (node, target) in seen:
                    raise ValueError('Invalid or duplicate animation channel')
                seen.add((node, target))
                ia, oa = self.doc['accessors'][sampler['input']], self.doc['accessors'][sampler['output']]
                if ia['type'] != 'SCALAR' or oa['type'] != ('VEC4' if target == 'rotation' else 'VEC3') or ia['componentType'] != 5126 or oa['componentType'] != 5126:
                    raise ValueError('Animation channels require float32 times and matching TRS values')
                times, values = self.accessor(sampler['input']).ravel(), self.accessor(sampler['output'])
                if len(times) != len(values) or not np.all(np.diff(times) > 0) or times[0] < 0:
                    raise ValueError('Animation times must be nonnegative and strictly increasing')
                if target == 'rotation' and np.any(np.linalg.norm(values, axis=1) == 0):
                    raise ValueError('Zero rotation quaternion')
                channels.append((node, target, times, values, interpolation))
            self.clips[name] = channels

    def local_values(self, clip, time):
        if not np.isfinite(time):
            raise ValueError('Non-finite sample time')
        values = {i: {'translation': n.get('translation', [0, 0, 0]),
                      'rotation': n.get('rotation', [0, 0, 0, 1]),
                      'scale': n.get('scale', [1, 1, 1])} for i, n in enumerate(self.nodes)}
        for i, target, times, rows, interpolation in self.clips[clip] if clip else []:
            left = max(0, min(len(times) - 1, int(np.searchsorted(times, time, side='right')) - 1))
            right = min(left + 1, len(times) - 1)
            t = 0 if interpolation == 'STEP' or times[left] == times[right] else min(1, max(0, (time - times[left]) / (times[right] - times[left])))
            if target == 'rotation':
                a, b = rows[left], rows[right]
                q = Quaternion((a[3], *a[:3])).slerp(Quaternion((b[3], *b[:3])), t)
                values[i][target] = (q.x, q.y, q.z, q.w)
            else:
                values[i][target] = rows[left] * (1 - t) + rows[right] * t
        return values

    def pose(self, clip, time):
        local = []
        for p in self.local_values(clip, time).values():
            q = p['rotation']
            rotation = Quaternion((q[3], *q[:3]))
            if self.normalize_rotations:
                rotation.normalize()
            local.append(Matrix.LocRotScale(Vector(p['translation']), rotation, Vector(p['scale'])))
        world = {}

        def visit(i):
            if i not in world:
                world[i] = visit(self.parents[i]) @ local[i] if i in self.parents else local[i]
            return world[i]

        return {n['name']: CONVERSION @ visit(i) @ CONVERSION.transposed() for i, n in enumerate(self.nodes)}
