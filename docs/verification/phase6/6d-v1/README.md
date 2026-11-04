# Phase 6D reproduction and evidence

Run from the repository root:

```bash
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
python3 -m unittest discover -s tests -p 'test_phase6*.py' -v
```

The retained engine run used `python3 tests/phase6d_engine.py`. It is not
idempotent: it refuses existing evidence, either target name or an unexpected
index inventory before writes. Reproduce only in a separate local laboratory
with the identical 39 retained prerequisite indices/sources and prior evidence,
without the 6D evidence directory or target indices. Do not delete retained
indices. No previous engine scenario is rerun by the preflight source audit.

The fixed endpoint defaults to http://127.0.0.1:19200 with no remote override.
The existing shared HTTP client supplies 15-second timeouts, redirect/proxy
rejection, namespace checks and create-only document writes. GreenClient only
strengthens health checking. Date timestamps, dynamic=strict mappings and
explicit keyword multifields are retained verbatim in results.json. One shard,
zero replicas per rule. Each scenario occupies an independent UTC day and
uses that exact timestamp range for EQL and source verification. Events are
at most 2000 seconds into a day, leaving over 23 hours between partitions.
No complete cross-scenario sequence can span the 30-minute window.

Only the exact published EQL bytes are executed, hashed before and during the
run. Requests use timestamp_field=timestamp, event_category_field=type.keyword,
size=10 and no tiebreaker. Full ordered IDs, response completeness and exact
stored sources are checked; HTTP 200 alone is insufficient. Four tie-order
investigations have null expectations and remain INCONCLUSIVE.

Resource guards require host available memory >=512 MiB, swap use <=512 MiB,
container usage <90%, running state without OOM/restart, green health and zero
pending tasks. The container limit must be 2 GiB. Sampling occurs initially,
before each scenario and finally, and does not capture instantaneous peaks.

REPORT.md contains the full A–P report. results.json preserves all fixtures,
mappings, requests, HTTP statuses, response bodies, ordered IDs, field caps,
source checks, resource samples and index inventories. integrity.json retains
baseline/postrun audits, all rule hashes, publication comparison, original
pre-correction fixture, correction rationale and final mapping/settings/counts.
regression.json records commands, output and preservation/whitespace checks.
The only prior source edited is the explicit development inventory/validator:
nine authorized paths plus exact synthetic path literals allowed in three
explicit files. Other paths/files remain rejected by regression tests.

No published rule, metadata, historical manifest or earlier evidence was edited.
No production readiness is implied by this bounded synthetic validation.
