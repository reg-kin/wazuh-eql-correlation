"""Offline Phase 6D contracts and independent retained-response assertions."""
import copy
import hashlib
import json
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
import phase6_engine as engine
import phase6d_engine as phase6d


def load(path):
    return json.loads((engine.ROOT / path).read_text())


class Phase6DChecks(unittest.TestCase):
    def test_fixture_contract(self):
        fixtures = load(phase6d.SUITE['fixtures'])
        mappings = load(phase6d.SUITE['mappings'])
        phase6d.validate_fixtures(fixtures, mappings)
        for mutate in [lambda f: f[0].update(filter=f[1]['filter']),
                       lambda f: f[0].update(expected=[['unknown']]),
                       lambda f: f[0]['events'][0]['source'].update(unexpected='bad')]:
            bad = copy.deepcopy(fixtures)
            mutate(bad)
            with self.assertRaises(ValueError):
                phase6d.validate_fixtures(bad, mappings)
        self.assertEqual(len(phase6d.phase6c.verify_rules()), 14)

    def test_write_scope_and_conflict(self):
        client = engine.Client('http://127.0.0.1:19200', 'phase6-wcorr-6d-v1-')
        with patch.object(client.opener, 'open') as opening:
            for method, path in [('DELETE', '/phase6-wcorr-6d-v1-ssh003'),
                                 ('PUT', '/phase6-wcorr-6b-v1-ssh003'),
                                 ('POST', '/phase6-wcorr-6d-v1-ssh003/_delete_by_query')]:
                with self.assertRaises(ValueError):
                    client.request(method, path, {})
            opening.assert_not_called()
        mocked = Mock()
        mocked.ok.side_effect = [{'version': {'number': '8.19.20'}},
                                 {'status': 'green', 'timed_out': False},
                                 [{'index': 'phase6-wcorr-6d-v1-ssh003'}]]
        args = SimpleNamespace(url='http://127.0.0.1:19200', authorize_non_loopback=False, run_id='6d-v1')
        with patch('phase6_engine.Client', return_value=mocked), patch('pathlib.Path.exists', return_value=False):
            with self.assertRaisesRegex(RuntimeError, 'Index conflict'):
                engine.run(args, phase6d.SUITE)
        self.assertTrue(all(c.args[0] == 'GET' for c in mocked.ok.call_args_list))
        mocked.request.assert_not_called()

    def test_green_health_guard(self):
        with patch.object(engine.Client, 'ok', return_value={'status': 'yellow', 'timed_out': False, 'number_of_pending_tasks': 0}):
            with self.assertRaisesRegex(RuntimeError, 'Green health'):
                phase6d.GreenClient('http://127.0.0.1:19200').ok('GET', '/_cluster/health')

    def test_synthetic_path_exception_is_narrow(self):
        import validate_repository as release
        import validate_development as development
        fixture = engine.ROOT / phase6d.SUITE['fixtures']
        check = development.DevelopmentChecks('test_no_private_addresses_identifiers_logs_or_dependencies')
        with patch.object(release, 'candidates', return_value=[fixture]):
            check.test_no_private_addresses_identifiers_logs_or_dependencies()
            original = fixture.read_text()
            with patch('pathlib.Path.read_text', return_value=original.replace('/home/' + 'lab/.ssh/', '/home/' + 'private/.ssh/')):
                with self.assertRaises(AssertionError):
                    check.test_no_private_addresses_identifiers_logs_or_dependencies()
        with patch.object(release, 'candidates', return_value=[engine.ROOT / 'README.md']):
            with patch('pathlib.Path.read_text', return_value=original):
                with self.assertRaises(AssertionError):
                    check.test_no_private_addresses_identifiers_logs_or_dependencies()

    def test_retained_evidence(self):
        path = engine.ROOT / 'docs/verification/phase6/6d-v1/results.json'
        if not path.exists():
            self.skipTest('Engine evidence not yet present')
        r = load(str(path.relative_to(engine.ROOT)))
        integrity = load('docs/verification/phase6/6d-v1/integrity.json')
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), integrity['results_sha256'])
        self.assertTrue(all(v['before'] == v['after'] for v in integrity['preexisting_unchanged'].values()))
        self.assertTrue(all(v['expected'] == v['actual'] for v in integrity['rules'].values()))
        fs = load(phase6d.SUITE['fixtures'])
        self.assertEqual(r['fixtures'], fs)
        self.assertEqual(r['mappings'], load(phase6d.SUITE['mappings']))
        self.assertEqual(len(r['scenarios']), len(fs))
        self.assertEqual(r['engine']['version']['number'], '8.19.20')
        for key, name in [('fixture_sha256','fixtures'), ('mapping_sha256','mappings')]:
            self.assertEqual(r[key], hashlib.sha256((engine.ROOT / phase6d.SUITE[name]).read_bytes()).hexdigest())
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
                for sequence in s['response'].get('hits', {}).get('sequences', []):
                    for event in sequence['events']:
                        self.assertEqual(event['_index'], s['index'])
                        self.assertEqual(event['_source'], sources[event['_id']])
                self.assertEqual(s['indexed_documents']['_shards']['failed'], 0)
                self.assertEqual(s['response']['hits']['total'], {'relation':'eq','value':len(actual)})
                self.assertEqual(s['request'], dict(engine.PARAMS, query=(engine.ROOT / phase6d.SUITE['rules'][f['rule']]).read_text(), filter=f['filter']))
                if actual and f['rule'] == 'ssh004' and f['expected'] is not None:
                    import datetime as dt
                    by_id = {e['id']: e['source'] for e in f['events']}
                    for sequence in actual:
                        self.assertEqual(sequence, [e['id'] for e in f['events']])
                        times = [dt.datetime.fromisoformat(by_id[i]['timestamp']) for i in sequence]
                        self.assertLess(times[0], times[1])
                        self.assertLess(times[1], times[2])
                        self.assertLessEqual((times[-1]-times[0]).total_seconds(), 1800)
                self.assertEqual(s['indexing']['refresh']['_shards']['failed'], 0)
                self.assertEqual(s['pending_tasks']['tasks'], [])
                for field in ['agent.id.keyword','rule.id.keyword','type.keyword'] + (['syscheck.path.keyword','syscheck.mode.keyword']):
                    self.assertIn('keyword', s['field_caps']['fields'][field])
        self.assertEqual(r['initial_health']['status'], 'green')
        self.assertEqual(r['final_health']['status'], 'green')
        self.assertEqual(r['rule_sha256'], r['final_rule_sha256'])
        # Storage sizes can change through background merges; UUID/count/source audit is authoritative.
        self.assertTrue(all(v['all_ids_and_sources_equal'] for v in integrity['prior_indices_postrun'].values()))
        self.assertEqual(r['final_pending_tasks']['tasks'], [])
        created = [i for i in r['indices_after'] if i['index'].startswith('phase6-wcorr-6d-v1-')]
        self.assertEqual(len(created), 2)
        for rule in ('ssh003', 'ssh004'):
            name = 'phase6-wcorr-6d-v1-' + rule
            checks = integrity['retained_index_checks'][name]
            self.assertEqual(checks['_mapping'][name]['mappings'], r['mappings'][rule])
            settings = checks['_settings'][name]['settings']['index']
            self.assertEqual(settings['number_of_shards'], '1')
            self.assertEqual(settings['number_of_replicas'], '0')
            self.assertEqual(checks['_count']['count'], sum(len(f['events']) for f in fs if f['rule'] == rule))
        self.assertEqual(len(integrity['prior_indices_postrun']), 39)
        self.assertEqual(set(integrity['baseline']['prior_indices']), set(integrity['prior_indices_postrun']))
        for name, value in integrity['prior_indices_postrun'].items():
            for key in ('uuid', 'docs.count'):
                self.assertEqual(value['inventory'][key], integrity['baseline']['prior_indices'][name]['inventory'][key])
        self.assertEqual(sum(int(i['docs.count']) for i in created), sum(len(f['events']) for f in fs))


if __name__ == '__main__':
    unittest.main()
