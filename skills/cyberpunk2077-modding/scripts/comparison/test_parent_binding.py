"""Copied-asset parent/bind diagnostic; run with Blender, never writes inputs.

Models a rigid mesh branch attached to an existing animated joint hierarchy.
This does not edit native animation, the real rig, a game graph, or an exporter.
Bounded to decoded Normal local-TRS clips and one rigid shell, not blended skinning.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import sys
import time

sys.dont_write_bytecode = True
import bpy
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from diagnostic_dependencies import preflight, require, load_helper


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rotation(q):
    """Independent float64 xyzw quaternion matrix, normalized explicitly."""
    x, y, z, w = np.asarray(q, dtype=np.float64) / np.linalg.norm(q)
    return np.array([[1-2*(y*y+z*z), 2*(x*y-z*w), 2*(x*z+y*w)],
                     [2*(x*y+z*w), 1-2*(x*x+z*z), 2*(y*z-x*w)],
                     [2*(x*z-y*w), 2*(y*z+x*w), 1-2*(x*x+y*y)]])


def slerp(a, b, factor):
    a, b = np.array(a) / np.linalg.norm(a), np.array(b) / np.linalg.norm(b)
    dot = float(a @ b)
    if dot < 0:
        b, dot = -b, -dot
    if dot > .9995:
        result = a + factor * (b-a)
        return result / np.linalg.norm(result)
    theta = np.arccos(np.clip(dot, -1, 1))
    return (np.sin((1-factor)*theta)*a + np.sin(factor*theta)*b)/np.sin(theta)


def reference_pose(document, accessor, clip_name, sample_time):
    """Independent channel sampling and hierarchy composition; no helper.pose use."""
    nodes = document['nodes']
    trs = [dict(translation=np.array(n.get('translation', [0, 0, 0])),
                rotation=np.array(n.get('rotation', [0, 0, 0, 1])),
                scale=np.array(n.get('scale', [1, 1, 1]))) for n in nodes]
    parents = {child:i for i,n in enumerate(nodes) for child in n.get('children', [])}
    if clip_name is not None:
        animation = next(a for a in document['animations'] if a['name'] == clip_name)
        for channel in animation['channels']:
            sampler = animation['samplers'][channel['sampler']]
            times, values = accessor(sampler['input']).ravel(), accessor(sampler['output'])
            right = int(np.searchsorted(times, sample_time, side='right'))
            if right == 0:
                result = values[0]
            elif right == len(times):
                result = values[-1]
            else:
                left = right-1
                f = (sample_time-times[left])/(times[right]-times[left])
                path = channel['target']['path']
                if sampler.get('interpolation', 'LINEAR') == 'STEP':
                    result = values[left]
                elif path == 'rotation':
                    result = slerp(values[left], values[right], f)
                else:
                    result = values[left]*(1-f)+values[right]*f
            trs[channel['target']['node']][channel['target']['path']] = result
    local = []
    for values in trs:
        m = np.eye(4)
        m[:3,:3] = rotation(values['rotation']) @ np.diag(values['scale'])
        m[:3,3] = values['translation']
        local.append(m)
    world = {}
    def walk(i):
        if i not in world:
            world[i] = (walk(parents[i]) @ local[i]) if i in parents else local[i]
        return world[i]
    c = np.array([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]], dtype=float)
    return {n['name']:c @ walk(i) @ c.T for i,n in enumerate(nodes)}


def points(matrix, homogeneous):
    return (homogeneous @ matrix.T)[:,:3]


def max_error(a, b):
    return float(np.linalg.norm(a-b, axis=1).max())


def euler_matrix(angles):
    result = np.eye(4)
    for axis, degree in enumerate(angles):
        q = np.zeros(4)
        q[axis], q[3] = np.sin(np.deg2rad(degree)/2), np.cos(np.deg2rad(degree)/2)
        m = np.eye(4)
        m[:3,:3] = rotation(q)
        result = m @ result
    return result


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument('--animation', required=True, type=Path)
    args.add_argument('--mesh', required=True, type=Path)
    args.add_argument('--helper', required=True, type=Path)
    args.add_argument('--out', required=True, type=Path)
    args.add_argument('--mesh-name', default='magazine')
    args.add_argument('--bone', default='mag_std')
    args.add_argument('--wrong-parent', default='mag_plug')
    args.add_argument('--hz', type=int, default=120)
    opt = args.parse_args(sys.argv[sys.argv.index('--')+1:])
    assert opt.hz > 0
    dependencies=require(preflight('parent',helper_paths={'cp_sampler':opt.helper},blender=bpy.app.version_string,numpy=np.__version__))
    opt.out.mkdir(parents=True, exist_ok=False)
    inputs = {str(p.resolve()):sha(p) for p in (opt.animation, opt.mesh, opt.helper)}
    started = time.monotonic()
    helper = load_helper('cp_sampler', opt.helper)
    anim = helper.GltfAnimation(opt.animation, normalize_rotations=True)
    assert anim.clips and all(a.get('extras', {}).get('animationType') == 'Normal'
                              for a in anim.doc['animations']), 'Only declared Normal clips are supported'
    doc, accessor = helper.glb(opt.mesh)
    assert len(doc['skins']) == 1, 'Bounded diagnostic expects one skin'
    skin = doc['skins'][0]
    joint_names = [doc['nodes'][n]['name'] for n in skin['joints']]
    joint = joint_names.index(opt.bone)
    mesh = next(m for m in doc['meshes'] if m['name'] == opt.mesh_name)
    assert len(mesh['primitives']) == 1, 'Select one complete shell primitive'
    primitive = mesh['primitives'][0]
    attr = primitive['attributes']
    positions = accessor(attr['POSITION'])
    faces = accessor(primitive['indices']).reshape(-1, 3).astype(int)
    joints = accessor(attr['JOINTS_0']).astype(int)
    weights = accessor(attr['WEIGHTS_0'])
    assert not any(k.startswith(('JOINTS_', 'WEIGHTS_')) and not k.endswith('_0') for k in attr)
    assert np.allclose(weights.sum(axis=1), 1, atol=1e-7)
    assert np.allclose(np.where(joints==joint, weights, 0).sum(axis=1), 1, atol=1e-7), 'Shell must be rigidly assigned to selected bone'
    c = np.asarray(helper.CONVERSION, dtype=float)
    inverse_bind = accessor(skin['inverseBindMatrices']).reshape(-1,4,4).transpose(0,2,1)[joint]
    inverse_bind = c @ inverse_bind @ c.T
    vertices = positions @ c[:3,:3].T
    vertices_h = np.c_[vertices, np.ones(len(vertices))]
    bone_local = points(inverse_bind, vertices_h)
    bone_local_h = np.c_[bone_local, np.ones(len(bone_local))]
    bone_index = next(i for i,n in enumerate(anim.nodes) if n['name']==opt.bone)
    parent = anim.nodes[anim.parents[bone_index]]['name']
    assert opt.wrong_parent != parent and opt.wrong_parent != opt.bone
    bind = {k:np.asarray(v,dtype=float) for k,v in anim.pose(None, 0).items()}
    reference_bind = reference_pose(anim.doc, anim.accessor, None, 0)
    b0, p0, q0 = bind[opt.bone], bind[parent], bind[opt.wrong_parent]
    local_correct = np.linalg.inv(p0) @ b0
    local_wrong = np.linalg.inv(q0) @ b0
    # Simulates model-branch parent restoration, rebasing its local bind while
    # preserving bind-world; animation nodes/channels themselves are untouched.
    local_repaired = np.linalg.inv(p0) @ (q0 @ local_wrong)
    native_bind_geometry = points(reference_bind[opt.bone] @ inverse_bind, vertices_h)
    bind_baseline = points(b0, bone_local_h)
    bind_wrong = points(q0 @ local_wrong, bone_local_h)
    bind_repaired = points(p0 @ local_repaired, bone_local_h)
    report = {
        'passed':False, 'runtimeVerified':False,
        'scope':'Rigid model-branch parent fault injection on copied native readback clips and authored skinned shell; not an actual HK416 defect or native export test',
        'versions':{'blender':bpy.app.version_string,'python':platform.python_version(),'numpy':np.__version__},
        'dependencyPreflight':dependencies,
        'inputsSHA256':inputs,
        'binding':{'child':opt.bone,'correctParent':parent,'wrongParent':opt.wrong_parent,'vertices':len(vertices),'triangles':len(faces),'rigidWeight':1.0,
                   'rebase':'L_correct=P0^-1*B0; L_wrong=Q0^-1*B0; L_repaired=P0^-1*(Q0*L_wrong)',
                   'unchangedLocalMotion':'D(t)=L_correct^-1 * P(t)^-1 * B(t)',
                   'evaluation':'baseline=B(t)*IB*v; wrong=Q(t)*L_wrong*D(t)*IB*v; repaired=P(t)*L_repaired*D(t)*IB*v'},
        'bindResidualMetres':{'baseline':max_error(bind_baseline,native_bind_geometry),'wrongParent':max_error(bind_wrong,native_bind_geometry),'repaired':max_error(bind_repaired,native_bind_geometry)},
        'samplePolicy':f'Every native channel key time plus a uniform {opt.hz} Hz grid across every available Normal magazine clip including endpoints; no animation graph or visibility-track composition',
        'clips':[], 'toleranceMetres':0.00001,
        'rotationDegreesXYZ':[[0,0,0],[45,30,20],[-70,12,95]],
        'limitations':['Native readback GLB and its existing receipt reused; native exporter not rerun.', 'Geometry is the existing authored GLB, not a newly reimported cooked mesh.', 'Normal component animation only: no additive layers, IK, state graph, skin blending, camera, visibility track or game loading.', 'Wrong parent is deliberately injected in an isolated model-branch calculation; production parenting is not diagnosed as faulty.', 'Source shell is already authored; this does not establish the best pivot for its real reload animation.']}
    rotations = [euler_matrix(a) for a in report['rotationDegreesXYZ']]
    worst = {'error':-1}
    total_samples = 0
    for name, channels in anim.clips.items():
        duration = max(float(t[-1]) for _,_,t,_,_ in channels)
        keys = np.unique(np.concatenate([t for _,_,t,_,_ in channels]))
        grid = np.linspace(0,duration,int(np.ceil(duration*opt.hz))+1)
        times = np.unique(np.r_[keys,grid])
        row = {'name':name,'durationSeconds':duration,'nativeKeyTimes':len(keys),'sampleTimes':len(times),
               'maxBaselineResidualMetres':0.0,'maxRepairedResidualMetres':0.0,'maxWrongParentErrorMetres':0.0,'wrongParentSamplesOver1mm':0,
               'maxRotationInvariantResidualMetres':0.0}
        for t in times:
            poses = {k:np.asarray(v,dtype=float) for k,v in anim.pose(name,float(t)).items()}
            expected = reference_pose(anim.doc, anim.accessor, name,float(t))
            target = points(expected[opt.bone] @ inverse_bind, vertices_h)
            local_motion = np.linalg.inv(local_correct) @ np.linalg.inv(poses[parent]) @ poses[opt.bone]
            baseline = points(poses[opt.bone],bone_local_h)
            wrong = points(poses[opt.wrong_parent] @ local_wrong @ local_motion,bone_local_h)
            repaired = points(poses[parent] @ local_repaired @ local_motion,bone_local_h)
            eb, er, ew = max_error(baseline,target), max_error(repaired,target), max_error(wrong,target)
            row['maxBaselineResidualMetres'] = max(row['maxBaselineResidualMetres'],eb)
            row['maxRepairedResidualMetres'] = max(row['maxRepairedResidualMetres'],er)
            row['maxWrongParentErrorMetres'] = max(row['maxWrongParentErrorMetres'],ew)
            row['wrongParentSamplesOver1mm'] += int(ew > .001)
            # Test rotated frames over every sample. Matrix transforms preserve
            # Euclidean error, avoiding an accidental axis-aligned success.
            for rot in rotations:
                r = rot[:3,:3]
                rotated = float(np.linalg.norm((wrong-target) @ r.T,axis=1).max())
                row['maxRotationInvariantResidualMetres'] = max(row['maxRotationInvariantResidualMetres'],abs(rotated-ew))
            if ew > worst['error']:
                worst = {'error':ew,'clip':name,'time':float(t),'baseline':baseline.copy(),'wrong':wrong.copy(),'repaired':repaired.copy()}
        assert row['maxBaselineResidualMetres'] < report['toleranceMetres'], row
        assert row['maxRepairedResidualMetres'] < report['toleranceMetres'], row
        report['clips'].append(row)
        total_samples += len(times)
    # Bounds-center experiment on the complete asymmetric shell in a fixed
    # canonical component frame. No vertex changes or actual rig edits.
    canonical = bind_baseline
    fixed_center = (canonical.min(axis=0)+canonical.max(axis=0))*.5
    ptest = []
    for angles in [[0,0,0],[0,0,45],[45,0,0],[0,45,0],[35,27,61]]:
        r = euler_matrix(angles)[:3,:3]
        posed = canonical @ r.T
        expected_center = r @ fixed_center
        recomputed = (posed.min(axis=0)+posed.max(axis=0))*.5
        ptest.append({'rotationDegreesXYZ':angles,'posedAabbCenterDriftMetres':float(np.linalg.norm(recomputed-expected_center)),
                      'fixedCanonicalCenterMetres':fixed_center.tolist(),'transformedCanonicalCenterMetres':expected_center.tolist(),'posedAabbCenterMetres':recomputed.tolist()})
    report['pivotExperiment'] = {'scope':'Bounds pivot should remain in its chosen authoring frame; this does not prescribe changing the existing Cyberpunk magazine pivot', 'cases':ptest}
    report['totalSampleTimes'] = total_samples
    report['rotationFrameEvaluations'] = total_samples*len(rotations)
    report['worstNegativeControl'] = {k:v for k,v in worst.items() if k not in ('baseline','wrong','repaired')}
    assert max(report['bindResidualMetres'].values()) < report['toleranceMetres']
    assert worst['error'] > .01, 'Negative control must visibly fail actual motion'
    assert max(p['posedAabbCenterDriftMetres'] for p in ptest) > .0001
    assert all(sha(path)==digest for path,digest in inputs.items()), 'Input unexpectedly modified'
    report['inputBytesUnchanged'] = True
    report['elapsedSeconds'] = time.monotonic()-started
    report['passed'] = True
    np.savez_compressed(opt.out/'comparison-geometry.npz',faces=faces,bind_baseline=bind_baseline,bind_wrong=bind_wrong,bind_repaired=bind_repaired,
                        peak_baseline=worst['baseline'],peak_wrong=worst['wrong'],peak_repaired=worst['repaired'],canonical=canonical)
    (opt.out/'results.json').write_text(json.dumps(report,indent=2)+'\n')
    print('RESULT '+json.dumps({'passed':report['passed'],'samples':total_samples,'worst':report['worstNegativeControl'],'output':str(opt.out)}))


if __name__ == '__main__':
    main()
