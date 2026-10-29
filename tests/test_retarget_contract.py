"""Synthetic contract regressions, never game/runtime certification."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/cyberpunk2077-animation-retargeting'
SCRIPT = SKILL / 'scripts/retarget_contract.py'
spec = importlib.util.spec_from_file_location('contract', SCRIPT)
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)


class FixtureTests(unittest.TestCase):
    def setUp(self):
        self.fixture = json.loads((SKILL / 'evals/fixtures/minimal.json').read_text())

    def test_valid_fixture_leaves_behavior_and_reference_pose_open(self):
        self.assertEqual(contract.validate_fixture(self.fixture)['behavior'], 'OPEN')
        self.assertEqual(contract.verify_mapping(self.fixture)['reference_pose_reconstruction'], 'OPEN')

    def test_parent_order_is_not_assumed(self):
        self.fixture['source']['skeleton']['parents'] = [1, -1]
        contract.validate_fixture(self.fixture)

    def test_reject_corrupt_skeletons_transforms_and_clocks(self):
        mutations = [
            lambda f: f['source']['skeleton'].update(parents=[1, 0]),
            lambda f: f['source']['skeleton'].update(parents=[-1, 99]),
            lambda f: f['source']['skeleton'].update(names=['root', 'root']),
            lambda f: f['source']['skeleton']['reference_local'][0].update(q=[0, 0, 0, 2]),
            lambda f: f['source']['skeleton']['reference_local'][0].update(s=[0, 1, 1]),
            lambda f: f['clip'].update(sample_times=[0, .5, .5]),
            lambda f: f['clip'].update(sample_times=[0, .5, 2]),
            lambda f: f['clip'].update(sample_times=[0, float('nan'), 1]),
            lambda f: f['clip']['local_samples'][1].pop(),
            lambda f: f['clip'].update(animation_type='additive', base_definition='none'),
            lambda f: f['clip'].update(interpolation='CUBICSPLINE'),
            lambda f: f.update(unsupported_semantics=['unknown source base']),
            lambda f: f['conventions'].update(quaternion='wxyz'),
            lambda f: f['conventions'].update(source_to_working=[0]*16),
        ]
        for mutate in mutations:
            data = copy.deepcopy(self.fixture)
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                contract.validate_fixture(data)

    def test_mapping_rejects_missing_duplicate_unknown_and_unjustified_bones(self):
        mutations = [
            lambda f: f['mapping'].pop(),
            lambda f: f['mapping'].append(f['mapping'][0]),
            lambda f: f['mapping'][1].update(source='unknown'),
            lambda f: f['mapping'][1].update(target='root'),
            lambda f: f['mapping'][1].update(source='root'),
            lambda f: f['unmapped_targets'].append({'target':'root','reason':'preserve'}),
        ]
        for mutate in mutations:
            data = copy.deepcopy(self.fixture)
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                contract.verify_mapping(data)
        self.fixture['mapping'].pop()
        self.fixture['unmapped_targets'] = [{'target':'hand', 'reason':''}]
        with self.assertRaises(ValueError):
            contract.verify_mapping(self.fixture)
        self.fixture['unmapped_targets'][0]['reason'] = 'preserve native helper track'
        contract.verify_mapping(self.fixture)

    def test_cli_rejects_malformed_duplicate_nonfinite_and_wrong_shapes(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'bad.json'
            for text in ('{', '{"schema_version":1,"schema_version":1}', '{"v":NaN}', '[]', 'null'):
                p.write_text(text)
                result = subprocess.run([sys.executable, '-B', str(SCRIPT), 'validate-fixture', str(p)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn('FAILED:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        def artifact(name, text):
            p = self.base / name
            p.write_text(text)
            return {'path':name, 'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
        self.proof = artifact('proof.txt', 'SYNTHETIC: no runtime observation')
        self.data = {
            'schema_version':1, 'project':'synthetic',
            'baseline':artifact('baseline.bin', 'original'),
            'candidate':artifact('candidate.bin', 'candidate'),
            'fixture':artifact('fixture.txt', 'synthetic input identities'),
            'current_gate':{'id':'native', 'question':'Do stored keys match?'},
            'gates':{g:{'status':'OPEN', 'evidence':[]} for g in contract.GATES},
            'attempts':[], 'discriminator':None, 'next_test':'Compare independently decoded stored times.'}

    def positive(self, gate):
        self.data['gates'][gate] = {'status':contract.POSITIVE[gate], 'scope':'synthetic test only',
            'fixture_sha256':self.data['fixture']['sha256'], 'candidate_sha256':self.data['candidate']['sha256'],
            'evidence':[self.proof], 'user_confirmation':'synthetic assertion, not a real user',
            'environment':'synthetic environment'}

    def summary(self):
        return contract.summarize_receipt(self.data, self.base)

    def failures(self, count):
        self.data['attempts'] = [{'gate':'native', 'hypothesis':'codec error', 'change':f'change {i}',
                                  'fixture_sha256':self.data['fixture']['sha256'],
                                  'result':'FAILED', 'evidence':[self.proof]} for i in range(count)]

    def discriminator(self, at):
        self.data['discriminator'] = {'gate':'native', 'question':'Writer or reader?',
            'fixture_sha256':self.data['fixture']['sha256'],
            'hypotheses':['writer changes time', 'reader misinterprets time'], 'after_attempt':at,
            'status':'CHECKED', 'evidence':[self.proof], 'result':'Synthetic independent parser result'}

    def test_offline_success_cannot_promote_visual_or_runtime(self):
        for gate in ('source', 'target', 'mapping', 'retarget', 'native', 'package'):
            self.positive(gate)
        result = self.summary()
        self.assertTrue(result['diagnostic_package_checks_recorded'])
        self.assertFalse(result['accepted_slice_evidence_recorded'])
        self.assertEqual(result['gates']['runtime'], 'OPEN')
        self.data['gates']['visual']['status'] = 'FAILED'
        self.assertTrue(self.summary()['diagnostic_package_checks_recorded'])
        self.assertFalse(self.summary()['full_set_expansion_allowed_by_record'])
        self.data['gates']['native']['status'] = 'FAILED'
        self.assertFalse(self.summary()['diagnostic_package_checks_recorded'])

    def test_only_all_scoped_categories_allow_expansion(self):
        for gate in contract.GATES:
            self.positive(gate)
        self.assertTrue(self.summary()['full_set_expansion_allowed_by_record'])
        self.failures(2)
        self.assertFalse(self.summary()['full_set_expansion_allowed_by_record'])

    def test_reject_false_success_category_and_missing_evidence(self):
        for gate in ('visual', 'runtime'):
            self.data['gates'][gate]['status'] = 'CHECKED'
            with self.assertRaises(ValueError):
                self.summary()
            self.data['gates'][gate]['status'] = 'OPEN'
        self.positive('native')
        self.data['gates']['native']['evidence'] = []
        with self.assertRaises(ValueError):
            self.summary()

    def test_reject_stale_candidate_fixture_or_missing_confirmation(self):
        self.positive('runtime')
        record = self.data['gates']['runtime']
        for field, value in (('candidate_sha256','0'*64), ('fixture_sha256','0'*64), ('user_confirmation','')):
            saved = record[field]
            record[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.summary()
            record[field] = saved

    def test_detect_changed_files_and_baseline_overwrite(self):
        self.positive('native')
        for field in ('baseline', 'candidate', 'fixture'):
            p = self.base / self.data[field]['path']
            original = p.read_bytes()
            p.write_bytes(b'changed')
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.summary()
            p.write_bytes(original)
        (self.base / self.proof['path']).write_text('changed evidence')
        with self.assertRaises(ValueError):
            self.summary()
        self.data['candidate'] = self.data['baseline']
        with self.assertRaisesRegex(ValueError, 'overwrite baseline'):
            self.summary()

    def test_baseline_hardlink_is_not_an_isolated_candidate(self):
        os.link(self.base / 'baseline.bin', self.base / 'alias.bin')
        self.data['candidate'] = dict(self.data['baseline'], path='alias.bin')
        with self.assertRaisesRegex(ValueError, 'overwrite baseline'):
            self.summary()

    def test_failed_gate_evidence_is_preserved_and_rehashed(self):
        self.data['gates']['native'] = {'status':'FAILED', 'evidence':[self.proof]}
        self.summary()
        (self.base / self.proof['path']).write_text('altered failure report')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.summary()

    def test_two_failures_require_actual_current_discriminator(self):
        self.failures(1)
        self.assertFalse(self.summary()['repair_blocked'])
        self.failures(2)
        self.assertEqual(self.summary()['next_action'], 'RUN_DISCRIMINATOR')
        self.discriminator(2)
        self.data['discriminator']['status'] = 'OPEN'
        self.assertTrue(self.summary()['repair_blocked'])
        self.data['discriminator']['status'] = 'CHECKED'
        self.data['discriminator']['gate'] = 'mapping'
        self.assertTrue(self.summary()['repair_blocked'])
        self.data['discriminator']['gate'] = 'native'
        self.assertFalse(self.summary()['repair_blocked'])
        self.failures(4)
        self.assertTrue(self.summary()['repair_blocked'])
        self.discriminator(4)
        self.assertFalse(self.summary()['repair_blocked'])
        self.data['discriminator']['evidence'] = []
        with self.assertRaises(ValueError):
            self.summary()

    def test_another_fixture_cannot_reset_this_repair_loop(self):
        self.failures(2)
        self.discriminator(2)
        self.data['discriminator']['fixture_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'stale discriminator'):
            self.summary()
        self.discriminator(2)
        self.data['attempts'][0]['fixture_sha256'] = '0'*64
        with self.assertRaisesRegex(ValueError, 'another fixture'):
            self.summary()

    def test_discriminator_cannot_be_future_or_same_hypothesis(self):
        self.failures(2)
        self.discriminator(3)
        with self.assertRaises(ValueError):
            self.summary()
        self.discriminator(2)
        self.data['discriminator']['hypotheses'] = ['one', 'one']
        with self.assertRaises(ValueError):
            self.summary()

    def test_no_runtime_baseline_is_explicit(self):
        self.data['baseline'] = None
        self.data['baseline_note'] = 'No runtime baseline exists.'
        self.assertFalse(self.summary()['accepted_slice_evidence_recorded'])

    def test_cli_is_read_only_and_does_not_hide_failed_gates(self):
        self.data['gates']['native']['status'] = 'FAILED'
        status = self.base / 'STATUS.json'
        status.write_text(json.dumps(self.data))
        before = {p.name:p.read_bytes() for p in self.base.iterdir()}
        result = subprocess.run([sys.executable, '-B', str(SCRIPT), 'summarize-receipt', str(status)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['gates']['native'], 'FAILED')
        self.assertEqual(before, {p.name:p.read_bytes() for p in self.base.iterdir()})


if __name__ == '__main__':
    unittest.main()
