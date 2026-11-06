#!/usr/bin/env python3
"""Current public-release offline checks; preserves staged and historical validators."""
import hashlib
import ipaddress
import json
import re
import subprocess
import unittest
from pathlib import Path
import validate_development as development
from validate_development import release

ROOT = release.ROOT
PACKAGE = ROOT / 'deployment/public-release'
REPORT = 'docs/verification/PUBLIC_RELEASE_RECONCILIATION.json'
# Explicit additions; no weakening of the frozen inventory checks.
development.DEVELOPMENT_FILES |= {
    'tests/validate_public_release.py',
    'docs/verification/PUBLIC_RELEASE_INTEGRATION.md',
    'docs/verification/ISOLATED_KIBANA_TEST_PLAN.md',
    REPORT,
    'docs/public-release-configuration.md',
    'deployment/public-release/README.md',
    'deployment/public-release/MANIFEST.sha256',
    'deployment/public-release/kibana-rules.ndjson',
    'deployment/public-release/rules/WCORR-EVAS-001.eql',
    'deployment/public-release/rules/WCORR-MAL-001.eql',
    'deployment/public-release/rules/WCORR-PERS-001.eql',
    'deployment/public-release/rules/WCORR-PERS-002.eql',
    'deployment/public-release/rules/WCORR-PRIV-001.eql',
    'deployment/public-release/rules/WCORR-SSH-001.eql',
    'deployment/public-release/rules/WCORR-SSH-002.eql',
    'deployment/public-release/rules/WCORR-SSH-003.eql',
    'deployment/public-release/rules/WCORR-SSH-004.eql',
    'deployment/public-release/rules/WCORR-SSH-005.eql',
    'deployment/public-release/rules/WCORR-WEB-001.eql',
    'deployment/public-release/rules/WCORR-WEB-002.eql',
    'deployment/public-release/rules/WCORR-WEB-003.eql',
    'deployment/public-release/rules/WCORR-WEB-004.eql',
}


def tokens(query):
    return re.findall(r'"(?:\\.|[^"\\])*"|\w+(?:\.\w+)*|[^\s]', query)


