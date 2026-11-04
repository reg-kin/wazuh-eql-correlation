"""Offline contracts and retained evidence checks for Phase 6G."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch
import phase6_engine as engine
import phase6g_engine as phase6g


def load(path):
    return json.loads((engine.ROOT / path).read_text())


class Phase6GChecks(unittest.TestCase):
    def test_fixture_contract(self):
        fs = load(phase6g.SUITE['fixtures'])
        ms = load(phase6g.SUITE['mappings'])
        phase6g.validate_fixtures(fs, ms)
        for mutate in (lambda f: f[0].update(filter=f[1]['filter']),
                       lambda f: f[0].update(expected=[['unknown']]),
                       lambda f: f[0]['events'][0]['source'].update(unexpected='bad')):
            bad = copy.deepcopy(fs)
            mutate(bad)
            with self.assertRaises(ValueError):
                phase6g.validate_fixtures(bad, ms)
        import datetime as dt
        times = [sorted(dt.datetime.fromisoformat(e['source']['timestamp']) for e in f['events']) for f in fs]
        for first, second in zip(times, times[1:]):
            self.assertGreater((second[0]-first[-1]).total_seconds(), 600)
        for rule in ('web003', 'web004'):
            cases = {f['id'].removeprefix(rule+'-'): f for f in fs if f['rule'] == rule}
            for name in ('positive', 'inside', 'boundary'):
                self.assertTrue(cases[name]['expected'])
            for name in ('outside', 'reversed', 'different-agent'):
                self.assertEqual(cases[name]['expected'], [])
            self.assertIsNone(cases['equal-timestamps']['expected'])

    def test_executed_fixture_chronology(self):
        # Retain the discovered post-execution defect rather than bless failures.
        import datetime as dt
        fs = load(phase6g.SUITE['fixtures'])
        reversed_defaults = [f['id'] for f in fs if f['rule'] == 'web004'
            and f['id'].split('web004-', 1)[1] not in
            {'inside', 'boundary', 'outside', 'reversed', 'equal-timestamps'}
            and dt.datetime.fromisoformat(f['events'][1]['source']['timestamp']) <
                dt.datetime.fromisoformat(f['events'][0]['source']['timestamp'])]
        self.assertEqual(len(reversed_defaults), 46)
        self.assertIn('web004-positive', reversed_defaults)

    def test_guard(self):
        client = engine.Client('http://127.0.0.1:19200', 'phase6-wcorr-6g-v1-')
        with patch.object(client.opener, 'open') as opening:
            for method, path in [('DELETE', '/phase6-wcorr-6g-v1-web003'), ('PUT', '/phase6-wcorr-6f-v1-web003')]:
                with self.assertRaises(ValueError):
                    client.request(method, path, {})
            opening.assert_not_called()
        with patch.object(engine.Client, 'ok', return_value={'status': 'yellow', 'timed_out': False, 'number_of_pending_tasks': 0}):
            with self.assertRaises(RuntimeError):
                phase6g.GreenClient('http://127.0.0.1:19200').ok('GET', '/_cluster/health')

    def test_retained_responses(self):
        path = engine.ROOT / 'docs/verification/phase6/6g-v1/results.json'
        if not path.exists():
            self.skipTest('Not executed yet')
        r = load(str(path.relative_to(engine.ROOT)))
        fs = load(phase6g.SUITE['fixtures'])
        self.assertEqual(r['fixtures'], fs)
        self.assertEqual(r['mappings'], load(phase6g.SUITE['mappings']))
        self.assertEqual(len(r['scenarios']), len(fs))
        self.assertEqual(r['engine']['version']['number'], '8.19.20')
        for s, f in zip(r['scenarios'], fs):
            with self.subTest(scenario=f['id']):
                self.assertEqual(s['expected'], f['expected'])
                self.assertEqual(s['http_status'], 200)
                for flag in ('is_partial', 'is_running', 'timed_out'):
                    self.assertIs(s['response'][flag], False)
                actual = [[e['_id'] for e in seq['events']] for seq in s['response'].get('hits', {}).get('sequences', [])]
                self.assertEqual(s['actual'], actual)
                self.assertEqual(s['outcome'], 'INCONCLUSIVE' if f['expected'] is None else ('PASS' if actual == f['expected'] else 'FAIL'))
                sources = {e['id']: e['source'] for e in f['events']}
                self.assertEqual({h['_id']: h['_source'] for h in s['indexed_documents']['hits']['hits']}, sources)
                self.assertEqual(s['indexed_documents']['hits']['total'], {'relation': 'eq', 'value': len(sources)})
                self.assertEqual(s['request'], dict(engine.PARAMS, query=(engine.ROOT / phase6g.SUITE['rules'][f['rule']]).read_text(), filter=f['filter']))
                self.assertEqual(s['pending_tasks']['tasks'], [])
                for field in ('agent.id.keyword', 'rule.id.keyword', 'data.srcip.keyword', 'syscheck.path.keyword'):
                    self.assertIn('keyword', s['field_caps']['fields'][field])
                for seq in s['response'].get('hits', {}).get('sequences', []):
                    for event in seq['events']:
                        self.assertEqual(event['_source'], sources[event['_id']])
                        self.assertEqual(event['_index'], s['index'])
        self.assertEqual(r['initial_health']['status'], 'green')
        self.assertEqual(r['final_health']['status'], 'green')
        self.assertEqual(r['rule_sha256'], r['final_rule_sha256'])

    def test_integrity(self):
        path = engine.ROOT / 'docs/verification/phase6/6g-v1/integrity.json'
        if not path.exists():
            self.skipTest('Integrity not finalized yet')
        i = load(str(path.relative_to(engine.ROOT)))
        self.assertEqual(i['results_sha256'], hashlib.sha256((path.parent / 'results.json').read_bytes()).hexdigest())
        self.assertEqual(len(i['prior_indices_postrun']), 45)
        for value in i['prior_indices_postrun'].values():
            self.assertTrue(value['all_ids_and_sources_equal'])
            self.assertTrue(value['identity_count_equal'])
        for value in i['preexisting_unchanged'].values():
            self.assertEqual(value['before'], value['after'])
        self.assertEqual(len(i['rules']), 14)
        for value in i['rules'].values():
            self.assertEqual(value['expected'], value['actual'])
        r = load('docs/verification/phase6/6g-v1/results.json')
        for rule in ('web003', 'web004'):
            name = 'phase6-wcorr-6g-v1-' + rule
            checks = i['retained_index_checks'][name]
            self.assertEqual(checks['_mapping'][name]['mappings'], r['mappings'][rule])
            settings = checks['_settings'][name]['settings']['index']
            self.assertEqual(settings['number_of_shards'], '1')
            self.assertEqual(settings['number_of_replicas'], '0')
            self.assertEqual(checks['_count']['count'], sum(len(f['events']) for f in r['fixtures'] if f['rule'] == rule))


if __name__ == '__main__':
    unittest.main()
