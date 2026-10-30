#!/usr/bin/env python3
"""Inventory explicit first-person references in exported RoN animation data."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def inventory(path, actions=()):
    raw = path.read_bytes()
    records = json.loads(raw)
    if isinstance(records, dict):
        records = [records]
    if not isinstance(records, list) or not records:
        raise ValueError('Expected exported class records with Properties')
    rows, available = [], set()

    def walk(value, field, context, first_person):
        if isinstance(value, dict):
            if 'ObjectPath' in value and first_person:
                ref = value['ObjectPath']
                if not isinstance(ref, str) or not ref or '\\' in ref or '..' in ref.split('/'):
                    raise ValueError('Invalid ObjectPath at ' + '.'.join(field))
                # Export object index is not part of the extraction package path.
                package = re.sub(r'\.\d+$', '', ref)
                if '/' not in package:
                    raise ValueError('Expected package path at ' + '.'.join(field))
                rows.append({**context, 'field': '.'.join(field), 'objectPath': ref,
                             'packagePath': package, 'objectName': value.get('ObjectName')})
            for key, child in value.items():
                walk(child, [*field, key], context, first_person or key.endswith('_FP'))
        elif isinstance(value, list):
            for i, child in enumerate(value):
                walk(child, [*field, str(i)], context, first_person)

    for index, record in enumerate(records):
        if not isinstance(record, dict) or not isinstance(record.get('Properties'), dict):
            raise ValueError('Every record must contain Properties')
        available.update(record['Properties'])
        for action, value in record['Properties'].items():
            if not actions or action in actions:
                walk(value, [action], {'record': index, 'class': record.get('Name'), 'action': action}, action.endswith('_FP'))
    missing = set(actions) - available
    if missing:
        raise ValueError('Unknown action(s): ' + ', '.join(sorted(missing)))
    if not rows:
        raise ValueError('No explicit first-person references in selected properties')
    return {'status': 'CHECKED', 'source': str(path), 'sha256': hashlib.sha256(raw).hexdigest(),
            'referenceCount': len(rows), 'packageCount': len({r['packagePath'] for r in rows}),
            'references': rows, 'packages': sorted({r['packagePath'] for r in rows}),
            'sourceSemanticsVerified': False, 'runtimeVerified': False,
            'limits': ['Explicit exported references only; inherited defaults and montage internals are not resolved.',
                       'Field paths retain array index and Body_FP/Gun_FP pairing; names do not prove additive semantics.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--action', action='append', default=[], help='Exact top-level property; repeat to select several')
    parser.add_argument('--output', type=Path, help='Write complete inventory to a new file; print only its summary')
    args = parser.parse_args()
    try:
        result = inventory(args.source.resolve(), args.action)
        if args.output:
            with args.output.open('x') as stream:
                json.dump(result, stream, indent=2);stream.write('\n')
            result = {k: v for k, v in result.items() if k not in ('references', 'packages')}
            result['output'] = str(args.output)
    except Exception as error:
        result = {'status': 'FAILED', 'error': str(error)}
    print(json.dumps(result, indent=2))
    return int(result['status'] == 'FAILED')


if __name__ == '__main__':
    raise SystemExit(main())
