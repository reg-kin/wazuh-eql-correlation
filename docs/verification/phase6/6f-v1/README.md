# Phase 6F reproduction and evidence

Run offline from the repository root:

```bash
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
python3 -m unittest discover -s tests -p 'test_phase6*.py' -v
```

Engine command: `python3 tests/phase6f_engine.py` against
http://127.0.0.1:19200. This retained run must not be rerun here: it
refuses existing evidence or index conflicts. Reproduction requires a separate
local Elasticsearch 8.19.20 lab with identical 43 prerequisite retained indices
and prior evidence, no Phase 6F target indices and no 6f-v1 evidence directory.
Never delete retained indices to rerun. No earlier engine scenarios are rerun.

The two targets are phase6-wcorr-6f-v1-web001 and
phase6-wcorr-6f-v1-web002. Only synthetic data is used. Exact original queries,
parameters, mappings, fixtures, expected IDs, HTTP statuses/responses, resource
samples and actual IDs are retained in results.json. integrity.json records
all 14 hashes, 50 publication comparisons, previous file digests, exact prior
source audits and live target mappings/settings/counts. regression.json records
final offline verification. REPORT.md contains the A–P findings and case table.
UTC-day filters and more than 23 hours between scenario events prevent
cross-scenario sequences. No expectations changed after execution; equal-time
investigations remain INCONCLUSIVE. No production readiness is claimed.
