#!/usr/bin/env python3
"""Resumable native animation checks using the existing WolvenKit adapters."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

HELPERS = Path(__file__).resolve().parents[2] / 'cyberpunk2077-modding/scripts/native-animation'
STEPS = ('baseline-json', 'rig-json', 'baseline-export', 'prepare', 'import',
         'native-json', 'native-export', 'readback', 'authored-check', 'semantics')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def save(path, value):
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    os.replace(temporary, path)


def glb_names(path):
    import struct
    with path.open('rb') as stream:
        magic, version, size, length, kind = struct.unpack('<5I', stream.read(20))
        if (magic, version, kind) != (0x46546C67, 2, 0x4E4F534A) or size != path.stat().st_size:
            raise ValueError('Invalid authored GLB header')
        document = json.loads(stream.read(length))
    animations = document.get('animations', [])
    names = [a['name'] for a in animations]
    if not names or len(names) != len(set(names)):
        raise ValueError('Authored GLB needs unique selected clip names')
    for animation in animations:
        extras = animation.get('extras', {})
        if extras.get('animationType') not in ('Normal', 'Additive', 'AdditiveWithoutFirstFrame') or extras.get('rootMotionType') != 'None':
            raise ValueError('Unsupported animation type or root motion')
        for event in extras.get('animEvents') or []:
            for field in ('startFrame', 'durationInFrames'):
                value = event.get(field)
                if (isinstance(value, bool) or not isinstance(value, (int, float))
                        or not 0 <= value <= 0xffffffff or int(value) != value):
                    raise ValueError(f'{animation["name"]}: {field} must be an unsigned integer native event frame')
    if document.get('extras', {}).get('betaAdditiveRepresentation'):
        raise ValueError('Supply the unprepared authored GLB, not raw additive intermediates')
    return names


def load_config(path):
    config = json.loads(path.read_text())
    if config.get('schema') != 1:
        raise ValueError('Expected schema 1')
    def resolve(value):
        p = Path(value).expanduser()
        return (p if p.is_absolute() else path.parent / p).resolve()
    inputs = {name: resolve(config['inputs'][name]) for name in ('native', 'rig', 'authored')}
    kit = resolve(config['tools']['wolvenkit'])
    adapter = resolve(config['tools']['native_adapter'])
    executables = {}
    for name in ('node', 'dotnet'):
        value = config['tools'][name]
        found = shutil.which(value) if '/' not in value else str(resolve(value))
        if not found or not os.access(found, os.X_OK):
            raise ValueError('Missing executable: ' + name)
        executables[name] = str(Path(found).resolve())
    cli = kit / 'WolvenKit.CLI'
    if not os.access(cli, os.X_OK):
        raise ValueError('Missing WolvenKit.CLI executable')
    required = [*inputs.values(), adapter, cli, *map(Path, executables.values()),
                Path(__file__).resolve(), *HELPERS.glob('*.mjs')]
    libraries = list(kit.glob('*.dll'))
    if not libraries:
        raise ValueError('WolvenKit assemblies are missing')
    required += libraries + list(adapter.parent.glob('*.runtimeconfig.json')) + list(adapter.parent.glob('*.deps.json'))
    for p in required:
        if not p.is_file() or not p.stat().st_size:
            raise ValueError('Missing or empty input/tool: ' + str(p))
    for name in ('native', 'rig'):
        with inputs[name].open('rb') as stream:
            if stream.read(4) != b'CR2W':
                raise ValueError('Expected native CR2W: ' + name)
    names = glb_names(inputs['authored'])
    output = resolve(config['output'])
    if any(p.is_relative_to(output) for p in required):
        raise ValueError('Output directory must not contain source inputs or tools')
    timeout = float(config.get('timeout_seconds', 55))
    if not 0 < timeout <= 60:
        raise ValueError('timeout_seconds must be greater than 0 and at most 60')
    lock = resolve(config.get('lock', '/tmp/cp2077-heavy-work.lock'))
    identity = {'config': config, 'files': {str(p): sha(p) for p in sorted(set(required))}}
    fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    return dict(inputs=inputs, kit=kit, adapter=adapter, executables=executables,
                output=output, timeout=timeout, lock=lock, names=names,
                fingerprint=fingerprint, identity=identity)


def command(step, folder, cfg, completed):
    node = cfg['executables']['node']
    native = [cfg['executables']['dotnet'], str(cfg['adapter']), str(cfg['kit'])]
    wk = [str(cfg['kit'] / 'WolvenKit.CLI'), 'cr2w', '-s']
    original, rig, authored = (cfg['inputs'][n] for n in ('native', 'rig', 'authored'))
    def result(name):
        return Path(completed[name]['output'])
    if step in ('baseline-json', 'rig-json', 'native-json'):
        source = original if step == 'baseline-json' else rig if step == 'rig-json' else result('import')
        return wk + [str(source), '-o', str(folder)], folder / (source.name + '.json'), 'json'
    if step in ('baseline-export', 'native-export'):
        source = original if step == 'baseline-export' else result('import')
        output = folder / 'animation.glb'
        return native + ['export', str(source), str(rig), str(output)], output, 'glb'
    if step == 'prepare':
        output = folder / 'prepared.glb'
        return [node, str(HELPERS / 'check-animation.mjs'), 'prepare', str(authored), str(output), '--preserve-key-sampling'], output, 'glb'
    if step == 'import':
        output = folder / 'animation.anims'
        return native + ['import', str(original), str(rig), str(result('prepare')), str(output)], output, 'cr2w'
    if step == 'readback':
        output = folder / 'readback.glb'
        return [node, '--max-old-space-size=768', str(HELPERS / 'readback-animation.mjs'), str(result('native-json')), str(result('rig-json')), str(result('native-export')), str(output), '--required-clips', ','.join(cfg['names'])], output, 'glb'
    if step == 'authored-check':
        args = [str(HELPERS / 'check-animation.mjs'), 'verify-authored', str(result('baseline-json')), str(result('native-json')), str(authored), str(result('readback'))]
    else:
        args = [str(HELPERS / 'verify-semantics.mjs'), str(result('baseline-json')), str(result('native-json')), str(result('rig-json')), str(authored), str(result('baseline-export'))]
    return [node, *args], folder / 'stdout.log', 'report'


def execute(argv, folder, expected, kind, cfg, lock_fd):
    log = folder / 'stdout.log'
    env = dict(os.environ, DOTNET_PROCESSOR_COUNT='2', DOTNET_GCHeapHardLimit='0x80000000',
               LD_LIBRARY_PATH=str(cfg['kit']), OPENBLAS_NUM_THREADS='2', OMP_NUM_THREADS='2',
               DOTNET_CLI_TELEMETRY_OPTOUT='1', DOTNET_NOLOGO='1',
               DOTNET_ROOT=str(Path(cfg['executables']['dotnet']).parent))
    start = time.monotonic()
    with log.open('xb') as stream:
        process = subprocess.Popen(['nice', '-n', '15', *argv], stdout=stream, stderr=subprocess.STDOUT,
                                   env=env, start_new_session=True, pass_fds=(lock_fd,))
        try:
            code = process.wait(timeout=cfg['timeout'])
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            raise RuntimeError('Timed out; process group stopped. Log: ' + str(log))
    content = log.read_text(errors='replace')
    if code or re.search(r'^\[\s*\d+:\s*Error\s*\]', content, re.MULTILINE):
        raise RuntimeError(f'Tool failed (exit {code}); log: {log}')
    if not expected.is_file() or expected.stat().st_size == 0:
        raise RuntimeError('Tool produced no nonempty expected output: ' + str(expected))
    if kind in ('glb', 'cr2w'):
        with expected.open('rb') as stream:
            if stream.read(4) != (b'glTF' if kind == 'glb' else b'CR2W'):
                raise RuntimeError('Invalid output signature: ' + str(expected))
    else:
        value = json.loads(expected.read_text())
        if kind == 'report' and value.get('passed') is not True:
            raise RuntimeError('Verifier did not report passed:true')
    return {'command': argv, 'output': str(expected), 'sha256': sha(expected),
            'log': str(log), 'seconds': time.monotonic() - start}


def run(config_path, mode):
    cfg = load_config(config_path)
    output = cfg['output'];state_path = output / 'state.json'
    state = json.loads(state_path.read_text()) if state_path.exists() else None
    if state is None and output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError('Refusing an unrecognized nonempty output directory')
    if state and state['fingerprint'] != cfg['fingerprint']:
        raise ValueError('Inputs, tools or config changed. Use a fresh output directory; old evidence is preserved.')
    if state:
        for name, result in state['completed'].items():
            if not Path(result['output']).is_file() or sha(result['output']) != result['sha256']:
                raise ValueError('Completed output changed: ' + name + '. Use a fresh output directory.')
    completed = state['completed'] if state else {}
    pending = [name for name in STEPS if name not in completed]
    if mode != 'run':
        return {'status': 'CHECKED' if not pending else 'OPEN', 'completed': list(completed),
                'pending': pending, 'clips': cfg['names'], 'output': str(output), 'runtimeVerified': False}
    if not pending:
        return {'status': 'CHECKED', 'stepsRun': 0, 'stepsReused': len(STEPS),
                'native': completed['import']['output'], 'readback': completed['readback']['output'], 'runtimeVerified': False}
    with cfg['lock'].open('a+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {'status': 'BUSY', 'lock': str(cfg['lock']), 'stepsRun': 0, 'runtimeVerified': False}
        # Re-read under the lock: another invocation may have finished during preflight.
        if state_path.exists() and json.loads(state_path.read_text()) != state:
            raise ValueError('Run state changed during preflight; rerun to resume it')
        if state is None:
            if output.exists() and any(output.iterdir()):
                raise ValueError('Refusing an unrecognized nonempty output directory')
            output.mkdir(parents=True, exist_ok=True)
            state = {'fingerprint': cfg['fingerprint'], 'inputs': cfg['identity'], 'completed': {}, 'attempts': [], 'status': 'OPEN'}
            save(state_path, state)
        reused = len(state['completed'])
        for name in pending:
            attempt = 1 + sum(a['step'] == name for a in state['attempts'])
            folder = output / f'{STEPS.index(name)+1:02d}-{name}' / f'attempt-{attempt:03d}'
            folder.mkdir(parents=True, exist_ok=False)
            argv, expected, kind = command(name, folder, cfg, state['completed'])
            item = {'step': name, 'attempt': attempt, 'status': 'RUNNING', 'log': str(folder / 'stdout.log')}
            state['attempts'].append(item);state['status'] = 'RUNNING';save(state_path, state)
            try:
                result = execute(argv, folder, expected, kind, cfg, lock.fileno())
                state['completed'][name] = result;item['status'] = 'CHECKED'
            except Exception as error:
                item.update(status='FAILED', error=str(error));state['status'] = 'FAILED';save(state_path, state)
                return {'status': 'FAILED', 'failedStep': name, 'error': str(error), 'stepsReused': reused,
                        'stepsRun': len(state['completed']) - reused,
                        'resume': ['python3', '-B', str(Path(__file__).resolve()), 'run', str(config_path)], 'runtimeVerified': False}
            save(state_path, state)
            print(json.dumps({'step': name, 'status': 'CHECKED', 'seconds': round(result['seconds'], 3)}), file=sys.stderr, flush=True)
        # Source mutation during a run invalidates its combined receipt.
        if load_config(config_path)['fingerprint'] != cfg['fingerprint']:
            state['status'] = 'FAILED';save(state_path, state)
            raise ValueError('An input/tool changed during execution; this run is invalid')
        state['status'] = 'CHECKED';save(state_path, state)
        return {'status': 'CHECKED', 'stepsRun': len(pending), 'stepsReused': reused,
                'native': state['completed']['import']['output'], 'readback': state['completed']['readback']['output'],
                'receipt': str(state_path), 'runtimeVerified': False, 'visuallyReviewed': False}


def batch(path, mode):
    """Preflight the complete batch, then use the existing runner serially."""
    started = time.monotonic()
    manifest = json.loads(path.read_text())
    fixtures = manifest.get('fixtures')
    if manifest.get('schema') != 1 or not isinstance(fixtures, list) or not fixtures:
        raise ValueError('Batch needs schema 1 and a nonempty fixtures array of config paths')
    if any(not isinstance(p, str) or not p for p in fixtures):
        raise ValueError('Each fixture must be a config path')
    paths = [(path.parent / Path(p).expanduser()).resolve() for p in fixtures]
    if len(paths) != len(set(paths)):
        raise ValueError('Duplicate fixture config')
    configs = [load_config(p) for p in paths]
    outputs = [c['output'] for c in configs]
    sources = {path, *paths, *(Path(p) for c in configs for p in c['identity']['files'])}
    if len({c['lock'] for c in configs}) != 1:
        raise ValueError('Batch fixtures must use the same heavy-work lock')
    for i, output in enumerate(outputs):
        if any(p.is_relative_to(output) for p in sources | {c['lock'] for c in configs}):
            raise ValueError('Batch output contains a config, input, tool or lock')
        if any(output.is_relative_to(other) or other.is_relative_to(output) for other in outputs[:i]):
            raise ValueError('Batch outputs overlap')
    # Validate every existing receipt before the first mutation.
    planned = [run(p, 'plan') for p in paths]
    rows = []
    for p, plan in zip(paths, planned):
        before = time.monotonic()
        try:
            result = run(p, mode) if mode == 'run' else plan
        except Exception as error:
            result = {'status': 'FAILED', 'error': str(error), 'runtimeVerified': False}
        rows.append({'config': str(p), 'secondsThisInvocation': round(time.monotonic() - before, 3), **result})
        if result['status'] in ('FAILED', 'BUSY'):
            break
    statuses = [r['status'] for r in rows]
    status = 'FAILED' if 'FAILED' in statuses else 'BUSY' if 'BUSY' in statuses else 'CHECKED' if all(s == 'CHECKED' for s in statuses) else 'OPEN'
    return {'status': status, 'fixtures': rows, 'fixturesNotRun': [str(p) for p in paths[len(rows):]],
            'stepsRun': sum(r.get('stepsRun', 0) for r in rows),
            'stepsReused': sum(r.get('stepsReused', 0) for r in rows),
            'secondsThisInvocation': round(time.monotonic() - started, 3),
            'runtimeVerified': False, 'visuallyReviewed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('plan', 'run', 'status', 'batch-plan', 'batch-run', 'batch-status'))
    parser.add_argument('config', type=Path)
    args = parser.parse_args()
    try:
        result = batch(args.config.resolve(), args.action[6:]) if args.action.startswith('batch-') else run(args.config.resolve(), args.action)
    except Exception as error:
        result = {'status': 'FAILED', 'error': str(error), 'runtimeVerified': False}
    print(json.dumps(result, indent=2))
    return 0 if result['status'] in ('CHECKED', 'OPEN') else 75 if result['status'] == 'BUSY' else 1


if __name__ == '__main__':
    sys.exit(main())
