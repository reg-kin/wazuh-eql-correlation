"""Offline safety and fixture contracts for the Phase 6 harness."""
import json
import unittest
from unittest.mock import patch
import phase6_engine as harness


class HarnessChecks(unittest.TestCase):
    def test_endpoint_scope(self):
        for url in ['http://127.0.0.1:19200', 'http://[::1]:19200']:
            self.assertEqual(harness.validate_url(url), url)
        for url in [ 'http://127.0.0.1/path', 'http://127.0.0.1/?x=y', 'file:///tmp/test']:
            with self.assertRaises(ValueError):
                harness.validate_url(url)
        remote = '192.' + '0.2.1'
        with patch('phase6_engine.socket.getaddrinfo', return_value=[(2, 1, 6, '', (remote, 19200))]):
            with self.assertRaises(ValueError):
                harness.validate_url('http://example.invalid:19200')
            self.assertEqual(harness.validate_url('http://example.invalid:19200', True), 'http://' + remote + ':19200')

    def test_write_scope_before_http(self):
        client = harness.Client('http://127.0.0.1:19200')
        with patch.object(client.opener, 'open') as opening:
            for method, path in [('DELETE','/unrelated'),('PUT','/production'),('POST','/_bulk'),('PUT','/phase6-wcorr-x/../production')]:
                with self.assertRaises(ValueError):
                    client.request(method, path, {})
            opening.assert_not_called()

    def test_fixture_contract(self):
        fixtures = json.loads((harness.ROOT / 'tests/fixtures/phase6/scenarios.json').read_text())
        self.assertEqual(len({s['id'] for s in fixtures}), len(fixtures))
        for s in fixtures:
            ids = [e['id'] for e in s['events']]
            self.assertEqual(len(set(ids)), len(ids))
            if s['expected']:
                self.assertEqual(s['expected'], [ids])
            for e in s['events']:
                self.assertIsInstance(e['source']['rule']['id'], str)
        self.assertTrue(any(s['expected'] is None for s in fixtures))

    def test_resource_stop(self):
        state = b'{"Status":"running","OOMKilled":true,"Restarting":false}'
        with patch('phase6_engine.subprocess.check_output', side_effect=[state, b'{}']):
            with self.assertRaisesRegex(RuntimeError, 'Resource safeguard'):
                harness.resources()


if __name__ == '__main__':
    unittest.main()
