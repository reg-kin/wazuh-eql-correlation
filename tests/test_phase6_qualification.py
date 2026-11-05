"""Offline qualification of retained evidence and strict inventory regressions."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import validate_development as development
import validate_repository as release

ROOT = release.ROOT


def load(name):
    return json.loads((ROOT / name).read_text())


class QualificationChecks(unittest.TestCase):
    def test_retained_evidence_and_assertions(self):
        path = ROOT / 'docs/verification/phase6/6a-v1/results.json'
        evidence = json.loads(path.read_text())
        qualification = load('tests/fixtures/phase6/qualification.json')
        fixtures = {s['id']: s for s in load('tests/fixtures/phase6/scenarios.json')}
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), qualification['evidence_sha256'])
        self.assertEqual(evidence['engine']['version']['number'], '8.19.20')
        self.assertEqual(evidence['request_parameters'],
                         {'timestamp_field': 'timestamp', 'event_category_field': 'type.keyword', 'size': 10})
        self.assertEqual(len(evidence['scenarios']), 35)
        self.assertEqual(set(fixtures), set(qualification['scenarios']))
        self.assertEqual({s['id'] for s in evidence['scenarios']}, set(fixtures))
        self.assertEqual([s['outcome'] for s in evidence['scenarios']].count('PASS'), 31)
        self.assertEqual([s['outcome'] for s in evidence['scenarios']].count('INCONCLUSIVE'), 4)
        for s in evidence['scenarios']:
            with self.subTest(scenario=s['id']):
                fixture = fixtures[s['id']]
                expected = qualification['scenarios'][s['id']]
                self.assertEqual(s['http_status'], 200)
                self.assertFalse(any(s['response'].get(k, False) for k in
                                     ['is_partial', 'is_running', 'timed_out']))
                actual = [[e['_id'] for e in seq['events']]
                          for seq in s['response'].get('hits', {}).get('sequences', [])]
                self.assertEqual(s['actual'], actual)
                self.assertEqual(actual, expected['expected'])
                self.assertEqual(s['expected'], fixture['expected'])
                stored = {h['_id']: h['_source'] for h in s['indexed_documents']['hits']['hits']}
                self.assertEqual(stored, {e['id']: e['source'] for e in fixture['events']})
                self.assertEqual(s['indexing']['documents'], len(stored))
                self.assertEqual(s['indexing']['refresh']['_shards']['failed'], 0)
                self.assertTrue(s['field_caps']['fields'])
        for name, digest in evidence['rule_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)
        self.assertEqual(evidence['rule_sha256'], evidence['final_rule_sha256'])
        self.assertTrue(evidence['unrelated_indices_unchanged'])
        self.assertEqual(len(evidence['indices_before']), 0)
        self.assertEqual(len(evidence['indices_after']), 35)

    def test_boundary_and_username_dispositions(self):
        fixtures = {s['id']: s for s in load('tests/fixtures/phase6/scenarios.json')}
        q = load('tests/fixtures/phase6/qualification.json')['scenarios']
        for rule, seconds in [('priv', 1800), ('mal', 3600)]:
            scenario = fixtures[rule + '-exact-window']
            times = [dt.datetime.fromisoformat(e['source']['timestamp']) for e in scenario['events']]
            self.assertEqual((times[-1] - times[0]).total_seconds(), seconds)
            self.assertEqual(q[scenario['id']]['classification'], 'observed_inclusive_boundary')
            self.assertEqual(q[scenario['id']]['expected'], [[e['id'] for e in scenario['events']]])
        for suffix in ['absent', 'null']:
            name = 'priv-optional-user-' + suffix
            self.assertEqual(q[name], {'expected': [], 'classification': 'known_semantic_limitation'})
            data = fixtures[name]['events'][-1]['source']['data']
            if suffix == 'absent':
                self.assertNotIn('srcuser', data)
            else:
                self.assertIsNone(data['srcuser'])

    def test_historical_rejects_extra_missing_and_corrupt_files(self):
        manifest = load('docs/verification/PUBLICATION_MANIFEST.json')
        with tempfile.TemporaryDirectory(prefix='wcorr-contract-') as directory:
            root = Path(directory)
            for name in manifest['publication_files']:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                if name in development.CURRENT_DOCUMENTATION:
                    target.write_bytes(subprocess.check_output(
                        ['git', 'show', 'v1.0.0:' + name], cwd=ROOT))
                else:
                    shutil.copyfile(ROOT / name, target)
            check = release.RepositoryChecks('test_publication_manifest')
            check.setUpClass()
            with patch.object(release, 'ROOT', root):
                check.test_publication_manifest()
                extra = root / 'unexpected.json'
                extra.write_text('{}')
                with self.assertRaises(AssertionError):
                    check.test_publication_manifest()
                extra.unlink()
                target = root / 'README.md'
                original = target.read_bytes()
                target.write_bytes(original + b'\n')
                with self.assertRaises(AssertionError):
                    check.test_publication_manifest()
                target.unlink()
                with self.assertRaises(AssertionError):
                    check.test_publication_manifest()

    def test_development_rejects_unlisted_file(self):
        check = development.DevelopmentChecks('test_publication_manifest')
        check.setUpClass()
        with patch.object(release, 'candidates', return_value=release.candidates() + [ROOT / 'unexpected.json']):
            with self.assertRaises(AssertionError):
                check.test_publication_manifest()


if __name__ == '__main__':
    unittest.main()
