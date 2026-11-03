#!/usr/bin/env python3
"""Read-only structural checks. Valid bookkeeping is not proof of animation behavior."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys


GATES = ('source', 'target', 'mapping', 'retarget', 'native', 'visual', 'package', 'runtime')
POSITIVE = {g: ('VISUALLY_REVIEWED' if g == 'visual' else
                'USER_RUNTIME_VERIFIED' if g == 'runtime' else 'CHECKED') for g in GATES}
PENDING = {'OPEN', 'FAILED', 'HYPOTHESIS', 'IMPLEMENTED'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value, label):
    require(isinstance(value, str) and bool(value.strip()), label + ': nonempty string required')


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def vector(value, size, label):
    require(isinstance(value, list) and len(value) == size and all(number(v) for v in value),
            label + ': finite vector required')


def digest(value):
    require(isinstance(value, str) and re.fullmatch(r'[0-9a-f]{64}', value), 'SHA-256 required')


def file_identity(value, base):
    nonempty(value['path'], 'artifact path')
    digest(value['sha256'])
    path = (base / value['path']).resolve()
    require(path.is_file(), 'missing artifact: ' + str(path))
    with path.open('rb') as stream:
        actual = hashlib.file_digest(stream, 'sha256').hexdigest()
    require(actual == value['sha256'], 'hash mismatch: ' + str(path))
    return path


def trs(value, label):
    for key, size in (('t', 3), ('q', 4), ('s', 3)):
        vector(value[key], size, label + '.' + key)
    require(abs(sum(v*v for v in value['q']) - 1) <= 1e-5, label + ': unit xyzw quaternion required')
    require(all(v != 0 for v in value['s']), label + ': singular scale unsupported')


def skeleton(value, label):
    names, parents, locals_ = value['names'], value['parents'], value['reference_local']
    require(isinstance(names, list) and len(names) > 0, label + ': bones required')
    for name in names:
        nonempty(name, label + ' bone')
    require(len(set(names)) == len(names), label + ': duplicate bone')
    require(len(names) == len(parents) == len(locals_), label + ': skeleton array lengths')
    for i, parent in enumerate(parents):
        require(type(parent) is int and -1 <= parent < len(names) and parent != i,
                label + ': invalid parent')
        seen = {i}
        p = parent
        while p != -1:
            require(type(p) is int and 0 <= p < len(names) and p not in seen,
                    label + ': invalid parent or cycle')
            seen.add(p)
            p = parents[p]
        trs(locals_[i], label + ':' + names[i])
    return names


def validate_fixture(data):
    require(data['schema_version'] == 1, 'unsupported fixture schema')
    for side in ('source', 'target'):
        value = data[side]
        nonempty(value['identity'], side + ' identity')
        digest(value['sha256'])
        skeleton(value['skeleton'], side)
    nonempty(data['source']['decoder'], 'decoder version')
    digest(data['target']['container_sha256'])
    convention = data['conventions']
    for key, expected in (('vectors', 'column'), ('matrix_storage', 'row-major'),
                          ('quaternion', 'xyzw'), ('time', 'seconds')):
        require(convention[key] == expected, 'unsupported convention: ' + key)
    for key in ('source_units', 'working_units', 'target_units'):
        nonempty(convention[key], key)
    for key in ('source_to_working', 'working_to_target'):
        matrix = convention[key]
        vector(matrix, 16, key)
        require(matrix[12:] == [0, 0, 0, 1], key + ': affine matrix required')
        a,b,c,d,e,f,g,h,i = (matrix[j] for j in (0,1,2,4,5,6,8,9,10))
        require(abs(a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)) > 1e-12,
                key + ': singular basis')
    clip = data['clip']
    nonempty(clip['name'], 'clip name')
    require(number(clip['duration']) and clip['duration'] > 0, 'positive clip duration required')
    require(clip['animation_type'] in ('absolute', 'additive'), 'unknown source animation type')
    nonempty(clip['base_definition'], 'explicit base definition (or none for absolute)')
    require(clip['animation_type'] != 'additive' or clip['base_definition'].lower() != 'none',
            'additive clip requires a base')
    require(clip['interpolation'] in ('LINEAR', 'STEP'), 'unsupported fixture interpolation')
    times = clip['sample_times']
    require(isinstance(times, list) and len(times) >= 2 and all(number(t) for t in times),
            'finite endpoint-inclusive sample times required')
    require(times[0] == 0 and abs(times[-1] - clip['duration']) <= 1e-9 and
            all(a < b for a,b in zip(times, times[1:])), 'invalid clock/endpoints')
    require(len(clip['local_samples']) == len(times), 'sample/time count mismatch')
    count = len(data['source']['skeleton']['names'])
    for frame in clip['local_samples']:
        require(len(frame) == count, 'incomplete source sample')
        for value in frame:
            trs(value, 'source sample')
    for key in ('events', 'curves'):
        require(isinstance(clip[key], list), key + ': explicit list required')
    require(data['unsupported_semantics'] == [], 'unsupported source semantics remain open')
    for key in ('player_anchor', 'weapon_root', 'component_mounts', 'ownership'):
        nonempty(data['assembly'][key], 'assembly ' + key)
    return {'structural_fixture': 'CHECKED', 'behavior': 'OPEN', 'samples': len(times)}


def verify_mapping(data):
    validate_fixture(data)
    source = set(data['source']['skeleton']['names'])
    target = set(data['target']['skeleton']['names'])
    used_source, used_target = set(), set()
    for pair in data['mapping']:
        s, t = pair['source'], pair['target']
        require(s in source and t in target, 'mapping names must exist')
        require(s not in used_source and t not in used_target, 'duplicate source or target mapping')
        used_source.add(s)
        used_target.add(t)
    require(bool(used_target), 'at least one mapped target required')
    for entry in data['unmapped_targets']:
        t = entry['target']
        require(t in target and t not in used_target, 'duplicate or unknown unmapped target')
        nonempty(entry['reason'], 'unmapped target reason')
        used_target.add(t)
    require(used_target == target, 'every target must be mapped or explicitly preserved')
    return {'structural_mapping': 'CHECKED', 'reference_pose_reconstruction': 'OPEN',
            'mapped_bones': len(data['mapping'])}


def inspect_source_motion(data):
    """Inventory sampled source motion; never choose a retarget disposition."""
    try:
        verify_mapping(data)
    except OverflowError as error:
        raise ValueError('source motion numeric range unsupported') from error
    source = data['source']['skeleton']
    target = data['target']['skeleton']
    clip = data['clip']
    times, frames = clip['sample_times'], clip['local_samples']
    basis = data['conventions']['source_to_working']
    parents = source['parents']
    # The existing fixture permits arbitrary array order, not just parent-first.
    children = [[] for _ in parents]
    order = []
    for i, parent in enumerate(parents):
        if parent == -1:
            order.append(i)
        else:
            children[parent].append(i)
    for i in order:
        order.extend(children[i])
    require(len(order) == len(parents), 'source hierarchy traversal incomplete')

    def matrix(value):
        t, q, s = (value[k] for k in ('t', 'q', 's'))
        norm = math.sqrt(sum(v*v for v in q))
        x,y,z,w = (v/norm for v in q)
        return [(1-2*(y*y+z*z))*s[0], 2*(x*y-z*w)*s[1], 2*(x*z+y*w)*s[2], t[0],
                2*(x*y+z*w)*s[0], (1-2*(x*x+z*z))*s[1], 2*(y*z-x*w)*s[2], t[1],
                2*(x*z-y*w)*s[0], 2*(y*z+x*w)*s[1], (1-2*(x*x+y*y))*s[2], t[2],
                0, 0, 0, 1]

    def positions(frame):
        world = [None] * len(parents)
        result = [None] * len(parents)
        for i in order:
            local = matrix(frame[i])
            parent = parents[i]
            world[i] = local if parent == -1 else [
                sum(world[parent][r*4+k]*local[k*4+c] for k in range(4))
                for r in range(4) for c in range(4)]
            require(all(number(v) for v in world[i]), 'nonfinite source hierarchy result')
            point = [world[i][3], world[i][7], world[i][11], 1]
            result[i] = [sum(basis[r*4+k]*point[k] for k in range(4)) for r in range(3)]
            require(all(number(v) for v in result[i]), 'nonfinite working-space position')
        return result

    def motion(values, reference):
        def distances(origin):
            result = [math.hypot(*(a-b for a,b in zip(value, origin))) for value in values]
            require(all(number(v) for v in result), 'nonfinite source motion distance')
            return result
        first_distances, reference_distances = distances(values[0]), distances(reference)
        def witness(distances_):
            index = max(range(len(values)), key=distances_.__getitem__)
            return {'distance': distances_[index], 'sample_index': index,
                    'time': times[index], 'value': list(values[index])}
        return {'reference': list(reference), 'first': list(values[0]),
                'minimum': [min(v[k] for v in values) for k in range(3)],
                'maximum': [max(v[k] for v in values) for k in range(3)],
                'changed_from_first_sample_indices': [i for i,d in enumerate(first_distances) if d != 0],
                'offset_from_reference_sample_indices': [i for i,d in enumerate(reference_distances) if d != 0],
                'maximum_distance_from_first': witness(first_distances),
                'maximum_distance_from_reference': witness(reference_distances)}

    reference_world = positions(source['reference_local'])
    world_positions = [[] for _ in parents]
    for frame in frames:
        for i, position in enumerate(positions(frame)):
            world_positions[i].append(position)
    mapped = {pair['source']: pair['target'] for pair in data['mapping']}
    target_reference = dict(zip(target['names'], target['reference_local']))
    bones, translation_review, scale_review = [], [], []
    for i, name in enumerate(source['names']):
        translation = motion([frame[i]['t'] for frame in frames], source['reference_local'][i]['t'])
        scale = motion([frame[i]['s'] for frame in frames], source['reference_local'][i]['s'])
        needs_translation = bool(translation['offset_from_reference_sample_indices'])
        needs_scale = bool(scale['offset_from_reference_sample_indices'])
        if needs_translation:
            translation_review.append(name)
        if needs_scale:
            scale_review.append(name)
        mapped_target = mapped.get(name)
        bones.append({'source': name, 'parent': source['names'][parents[i]] if parents[i] != -1 else None,
                      'mapped_target': mapped_target,
                      'target_reference_local': target_reference[mapped_target] if mapped_target else None,
                      'local_translation': translation, 'local_scale': scale,
                      'world_position_working': motion(world_positions[i], reference_world[i]),
                      'translation_requires_disposition': needs_translation,
                      'translation_disposition': 'OPEN' if needs_translation else None,
                      'scale_requires_disposition': needs_scale,
                      'scale_disposition': 'OPEN' if needs_scale else None})
    clip_hash = hashlib.sha256(json.dumps(clip, sort_keys=True, separators=(',', ':'),
                                          allow_nan=False).encode('utf-8')).hexdigest()
    return {'source_motion_inventory': 'CHECKED', 'behavior': 'OPEN',
            'translation_handling': 'OPEN', 'scale_handling': 'OPEN',
            'retarget': 'OPEN', 'visual': 'OPEN', 'runtime': 'OPEN',
            'rotation_only_assumption_supported': False,
            'identities': {'source': data['source']['identity'], 'source_sha256': data['source']['sha256'],
                           'target': data['target']['identity'], 'target_sha256': data['target']['sha256'],
                           'target_container_sha256': data['target']['container_sha256'],
                           'clip': clip['name'], 'clip_canonical_payload_sha256': clip_hash},
            'sample_times': list(times), 'duration': clip['duration'],
            'animation_type': clip['animation_type'], 'base_definition': clip['base_definition'],
            'interpolation': clip['interpolation'],
            'world_position_semantics': ('ABSOLUTE_SOURCE_HIERARCHY' if clip['animation_type'] == 'absolute'
                                         else 'UNCOMPOSED_ADDITIVE_HIERARCHY_DIAGNOSTIC'),
            'units': {'local_translation': data['conventions']['source_units'], 'local_scale': 'dimensionless',
                      'world_position_working': data['conventions']['working_units'],
                      'target_reference_local_translation': data['conventions']['target_units']},
            'source_to_working': list(basis), 'bones': bones,
            'translation_review_bones': translation_review, 'scale_review_bones': scale_review,
            'limits': ['Inventory covers every supplied sample, not unsupplied sparse keys or between-key extrema.',
                       'Exact nonzero differences are reported without an invented tolerance or disposition.',
                       'Complete local samples do not identify serialized channel presence versus decoder-filled defaults.',
                       'Working positions use declared affine source_to_working after parent composition; quaternions normalize for evaluation only. Unit labels and bases are declarations, not independently authenticated.',
                       'Source/target hashes are declared identities; clip hash is computed over sorted compact JSON of this fixture clip, not a native clip file.',
                       'Additive samples are inventoried as supplied; no base pose is applied and their working positions are diagnostic, not evaluated source motion.',
                       'Target reference locals are shown for disposition review, not directly subtracted across different rigs/units.',
                       'Observed translation or scale offsets require an explicit preserve/adapt/reject decision with evidence; this command makes none and proves no retarget, contact, visual or runtime behavior.']}


def evidence(record, base, required=True):
    require(isinstance(record['evidence'], list) and (not required or bool(record['evidence'])),
            'evidence file list required')
    for item in record['evidence']:
        file_identity(item, base)


def summarize_receipt(data, base):
    require(data['schema_version'] == 1, 'unsupported receipt schema')
    nonempty(data['project'], 'project')
    baseline = file_identity(data['baseline'], base) if data['baseline'] else None
    if not baseline:
        nonempty(data['baseline_note'], 'missing baseline explanation')
    candidate = file_identity(data['candidate'], base) if data['candidate'] else None
    require(not baseline or not candidate or not baseline.samefile(candidate),
            'candidate must not overwrite baseline')
    file_identity(data['fixture'], base)
    require(data['current_gate']['id'] in GATES, 'unknown current gate')
    nonempty(data['current_gate']['question'], 'one blocking question')
    nonempty(data['next_test'], 'next test')
    require(set(data['gates']) == set(GATES), 'all eight gates required')
    ready = {}
    for gate in GATES:
        record = data['gates'][gate]
        status = record['status']
        require(status in PENDING | {POSITIVE[gate]}, gate + ': wrong evidence category')
        ready[gate] = status == POSITIVE[gate]
        evidence(record, base, required=ready[gate])
        if ready[gate]:
            nonempty(record['scope'], gate + ' checked scope')
            require(record['fixture_sha256'] == data['fixture']['sha256'], gate + ': stale fixture evidence')
            if gate in ('retarget', 'native', 'visual', 'package', 'runtime'):
                require(candidate is not None and record['candidate_sha256'] == data['candidate']['sha256'],
                        gate + ': stale/missing candidate evidence')
            if gate == 'runtime':
                nonempty(record['user_confirmation'], 'identified user runtime confirmation')
                nonempty(record['environment'], 'runtime environment/profile/variant')
    attempts = data['attempts']
    require(isinstance(attempts, list), 'attempt list required')
    for attempt in attempts:
        require(attempt['gate'] in GATES and attempt['result'] in ('FAILED', 'CHECKED'), 'invalid attempt')
        require(attempt['fixture_sha256'] == data['fixture']['sha256'], 'attempt belongs to another fixture')
        nonempty(attempt['change'], 'attempt change')
        nonempty(attempt['hypothesis'], 'attempt hypothesis')
        evidence(attempt, base)
    discriminator = data['discriminator']
    reset_at = 0
    if discriminator is not None:
        require(discriminator['gate'] in GATES, 'unknown discriminator gate')
        require(discriminator['fixture_sha256'] == data['fixture']['sha256'], 'stale discriminator fixture')
        nonempty(discriminator['question'], 'discriminator question')
        hypotheses = discriminator['hypotheses']
        require(isinstance(hypotheses, list) and len(hypotheses) >= 2, 'two hypotheses required')
        for hypothesis in hypotheses:
            nonempty(hypothesis, 'discriminator hypothesis')
        require(len(set(hypotheses)) == len(hypotheses), 'distinct hypotheses required')
        require(discriminator['status'] in ('OPEN', 'CHECKED'), 'discriminator status')
        evidence(discriminator, base, required=discriminator['status'] == 'CHECKED')
        index = discriminator['after_attempt']
        require(type(index) is int and 0 <= index <= len(attempts), 'invalid discriminator attempt boundary')
        if discriminator['status'] == 'CHECKED':
            nonempty(discriminator['result'], 'discriminator result')
            if discriminator['gate'] == data['current_gate']['id']:
                reset_at = index
    failures = sum(a['gate'] == data['current_gate']['id'] and a['result'] == 'FAILED'
                   for a in attempts[reset_at:])
    repair_blocked = failures >= 2
    diagnostic = all(ready[g] for g in ('source', 'target', 'mapping', 'retarget', 'native', 'package'))
    accepted = all(ready.values())
    return {'project': data['project'], 'gates': {g: data['gates'][g]['status'] for g in GATES},
            'repair_blocked': repair_blocked, 'next_action': 'RUN_DISCRIMINATOR' if repair_blocked else data['next_test'],
            'diagnostic_package_checks_recorded': diagnostic,
            'accepted_slice_evidence_recorded': accepted,
            'full_set_expansion_allowed_by_record': accepted and not repair_blocked,
            'limitation': 'Hashes and receipt structure checked; evidence truth and behavior require independent review.'}


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'duplicate JSON field: ' + key)
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError('nonfinite JSON constant: ' + value)
    return json.loads(path.read_text(), object_pairs_hook=unique, parse_constant=invalid_constant)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('validate-fixture', 'verify-mapping', 'inspect-source-motion', 'summarize-receipt'))
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    try:
        fixture_hash = hashlib.sha256(args.path.read_bytes()).hexdigest() if args.command == 'inspect-source-motion' else None
        data = load_json(args.path)
        if args.command == 'validate-fixture':
            result = validate_fixture(data)
        elif args.command == 'verify-mapping':
            result = verify_mapping(data)
        elif args.command == 'inspect-source-motion':
            result = inspect_source_motion(data)
            require(hashlib.sha256(args.path.read_bytes()).hexdigest() == fixture_hash, 'fixture changed during inspection')
            result['identities']['fixture_file_sha256'] = fixture_hash
        else:
            result = summarize_receipt(data, args.path.resolve().parent)
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, OSError, IndexError) as error:
        print('FAILED: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