class PublicReleaseChecks(development.DevelopmentChecks):
    def test_no_private_addresses_identifiers_logs_or_dependencies(self):
        # The frozen release predates synthetic SSH address fixtures. Permit only
        # these two documentation-only literals in two explicitly inventoried files;
        # retain every other inherited content check verbatim.
        synthetic_paths = {'tests/fixtures/phase6/6b-scenarios.json',
                           'docs/verification/phase6/6b-v1/results.json'}
        synthetic_addresses = {'192.' + '0.2.10', '192.' + '0.2.11'}
        allowed_suffixes = {'.md', '.conf', '.yml', '.example', '.eql', '.json', '.py', '.ndjson', '.sha256'}
        allowed_special = {'LICENSE', '.gitignore'}
        for path in release.candidates():
            name = str(path.relative_to(release.ROOT))
            self.assertTrue(path.suffix in allowed_suffixes or path.name in allowed_special, name)
            data = path.read_text(encoding='utf-8')
            # Version strings have four parts too: accept only literal IP tokens.
            for value in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])', data):
                addr = ipaddress.ip_address(value)
                self.assertTrue(addr.is_loopback or (name in synthetic_paths and value in synthetic_addresses), 'Address check: ' + name)
            user_path_data = data
            # Explicit synthetic authorized-key paths, never real workspace paths.
            if name in {'tests/fixtures/phase6/6d-scenarios.json',
                        'docs/verification/phase6/6d-v1/results.json',
                        'docs/verification/phase6/6d-v1/integrity.json'}:
                for synthetic_path in ('/home/' + 'lab/.ssh/authorized_keys',
                                       '/home/' + 'lab/nested/.ssh/authorized_keys'):
                    user_path_data = user_path_data.replace(synthetic_path, '/synthetic-authorized-key')
            self.assertTrue(re.search(r'/home/[a-zA-Z0-9_-]+/', user_path_data) is None, 'User path check: ' + name)
            self.assertTrue(re.search(r'git' + r'@[^\s]+:|https://github\.com/[^\s]+', data) is None, 'Dependency check: ' + name)
            self.assertTrue(re.search(r'"(?:full_log|predecoder)"\s*:', data) is None, 'Production payload check: ' + name)
            self.assertNotIn(path.name, {'alerts.json', 'package-lock.json', 'requirements.txt'}, name)
            for line in data.splitlines():
                if line.lstrip().startswith('{'):
                    try:
                        obj = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(obj, dict):
                        self.assertFalse({'timestamp', 'agent', 'rule'} <= obj.keys(), 'Event payload check: ' + name)

    def test_public_release_integrity_and_contract(self):
        inventory = json.loads((ROOT / REPORT).read_text())
        self.assertEqual(hashlib.sha256((PACKAGE / 'MANIFEST.sha256').read_bytes()).hexdigest(),
                         inventory['archive_manifest_sha256'])
        entries = {}
        for line in (PACKAGE / 'MANIFEST.sha256').read_text().splitlines():
            digest, name = line.split(maxsplit=1)
            name = name.lstrip('*')
            self.assertNotIn(name, entries)
            self.assertTrue((PACKAGE / name).resolve().is_relative_to(PACKAGE))
            self.assertEqual(hashlib.sha256((PACKAGE / name).read_bytes()).hexdigest(), digest, name)
            entries[name] = digest
        self.assertEqual(set(entries), {p.relative_to(PACKAGE).as_posix()
                         for p in PACKAGE.rglob('*') if p.is_file()} - {'MANIFEST.sha256'})
        records = [json.loads(line) for line in (PACKAGE / 'kibana-rules.ndjson').read_text().splitlines()]
        self.assertEqual(len(records), 14)
        self.assertEqual(len({r['rule_id'] for r in records}), 14)
        self.assertEqual({r['name'].split()[0] for r in records}, set(release.EXPECTED))
        self.assertEqual({p.stem for p in (PACKAGE / 'rules').glob('*.eql')}, set(release.EXPECTED))
        self.assertEqual(len(inventory['rules']), 14)
        reconciliation = {r['id']: r for r in inventory['rules']}
        canonical = {r['id']: r for r in self.manifest}
        # Exact allowlist excludes server IDs, ownership, execution and space metadata.
        allowed = set('name tags interval enabled description risk_score severity license author false_positives from rule_id max_signals risk_score_mapping severity_mapping threat to references version exceptions_list immutable rule_source related_integrations required_fields setup type language index query filters actions'.split())
        changes = set()
        for record in records:
            rid = record['name'].split()[0]
            expected = reconciliation[rid]
            self.assertEqual(set(record), allowed)
            self.assertIs(record['enabled'], False)
            for key in ['actions', 'exceptions_list', 'filters', 'author', 'references', 'related_integrations']:
                self.assertEqual(record[key], [])
            self.assertEqual(record['rule_source'], {'type': 'internal'})
            self.assertEqual(record['rule_id'], expected['export_rule_id'])
            self.assertEqual(record['index'], ['wazuh-alerts-4.x-*'])
            self.assertEqual((record['type'], record['language']), ('eql', 'eql'))
            self.assertEqual(record['interval'], '5m')
            self.assertEqual(record['to'], 'now')
            span = re.search(r'with maxspan=(\d+)m', record['query']).group(1)
            self.assertEqual(span + 'm', canonical[rid]['maxspan'])
            self.assertEqual(record['from'], 'now-' + str(int(span) + 6) + 'm')
            for key in ['interval', 'from', 'to']:
                self.assertEqual(record[key], expected[key])
            self.assertEqual(record['query'].count('['), record['query'].count(']'))
            eql = (PACKAGE / 'rules' / (rid + '.eql')).read_text()
            # Companion files normalise the final newline; export strings retain exact source bytes.
            self.assertEqual(record['query'].rstrip('\n') + '\n', eql)
            self.assertEqual(hashlib.sha256(record['query'].encode()).hexdigest(), expected['export_query_sha256'])
            old = (ROOT / canonical[rid]['eql']).read_bytes()
            self.assertEqual(hashlib.sha256(old).hexdigest(), expected['canonical_sha256'])
            same = tokens(record['query']) == tokens(old.decode())
            self.assertEqual(same, expected['query_tokens_equal'])
            if not same:
                changes.add(rid)
            self.assertEqual(record['severity'], expected['export_severity'])
            self.assertEqual(record['severity'], 'high' if rid == 'WCORR-PERS-002' else canonical[rid]['severity'].lower())
            self.assertEqual(record['risk_score'], canonical[rid]['risk_score'])
            stage = json.loads((ROOT / 'deployment/stage2a/definitions' / (rid + '.json')).read_text())
            self.assertEqual(stage['from'], expected['stage2a_from'])
            self.assertNotEqual(stage['rule_id'], record['rule_id'])
        self.assertEqual(changes, {'WCORR-PRIV-001', 'WCORR-SSH-002'})
        priv = next(r['query'] for r in records if r['name'].startswith('WCORR-PRIV-001 '))
        self.assertNotIn('] by ', priv)
        self.assertNotIn('!= null', priv)
        self.assertTrue(priv.startswith('sequence by agent.id.keyword with maxspan=30m'))
        ssh = next(r['query'] for r in records if r['name'].startswith('WCORR-SSH-002 '))
        self.assertIn('data.dstuser.keyword != null', ssh)
        self.assertIn('data.command.keyword != null', ssh)
        for path in ROOT.rglob('*.json'):
            if '.git' not in path.parts:
                json.loads(path.read_text())

    def test_stage2a_preservation(self):
        expected = json.loads((ROOT / REPORT).read_text())['preserved_staged_sha256']
        self.assertEqual(len(expected), 18)
        for name, digest in expected.items():
            current = (ROOT / name).read_bytes()
            self.assertEqual(hashlib.sha256(current).hexdigest(), digest, name)
            self.assertEqual(current, subprocess.check_output(['git', 'show', ':' + name], cwd=ROOT), name)


if __name__ == '__main__':
    unittest.main(verbosity=2)
