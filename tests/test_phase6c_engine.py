"""Offline Phase 6C contracts and independent retained-response assertions."""
import copy
import hashlib
import json
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
import phase6_engine as engine
import phase6c_engine as phase6c


def load(path):
    return json.loads((engine.ROOT / path).read_text())


class Phase6CChecks(unittest.TestCase):
    def test_fixture_contract(self):
        fixtures = load(phase6c.SUITE['fixtures'])
        mappings = load(phase6c.SUITE['mappings'])
        phase6c.validate_fixtures(fixtures, mappings)
        for mutate in [lambda f: f[0].update(filter=f[1]['filter']),
                       lambda f: f[0].update(expected=[['unknown']]),
                       lambda f: f[0]['events'][0]['source'].update(unexpected='bad')]:
            bad = copy.deepcopy(fixtures)
            mutate(bad)
            with self.assertRaises(ValueError):
                phase6c.validate_fixtures(bad, mappings)
        self.assertEqual(len(phase6c.verify_rules()), 14)

    def test_write_scope_and_conflict(self):
        client = engine.Client('http://127.0.0.1:19200', 'phase6-wcorr-6c-v1-')
        with patch.object(client.opener, 'open') as opening:
            for method, path in [('DELETE', '/phase6-wcorr-6c-v1-ssh'),
                                 ('PUT', '/phase6-wcorr-6b-v1-ssh'),
                                 ('POST', '/phase6-wcorr-6c-v1-ssh/_delete_by_query')]:
                with self.assertRaises(ValueError):
                    client.request(method, path, {})
            opening.assert_not_called()
        mocked = Mock()
        mocked.ok.side_effect = [{'version': {'number': '8.19.20'}},
                                 {'status': 'green', 'timed_out': False},
                                 [{'index': 'phase6-wcorr-6c-v1-ssh'}]]
        args = SimpleNamespace(url='http://127.0.0.1:19200', authorize_non_loopback=False, run_id='6c-v1')
        with patch('phase6_engine.Client', return_value=mocked), patch('pathlib.Path.exists', return_value=False):
            with self.assertRaisesRegex(RuntimeError, 'Index conflict'):
                engine.run(args, phase6c.SUITE)
        self.assertTrue(all(c.args[0] == 'GET' for c in mocked.ok.call_args_list))
        mocked.request.assert_not_called()

    def test_retained_evidence(self):
        path = engine.ROOT / 'docs/verification/phase6/6c-v1/results.json'
        if not path.exists():
            self.skipTest('Engine evidence not yet present')
        r = load(str(path.relative_to(engine.ROOT)))
        integrity = load('docs/verification/phase6/6c-v1/integrity.json')
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), integrity['results_sha256'])
        self.assertTrue(all(v['before'] == v['after'] for v in integrity['preexisting_unchanged'].values()))
        self.assertTrue(all(v['expected'] == v['actual'] for v in integrity['rules'].values()))
        fs = load(phase6c.SUITE['fixtures'])
        self.assertEqual(r['fixtures'], fs)
        self.assertEqual(r['mappings'], load(phase6c.SUITE['mappings']))
        self.assertEqual(len(r['scenarios']), len(fs))
        self.assertEqual(r['engine']['version']['number'], '8.19.20')
        for key, name in [('fixture_sha256','fixtures'), ('mapping_sha256','mappings')]:
            self.assertEqual(r[key], hashlib.sha256((engine.ROOT / phase6c.SUITE[name]).read_bytes()).hexdigest())
        for s, f in zip(r['scenarios'], fs):
            with self.subTest(scenario=f['id']):
                self.assertEqual(s['id'], f['id'])
                self.assertEqual(s['expected'], f['expected'])
                self.assertEqual(s['http_status'], 200)
                for flag in ['is_partial','is_running','timed_out']:
                    self.assertIs(s['response'][flag], False)
                actual = [[e['_id'] for e in seq['events']] for seq in s['response'].get('hits',{}).get('sequences',[])]
                self.assertEqual(s['actual'], actual)
                self.assertEqual(s['outcome'], 'INCONCLUSIVE' if f['expected'] is None else 'PASS')
                if f['expected'] is not None:
                    self.assertEqual(actual, f['expected'])
                sources = {e['id']:e['source'] for e in f['events']}
                self.assertEqual({e['_id']:e['_source'] for e in s['indexed_documents']['hits']['hits']}, sources)
                self.assertEqual(s['indexed_documents']['hits']['total'], {'relation':'eq','value':len(sources)})
                self.assertEqual(s['response']['hits']['total'], {'relation':'eq','value':len(actual)})
                self.assertEqual(s['request'], dict(engine.PARAMS, query=(engine.ROOT / phase6c.SUITE['rules'][f['rule']]).read_text(), filter=f['filter']))
                self.assertEqual(s['indexing']['refresh']['_shards']['failed'], 0)
                self.assertEqual(s['pending_tasks']['tasks'], [])
                for field in ['agent.id.keyword','rule.id.keyword','type.keyword'] + (['data.dstuser.keyword','data.command.keyword'] if f['rule']=='ssh' else ['syscheck.path.keyword']):
                    self.assertIn('keyword', s['field_caps']['fields'][field])
        self.assertEqual(r['rule_sha256'], r['final_rule_sha256'])
        self.assertTrue(r['unrelated_indices_unchanged'])
        self.assertEqual(r['final_pending_tasks']['tasks'], [])
        created = [i for i in r['indices_after'] if i['index'].startswith('phase6-wcorr-6c-v1-')]
        self.assertEqual(len(created), 2)
        self.assertEqual(sum(int(i['docs.count']) for i in created), sum(len(f['events']) for f in fs))


if __name__ == '__main__':
    unittest.main()
