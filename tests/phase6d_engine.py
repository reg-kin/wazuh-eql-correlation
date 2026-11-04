#!/usr/bin/env python3
"""Phase 6D suite and strict preflight for the established shared harness."""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
from collections import Counter
import phase6_engine as engine
import phase6b_engine as phase6b
import phase6c_engine as phase6c

SUITE = {
    'rules': {'ssh003': 'rules/ssh/WCORR-SSH-003.eql',
              'ssh004': 'rules/ssh/WCORR-SSH-004.eql'},
    'fixtures': 'tests/fixtures/phase6/6d-scenarios.json',
    'mappings': 'tests/fixtures/phase6/6d-mappings.json',
    'grouped': True,
}


def validate_fixtures(fixtures, mappings):
    # Adapt only the two-/three-stage suite labels to the existing 6B contract.
    labels = {'ssh003': 'ssh', 'ssh004': 'pers'}
    adapted = copy.deepcopy(fixtures)
    for scenario in adapted:
        if scenario['rule'] not in labels:
            raise ValueError('Unexpected rule')
        scenario['rule'] = labels[scenario['rule']]
    phase6c.validate_fixtures(adapted, {labels[k]: v for k, v in mappings.items()})
    for scenario in fixtures:
        bounds = scenario['filter']['range']['timestamp']
        if not all(bounds[k].endswith('+00:00') for k in ('gte', 'lt')):
            raise ValueError('UTC required')


class GreenClient(engine.Client):
    """Keep shared transport and write guards; require green on every health check."""
    def ok(self, method, path, body=None):
        response = super().ok(method, path, body)
        if path == '/_cluster/health' and (response['status'] != 'green' or response['timed_out'] or response['number_of_pending_tasks']):
            raise RuntimeError('Green health prerequisite failed')
        return response


def preflight(client):
    root = engine.ROOT
    hashes = phase6c.verify_rules()
    manifest = json.loads((root / 'docs/verification/PUBLICATION_MANIFEST.json').read_text())
    for path in manifest['publication_files']:
        if (root / path).read_bytes() != subprocess.check_output(['git', 'show', 'v1.0.0:' + path], cwd=root):
            raise RuntimeError('Publication bytes changed: ' + path)
    expected, inventories, counts = {}, {}, Counter()
    for phase in ('6a', '6b', '6c'):
        result = json.loads((root / f'docs/verification/phase6/{phase}-v1/results.json').read_text())
        inventories.update({i['index']: i for i in result['indices_after']})
        for s in result['scenarios']:
            counts[s['outcome']] += 1
            expected.setdefault(s['index'], {}).update({h['_id']: h['_source'] for h in s['indexed_documents']['hits']['hits']})
    if counts != {'PASS': 163, 'INCONCLUSIVE': 8} or len(expected) != 39:
        raise RuntimeError('Prior evidence count mismatch')
    for phase in ('6b', '6c'):
        integrity = json.loads((root / f'docs/verification/phase6/{phase}-v1/integrity.json').read_text())
        for path, v in integrity['preexisting_unchanged'].items():
            if path != 'tests/validate_development.py' and hashlib.sha256((root / path).read_bytes()).hexdigest() != v['after']:
                raise RuntimeError('Prior file changed: ' + path)
        if hashlib.sha256((root / f'docs/verification/phase6/{phase}-v1/results.json').read_bytes()).hexdigest() != integrity['results_sha256']:
            raise RuntimeError('Prior result digest mismatch')
    live = {i['index']: i for i in engine.inventory(client)}
    if set(live) != set(expected):
        raise RuntimeError('Index conflict or unexpected/missing retained index')
    for name, sources in expected.items():
        if any(live[name][k] != inventories[name][k] for k in ('uuid', 'docs.count')):
            raise RuntimeError('Prior index identity/count mismatch')
        response = client.ok('GET', '/' + name + '/_search?size=1000&track_total_hits=true')
        if {h['_id']: h['_source'] for h in response['hits']['hits']} != sources or response['hits']['total'] != {'value': len(sources), 'relation': 'eq'}:
            raise RuntimeError('Prior source mismatch')
    if client.ok('GET', '/')['version']['number'] != '8.19.20':
        raise RuntimeError('Wrong engine version')
    client.ok('GET', '/_cluster/health')
    if client.ok('GET', '/_cluster/pending_tasks')['tasks']:
        raise RuntimeError('Pending tasks')
    resource = engine.resources()
    limit = int(subprocess.check_output(['docker', 'inspect', '--format', '{{.HostConfig.Memory}}', 'wcorr-phase6-elasticsearch'], text=True))
    if limit != 2 * 1024**3 or float(resource['container_stats']['MemPerc'].rstrip('%')) >= 90:
        raise RuntimeError('Container resource prerequisite failed')
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:19200')
    args = parser.parse_args()
    args.authorize_non_loopback = False
    args.run_id = '6d-v1'
    validate_fixtures(json.loads((engine.ROOT / SUITE['fixtures']).read_text()),
                      json.loads((engine.ROOT / SUITE['mappings']).read_text()))
    preflight(GreenClient(engine.validate_url(args.url)))
    original = engine.Client
    try:
        engine.Client = GreenClient
        return engine.run(args, SUITE)
    finally:
        engine.Client = original


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
