#!/usr/bin/env python3
"""Phase 6C configuration; reuse Phase 6A HTTP execution and 6B fixture contract."""
import argparse
import hashlib
import json
import subprocess
import sys
import phase6_engine as engine
import phase6b_engine as phase6b

SUITE = {
    'rules': {'ssh': 'rules/ssh/WCORR-SSH-002.eql',
              'pers': 'rules/persistence/WCORR-PERS-002.eql'},
    'fixtures': 'tests/fixtures/phase6/6c-scenarios.json',
    'mappings': 'tests/fixtures/phase6/6c-mappings.json',
    'grouped': True,
}


def validate_fixtures(fixtures, mappings):
    phase6b.validate_fixtures(fixtures, mappings)
    for mapping in mappings.values():
        if mapping['properties']['timestamp'] != {'type': 'date'}:
            raise ValueError('Expected date timestamp')
        def keywords(properties):
            for name, field in properties.items():
                if 'properties' in field:
                    keywords(field['properties'])
                elif name != 'timestamp' and field != {'type': 'text', 'fields': {'keyword': {'type': 'keyword'}}}:
                    raise ValueError('Expected explicit keyword multifield')
        keywords(mapping['properties'])


def verify_rules():
    manifest = json.loads((engine.ROOT / 'tests/rule-manifest.json').read_text())
    if len(manifest) != 14:
        raise RuntimeError('Expected 14 published rules')
    hashes = {}
    for rule in manifest:
        actual = hashlib.sha256((engine.ROOT / rule['eql']).read_bytes()).hexdigest()
        if actual != rule['sha256']:
            raise RuntimeError('Published hash mismatch: ' + rule['eql'])
        hashes[rule['eql']] = actual
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', default='http://127.0.0.1:19200')
    args = parser.parse_args()
    args.authorize_non_loopback = False
    args.run_id = '6c-v1'
    validate_fixtures(json.loads((engine.ROOT / SUITE['fixtures']).read_text()),
                      json.loads((engine.ROOT / SUITE['mappings']).read_text()))
    verify_rules()
    client = engine.Client(engine.validate_url(args.url))
    health = client.ok('GET', '/_cluster/health')
    pending = client.ok('GET', '/_cluster/pending_tasks')
    if health['status'] != 'green' or health['timed_out'] or health['number_of_pending_tasks'] or pending['tasks']:
        raise RuntimeError('Preflight health prerequisite failed')
    resource = engine.resources()
    limit = int(subprocess.check_output(['docker', 'inspect', '--format',
                '{{.HostConfig.Memory}}', 'wcorr-phase6-elasticsearch'], text=True))
    if limit != 2 * 1024**3 or float(resource['container_stats']['MemPerc'].rstrip('%')) >= 90:
        raise RuntimeError('Preflight container resource prerequisite failed')
    return engine.run(args, SUITE)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
