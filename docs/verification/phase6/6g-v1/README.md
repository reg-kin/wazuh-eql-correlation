# Phase 6G reproduction

Read REPORT.md for scope and limitations. All events are deterministic synthetic fixtures.

From repository root, run offline retained-evidence checks:

```sh
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
python3 -m unittest discover -s tests -p 'test_phase6*.py'
```

Original sequential engine command (already executed; refuses retained conflicts):

```sh
python3 tests/phase6g_engine.py --url http://127.0.0.1:19200
```

Requires existing Phases 6A–6F files and all 45 exact retained indices, local Elasticsearch 8.19.20, green health, no pending tasks and the unchanged 2 GiB container limit. Do not delete indices to rerun. A separate authorized namespace is required for another execution. Only 6G ran; consolidated qualification did not begin. The run contains a discovered WEB-004 reversed-timestamp fixture defect; see REPORT.md. Expectations, fixture definitions, strict mappings, request parameters and full responses are embedded in results.json and source definitions are in tests/fixtures/phase6/6g-*.json. No fixture corrections or expectation changes occurred. Timestamp ties remain INCONCLUSIVE regardless of observed matches.
