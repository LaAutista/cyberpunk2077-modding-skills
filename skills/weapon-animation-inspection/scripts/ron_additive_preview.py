"""Preview WKit 9.0.1 bind-relative additive exports on an explicit base pose.

Run inside Blender. This composes positive-scale local transforms at full weight;
it does not emulate REDengine animation graphs, events, masks or first-frame rules.
Input must have been exported with additiveAddRelative=True. Raw additive GLBs
are a different contract; this module cannot recover exporter-lost rotation data.
"""
from mathutils import Matrix, Quaternion, Vector
from math import isfinite
from weapon_animation_gltf import GltfAnimation, CONVERSION


def _local_values(animation, clip, time):
    """Sample channels before hierarchy multiplication; avoid decomposing shear."""
    return animation.local_values(clip, time)


def _rotation(value):
    return Quaternion((value[3],*value[:3])).normalized()


def additive_pose(animation: GltfAnimation, clip: str, time: float,
                  base_clip: str, base_time: float = 0.0):
    """Return the same named Blender-world matrices as GltfAnimation.pose()."""
    metadata = {a['name']: a.get('extras', {}) for a in animation.doc['animations']}
    kind = metadata[clip].get('animationType')
    if kind not in ('Additive', 'AdditiveWithoutFirstFrame'):
        raise ValueError(f'{clip}: expected an additive clip, got {kind}')
    if metadata[base_clip].get('animationType') != 'Normal':
        raise ValueError(f'{base_clip}: base must be an explicitly selected normal clip')
    names = [n.get('name') for n in animation.nodes]
    if None in names or len(set(names)) != len(names):
        raise ValueError('Preview requires unique names for all nodes')
    parents = {names[child]: names[parent] for child, parent in animation.parents.items()}
    exported = _local_values(animation, clip, time)
    base = _local_values(animation, base_clip, base_time)
    locals_ = {}
    for index, name in enumerate(names):
        node = animation.nodes[index]
        bt, bq, bs = Vector(node.get('translation',[0,0,0])), _rotation(node.get('rotation',[0,0,0,1])), Vector(node.get('scale',[1,1,1]))
        e, p = exported[index], base[index]
        et, eq, es = Vector(e['translation']), _rotation(e['rotation']), Vector(e['scale'])
        pt, pq, ps = Vector(p['translation']), _rotation(p['rotation']), Vector(p['scale'])
        # WKit multiplies scale componentwise, snapping within 1e-7 of one.
        # Preserve the source's small nonunit recoil scales; do not clamp them.
        if any(not isfinite(v) or v <= 0 for scale in (bs, es, ps) for v in scale):
            raise ValueError(f'{clip}/{name}: singular/reflected scale requires separate validation')
        delta_rotation = bq.normalized().inverted() @ eq.normalized()
        result_rotation = (pq.normalized() @ delta_rotation).normalized()
        result_scale = Vector(tuple(ps[i] * es[i] / bs[i] for i in range(3)))
        locals_[name] = Matrix.LocRotScale(pt + et - bt, result_rotation, result_scale)
    worlds = {}

    def visit(name):
        if name not in worlds:
            worlds[name] = visit(parents[name]) @ locals_[name] if name in parents else locals_[name]
        return worlds[name]

    return {name: CONVERSION @ visit(name) @ CONVERSION.transposed() for name in names}
