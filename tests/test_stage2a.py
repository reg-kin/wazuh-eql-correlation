"""Offline safety and schedule regression checks; no Elastic client."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('stage2a', Path(__file__).resolve().parents[1] / 'scripts/stage2a.py')
stage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stage)


class Stage2ATest(unittest.TestCase):
    def setUp(self):
        self.rules = stage.expected()
        self.ssh = self.rules[0]
        self.existing = dict(self.ssh, id='server-uuid')

    def test_all_definitions_and_schedule_boundaries(self):
        self.assertEqual(len(stage.validate()), 14)

    def test_create_then_repeat_is_noop(self):
        first = stage.plan(self.rules, {'total': 0, 'data': []}, self.ssh['rule_id'])
        self.assertEqual(first['operation'], 'CREATE_DISABLED')
        second = stage.plan(self.rules, {'total': 1, 'data': [self.existing]}, self.ssh['rule_id'])
        self.assertEqual(second['operation'], 'NOOP')

    def test_reject_incomplete_inventory(self):
        with self.assertRaises(AssertionError):
            stage.plan(self.rules, {'total': 2, 'data': [self.existing]}, self.ssh['rule_id'])

    def test_reject_duplicate_ids(self):
        duplicate = dict(self.existing, id='another-uuid')
        with self.assertRaises(AssertionError):
            stage.plan(self.rules, {'total': 2, 'data': [self.existing, duplicate]}, self.ssh['rule_id'])

    def test_reject_query_under_different_id(self):
        duplicate = dict(self.existing, rule_id='unmanaged', name='Other name')
        with self.assertRaises(AssertionError):
            stage.plan(self.rules, {'total': 1, 'data': [duplicate]}, self.ssh['rule_id'])

    def test_reject_drift_and_enabled_rules(self):
        for key, value in [('enabled', True), ('timestamp_field', '@timestamp'), ('query', 'any where true'), ('actions', [{}])]:
            changed = copy.deepcopy(self.existing)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(AssertionError):
                stage.plan(self.rules, {'total': 1, 'data': [changed]}, self.ssh['rule_id'])

    def test_privilege_rule_held(self):
        with self.assertRaises(AssertionError):
            stage.plan(self.rules, {'total': 0, 'data': []}, 'WCORR-PRIV-001')

    def test_short_legacy_window_cannot_cover_maxspan(self):
        for rule in self.rules:
            span = int(stage.re.search(r'maxspan=(\d+)m', rule['query'])[1])
            self.assertGreater(span, 6)
