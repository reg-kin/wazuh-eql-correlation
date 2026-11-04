"""Recovery chronology, predicate isolation, preservation and engine evidence."""
import copy
import hashlib
import unittest
from collections import Counter
from unittest.mock import patch
import phase6gr_engine as recovery
import phase6g_engine as original
import phase6_engine as engine


class RecoveryChecks(unittest.TestCase):
    def test_gate(self):
        fs = recovery.load(recovery.SUITE['fixtures'])
        checks = recovery.validate_fixtures(fs, recovery.load(recovery.SUITE['mappings']))
        self.assertEqual(len(checks), 51)
        self.assertTrue(all(c['valid'] for c in checks))

    def test_all_46_original_reversals_rejected(self):
        fs = recovery.load(recovery.SUITE['fixtures'])
        old = {s['id']: s for s in recovery.load(original.SUITE['fixtures'])}
        checked = 0
        for n, scenario in enumerate(fs):
            if scenario['note'] in recovery.SPECIAL: continue
            bad = copy.deepcopy(fs)
            bad[n] = old[scenario['id']]
            with self.subTest(scenario=scenario['id']), self.assertRaises(ValueError):
                recovery.validate_fixtures(bad, recovery.load(recovery.SUITE['mappings']))
            checked += 1
        self.assertEqual(checked, 46)

    def test_predicate_isolation_and_expected_ids(self):
        fs = recovery.load(recovery.SUITE['fixtures'])
        for mutate in (
            lambda f: f[1]['events'][0]['source']['rule'].update(id='555'),
            lambda f: f[0].update(expected=[]),
            lambda f: f[0].update(expected=[list(reversed(f[0]['expected'][0]))]),
            lambda f: f[0]['events'][0]['source']['syscheck'].update(path='/other.php'),
            lambda f: f[20].update(expected=[]),
            lambda f: f[0].update(filter=f[1]['filter']),
        ):
            bad = copy.deepcopy(fs); mutate(bad)
            with self.assertRaises(ValueError):
                recovery.validate_fixtures(bad, recovery.load(recovery.SUITE['mappings']))

    def test_write_scope(self):
        client = recovery.ValidatingClient('http://127.0.0.1:19200', 'phase6-wcorr-6gr-v1-')
        with patch.object(client.opener, 'open') as opening:
            for method, path in [('DELETE', '/phase6-wcorr-6gr-v1-web004'), ('PUT', '/phase6-wcorr-6g-v1-web004')]:
                with self.assertRaises(ValueError): client.request(method, path, {})
            opening.assert_not_called()

    def test_recovery_evidence(self):
        if not (recovery.OUT / 'results.json').exists(): self.skipTest('Not executed')
        r = recovery.load('docs/verification/phase6/6gr-v1/results.json')
        fs = recovery.load(recovery.SUITE['fixtures'])
        self.assertEqual(r['fixtures'], fs)
        self.assertEqual(r['fixture_sha256'], recovery.digest(recovery.SUITE['fixtures']))
        self.assertEqual(r['original_fixture_sha256'], recovery.digest(original.SUITE['fixtures']))
        self.assertEqual(r['rule_sha256'], r['final_rule_sha256'])
        self.assertEqual(len(r['scenarios']), 51)
        self.assertEqual(r['offline_preexecution_validation'], recovery.validate_fixtures(fs, r['mappings']))
        self.assertEqual(Counter(s['outcome'] for s in r['scenarios']), {'PASS': 50, 'INCONCLUSIVE': 1})
        for s, f in zip(r['scenarios'], fs):
            with self.subTest(scenario=s['id']):
                self.assertEqual(s['id'], f['id'])
                self.assertEqual(s['http_status'], 200)
                self.assertEqual(s['expected'], f['expected'])
                for flag in ('is_partial', 'is_running', 'timed_out'): self.assertIs(s['response'][flag], False)
                actual = [[e['_id'] for e in seq['events']] for seq in s['response'].get('hits', {}).get('sequences', [])]
                self.assertEqual(actual, s['actual'])
                self.assertEqual(s['outcome'], 'INCONCLUSIVE' if f['expected'] is None else ('PASS' if actual == f['expected'] else 'FAIL'))
                self.assertEqual(s['request'], dict(engine.PARAMS, query=(engine.ROOT / recovery.SUITE['rules']['web004']).read_text(), filter=f['filter']))
                self.assertEqual({h['_id']: h['_source'] for h in s['indexed_documents']['hits']['hits']}, {e['id']: e['source'] for e in f['events']})
                self.assertEqual(s['indexed_documents']['hits']['total'], {'value': 2, 'relation': 'eq'})
                self.assertEqual(s['pending_tasks']['tasks'], [])
        self.assertEqual(r['initial_health']['status'], 'green')
        self.assertEqual(r['final_health']['status'], 'green')

    def test_integrity(self):
        if not (recovery.OUT / 'integrity.json').exists(): self.skipTest('Not finalized')
        i = recovery.load('docs/verification/phase6/6gr-v1/integrity.json')
        self.assertEqual(i['results_sha256'], recovery.digest('docs/verification/phase6/6gr-v1/results.json'))
        self.assertEqual(len(i['prior_indices_postrun']), 47)
        for v in i['prior_indices_postrun'].values():
            self.assertTrue(v['identity_count_equal'] and v['all_ids_and_sources_equal'])
        for path, v in i['preexisting_unchanged'].items():
            self.assertEqual(v['before'], v['after'], path)
            self.assertEqual(v['after'], recovery.digest(path), path)
        self.assertEqual(len(i['rules']), 14)
        for path, v in i['rules'].items(): self.assertEqual(v['actual'], recovery.digest(path))
        old = recovery.load('docs/verification/phase6/6g-v1/results.json')
        self.assertEqual(Counter(s['outcome'] for s in old['scenarios'] if s['rule'] == 'web004'), {'PASS': 34, 'FAIL': 16, 'INCONCLUSIVE': 1})
        checks = i['recovery_index_checks']; name = 'phase6-wcorr-6gr-v1-web004'
        self.assertEqual(checks['_count']['count'], 102)
        self.assertEqual(checks['_mapping'][name]['mappings'], recovery.load(recovery.SUITE['mappings'])['web004'])
        settings = checks['_settings'][name]['settings']['index']
        self.assertEqual(settings['number_of_shards'], '1'); self.assertEqual(settings['number_of_replicas'], '0')


if __name__ == '__main__': unittest.main()
