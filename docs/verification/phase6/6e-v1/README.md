# Phase 6E reproduction and evidence

Offline reproduction from the repository root:

```bash
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
python3 -m unittest discover -s tests -p 'test_phase6*.py' -v
```

The retained engine command was `python3 tests/phase6e_engine.py`, using
http://127.0.0.1:19200. This is create-only, refuses conflicts and must not be
rerun in this retained laboratory. Reproduction requires a separate local lab
with identical 41 prerequisite indices and prior evidence, without the target
6E indices/evidence directory. Never delete retained indices to rerun it.
No prior engine scenarios are executed by the source audit.

See REPORT.md for the A–P report and scenario tables. results.json preserves
exact fixtures, requests, responses, status, classifications and resources.
integrity.json pins results, all prior files except the authorized inventory
edit, publication, rule hashes and live index settings/mappings/counts.
regression.json contains final validation outputs. Unique UTC-day ranges and
more than 23 hours between partitions prevent cross-scenario correlation.
All expectations were declared before engine execution; null expectations
remain INCONCLUSIVE. Resource guards and the 2 GiB limit remain unchanged.
No production readiness is implied.
