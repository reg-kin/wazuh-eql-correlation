# Phase 6G-R v1 — WEB-004 fixture recovery

The original Phase 6G evidence and classifications remain unchanged. Only WEB-004 was executed in this recovery.

Offline gate and tests:

```sh
python3 -m unittest discover -s tests -p 'test_phase6*.py'
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
```

Original execution command (now refuses retained index/evidence conflicts):

```sh
python3 tests/phase6gr_engine.py
```

The adapter calls the existing shared Phase 6 runner and HTTP transport. No retry, cleanup or arbitrary namespace is provided. Exact query, definitions, pre-execution gate, complete engine responses and ordered IDs are in results.json. Integrity includes all 51 original definitions and original/recovery comparisons, frozen hashes, retained index settings and 47 prior exact-source audits. REPORT.md documents scope and limitations; regression.json retains command output. Recovery fixtures are tests/fixtures/phase6/6gr-scenarios.json; mapping is the unchanged original 6G mapping. Document IDs intentionally retain original identity, isolated in the dedicated recovery index.
