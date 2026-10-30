import contextlib
import hashlib
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
ron = module('ron_action_inventory')


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

    def make_batch(self):
        second = self.root / 'second.json'
        value = json.loads(self.config.read_text());value['output'] = 'second-output'
        second.write_text(json.dumps(value))
        manifest = self.root / 'batch.json'
        manifest.write_text(json.dumps({'schema': 1, 'fixtures': [self.config.name, second.name]}))
        return manifest, second

    def test_batch_preflights_every_fixture_before_any_mutation(self):
        manifest, second = self.make_batch()
        value = json.loads(second.read_text());value['inputs']['rig'] = 'missing.rig';second.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'Missing or empty'), patch.object(pipeline, 'execute', self.fake_execute):
            pipeline.batch(manifest, 'run')
        self.assertFalse((self.root / 'output').exists());self.assertFalse(self.calls)

    def test_batch_stops_on_failure_and_resumes_serially(self):
        manifest, _ = self.make_batch()
        def interrupted(*args):
            if args[4]['output'].name == 'second-output' and args[1].parent.name == '03-baseline-export':
                raise RuntimeError('fixture failure')
            return self.fake_execute(*args)
        with patch.object(pipeline, 'execute', interrupted), contextlib.redirect_stderr(io.StringIO()):
            result = pipeline.batch(manifest, 'run')
        self.assertEqual(result['status'], 'FAILED');self.assertEqual(result['stepsRun'], 12)
        with patch.object(pipeline, 'execute', self.fake_execute), contextlib.redirect_stderr(io.StringIO()):
            result = pipeline.batch(manifest, 'run')
            self.assertEqual((result['stepsRun'], result['stepsReused']), (8, 12))
            result = pipeline.batch(manifest, 'run')
            self.assertEqual((result['stepsRun'], result['stepsReused']), (0, 20))
        self.assertEqual(len(self.calls), 20);self.assertFalse(result['runtimeVerified'])

    def test_batch_rejects_later_unrecognized_output_before_starting(self):
        manifest, _ = self.make_batch()
        existing = self.root / 'second-output';existing.mkdir();(existing/'valuable.txt').write_text('preserve')
        with self.assertRaisesRegex(ValueError, 'unrecognized nonempty'):
            pipeline.batch(manifest, 'run')
        self.assertFalse((self.root/'output').exists())
        self.assertEqual((existing/'valuable.txt').read_text(), 'preserve')

    def test_batch_rejects_overlapping_outputs_and_cross_fixture_sources(self):
        manifest, second = self.make_batch()
        value = json.loads(second.read_text());value['output'] = 'output/child';second.write_text(json.dumps(value))
        with self.assertRaisesRegex(ValueError, 'overlap'):pipeline.batch(manifest, 'plan')
        value['output'] = 'second-output';second.write_text(json.dumps(value))
        first = json.loads(self.config.read_text());first['output'] = 'kit';self.config.write_text(json.dumps(first))
        with self.assertRaisesRegex(ValueError, 'source inputs or tools'):pipeline.batch(manifest, 'plan')

    def test_event_fraction_rejected_before_native_work(self):
        raw = self.authored.read_bytes();document = json.loads(raw[20:])
        document['animations'][0]['extras']['animEvents'] = [{'type': 'Phase', 'startFrame': 27.5, 'durationInFrames': 2}]
        def write():
            data = json.dumps(document).encode();data += b' ' * (-len(data) % 4)
            self.authored.write_bytes(struct.pack('<5I', 0x46546C67, 2, 20+len(data), len(data), 0x4E4F534A)+data)
        write()
        with self.assertRaisesRegex(ValueError, 'unsigned integer native event frame'):pipeline.run(self.config, 'plan')
        self.assertFalse((self.root / 'output').exists())
        document['animations'][0]['extras']['animEvents'][0]['startFrame'] = 28.0;write()
        self.assertEqual(pipeline.run(self.config, 'plan')['status'], 'OPEN')
        document['animations'][0]['extras']['animEvents'] = None;write()
        self.assertEqual(pipeline.run(self.config, 'plan')['status'], 'OPEN')


