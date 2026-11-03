#!/usr/bin/env python3
"""Offline repository checks only; no third-party modules or service access."""
from pathlib import Path
import hashlib
import ipaddress
import json
import re
import sys
import unittest
import os
import textwrap

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    **{f'WCORR-SSH-{i:03}': n for i, n in enumerate([1, 10, 1, 0, 0], 1)},
    **{f'WCORR-WEB-{i:03}': n for i, n in enumerate([10, 0, 0, 0], 1)},
    'WCORR-PRIV-001': 2, 'WCORR-PERS-001': 0, 'WCORR-PERS-002': 0,
    'WCORR-EVAS-001': 0, 'WCORR-MAL-001': 7,
}
DOCS = ['architecture', 'installation', 'configuration',
        'ecs-normalisation-decision', 'correlation-rule-catalogue',
        'validation-results', 'troubleshooting', 'security']


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def candidates():
    # Do not inspect Git internals or ignored Python bytecode. Scan all other
    # files, including unexpected ones, rather than relying on git status.
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and not any(x in {'.git', '__pycache__'} for x in p.relative_to(ROOT).parts))


class RepositoryChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(read('tests/rule-manifest.json'))

    def test_structure(self):
        for name in ['README.md', 'LICENSE', '.gitignore',
                     'config/logstash/logstash.conf', 'config/logstash/pipelines.yml',
                     'config/logstash/environment.example',
                     'docs/verification/PHASE1_REPORT.md'] + [f'docs/{d}.md' for d in DOCS]:
            self.assertTrue((ROOT / name).is_file(), name)
        for folder in ['ssh', 'web', 'privilege-escalation', 'persistence', 'defence-evasion', 'malware']:
            self.assertTrue((ROOT / 'rules' / folder).is_dir(), folder)
        self.assertIn('Version 2.0, January 2004', read('LICENSE'))
        self.assertIn('END OF TERMS AND CONDITIONS', read('LICENSE'))

    def test_exact_catalogue_and_counts(self):
        self.assertEqual(len(self.manifest), 14)
        self.assertEqual({r['id'] for r in self.manifest}, set(EXPECTED))
        self.assertEqual(len(list((ROOT / 'rules').rglob('*.md'))), 14)
        self.assertEqual({r['entry'] for r in self.manifest},
                         {str(p.relative_to(ROOT)) for p in (ROOT / 'rules').rglob('*.md')})
        for r in self.manifest:
            self.assertEqual(r['historical_returned_sequences'], EXPECTED[r['id']])
            self.assertEqual(r['historical_query_size'], 10)
            for doc in ['docs/correlation-rule-catalogue.md', 'docs/validation-results.md']:
                self.assertRegex(read(doc), re.escape(r['id']) + r'.*?\|\s*' + str(EXPECTED[r['id']]) + r'\s*\|')

    def test_fourteen_sources_and_integrity(self):
        complete = [r for r in self.manifest if r['source_status'] == 'COMPLETE_SOURCE']
        self.assertEqual(len(complete), 14)
        self.assertEqual({r['eql'] for r in complete},
                         {str(p.relative_to(ROOT)) for p in (ROOT / 'rules').rglob('*.eql')})
        windows = {'SSH-001': '15m', 'SSH-002': '15m', 'SSH-003': '30m', 'SSH-004': '30m', 'SSH-005': '30m', 'WEB-001': '10m', 'WEB-002': '10m', 'WEB-003': '10m',
                   'WEB-004': '30m', 'PRIV-001': '30m', 'PERS-001': '30m',
                   'PERS-002': '30m', 'EVAS-001': '20m', 'MAL-001': '60m'}
        for r in complete:
            raw = (ROOT / r['eql']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), r['sha256'], r['id'])
            query = raw.decode('utf-8')
            self.assertTrue(query.startswith('sequence by agent.id.keyword'))
            self.assertIn('with maxspan=' + windows[r['id'][6:]], query)
            self.assertEqual(r['maxspan'], windows[r['id'][6:]])
            self.assertNotRegex(query.lower(), r'pending|placeholder|todo|where\s+true|where\s+false')
            self.assertEqual(query.count('['), query.count(']'))
            actual_fields = set(re.findall(r'\b[a-z][a-z0-9_.]*\.keyword', query))
            self.assertEqual(set(r['required_fields']), actual_fields | {'timestamp', 'type.keyword'})

    def test_source_expression_preservation(self):
        # Optional read-only external source check; never publish its contents.
        source_path = os.environ.get('WCORR_SOURCE_FILE')
        if not source_path:
            self.skipTest('External source comparison requires WCORR_SOURCE_FILE')
        source = Path(source_path).read_text()
        heads = list(re.finditer(r'^(?:\d+\. )?(WCORR-[A-Z]+-\d{3}) — (.+)$', source, re.M))
        self.assertEqual([h.group(1) for h in heads], [r['id'] for r in self.manifest])
        tokens = lambda q: re.findall(r'"(?:\\.|[^"\\])*"|\w+(?:\.\w+)*|[^\s]', q)
        for i, (r, h) in enumerate(zip(self.manifest, heads)):
            section = source[h.end():heads[i+1].start() if i+1 < len(heads) else len(source)]
            blocks = re.findall(r'"query": """\n(.*?)\n\s*"""', section, re.S)
            query = blocks[0] if blocks else re.search(r'(sequence by .*?\n(?:.*\n)*?)(?=\n-{10,})', section).group(1)
            self.assertTrue(tokens(query) == tokens(read(r['eql'])), 'Source mismatch: ' + r['id'])
            self.assertEqual(r['name'], h.group(2).strip())
            severity, risk = re.search(r'Severity: (\w+) \| Risk score: (\d+)', section).groups()
            self.assertEqual((r['severity'], r['risk_score']), (severity, int(risk)))

    def test_revised_join_and_filter_contracts(self):
        priv = read('rules/privilege-escalation/WCORR-PRIV-001.eql')
        for term in ['] by data.dstuser.keyword', '] by data.srcuser.keyword',
                     '] by ?data.srcuser.keyword', 'data.dstuser.keyword == "root"',
                     'data.command.keyword like "*useradd*"', 'data.command.keyword like "*adduser*"']:
            self.assertIn(term, priv)
        mal = read('rules/malware/WCORR-MAL-001.eql')
        for term in ['syscheck.mode.keyword == "realtime"', '] by syscheck.path.keyword',
                     '] by data.file.keyword', 'data.file.keyword != null',
                     r'data.file.keyword != "/dev/null\r"']:
            self.assertIn(term, mal)
        ssh = read('rules/ssh/WCORR-SSH-002.eql')
        self.assertNotIn('data.dstuser.keyword != null', ssh)
        self.assertNotIn('data.command.keyword != null', ssh)

    def test_no_pending_definitions(self):
        marker = 'PENDING' + '_SOURCE'
        for path in candidates():
            self.assertNotIn(marker, path.read_text(), str(path.relative_to(ROOT)))
        for r in self.manifest:
            for key in ['name', 'description', 'severity', 'risk_score', 'limitations',
                        'deployment_prerequisites', 'sha256', 'eql', 'maxspan']:
                self.assertTrue(r[key], r['id'] + ': ' + key)
            self.assertEqual(r['activation_readiness'], 'LAB_VALIDATION_REQUIRED')
            self.assertEqual(r['final_execution'], 'NOT_PERFORMED')

    def test_required_metadata_and_entry_documentation(self):
        for r in self.manifest:
            self.assertEqual(r['timestamp_field'], 'timestamp')
            self.assertEqual(r['event_category_field'], 'type.keyword')
            self.assertEqual(r['index_pattern'], 'wazuh-alerts-4.x-*')
            text = read(r['entry'])
            for label in ['Rule identifier:', 'Detection objective:', 'Required event fields:',
                          'Correlation window:', 'Historical match count:',
                          'False-positive considerations / Detection limitations:', 'Validation limitations:',
                          'Activation readiness:', 'EQL definition:',
                          'timestamp_field = timestamp', 'event_category_field = type.keyword',
                          'query size was limited to 10', 'No activation in Kibana is claimed']:
                self.assertIn(label, text, r['id'])
            if EXPECTED[r['id']] == 0:
                self.assertIn('positive detection efficacy has not been demonstrated', text)


    def test_configuration_variable_consistency(self):
        conf = read('config/logstash/logstash.conf')
        names = set(re.findall(r'\$\{([A-Z_]+)\}', conf))
        example = read('config/logstash/environment.example')
        values = dict(re.findall(r'^([A-Z_]+)=(.*)$', example, re.M))
        expected = {'WAZUH_ALERTS_PATH', 'ELASTICSEARCH_URL', 'ELASTICSEARCH_USERNAME',
                    'ELASTICSEARCH_PASSWORD', 'ELASTICSEARCH_CA_PATH'}
        self.assertEqual(names, expected)
        self.assertEqual(set(values), expected)
        self.assertEqual(values['ELASTICSEARCH_PASSWORD'], 'CHANGE_ME')
        self.assertEqual(values['ELASTICSEARCH_URL'], 'https://localhost:9201')
        for name in names:
            self.assertIn(name, read('docs/configuration.md'))
        for option in ['codec => json', 'start_position => "end"',
                       '/var/lib/logstash/plugins/inputs/file/sincedb_wazuh',
                       'index => "wazuh-alerts-4.x-%{+YYYY.MM.dd}"',
                       'ssl_verification_mode => "full"', 'ssl_enabled => true',
                       'ssl_certificate_authorities => ["${ELASTICSEARCH_CA_PATH}"]',
                       'manage_template => false', 'ilm_enabled => false', 'data_stream => false']:
            self.assertIn(option, conf)
        self.assertNotRegex(conf, r'(?m)^\s*filter\s*\{')
        self.assertNotIn('queue.type', conf)
        self.assertIn('pipeline.ecs_compatibility: disabled', read('config/logstash/pipelines.yml'))

    def test_no_embedded_credentials_or_material(self):
        # Failure output identifies a filename and check, never matching content.
        patterns = [r'-----BEGIN (?:[A-Z ]*PRIVATE KEY|CERTIFICATE)-----',
                    r'(?i)https?://[^\s/@:]+:[^\s/@]+@',
                    r'\bAKIA[A-Z0-9]{16}\b', r'\bgh[pousr]_[A-Za-z0-9]{20,}\b',
                    r'\bgithub_pat_[A-Za-z0-9_]{20,}\b',
                    r'(?i)(?:password|passwd|api_key|access_token)\s*(?:=>|=|:)\s*[\"\'](?!\$\{|CHANGE_ME)[A-Za-z0-9_+/=-]{8,}[\"\']']
        for path in candidates():
            name = str(path.relative_to(ROOT))
            self.assertNotIn(path.suffix.lower(), {'.pem', '.key', '.crt', '.p12', '.pfx', '.jks'}, name)
            data = path.read_text(encoding='utf-8')
            for pattern in patterns:
                self.assertTrue(re.search(pattern, data) is None, 'Sensitive-content check: ' + name)

    def test_no_private_addresses_identifiers_logs_or_dependencies(self):
        allowed_suffixes = {'.md', '.conf', '.yml', '.example', '.eql', '.json', '.py'}
        allowed_special = {'LICENSE', '.gitignore'}
        for path in candidates():
            name = str(path.relative_to(ROOT))
            self.assertTrue(path.suffix in allowed_suffixes or path.name in allowed_special, name)
            data = path.read_text(encoding='utf-8')
            # Version strings have four parts too: accept only literal IP tokens.
            for value in re.findall(r'(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])', data):
                addr = ipaddress.ip_address(value)
                self.assertFalse(not addr.is_loopback, 'Address check: ' + name)
            self.assertTrue(re.search(r'/home/[a-zA-Z0-9_-]+/', data) is None, 'User path check: ' + name)
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

    def test_documentation_links_and_consistency(self):
        for path in candidates():
            if path.suffix != '.md':
                continue
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                dest = (path.parent / target.split('#')[0]).resolve()
                self.assertTrue(dest.is_relative_to(ROOT), 'Link escapes repository')
                self.assertTrue(dest.exists(), f'Broken link in {path.relative_to(ROOT)}')
        confdoc = read('docs/configuration.md')
        for field in {'timestamp', 'type.keyword', 'rule.id.keyword', 'agent.id.keyword',
                      'data.srcip.keyword', 'data.dstuser.keyword', 'data.audit.type.keyword',
                      'data.url.keyword', 'syscheck.path.keyword', 'syscheck.event.keyword'}:
            self.assertIn('"' + field + '"', confdoc)
        for term in ['field_caps', 'include_unmapped=true', 'does not establish',
                     'not configured in the pipeline', 'EnvironmentFile=', 'ACL', 'sincedb',
                     'start_position', 'queue.type', 'date', 'keyword']:
            self.assertIn(term, confdoc)
        results = read('docs/validation-results.md')
        for term in ['Different usernames', 'Routine SSH administration and sudo',
                     'observation timestamps', 'Reverse-proxy', 'same attacker',
                     'not necessarily the same PHP file', 'account creation',
                     'same-session', '/dev/null', 'carriage return',
                     'size limited to 10', 'not exhaustive', 'not proof']:
            self.assertIn(term, results)
        for term in ['journald', 'recursive ingestion', 'root-cause']:
            self.assertIn(term, read('docs/troubleshooting.md'))
        self.assertIn('Experimental reference implementation', read('README.md'))
        self.assertIn('not a production-validated rule pack', read('README.md'))
        deployment = read('docs/installation.md')
        for term in ['5 minutes', '1 minute', 'Disabled initially', 'None initially', 'deduplication', 'maxspan', 'query-window coverage']:
            self.assertIn(term, deployment)
        self.assertIn('No rules have been activated', results)

    def test_report_exact_inventory(self):
        report = read('docs/verification/PHASE2_REPORT.md')
        inventory = re.findall(r'^- `([^`]+)`$', report, re.M)
        actual = [str(p.relative_to(ROOT)) for p in candidates()]
        self.assertTrue(set(inventory) <= set(actual))
        self.assertEqual(len(inventory), 46)
        self.assertEqual(len(inventory), len(set(inventory)))


    def test_project_identity(self):
        manifest = json.loads(read('docs/verification/PUBLICATION_MANIFEST.json'))
        self.assertEqual(manifest['project_name'], 'wazuh-eql-correlation')
        self.assertEqual(manifest['project_title'], 'Wazuh EQL Correlation')
        self.assertEqual(manifest['project_description'],
                         'Multi-stage security alert correlation for Wazuh using '
                         'Elasticsearch EQL, with Logstash ingestion, detection rules '
                         'and deployment guidance.')
        self.assertTrue(read('README.md').startswith('# ' + manifest['project_title'] + '\n'))
        self.assertIn(manifest['project_description'], read('README.md'))
        for name in ['README.md', 'CONTRIBUTING.md'] + [f'docs/{d}.md' for d in
                ['installation', 'configuration', 'architecture', 'security']]:
            self.assertIn(manifest['project_name'], read(name))
        old_name = 'wazuh-' + 'elastic-security-correlation'
        historical = {'docs/verification/PHASE4_RENAME_REPORT.md',
                      'docs/verification/PUBLICATION_MANIFEST.json'}
        historical.update(f'docs/verification/{n}' for n in
                          ['PHASE1_REPORT.md', 'PHASE2_REPORT.md', 'PHASE3_PUBLICATION_AUDIT.md'])
        for path in candidates():
            name = path.relative_to(ROOT).as_posix()
            self.assertNotIn(old_name, name)
            if name not in historical:
                self.assertNotIn(old_name, path.read_text(), name)

    def test_phase3_preservation(self):
        manifest = json.loads(read('docs/verification/PUBLICATION_MANIFEST.json'))
        baseline = manifest['phase3_baseline_sha256']
        changed = set(manifest['files_modified'])
        for name, digest in baseline.items():
            if name not in changed:
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                                 digest, name)
        eql = {r['eql']: r['sha256'] for r in self.manifest}
        self.assertEqual(len(eql), 14)
        for name, digest in eql.items():
            self.assertEqual(baseline[name], digest, name)
            self.assertEqual(manifest['source_checksums'][name], digest, name)
        for name in manifest['source_file_paths']:
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                             manifest['source_checksums'][name], name)

    def test_publication_manifest(self):
        manifest_path = 'docs/verification/PUBLICATION_MANIFEST.json'
        manifest = json.loads(read(manifest_path))
        actual = {str(p.relative_to(ROOT)) for p in candidates()}
        self.assertEqual(set(manifest['publication_files']), actual)
        self.assertEqual(set(manifest['sha256']), actual - {manifest_path})
        for name, digest in manifest['sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(manifest['rules'], self.manifest)
        self.assertEqual(manifest['readiness']['publication_ready'], True)
        self.assertEqual(manifest['readiness']['detection_validated'], False)
        self.assertEqual(manifest['readiness']['production_ready'], False)
        self.assertEqual(manifest['documentation_inventory'],
                         sorted(name for name in actual if name.endswith('.md')))


if __name__ == '__main__':
    unittest.main(verbosity=2)
