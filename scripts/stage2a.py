#!/usr/bin/env python3
"""Generate, validate and plan Stage 2A locally. No network or deployment code."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'deployment/stage2a'


def expected():
    if not __debug__:
        raise RuntimeError('Safety validation requires Python without -O')
    result = []
    for row in json.loads((ROOT / 'tests/rule-manifest.json').read_text()):
        query = (ROOT / row['eql']).read_bytes().decode('utf-8')
        assert hashlib.sha256(query.encode()).hexdigest() == row['sha256'], row['id']
        span = int(re.search(r'with maxspan=(\d+)m', query)[1])
        assert row['maxspan'] == f'{span}m'
        rule = dict(rule_id=row['id'], name=f"{row['id']}: {row['name']}",
                    description=row['description'], type='eql', language='eql',
                    index=['wazuh-alerts-4.x-*'], query=query,
                    timestamp_field='timestamp', timestamp_override='timestamp',
                    timestamp_override_fallback_disabled=True,
                    event_category_override='type.keyword', interval='5m',
                    **{'from': f'now-{span + 10}m', 'to': 'now'},
                    enabled=False, severity=row['severity'].lower(), risk_score=row['risk_score'],
                    max_signals=100, actions=[], author=['Wazuh EQL Correlation'],
                    tags=['Wazuh', 'EQL', 'Multi-stage', row['id'].split('-')[1]],
                    false_positives=[row['limitations']],
                    required_fields=[{'name': f, 'type': 'date' if f == 'timestamp' else 'keyword',
                                      'ecs': False} for f in row['required_fields']],
                    setup=row['deployment_prerequisites'], version=1)
        result.append(rule)
    return result


def validate():
    rules = expected()
    assert len(rules) == 14
    assert len({r['rule_id'] for r in rules}) == 14
    assert {p.stem for p in (OUT / 'definitions').glob('*.json')} == {r['rule_id'] for r in rules}
    for r in rules:
        actual = json.loads((OUT / 'definitions' / (r['rule_id'] + '.json')).read_text())
        assert actual == r, f"Definition drift: {r['rule_id']}"
        assert r['severity'] in {'low', 'medium', 'high', 'critical'}
        assert type(r['risk_score']) is int and 0 <= r['risk_score'] <= 100
        assert r['enabled'] is False and not r['actions']
        # Enumerate completion phase and each stage's bounded ingestion delay.
        span = int(re.search(r'maxspan=(\d+)m', r['query'])[1])
        window = int(re.fullmatch(r'now-(\d+)m', r['from'])[1]) * 60
        for phase in range(300):
            for delay in (0, 1, 299, 300):
                end = phase
                start = end - span * 60
                visible = end + delay
                run = ((visible + 299) // 300) * 300
                assert run - window <= start <= end <= run
    return rules


def plan(rules, snapshot, selected):
    """Fail closed on incomplete snapshots, duplicates, unmanaged equivalents or drift."""
    assert isinstance(snapshot, dict) and isinstance(snapshot.get('data'), list)
    data = snapshot['data']
    assert type(snapshot.get('total')) is int and snapshot['total'] == len(data), 'Need complete paginated inventory'
    assert len({r['id'] for r in data}) == len(data), 'Duplicate server IDs'
    wanted = next(r for r in rules if r['rule_id'] == selected)
    assert selected != 'WCORR-PRIV-001', 'PRIV-001 is held'
    matches = [r for r in data if r.get('rule_id') == selected]
    assert len(matches) <= 1, 'Duplicate stable rule ID'
    for other in data:
        if other in matches:
            continue
        assert other.get('name') != wanted['name'], 'Conflicting name'
        assert other.get('query', '').strip() != wanted['query'].strip(), 'Equivalent query under another ID'
    if matches:
        existing = matches[0]
        for key, value in wanted.items():
            assert existing.get(key) == value, f'Drift or active rule: {key}; manual review required'
        return {'rule_id': selected, 'operation': 'NOOP', 'reason': 'Exact disabled definition exists'}
    return {'rule_id': selected, 'operation': 'CREATE_DISABLED',
            'method': 'POST', 'path': '/api/detection_engine/rules',
            'body_file': f'deployment/stage2a/definitions/{selected}.json'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['generate', 'validate', 'plan'])
    parser.add_argument('--snapshot', type=Path)
    parser.add_argument('--rule-id', default='WCORR-SSH-001')
    args = parser.parse_args()
    if args.command == 'generate':
        for rule in expected():
            (OUT / 'definitions' / (rule['rule_id'] + '.json')).write_text(json.dumps(rule, indent=2) + '\n')
    rules = validate()
    if args.command == 'plan':
        assert args.snapshot, '--snapshot required; nothing is contacted automatically'
        print(json.dumps(plan(rules, json.loads(args.snapshot.read_text()), args.rule_id), indent=2))
    else:
        print('PASS: 14 disabled definitions; exact source hashes, metadata, API field contract and bounded schedule coverage')


if __name__ == '__main__':
    main()
