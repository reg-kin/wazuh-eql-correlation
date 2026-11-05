#!/usr/bin/env python3
"""Offline development checks; the frozen release validator remains unchanged."""
import argparse
import hashlib
import shutil
from contextlib import contextmanager
import json
import ipaddress
import re
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import validate_repository as release

# Explicit inventory: additions require review here, never a directory wildcard.
DEVELOPMENT_FILES = {
    'docs/verification/scheduled-kibana-validation/REPORT.md',
    'docs/verification/phase7/7b-v1/REPORT.md',
    'docs/verification/phase7/7b-v1/results.json',
    'docs/verification/phase7/QUALIFICATION_EVIDENCE_REVIEW.md',
    'docs/verification/phase7/7a-v1/REPORT.md',
    'docs/verification/phase7/7a-v1/README.md',
    'docs/verification/phase7/7a-v1/field-contract.json',
    'docs/verification/phase7/7a-v1/rule-dependencies.json',
    'docs/verification/phase7/7a-v1/mapping-requirements.json',
    'docs/verification/phase7/7a-v1/phase7b-inspection-plan.md',
    'docs/verification/phase6/6h-v1/REPORT.md',
    'docs/verification/phase6/6h-v1/README.md',
    'docs/verification/phase6/6h-v1/qualification.json',
    'docs/verification/phase6/6h-v1/limitations.json',
    'docs/verification/phase6/6h-v1/integrity.json',
    'docs/verification/phase6/6h-v1/regression.json',
    'tests/phase6gr_engine.py',
    'tests/test_phase6gr_engine.py',
    'tests/fixtures/phase6/6gr-scenarios.json',
    'docs/verification/phase6/6gr-v1/REPORT.md',
    'docs/verification/phase6/6gr-v1/README.md',
    'docs/verification/phase6/6gr-v1/results.json',
    'docs/verification/phase6/6gr-v1/integrity.json',
    'docs/verification/phase6/6gr-v1/regression.json',

    'tests/phase6g_engine.py',
    'tests/test_phase6g_engine.py',
    'tests/fixtures/phase6/6g-mappings.json',
    'tests/fixtures/phase6/6g-scenarios.json',
    'docs/verification/phase6/6g-v1/REPORT.md',
    'docs/verification/phase6/6g-v1/README.md',
    'docs/verification/phase6/6g-v1/results.json',
    'docs/verification/phase6/6g-v1/integrity.json',
    'docs/verification/phase6/6g-v1/regression.json',

    'tests/phase6f_engine.py',
    'tests/test_phase6f_engine.py',
    'tests/fixtures/phase6/6f-mappings.json',
    'tests/fixtures/phase6/6f-scenarios.json',
    'docs/verification/phase6/6f-v1/REPORT.md',
    'docs/verification/phase6/6f-v1/README.md',
    'docs/verification/phase6/6f-v1/results.json',
    'docs/verification/phase6/6f-v1/integrity.json',
    'docs/verification/phase6/6f-v1/regression.json',

    'tests/phase6e_engine.py',
    'tests/test_phase6e_engine.py',
    'tests/fixtures/phase6/6e-mappings.json',
    'tests/fixtures/phase6/6e-scenarios.json',
    'docs/verification/phase6/6e-v1/REPORT.md',
    'docs/verification/phase6/6e-v1/README.md',
    'docs/verification/phase6/6e-v1/results.json',
    'docs/verification/phase6/6e-v1/integrity.json',
    'docs/verification/phase6/6e-v1/regression.json',

    'tests/phase6d_engine.py',
    'tests/test_phase6d_engine.py',
    'tests/fixtures/phase6/6d-mappings.json',
    'tests/fixtures/phase6/6d-scenarios.json',
    'docs/verification/phase6/6d-v1/REPORT.md',
    'docs/verification/phase6/6d-v1/README.md',
    'docs/verification/phase6/6d-v1/results.json',
    'docs/verification/phase6/6d-v1/integrity.json',
    'docs/verification/phase6/6d-v1/regression.json',

    'tests/phase6c_engine.py',
    'tests/test_phase6c_engine.py',
    'tests/fixtures/phase6/6c-mappings.json',
    'tests/fixtures/phase6/6c-scenarios.json',
    'docs/verification/phase6/6c-v1/REPORT.md',
    'docs/verification/phase6/6c-v1/README.md',
    'docs/verification/phase6/6c-v1/results.json',
    'docs/verification/phase6/6c-v1/integrity.json',
    'docs/verification/phase6/6c-v1/regression.json',

    'tests/phase6b_engine.py',
    'tests/test_phase6b_engine.py',
    'tests/fixtures/phase6/6b-mappings.json',
    'tests/fixtures/phase6/6b-scenarios.json',
    'docs/verification/phase6/6b-v1/results.json',
    'docs/verification/phase6/6b-v1/README.md',
    'docs/verification/phase6/6b-v1/REPORT.md',
    'docs/verification/phase6/6b-v1/regression.json',
    'docs/verification/phase6/6b-v1/integrity.json',
    'tests/validate_development.py',
    'tests/test_phase6_qualification.py',
    'tests/phase6_engine.py',
    'tests/test_phase6_engine.py',
    'tests/fixtures/phase6/mappings.json',
    'tests/fixtures/phase6/scenarios.json',
    'tests/fixtures/phase6/qualification.json',
    'docs/verification/phase6/README.md',
    'docs/verification/phase6/REPORT.md',
    'docs/verification/phase6/integrity.json',
    'docs/verification/phase6/regression.json',
    'docs/verification/phase6/6a-v1/results.json',
    'docs/verification/phase6/QUALIFICATION.md',
}


