import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/cyberpunk2077-animation-retargeting/scripts'


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    value = importlib.util.module_from_spec(spec);spec.loader.exec_module(value)
    return value


pipeline = module('native_pipeline')
inspect = module('asset_inspect')


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='retarget tools ')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        kit = self.root / 'kit';kit.mkdir()
        cli = kit / 'WolvenKit.CLI';cli.write_text('#!/bin/sh\nexit 0\n');cli.chmod(0o755)
        (kit / 'WolvenKit.Modkit.dll').write_bytes(b'fixture assembly')
        (self.root / 'adapter.dll').write_bytes(b'fixture adapter')
        for name in ('base.anims', 'base.rig'):(self.root / name).write_bytes(b'CR2Wfixture')
        self.authored = self.root / 'authored.glb'
        document = {'animations': [{'name': 'selected', 'extras': {'animationType': 'Normal', 'rootMotionType': 'None'}}]}
        raw = json.dumps(document).encode();raw += b' ' * (-len(raw) % 4)
        self.authored.write_bytes(struct.pack('<5I', 0x46546C67, 2, 20 + len(raw), len(raw), 0x4E4F534A) + raw)
        self.config = self.root / 'fixture.json'
        self.config.write_text(json.dumps({'schema': 1, 'inputs': {'native': 'base.anims', 'rig': 'base.rig', 'authored': 'authored.glb'},
            'tools': {'wolvenkit': 'kit', 'native_adapter': 'adapter.dll', 'node': sys.executable, 'dotnet': sys.executable},
            'output': 'output', 'lock': str(self.root / 'heavy.lock')}))
        self.calls = []

    def fake_execute(self, argv, folder, expected, kind, cfg, lock_fd):
        self.calls.append(folder.parent.name)
        expected.write_bytes(b'glTFfixture' if kind == 'glb' else b'CR2Wfixture' if kind == 'cr2w' else b'{"passed":true}')
        return {'command': argv, 'output': str(expected), 'sha256': pipeline.sha(expected), 'log': str(folder / 'stdout.log'), 'seconds': .01}

    def test_plan_is_read_only_and_resume_reuses_verified_outputs(self):
        self.assertEqual(len(pipeline.run(self.config, 'plan')['pending']), 10)
        self.assertFalse((self.root / 'output').exists())
        with patch.object(pipeline, 'execute', self.fake_execute), contextlib.redirect_stderr(io.StringIO()):
            result = pipeline.run(self.config, 'run')
            self.assertEqual(result['stepsRun'], 10)
            self.assertEqual(pipeline.run(self.config, 'run')['stepsRun'], 0)
        self.assertEqual(len(self.calls), 10)
        Path(result['native']).write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'Completed output changed'):
            pipeline.run(self.config, 'run')

    def test_failed_stage_resumes_without_repeating_successful_stages(self):
        def interrupted(*args):
            if args[1].parent.name == '03-baseline-export':raise RuntimeError('fixture failure')
            return self.fake_execute(*args)
        with patch.object(pipeline, 'execute', interrupted), contextlib.redirect_stderr(io.StringIO()):
            result = pipeline.run(self.config, 'run')
        self.assertEqual(result['failedStep'], 'baseline-export')
        with patch.object(pipeline, 'execute', self.fake_execute), contextlib.redirect_stderr(io.StringIO()):
            result = pipeline.run(self.config, 'run')
        self.assertEqual(result['stepsReused'], 2)
        self.assertEqual(self.calls.count('01-baseline-json'), 1)
        self.assertTrue((self.root / 'output/03-baseline-export/attempt-001').is_dir())
        self.assertTrue((self.root / 'output/03-baseline-export/attempt-002').is_dir())

    def test_changed_input_invalidates_reuse(self):
        with patch.object(pipeline, 'execute', self.fake_execute), contextlib.redirect_stderr(io.StringIO()):pipeline.run(self.config, 'run')
        (self.root / 'base.anims').write_bytes(b'CR2Wchanged')
        with self.assertRaisesRegex(ValueError, 'Inputs, tools or config changed'):pipeline.run(self.config, 'run')

    def test_lock_contention_does_not_start_another_job(self):
        with (self.root / 'heavy.lock').open('w') as lock:
            pipeline.fcntl.flock(lock, pipeline.fcntl.LOCK_EX)
            self.assertEqual(pipeline.run(self.config, 'run')['status'], 'BUSY')
        self.assertFalse((self.root / 'output').exists())

    def test_exit_zero_without_output_is_failure(self):
        cfg = pipeline.load_config(self.config);folder = self.root / 'missing';folder.mkdir()
        with (self.root / 'lock').open('w') as lock, self.assertRaisesRegex(RuntimeError, 'no nonempty expected output'):
            pipeline.execute([sys.executable, '-c', 'pass'], folder, folder / 'missing.anims', 'cr2w', cfg, lock.fileno())

    def test_exit_zero_with_logged_wolvenkit_error_is_failure(self):
        cfg = pipeline.load_config(self.config);folder = self.root / 'logged-error';folder.mkdir()
        with (self.root / 'lock').open('w') as lock, self.assertRaisesRegex(RuntimeError, 'Tool failed'):
            pipeline.execute([sys.executable, '-c', 'print("[ 0: Error       ] - conversion failed")'], folder, folder / 'output', 'cr2w', cfg, lock.fileno())

    def test_timeout_terminates_tool(self):
        cfg = pipeline.load_config(self.config);cfg['timeout'] = .05
        folder = self.root / 'timeout';folder.mkdir()
        with (self.root / 'lock').open('w') as lock, self.assertRaisesRegex(RuntimeError, 'process group stopped'):
            pipeline.execute([sys.executable, '-c', 'import time;time.sleep(5)'], folder, folder / 'output', 'cr2w', cfg, lock.fileno())

    def test_tool_receives_configured_runtime_root(self):
        cfg = pipeline.load_config(self.config);folder = self.root / 'environment';folder.mkdir()
        code = 'import os,json;print(json.dumps({"passed":True,"root":os.environ["DOTNET_ROOT"]}))'
        with (self.root / 'lock').open('w') as lock:
            result = pipeline.execute([sys.executable, '-c', code], folder, folder / 'stdout.log', 'report', cfg, lock.fileno())
        self.assertEqual(json.loads(Path(result['output']).read_text())['root'], str(Path(cfg['executables']['dotnet']).parent))

    def test_input_directory_cannot_be_output(self):
        value = json.loads(self.config.read_text());value['output'] = '.';self.config.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'must not contain source'):pipeline.load_config(self.config)


