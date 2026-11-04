"""Phase 6B fixture, scope, isolation and retained-evidence assertions."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch, Mock
from types import SimpleNamespace
import validate_development as development
import validate_repository as release
import phase6_engine as engine
import phase6b_engine as phase6b


def load(path):
    return json.loads((engine.ROOT / path).read_text())


class Phase6BChecks(unittest.TestCase):
    def test_fixture_contract_and_isolation(self):
        fixtures = load(phase6b.SUITE['fixtures'])
        mappings = load(phase6b.SUITE['mappings'])
        phase6b.validate_fixtures(fixtures, mappings)
        for mutate in [lambda f: f[0]['events'][0]['source'].update(unexpected='bad'),
                       lambda f: f[0]['events'][0]['source']['rule'].update(id=5712),
                       lambda f: f[0].update(filter=f[1]['filter']),
                       lambda f: f[0].update(expected=[['unknown']])]:
            bad = copy.deepcopy(fixtures)
            mutate(bad)
            with self.assertRaises(ValueError):
                phase6b.validate_fixtures(bad, mappings)
        for mapping in mappings.values():
            self.assertEqual(mapping['properties']['timestamp']['type'], 'date')
            self.assertEqual(mapping['properties']['rule']['properties']['id']['fields']['keyword']['type'], 'keyword')

    def test_write_scope(self):
        client = engine.Client('http://127.0.0.1:19200', 'phase6-wcorr-6b-v1-')
        with patch.object(client.opener, 'open') as opening:
            for method, path in [('PUT', '/phase6-wcorr-6a-v1-x'),
                                 ('DELETE', '/phase6-wcorr-6b-v1-ssh'),
                                 ('POST', '/phase6-wcorr-6b-v1-ssh/_delete_by_query')]:
                with self.assertRaises(ValueError):
                    client.request(method, path, {})
            opening.assert_not_called()

    def test_index_conflict_stops_before_writes(self):
        client = Mock()
        client.ok.side_effect = [
            {'version': {'number': '8.19.20'}},
            {'status': 'green', 'timed_out': False},
            [{'index': 'phase6-wcorr-6b-v1-ssh'}],
        ]
        args = SimpleNamespace(url='http://127.0.0.1:19200',
                               authorize_non_loopback=False, run_id='6b-v1')
        with patch('phase6_engine.Client', return_value=client), patch('pathlib.Path.exists', return_value=False):
            with patch('phase6_engine.resources') as resources:
                with self.assertRaisesRegex(RuntimeError, 'Index conflict'):
                    engine.run(args, phase6b.SUITE)
                resources.assert_not_called()
        self.assertTrue(all(call.args[0] == 'GET' for call in client.ok.call_args_list))
        client.request.assert_not_called()

    def test_documentation_address_exception_is_narrow(self):
        check = development.DevelopmentChecks('test_no_private_addresses_identifiers_logs_or_dependencies')
        fixture = engine.ROOT / phase6b.SUITE['fixtures']
        original = fixture.read_text()
        with patch.object(release, 'candidates', return_value=[fixture]):
            check.test_no_private_addresses_identifiers_logs_or_dependencies()
            with patch('pathlib.Path.read_text', return_value=original.replace('192.' + '0.2.10', '198.' + '51.100.1')):
                with self.assertRaises(AssertionError):
                    check.test_no_private_addresses_identifiers_logs_or_dependencies()
        with patch.object(release, 'candidates', return_value=[engine.ROOT / 'README.md']):
            with patch('pathlib.Path.read_text', return_value=original):
                with self.assertRaises(AssertionError):
                    check.test_no_private_addresses_identifiers_logs_or_dependencies()

    def test_retained_engine_evidence(self):
        path = engine.ROOT / 'docs/verification/phase6/6b-v1/results.json'
        if not path.exists():
            self.skipTest('Real-engine execution has not yet produced evidence')
        evidence = json.loads(path.read_text())
        integrity = load('docs/verification/phase6/6b-v1/integrity.json')
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), integrity['results_sha256'])
        fixtures = load(phase6b.SUITE['fixtures'])
        self.assertEqual(evidence['engine']['version']['number'], '8.19.20')
        self.assertEqual(evidence['fixtures'], fixtures)
        self.assertEqual(evidence['mappings'], load(phase6b.SUITE['mappings']))
        for key, name in [('fixture_sha256', 'fixtures'), ('mapping_sha256', 'mappings')]:
            self.assertEqual(evidence[key], hashlib.sha256((engine.ROOT / phase6b.SUITE[name]).read_bytes()).hexdigest())
        self.assertEqual(len(evidence['scenarios']), len(fixtures))
        for s, f in zip(evidence['scenarios'], fixtures):
            with self.subTest(scenario=s['id']):
                self.assertEqual(s['id'], f['id'])
                self.assertEqual(s['expected'], f['expected'])
                self.assertEqual(s['http_status'], 200)
                for key in ('is_partial', 'is_running', 'timed_out'):
                    self.assertIs(s['response'][key], False)
                self.assertEqual(s['response']['hits']['total'], {'relation': 'eq', 'value': len(s['actual'])})
                self.assertEqual(s['indexed_documents']['hits']['total'], {'relation': 'eq', 'value': len(f['events'])})
                self.assertEqual(s['indexed_documents']['_shards']['failed'], 0)
                expected_sources = {e['id']: e['source'] for e in f['events']}
                for sequence in s['response']['hits']['sequences']:
                    for event in sequence['events']:
                        self.assertEqual(event['_index'], s['index'])
                        self.assertEqual(event['_source'], expected_sources[event['_id']])
                self.assertEqual(s['actual'], [[e['_id'] for e in seq['events']] for seq in s['response'].get('hits', {}).get('sequences', [])])
                self.assertEqual(s['outcome'], 'INCONCLUSIVE' if f['expected'] is None else 'PASS')
                if f['expected'] is not None:
                    self.assertEqual(s['actual'], f['expected'])
                self.assertEqual(s['request']['filter'], f['filter'])
                self.assertEqual(s['request']['query'], (engine.ROOT / phase6b.SUITE['rules'][s['rule']]).read_text())
                self.assertEqual({e['_id']:e['_source'] for e in s['indexed_documents']['hits']['hits']}, {e['id']:e['source'] for e in f['events']})
                self.assertEqual(s['indexing']['refresh']['_shards']['failed'], 0)
                self.assertEqual(s['pending_tasks']['tasks'], [])
                for field in ['agent.id.keyword','rule.id.keyword','type.keyword'] + (['data.srcip.keyword'] if s['rule']=='ssh' else ['syscheck.path.keyword']):
                    self.assertIn('keyword', s['field_caps']['fields'][field])
        self.assertEqual(evidence['rule_sha256'], evidence['final_rule_sha256'])
        self.assertTrue(evidence['unrelated_indices_unchanged'])
        self.assertEqual(evidence['final_pending_tasks']['tasks'], [])
        before = {x['index'] for x in evidence['indices_before']}
        created = [x for x in evidence['indices_after'] if x['index'] not in before]
        self.assertEqual({x['index'] for x in created}, {'phase6-wcorr-6b-v1-ssh','phase6-wcorr-6b-v1-pers'})
        self.assertEqual(sum(int(x['docs.count']) for x in created), sum(len(f['events']) for f in fixtures))
        for rule in ('ssh', 'pers'):
            name = 'phase6-wcorr-6b-v1-' + rule
            checks = integrity['retained_index_checks'][name]
            self.assertEqual(checks['_mapping'][name]['mappings'], evidence['mappings'][rule])
            settings = checks['_settings'][name]['settings']['index']
            self.assertEqual(settings['number_of_shards'], '1')
            self.assertEqual(settings['number_of_replicas'], '0')
            self.assertEqual(checks['_count']['count'], sum(len(f['events']) for f in fixtures if f['rule'] == rule))


if __name__ == '__main__':
    unittest.main()
