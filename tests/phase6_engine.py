#!/usr/bin/env python3
"""Sequential, synthetic-only Elasticsearch 8.19.20 validation; no cleanup."""
import argparse
import datetime as dt
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import socket
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'phase6-wcorr-'
PARAMS = {'timestamp_field': 'timestamp', 'event_category_field': 'type.keyword', 'size': 10}
RULES = {'priv': 'rules/privilege-escalation/WCORR-PRIV-001.eql',
         'mal': 'rules/malware/WCORR-MAL-001.eql'}


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def validate_url(url, authorize_non_loopback=False):
    p = urllib.parse.urlsplit(url)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password or p.path not in ('', '/') or p.query or p.fragment:
        raise ValueError('Expected HTTP(S) origin without credentials, path, query or fragment')
    # Resolve once and pin the connection to the checked address to avoid DNS rebinding.
    addresses = sorted({v[4][0] for v in socket.getaddrinfo(p.hostname, p.port or (443 if p.scheme == 'https' else 80), type=socket.SOCK_STREAM)})
    if not addresses or (not authorize_non_loopback and not all(ipaddress.ip_address(a).is_loopback for a in addresses)):
        raise ValueError('Non-loopback endpoint requires --authorize-non-loopback')
    address = addresses[0]
    host = '[' + address + ']' if ':' in address else address
    return urllib.parse.urlunsplit((p.scheme, host + ':' + str(p.port or (443 if p.scheme == 'https' else 80)), '', '', ''))


class Client:
    def __init__(self, url, write_prefix=None):
        self.url = url
        self.write_prefix = write_prefix
        # Ignore environment proxies; never redirect a write to another origin.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *args, **kwargs):
                return None
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())

    def request(self, method, path, body=None):
        if method != 'GET' and self.write_prefix is not None:
            if method not in ('PUT', 'POST') or not path.startswith('/' + self.write_prefix):
                raise ValueError('Write outside selected run scope')
        if method != 'GET' and not re.fullmatch(r'/phase6-wcorr-[a-z0-9-]+(?:/(?:_create/[a-z0-9-]+|_refresh|_eql/search))?', path):
            raise ValueError('Write outside laboratory index scope')
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.url + path, data=data, method=method, headers={'Content-Type': 'application/json'})
        try:
            with self.opener.open(req, timeout=15) as response:
                return response.status, json.load(response)
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def ok(self, method, path, body=None):
        status, response = self.request(method, path, body)
        if not 200 <= status < 300:
            raise RuntimeError(json.dumps({'method': method, 'path': path, 'status': status, 'response': response}))
        return response


def resources():
    values = {}
    for line in Path('/proc/meminfo').read_text().splitlines():
        name, value = line.split(':', 1)
        if name in ('MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree'):
            values[name] = int(value.split()[0]) * 1024
    inspect = json.loads(subprocess.check_output(['docker', 'inspect', '--format', '{{json .State}}', 'wcorr-phase6-elasticsearch'], text=True))
    values['container'] = {key: inspect[key] for key in ('Status', 'OOMKilled', 'Restarting')}
    values['container_stats'] = json.loads(subprocess.check_output(['docker', 'stats', '--no-stream', '--format', '{{json .}}', 'wcorr-phase6-elasticsearch'], text=True))
    if values['MemAvailable'] < 512 * 1024**2 or values['SwapTotal'] - values['SwapFree'] > 512 * 1024**2 or inspect['OOMKilled'] or inspect['Restarting'] or inspect['Status'] != 'running':
        raise RuntimeError('Resource safeguard stopped execution: ' + json.dumps(values))
    return values


def inventory(client):
    return client.ok('GET', '/_cat/indices?format=json&expand_wildcards=all&h=index,uuid,docs.count,store.size')