class AssetInspectionTests(unittest.TestCase):
    def test_archive_locator_reads_index_and_rejects_truncation(self):
        self.assertEqual(inspect.depot_hash('base/gameplay/anim_graphs/player_ranged.animgraph'), 9415081112732784683)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'fixture.archive';wanted = 12345
            index = bytearray(28 + 56);struct.pack_into('<III', index, 16, 1, 0, 0);struct.pack_into('<Q', index, 28, wanted)
            path.write_bytes(struct.pack('<4sIQI', b'RDAR', 12, 20, len(index)) + index)
            self.assertTrue(inspect.archive_has(path, wanted));self.assertFalse(inspect.archive_has(path, 999))
            path.write_bytes(path.read_bytes()[:-1])
            with self.assertRaises(ValueError):inspect.archive_has(path, wanted)

    def test_graph_readback_accepts_renumbering_but_detects_alias_changes(self):
        def graph(one, two, shared):
            return {'Data': {'RootChunk': {'$type': 'animAnimGraph', 'nodesToInit': [
                {'HandleId': one, 'Data': {'$type': 'animAnimNode_FloatConstant', 'value': .1}},
                {'HandleId': two, 'Data': {'$type': 'animAnimNode_FloatConstant', 'value': .1}}],
                'rootNode': {'HandleRefId': one}, 'shared': {'HandleRefId': one if shared else two}}}}
        with tempfile.TemporaryDirectory() as temp:
            a, b = (Path(temp) / n for n in ('a.json', 'b.json'))
            a.write_text(json.dumps(graph('0', '1', True)));b.write_text(json.dumps(graph('11', '12', True)))
            self.assertTrue(inspect.compare_graphs(a, b)['passed'])
            b.write_text(json.dumps(graph('11', '12', False)))
            self.assertFalse(inspect.compare_graphs(a, b)['passed'])

    def test_summary_does_not_expand_nested_handle_payload(self):
        payload = {'nodes': [{'HandleId': str(i), 'Data': {'secretLargeTree': 'x' * 10000}} for i in range(1000)]}
        result = inspect.short(payload)
        self.assertLess(len(json.dumps(result)), 1000)
        self.assertEqual(result['nodes'][-1]['omittedItems'], 980)


if __name__ == '__main__':
    unittest.main()
