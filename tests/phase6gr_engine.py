#!/usr/bin/env python3
"""WEB-004 recovery adapter; shared Phase 6 transport and execution only."""
import argparse
import datetime as dt
import fnmatch
import hashlib
import json
import subprocess
from collections import Counter
import phase6_engine as engine
import phase6g_engine as phase6g
import phase6c_engine as phase6c

SUITE = dict(phase6g.SUITE, rules={'web004': phase6g.SUITE['rules']['web004']},
             fixtures='tests/fixtures/phase6/6gr-scenarios.json')
OUT = engine.ROOT / 'docs/verification/phase6/6gr-v1'
SPECIAL = {'inside': 1799.999, 'boundary': 1800, 'outside': 1800.001,
           'reversed': -60, 'equal-timestamps': 0}


def load(path):
    return json.loads((engine.ROOT / path).read_text())


def digest(path):
    return hashlib.sha256((engine.ROOT / path).read_bytes()).hexdigest()


def conditions(s):
    a, b = [e['source'] for e in s['events']]
    agent1, agent2 = a.get('agent', {}).get('id'), b.get('agent', {}).get('id')
    path, url = a.get('syscheck', {}).get('path'), b.get('data', {}).get('url')
    return {
        'agent': agent1 is not None and agent2 is not None and agent1 == agent2,
        'rule': a.get('rule', {}).get('id') == '554',
        'event': a.get('syscheck', {}).get('event') == 'added',
        'path': isinstance(path, str) and fnmatch.fnmatchcase(path, '/var/lib/docker/volumes/web_wp_data/_data/wp-content/uploads/*.php'),
        'url': isinstance(url, str) and fnmatch.fnmatchcase(url, '/wp-content/uploads/*.php*'),
    }


def intended_failure(name):
    if name in {'outside', 'reversed'}: return set()
    if name.startswith('agent-id-') or name == 'different-agent': return {'agent'}
    if name.startswith('rule-id-') or name == 'wrong-fim-id': return {'rule'}
    if name.startswith('syscheck-event-') or name.startswith('fim-event-'): return {'event'}
    if name.startswith('syscheck-path-') or name.startswith('fim-'): return {'path'}
    if name.startswith('data-url-') or name.startswith('url-'): return {'url'}
    raise ValueError('Unknown negative purpose: ' + name)


def validate_fixtures(fixtures, mappings):
    phase6g.validate_fixtures(fixtures, mappings)
    originals = [s for s in load(phase6g.SUITE['fixtures']) if s['rule'] == 'web004']
    if len(fixtures) != 51 or [s['id'] for s in fixtures] != [s['id'] for s in originals]:
        raise ValueError('All 51 original WEB-004 identities required')
    checks = []
    for s, original in zip(fixtures, originals):
        name = s['id'].removeprefix('web004-')
        span = (dt.datetime.fromisoformat(s['events'][1]['source']['timestamp']) - dt.datetime.fromisoformat(s['events'][0]['source']['timestamp'])).total_seconds()
        if span != SPECIAL.get(name, 60):
            raise ValueError('Wrong intended chronology: ' + s['id'])
        predicates = conditions(s)
        failed = {k for k, v in predicates.items() if not v}
        intended = intended_failure(name) if s['expected'] == [] else set()
        if failed != intended:
            raise ValueError('Unisolated predicate: ' + s['id'] + str(failed))
        expected = None if name == 'equal-timestamps' else ([[e['id'] for e in s['events']]] if not failed and 0 < span <= 1800 else [])
        if expected != s['expected']:
            raise ValueError('Expectation disagrees with published predicates: ' + s['id'])
        # Recovery permits only the precisely specified timestamp repair.
        repaired = json.loads(json.dumps(original))
        if name not in SPECIAL:
            repaired['events'][1]['source']['timestamp'] = (dt.datetime.fromisoformat(repaired['events'][0]['source']['timestamp']) + dt.timedelta(seconds=60)).isoformat()
        if repaired != s:
            raise ValueError('Unapproved definition change: ' + s['id'])
        checks.append({'id': s['id'], 'span_seconds': span, 'predicates': predicates,
                       'intended_failed_predicates': sorted(intended), 'expected': expected, 'valid': True})
    return checks


