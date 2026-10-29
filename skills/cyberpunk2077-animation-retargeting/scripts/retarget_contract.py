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
    parser.add_argument('command', choices=('validate-fixture', 'verify-mapping', 'summarize-receipt'))
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    try:
        data = load_json(args.path)
        if args.command == 'validate-fixture':
            result = validate_fixture(data)
        elif args.command == 'verify-mapping':
            result = verify_mapping(data)
        else:
            result = summarize_receipt(data, args.path.resolve().parent)
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, TypeError, OSError, IndexError) as error:
        print('FAILED: ' + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
