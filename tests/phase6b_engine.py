#!/usr/bin/env python3
"""Phase 6B configuration for the shared sequential, synthetic-only harness."""
import argparse
import datetime as dt
import hashlib
import json
import re
import sys
import phase6_engine as engine

SUITE = {
    'rules': {'ssh': 'rules/ssh/WCORR-SSH-001.eql',
              'pers': 'rules/persistence/WCORR-PERS-001.eql'},
    'fixtures': 'tests/fixtures/phase6/6b-scenarios.json',
    'mappings': 'tests/fixtures/phase6/6b-mappings.json',
    'grouped': True,
}


def validate_fixtures(fixtures, mappings):
    """Reject malformed sources and prove disjoint bounded query partitions offline."""
    ids, days = set(), set()

    def source_contract(source, mapping):
        if not isinstance(source, dict):
            raise ValueError('Expected object')
        for key, value in source.items():
            if key not in mapping['properties']:
                raise ValueError('Unexpected fixture field: ' + key)
            field = mapping['properties'][key]
            if 'properties' in field:
                source_contract(value, field)
            elif value is not None and not isinstance(value, str):
                raise ValueError('Expected string/date/null scalar: ' + key)

    for s in fixtures:
        if s['rule'] not in SUITE['rules'] or not re.fullmatch('[a-z0-9-]+', s['id']) or s['id'] in ids:
            raise ValueError('Invalid/duplicate scenario')
        ids.add(s['id'])
        mapping = mappings[s['rule']]
        if mapping['dynamic'] != 'strict':
            raise ValueError('Strict mapping required')
        bounds = s['filter']['range']['timestamp']
        start, end = (dt.datetime.fromisoformat(bounds[k]) for k in ('gte', 'lt'))
        if start.tzinfo is None or start.hour or start.minute or start.second or end - start != dt.timedelta(days=1) or start in days:
            raise ValueError('Expected unique UTC day partition')
        days.add(start)
        event_ids = []
        for event in s['events']:
            if not re.fullmatch(re.escape(s['id']) + r'-s[1-3]', event['id']) or event['id'] in event_ids:
                raise ValueError('Invalid/duplicate document ID')
            event_ids.append(event['id'])
            source_contract(event['source'], mapping)
            timestamp = dt.datetime.fromisoformat(event['source']['timestamp'])
            if not start <= timestamp < end:
                raise ValueError('Event outside scenario partition')
        if len(event_ids) != (2 if s['rule'] == 'ssh' else 3):
            raise ValueError('Wrong stage count')
        if s['expected'] not in (None, [], [event_ids]):
            raise ValueError('Unknown expected document IDs')
        if (s['expected'] is None) != (s['classification'] == 'semantic_investigation'):
            raise ValueError('Investigation must remain explicit')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:19200')
    args = parser.parse_args()
    # Phase 6B deliberately has no non-loopback override or arbitrary run namespace.
    args.authorize_non_loopback = False
    args.run_id = '6b-v1'
    fixtures = json.loads((engine.ROOT / SUITE['fixtures']).read_text())
    mappings = json.loads((engine.ROOT / SUITE['mappings']).read_text())
    validate_fixtures(fixtures, mappings)
    manifest = json.loads((engine.ROOT / 'tests/rule-manifest.json').read_text())
    for rule in manifest:
        if hashlib.sha256((engine.ROOT / rule['eql']).read_bytes()).hexdigest() != rule['sha256']:
            raise RuntimeError('Published rule hash mismatch: ' + rule['eql'])
    return engine.run(args, SUITE)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
