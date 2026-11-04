# Phase 6C evidence

Read REPORT.md for all results and limitations. results.json preserves exact requests, response status/body, sources, mappings, IDs and resource observations. integrity.json pins results and prior evidence; regression.json records verification commands.

From the repository root, run offline checks:

```bash
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
python3 -m unittest discover -s tests -p 'test_phase6*.py' -v
git diff --check
```

Original engine command (already executed once):

```bash
python3 tests/phase6c_engine.py --url http://127.0.0.1:19200
```

It now refuses the existing evidence directory and indices. Do not remove or overwrite them. Reproduction requires a separately authorized new evidence/index namespace and an explicit inventory update; preserve the original fixtures and predeclared expectations. The shared engine partitions scenarios into disjoint UTC days and executes sequentially with 15-second HTTP timeouts, resource guards, create-only documents and exact source/sequence checks. No cleanup is provided. Do not rerun Phase 6A/6B engines.
