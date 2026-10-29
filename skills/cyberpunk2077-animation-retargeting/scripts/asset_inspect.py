#!/usr/bin/env python3
"""Bounded archive ownership and CR2W graph inspection for agents; read-only."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import struct
import sys

sys.setrecursionlimit(20000)


def depot_hash(path):
    value = 14695981039346656037
    for byte in path.lower().replace('/', '\\').encode():
        value = ((value ^ byte) * 1099511628211) & ((1 << 64) - 1)
    return value


def archive_has(path, wanted):
    with path.open('rb') as stream:
        magic, version, offset, size = struct.unpack('<4sIQI', stream.read(20))
        if magic != b'RDAR' or version != 12 or offset + size > path.stat().st_size:
            raise ValueError('Unsupported or truncated archive header')
        stream.seek(offset)
        header = stream.read(28)
        files, segments, dependencies = struct.unpack_from('<III', header, 16)
        if size != 28 + files * 56 + segments * 16 + dependencies * 8:
            raise ValueError('Invalid archive index layout')
        for _ in range(files):
            entry = stream.read(56)
            if len(entry) != 56:
                raise ValueError('Truncated archive file table')
            if struct.unpack_from('<Q', entry)[0] == wanted:
                return True
    return False


def load_graph(path):
    doc = json.loads(path.read_text())
    if doc.get('Data', {}).get('RootChunk', {}).get('$type') != 'animAnimGraph':
        raise ValueError('Expected serialized animAnimGraph')
    handles = {}
    stack = [doc['Data']]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            if 'HandleId' in value:
                if value['HandleId'] in handles:
                    raise ValueError('Duplicate handle: ' + value['HandleId'])
                handles[value['HandleId']] = value['Data']
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    return doc['Data'], handles


def short(value, limit=20):
    if isinstance(value, list):
        result = [short(x, limit) for x in value[:limit]]
        return result + ([{'omittedItems': len(value) - limit}] if len(value) > limit else [])
    if isinstance(value, dict):
        if 'HandleId' in value or 'HandleRefId' in value:
            return {'ref': value.get('HandleId', value.get('HandleRefId'))}
        if '$value' in value:
            return value['$value']
        return {k: short(v, limit) for k, v in value.items()
                if not k.startswith(('vis', 'debug')) and k not in ('poseInfoLogger', 'id')}
    return value[:500] + '...' if isinstance(value, str) and len(value) > 500 else value


def compare_graphs(first, second):
    left, lh = load_graph(first);right, rh = load_graph(second)
    matched = {};reverse = {};differences = [];count = 0;maximum = 0.0
    def mismatch(path, a, b):
        nonlocal count
        count += 1
        if len(differences) < 20:
            differences.append({'path': path, 'before': short(a, 3), 'after': short(b, 3)})
    def compare(a, b, path='Data'):
        nonlocal maximum
        if isinstance(a, dict) and ('HandleId' in a or 'HandleRefId' in a):
            i = a.get('HandleId', a.get('HandleRefId'))
            j = b.get('HandleId', b.get('HandleRefId')) if isinstance(b, dict) else None
            if i == '-1':
                if j != '-1':mismatch(path, i, j)
                return
            if i in matched:
                if matched[i] != j:mismatch(path + '/handle-alias', matched[i], j)
                return
            if i not in lh or j not in rh or j in reverse:
                mismatch(path + '/handle-identity', i, j);return
            matched[i] = j;reverse[j] = i
            compare(lh[i], rh[j], path + '/handle');return
        if isinstance(a, dict) and isinstance(b, dict):
            if set(a) != set(b):mismatch(path + '/keys', sorted(a), sorted(b))
            for key in sorted(a.keys() & b.keys()):compare(a[key], b[key], path + '/' + key)
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):mismatch(path + '/length', len(a), len(b))
            for i, (x, y) in enumerate(zip(a, b)):compare(x, y, path + '/' + str(i))
        elif type(a) in (int, float) and type(b) in (int, float):
            maximum = max(maximum, abs(a - b))
            if not math.isclose(a, b, rel_tol=2e-8, abs_tol=2e-8):mismatch(path, a, b)
        elif a != b:
            mismatch(path, a, b)
    compare(left, right)
    return {'passed': count == 0, 'matchedHandles': len(matched), 'sourceHandles': len(lh),
            'readbackHandles': len(rh), 'maxNumericDelta': maximum,
            'differenceCount': count, 'differences': differences, 'runtimeVerified': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    locate = sub.add_parser('locate', help='Find actual owning archives by depot hash')
    locate.add_argument('root', type=Path);locate.add_argument('depot')
    graph = sub.add_parser('graph', help='Summarize graph without printing nested handle trees')
    graph.add_argument('file', type=Path);graph.add_argument('--node');graph.add_argument('--clip')
    compare = sub.add_parser('compare-graphs', help='Check full graph properties and reference identity after serialization')
    compare.add_argument('authored', type=Path);compare.add_argument('readback', type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'locate':
            wanted = depot_hash(args.depot);matches = [];errors = [];scanned = 0
            paths = [args.root] if args.root.is_file() else sorted(args.root.rglob('*.archive'))
            if not paths:raise ValueError('No archives found at the supplied root')
            for path in paths:
                scanned += 1
                try:
                    if archive_has(path, wanted):matches.append(str(path.resolve()))
                except (OSError, ValueError, struct.error) as error:
                    errors.append({'archive': str(path), 'error': str(error)})
            result = {'depot': args.depot, 'hash': str(wanted), 'scanned': scanned, 'matches': matches,
                      'errors': errors, 'complete': not errors, 'loadOrderVerified': False}
        elif args.action == 'graph':
            doc, handles = load_graph(args.file)
            if args.node:
                if args.node not in handles:raise ValueError('Unknown node ID')
                result = {'node': args.node, 'data': short(handles[args.node])}
            else:
                clips = {k: v['animation']['$value'] for k, v in handles.items()
                         if v.get('$type') in ('animAnimNode_SkAnim', 'animAnimNode_SkFrameAnim', 'animAnimNode_SkSpeedAnim')}
                result = {'handles': len(handles), 'initializers': len(doc['RootChunk']['nodesToInit']),
                          'types': dict(Counter(v['$type'] for v in handles.values())),
                          'clips': sorted(set(clips.values()))}
                if args.clip:
                    result = {'clip': args.clip, 'nodes': [k for k, v in clips.items() if v == args.clip]}
        else:
            result = compare_graphs(args.authored, args.readback)
        print(json.dumps(result, indent=2))
        return 1 if result.get('passed') is False or result.get('complete') is False else 0
    except (OSError, ValueError, KeyError, struct.error) as error:
        print(json.dumps({'status': 'FAILED', 'error': str(error)}));return 1


if __name__ == '__main__':
    sys.exit(main())