def run(args, suite=None):
    suite = suite or {}
    rules = suite.get('rules', RULES)
    fixture_path = ROOT / suite.get('fixtures', 'tests/fixtures/phase6/scenarios.json')
    mapping_path = ROOT / suite.get('mappings', 'tests/fixtures/phase6/mappings.json')
    grouped = suite.get('grouped', False)
    client = Client(validate_url(args.url, args.authorize_non_loopback),
                    PREFIX + args.run_id + '-' if grouped else None)
    fixtures = json.loads(fixture_path.read_text())
    mappings = json.loads(mapping_path.read_text())
    if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', args.run_id):
        raise ValueError('Invalid run ID')
    out = ROOT / 'docs/verification/phase6' / args.run_id
    if out.exists():
        raise RuntimeError('Evidence directory already exists; use a new explicit run ID')
    baseline = client.ok('GET', '/')
    health = client.ok('GET', '/_cluster/health')
    if baseline['version']['number'] != '8.19.20' or health['status'] not in ('green', 'yellow') or health['timed_out']:
        raise RuntimeError('Engine prerequisite failed')
    before = inventory(client)
    names = [PREFIX + args.run_id + '-' + (s['rule'] if grouped else s['id']) for s in fixtures]
    if set(names) & {x['index'] for x in before}:
        raise RuntimeError('Index conflict; nothing written')
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in rules.values()}
    initial_resources = resources()
    out.mkdir()
    evidence = {'executed_at': dt.datetime.now(dt.timezone.utc).isoformat(), 'endpoint': client.url,
                'engine': baseline, 'initial_health': health, 'indices_before': before,
                'branch': subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip(),
                'commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
                'fixture_sha256': hashlib.sha256(fixture_path.read_bytes()).hexdigest(),
                'mapping_sha256': hashlib.sha256(mapping_path.read_bytes()).hexdigest(),
                'fixtures': fixtures, 'mappings': mappings,
                'rule_sha256': hashes, 'request_parameters': PARAMS, 'initial_resources': initial_resources, 'scenarios': []}
    save(out / 'results.json', evidence)
    created_indices = set()
    try:
        for scenario, index in zip(fixtures, names):
            resource = resources()
            health = client.ok('GET', '/_cluster/health')
            if health['status'] not in ('green', 'yellow') or health['timed_out']:
                raise RuntimeError('Cluster health safeguard stopped execution')
            if grouped:
                if float(resource['container_stats']['MemPerc'].rstrip('%')) >= 90:
                    raise RuntimeError('Container memory safeguard stopped execution')
                pending = client.ok('GET', '/_cluster/pending_tasks')
                if pending['tasks'] or health['number_of_pending_tasks']:
                    raise RuntimeError('Pending tasks safeguard stopped execution')
                if hashlib.sha256(fixture_path.read_bytes()).hexdigest() != evidence['fixture_sha256'] or hashlib.sha256(mapping_path.read_bytes()).hexdigest() != evidence['mapping_sha256']:
                    raise RuntimeError('Fixture or mapping changed during execution')
            mapping = mappings[scenario['rule']]
            created = {'reused_within_run': True}
            if index not in created_indices:
                if grouped and index in {x['index'] for x in inventory(client)}:
                    raise RuntimeError('Index appeared before creation; refuse overwrite')
                created = client.ok('PUT', '/' + index, {'settings': {'number_of_shards': 1, 'number_of_replicas': 0}, 'mappings': mapping})
                if not created.get('acknowledged'):
                    raise RuntimeError('Index creation not acknowledged')
                created_indices.add(index)
            indexed = []
            for event in scenario['events']:
                indexed.append(client.ok('PUT', '/' + index + '/_create/' + event['id'], event['source']))
            refreshed = client.ok('POST', '/' + index + '/_refresh')
            if refreshed['_shards']['failed']:
                raise RuntimeError('Refresh failed')
            path = rules[scenario['rule']]
            raw = (ROOT / path).read_bytes()
            if hashlib.sha256(raw).hexdigest() != hashes[path]:
                raise RuntimeError('Rule changed during execution')
            request = dict(PARAMS, query=raw.decode())
            if grouped:
                request['filter'] = scenario['filter']
            status, response = client.request('POST', '/' + index + '/_eql/search', request)
            actual = [[e['_id'] for e in sequence['events']] for sequence in response.get('hits', {}).get('sequences', [])]
            expected = scenario['expected']
            outcome = 'FAIL' if status != 200 or response.get('is_partial') or response.get('is_running') or response.get('timed_out') else ('INCONCLUSIVE' if expected is None else ('PASS' if actual == expected else 'FAIL'))
            record = {'id': scenario['id'], 'rule': scenario['rule'], 'index': index,
                      'expected': expected, 'actual': actual, 'outcome': outcome,
                      'request': request, 'pending_tasks': pending if grouped else None,
                      'note': scenario['note'], 'http_status': status, 'response': response,
                      'indexing': {'created': created, 'documents': len(indexed), 'refresh': refreshed}, 'resources': resource}
            # Always verify stored count, exact sources and field capabilities, especially zero matches.
            record['indexed_documents'] = client.ok('GET', '/' + index + '/_search?size=10&sort=timestamp:asc',
                                                     {'query': scenario['filter']} if grouped else None)
            record['field_caps'] = client.ok('GET', '/' + index + '/_field_caps?fields=*')
            stored = {h['_id']: h['_source'] for h in record['indexed_documents']['hits']['hits']}
            if stored != {e['id']: e['source'] for e in scenario['events']}:
                record['outcome'] = 'FAIL'
                record['fixture_error'] = 'Stored documents differ from fixture'
            evidence['scenarios'].append(record)
            save(out / 'results.json', evidence)
            print(scenario['id'], record['outcome'], 'expected=', expected, 'actual=', actual, 'HTTP', status, flush=True)
    finally:
        if grouped:
            evidence['final_pending_tasks'] = client.ok('GET', '/_cluster/pending_tasks')
        evidence['final_health'] = client.ok('GET', '/_cluster/health')
        evidence['final_resources'] = resources()
        evidence['indices_after'] = inventory(client)
        evidence['final_rule_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in rules.values()}
        after = {x['index']: x for x in evidence['indices_after']}
        evidence['unrelated_indices_unchanged'] = all(after.get(x['index']) == x for x in before) and set(after) - {x['index'] for x in before} <= set(names)
        save(out / 'results.json', evidence)
    return 1 if any(s['outcome'] == 'FAIL' for s in evidence['scenarios']) else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:19200')
    parser.add_argument('--authorize-non-loopback', action='store_true', help='Explicit authorization for an alternative endpoint; never use production')
    parser.add_argument('--run-id', default='6a-v1', help='Retained index/evidence namespace; reruns require a new ID')
    try:
        sys.exit(run(parser.parse_args()))
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