# Current documentation may evolve; frozen release hashes are checked against
# the original tag for these exact paths only. All other release bytes stay live.
CURRENT_DOCUMENTATION = {
    'README.md',
    'docs/correlation-rule-catalogue.md',
    'docs/installation.md',
    'docs/security.md',
    'docs/validation-results.md',
    'rules/privilege-escalation/WCORR-PRIV-001.md',
}


@contextmanager
def release_evidence_view():
    original_root = release.ROOT
    manifest = json.loads(release.read('docs/verification/PUBLICATION_MANIFEST.json'))
    with tempfile.TemporaryDirectory(prefix='wcorr-evidence-') as directory:
        root = Path(directory)
        for name in manifest['publication_files']:
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name in CURRENT_DOCUMENTATION:
                target.write_bytes(subprocess.check_output(
                    ['git', 'show', 'v1.0.0:' + name], cwd=original_root))
            else:
                shutil.copyfile(original_root / name, target)
        with patch.object(release, 'ROOT', root):
            yield


class DevelopmentChecks(release.RepositoryChecks):
    def test_phase3_preservation(self):
        with release_evidence_view():
            super().test_phase3_preservation()

    def test_scheduled_validation(self):
        report = release.read('docs/verification/scheduled-kibana-validation/REPORT.md')
        rows = re.findall(r'^\| (WCORR-[A-Z]+-\d{3}) \| (PASS[^|]*) \| Yes \|$', report, re.M)
        self.assertEqual(len(rows), 14)
        self.assertEqual({row[0] for row in rows}, {r['id'] for r in self.manifest})
        raw = (release.ROOT / 'docs/verification/scheduled-kibana-validation/REPORT.md').read_bytes()
        candidate = raw.split(b'```eql\n', 1)[1].split(b'```', 1)[0]
        digest = re.search(r'Digest: `([a-f0-9]{64})`', report).group(1)
        self.assertEqual(hashlib.sha256(candidate).hexdigest(), digest)
        self.assertNotEqual(candidate, (release.ROOT / 'rules/privilege-escalation/WCORR-PRIV-001.eql').read_bytes())
        self.assertNotIn(b'] by ', candidate)
        for term in ['published original expression', 'remains unchanged',
                     'not the deployed production rule', 'false-positive risk',
                     'user-confirmed validation evidence', 'not independently retrieved evidence',
                     'not historical test results', 'not qualification requirements']:
            self.assertIn(term, report)
        for name in ['README.md', 'docs/installation.md', 'docs/security.md']:
            self.assertRegex(release.read(name), r'not qualification requirements|outside this independent project.s qualification requirements')

    def test_documentation_links_and_consistency(self):
        for path in release.candidates():
            if path.suffix != '.md':
                continue
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', path.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                dest = (path.parent / target.split('#')[0]).resolve()
                self.assertTrue(dest.is_relative_to(release.ROOT), 'Link escapes repository')
                self.assertTrue(dest.exists(), f'Broken link in {path.relative_to(release.ROOT)}')
        confdoc = release.read('docs/configuration.md')
        for field in {'timestamp', 'type.keyword', 'rule.id.keyword', 'agent.id.keyword',
                      'data.srcip.keyword', 'data.dstuser.keyword', 'data.audit.type.keyword',
                      'data.url.keyword', 'syscheck.path.keyword', 'syscheck.event.keyword'}:
            self.assertIn('"' + field + '"', confdoc)
        for term in ['field_caps', 'include_unmapped=true', 'does not establish',
                     'not configured in the pipeline', 'EnvironmentFile=', 'ACL', 'sincedb',
                     'start_position', 'queue.type', 'date', 'keyword']:
            self.assertIn(term, confdoc)
        results = release.read('docs/validation-results.md')
        for term in ['Different usernames', 'Routine SSH administration and sudo',
                     'observation timestamps', 'Reverse-proxy', 'same attacker',
                     'not necessarily the same PHP file', 'account creation',
                     'same-session', '/dev/null', 'carriage return',
                     'size limited to 10', 'not exhaustive', 'not proof']:
            self.assertIn(term, results)
        for term in ['journald', 'recursive ingestion', 'root-cause']:
            self.assertIn(term, release.read('docs/troubleshooting.md'))
        self.assertIn('Experimental reference implementation', release.read('README.md'))
        self.assertIn('not a production-validated rule pack', release.read('README.md'))
        deployment = release.read('docs/installation.md')
        for term in ['5 minutes', '1 minute', 'Disabled initially', 'None initially', 'deduplication', 'maxspan', 'query-window coverage']:
            self.assertIn(term, deployment)
        self.assertIn('Scheduled synthetic activation is now user-confirmed', results)
        self.assertIn('production activation is not established', results)

    def test_required_metadata_and_entry_documentation(self):
        for r in self.manifest:
            self.assertEqual(r['timestamp_field'], 'timestamp')
            self.assertEqual(r['event_category_field'], 'type.keyword')
            self.assertEqual(r['index_pattern'], 'wazuh-alerts-4.x-*')
            text = release.read(r['entry'])
            for label in ['Rule identifier:', 'Detection objective:', 'Required event fields:',
                          'Correlation window:', 'Historical match count:',
                          'False-positive considerations / Detection limitations:', 'Validation limitations:',
                          'Activation readiness:', 'EQL definition:',
                          'timestamp_field = timestamp', 'event_category_field = type.keyword',
                          'query size was limited to 10']:
                self.assertIn(label, text, r['id'])
            if r['id'] != 'WCORR-PRIV-001':
                self.assertIn('No activation in Kibana is claimed', text)
            else:
                self.assertIn('Production qualification pending', text)
                self.assertIn('does not validate scheduled execution', text)
            if release.EXPECTED[r['id']] == 0:
                self.assertIn('positive detection efficacy has not been demonstrated', text)

    def test_no_private_addresses_identifiers_logs_or_dependencies(self):
        # The frozen release predates synthetic SSH address fixtures. Permit only
        # these two documentation-only literals in two explicitly inventoried files;
        # retain every other inherited content check verbatim.
        synthetic_paths = {'tests/fixtures/phase6/6b-scenarios.json',
                           'docs/verification/phase6/6b-v1/results.json'}
        synthetic_addresses = {'192.' + '0.2.10', '192.' + '0.2.11'}
        allowed_suffixes = {'.md', '.conf', '.yml', '.example', '.eql', '.json', '.py'}
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

    def test_publication_manifest(self):
        historical = set(json.loads(release.read(
            'docs/verification/PUBLICATION_MANIFEST.json'))['publication_files'])
        self.assertFalse(historical & DEVELOPMENT_FILES)
        paths = release.candidates()
        self.assertEqual({p.relative_to(release.ROOT).as_posix() for p in paths},
                         historical | DEVELOPMENT_FILES)
        # Validate historical digests/readiness/inventory in a release view.
        # Only explicitly evolving documents come from the immutable local tag.
        with release_evidence_view():
            super().test_publication_manifest()
        # The manifest excludes its own digest; pin its bytes to the local tag.
        frozen = subprocess.check_output(['git', 'show',
            'v1.0.0:docs/verification/PUBLICATION_MANIFEST.json'], cwd=release.ROOT)
        self.assertEqual((release.ROOT / 'docs/verification/PUBLICATION_MANIFEST.json').read_bytes(), frozen)


def historical():
    """Materialize the entire local tag, then run its original exact validator."""
    with tempfile.TemporaryDirectory(prefix='wcorr-release-') as directory:
        root = Path(directory)
        names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only',
                                         'v1.0.0'], cwd=release.ROOT).decode().splitlines()
        for name in names:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(subprocess.check_output(
                ['git', 'show', 'v1.0.0:' + name], cwd=release.ROOT))
        return subprocess.call(['python3', str(root / 'tests/validate_repository.py')], cwd=root)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--historical', action='store_true',
                        help='Validate the complete local v1.0.0 tag in a temporary tree')
    args = parser.parse_args()
    if args.historical:
        raise SystemExit(historical())
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(DevelopmentChecks)
    raise SystemExit(not unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful())