def audit_indices(client, allow_recovery=False):
    expected, identities = {}, {}
    for phase in 'abcdefg':
        r = load(f'docs/verification/phase6/6{phase}-v1/results.json')
        identities.update({i['index']: i for i in r['indices_after']})
        for s in r['scenarios']:
            expected.setdefault(s['index'], {}).update({h['_id']: h['_source'] for h in s['indexed_documents']['hits']['hits']})
    live = {i['index']: i for i in engine.inventory(client)}
    target = 'phase6-wcorr-6gr-v1-web004'
    if len(expected) != 47 or set(live) != set(expected) | ({target} if allow_recovery else set()):
        raise RuntimeError('Prior index inventory/conflict failed')
    audit = {}
    for name, sources in expected.items():
        identity = all(live[name][k] == identities[name][k] for k in ('uuid', 'docs.count'))
        r = client.ok('GET', '/' + name + '/_search?size=1000&track_total_hits=true')
        exact = {h['_id']: h['_source'] for h in r['hits']['hits']} == sources and r['hits']['total'] == {'value': len(sources), 'relation': 'eq'}
        if not identity or not exact: raise RuntimeError('Prior index changed: ' + name)
        audit[name] = {'identity_count_equal': identity, 'all_ids_and_sources_equal': exact, 'identity': live[name]}
    return audit


def preflight(client):
    if OUT.exists(): raise RuntimeError('Evidence conflict')
    rules = phase6c.verify_rules()
    manifest = load('docs/verification/PUBLICATION_MANIFEST.json')
    for path in manifest['publication_files'] + ['docs/verification/PUBLICATION_MANIFEST.json', 'tests/validate_repository.py']:
        if (engine.ROOT / path).read_bytes() != subprocess.check_output(['git', 'show', 'v1.0.0:' + path], cwd=engine.ROOT):
            raise RuntimeError('Frozen file changed: ' + path)
    for phase in 'bcdefg':
        base = f'docs/verification/phase6/6{phase}-v1/'
        i = load(base + 'integrity.json')
        if digest(base + 'results.json') != i['results_sha256']: raise RuntimeError('Result hash mismatch')
        for path, v in i['preexisting_unchanged'].items():
            if path != 'tests/validate_development.py' and digest(path) != v['after']:
                raise RuntimeError('Prior evidence changed: ' + path)
    indices = audit_indices(client)
    if client.ok('GET', '/')['version']['number'] != '8.19.20': raise RuntimeError('Engine version')
    health = client.ok('GET', '/_cluster/health')
    if client.ok('GET', '/_cluster/pending_tasks')['tasks']: raise RuntimeError('Pending tasks')
    resource = engine.resources()
    limit = int(subprocess.check_output(['docker', 'inspect', '--format', '{{.HostConfig.Memory}}', 'wcorr-phase6-elasticsearch']))
    if limit != 2 * 1024**3 or float(resource['container_stats']['MemPerc'].rstrip('%')) >= 90: raise RuntimeError('Unsafe resources')
    return {'rules': rules, 'publication_files': len(manifest['publication_files']), 'prior_indices': indices,
            'health': health, 'resources': resource, 'container_limit': limit}


class ValidatingClient(phase6g.GreenClient):
    def ok(self, method, path, body=None):
        if method == 'PUT' and '/_create/' in path:
            # Revalidate the complete immutable suite before each document write.
            validate_fixtures(load(SUITE['fixtures']), load(SUITE['mappings']))
        return super().ok(method, path, body)


def main():
    checks = validate_fixtures(load(SUITE['fixtures']), load(SUITE['mappings']))
    client = ValidatingClient(engine.validate_url('http://127.0.0.1:19200'))
    baseline = preflight(client)
    # Persist preflight and gate BEFORE the first engine write via the shared
    # runner's initial evidence save; no second HTTP framework is introduced.
    original_save, original_client = engine.save, engine.Client
    def save(path, value):
        if path.name == 'results.json':
            value['recovery_preflight'] = baseline
            value['offline_preexecution_validation'] = checks
            value['original_fixture_sha256'] = digest(phase6g.SUITE['fixtures'])
        original_save(path, value)
    try:
        engine.save, engine.Client = save, ValidatingClient
        return engine.run(argparse.Namespace(url=client.url, authorize_non_loopback=False, run_id='6gr-v1'), SUITE)
    finally:
        engine.save, engine.Client = original_save, original_client


if __name__ == '__main__':
    raise SystemExit(main())