class SourceInventoryTests(unittest.TestCase):
    def test_nested_arrays_keep_pairing_and_deduplicate_extraction_paths(self):
        ref = lambda n: {'ObjectPath': 'Game/Animations/' + n + '.0', 'ObjectName': "AnimSequence'"+n+"'"}
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'class.json'
            path.write_text(json.dumps([{'Name': 'Synthetic', 'Properties': {
                'FireSingle': [{'Body_FP': ref('arms'), 'Gun_FP': ref('weapon'), 'Body_TP': ref('third')},
                               {'Body_FP': ref('arms'), 'Gun_FP': ref('weapon2')}],
                'Idle_FP': ref('idle') }}]))
            before = path.read_bytes();result = ron.inventory(path, ['FireSingle'])
            self.assertEqual((result['referenceCount'], result['packageCount']), (4, 3))
            self.assertEqual([r['field'] for r in result['references']],
                ['FireSingle.0.Body_FP', 'FireSingle.0.Gun_FP', 'FireSingle.1.Body_FP', 'FireSingle.1.Gun_FP'])
            self.assertNotIn('Game/Animations/third', result['packages'])
            self.assertEqual(result['sha256'], hashlib.sha256(before).hexdigest())
            self.assertEqual(path.read_bytes(), before);self.assertFalse(result['sourceSemanticsVerified'])
            with self.assertRaisesRegex(ValueError, 'Unknown action'):ron.inventory(path, ['typo'])
            with patch.object(sys, 'argv', ['inventory', str(path), '--output', str(path)]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(ron.main(), 1)
            self.assertEqual(path.read_bytes(), before)

    def test_malformed_or_empty_references_fail_explicitly(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'class.json'
            for value in [[], {}, {'Properties': {}}, {'Properties': {'Idle_FP': {'ObjectPath': 4}}},
                          {'Properties': {'Idle_FP': {'ObjectPath': 'Game/../secret.0'}}}]:
                path.write_text(json.dumps(value))
                with self.subTest(value=value), self.assertRaises(ValueError):ron.inventory(path)


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


class RigMaskTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'rig.json'
        source = SCRIPTS.parent / 'evals/fixtures/rig-mask.json'
        self.path.write_bytes(source.read_bytes())
        self.doc = json.loads(self.path.read_bytes())
        self.rig = self.doc['Data']['RootChunk']
        self.part = self.rig['parts'][0]

    def check(self, *bones):
        self.path.write_text(json.dumps(self.doc))
        return inspect.rig_mask(self.path, '_base_upperbody', bones)

    def test_carriers_are_excluded_while_camera_and_chest_survive(self):
        before = self.path.read_bytes()
        result = inspect.rig_mask(self.path, '_base_upperbody', ['Hips', 'Torso_COG_Control_JNT',
            'Torso_fppCamera_Control_GRP', 'Torso_Chest_Control_Override_GRP', 'WeaponRight'])
        self.assertEqual([b['weight'] for b in result['bones']], [0, 0, 1, 1, 1])
        self.assertEqual(result['nonzeroWeightBones'], 7)
        self.assertEqual(result['sha256'], hashlib.sha256(before).hexdigest())
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse(result['activeMaskVerified']);self.assertFalse(result['runtimeVerified'])

    def test_nested_fractional_overrides_and_separate_single_bone(self):
        def tree(n, w, children):
            return {'rootBone': {'$type': 'CName', '$value': n}, 'weight': w, 'subtreesToChange': children}
        self.part['treeBones'] = [tree('Torso_Chest_Control_GRP', .75, [
            tree('Torso_Chest_Control_Override_GRP', .25, [tree('Torso_Chest_Driver_GRP', 0, [])])])]
        self.part['singleBones'] = [{'bone': {'$type': 'CName', '$value': 'Hips'}, 'weight': .5}]
        self.part['bonesWithRotationInModelSpace'] = [{'$type': 'CName', '$value': 'Torso_fppCamera_Control_GRP'}]
        result = self.check('Hips', 'Torso_Chest_Control_Override_GRP', 'Torso_Chest_Driver_GRP', 'Torso_fppCamera_Control_GRP')
        self.assertEqual([b['weight'] for b in result['bones']], [.5, .25, 0, .75])
        self.assertEqual([b['modelSpaceRotationDeclared'] for b in result['bones']], [False, False, False, True])

    def test_conflicting_overlap_is_rejected_instead_of_guessing_precedence(self):
        self.part['treeBones'][-1]['weight'] = .5
        with self.assertRaisesRegex(ValueError, 'conflicting'):self.check()
        self.part['treeBones'][-1]['weight'] = 1
        self.part['singleBones'] = [{'bone': {'$type': 'CName', '$value': 'WeaponRight'}, 'weight': 0}]
        with self.assertRaisesRegex(ValueError, 'conflicting'):self.check()

    def test_invalid_hierarchies_are_rejected(self):
        original = list(self.rig['boneParentIndexes'])
        for parents in [original[:-1], [True]+original[1:], [10]+original[1:], [-2]+original[1:],
                        [0]+original[1:], [4]+original[1:]]:
            with self.subTest(parents=parents):
                self.rig['boneParentIndexes'] = parents
                with self.assertRaises(ValueError):self.check()
        self.rig['boneParentIndexes'] = original
        self.rig['boneNames'][1] = self.rig['boneNames'][0]
        with self.assertRaises(ValueError):self.check()

    def test_invalid_weights_references_and_compiled_masks_are_rejected(self):
        entry = self.part['treeBones'][0]
        for value in [True, -.1, 1.1, 10**1000, float('nan'), float('inf'), '1']:
            with self.subTest(weight=value):
                entry['weight'] = value
                with self.assertRaises(ValueError):self.check()
        entry['weight'] = 1
        entry['subtreesToChange'] = [{'rootBone': {'$type': 'CName', '$value': 'Root'}, 'weight': 0, 'subtreesToChange': []}]
        with self.assertRaisesRegex(ValueError, 'descend'):self.check()
        entry['subtreesToChange'] = []
        for key in ['mask', 'maskRotMS']:
            self.part[key] = [1]
            with self.assertRaisesRegex(ValueError, 'Compiled'):self.check()
            self.part[key] = []
        entry['rootBone']['$value'] = 'Missing'
        with self.assertRaisesRegex(ValueError, 'Unknown bone'):self.check()

    def test_cli_json_errors_and_bounded_selection(self):
        with patch.object(sys, 'argv', ['inspect', 'rig-mask', str(self.path), '--mask', '_base_upperbody', '--bone', 'Hips']), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(inspect.main(), 0)
        self.assertEqual(json.loads(out.getvalue())['bones'][0]['weight'], 0)
        with self.assertRaisesRegex(ValueError, 'exactly one'):inspect.rig_mask(self.path, 'missing', [])
        with self.assertRaisesRegex(ValueError, 'Unknown selected'):inspect.rig_mask(self.path, '_base_upperbody', ['missing'])
        with self.assertRaisesRegex(ValueError, 'at most 32'):inspect.rig_mask(self.path, '_base_upperbody', [str(i) for i in range(33)])
        self.path.write_text('{"Data":null}')
        with patch.object(sys, 'argv', ['inspect', 'rig-mask', str(self.path), '--mask', '_base_upperbody']), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(inspect.main(), 1)
        self.assertEqual(json.loads(out.getvalue())['status'], 'FAILED')


if __name__ == '__main__':
    unittest.main()
