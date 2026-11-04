# Phase 6B reproduction and evidence

From the repository root, run sequentially:

```bash
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
python3 -m unittest discover -s tests -p 'test_phase6*.py' -v
python3 tests/phase6b_engine.py
```

The last command is an evidence-producing execution, not an idempotent test.
It refuses an existing `6b-v1` evidence directory or either retained index before
any writes. Reproduce in a separate laboratory with the code and fixtures,
without copying this run's evidence directory, and with neither target index
present. Never delete retained indices to rerun. This entry point deliberately
has no alternative namespace or non-loopback authorization option.

The runner imports the existing standard-library harness. Published EQL bytes
are read directly from the original files. There is no query substitute.
All 14 rule hashes must agree with the frozen rule manifest before execution.
Fixtures and mappings are validated and hashed before execution and their hashes
are checked again before each scenario. Each scenario occupies a separate UTC
day; its EQL request and source verification use that exact day range. All events
are within their partition. Adjacent scenario days exceed both maxspan values,
so even without filtering no complete cross-scenario sequence can occur.
This permits two bounded indices rather than 61 primary shards.

The strict mappings explicitly map `timestamp` as date, `type`, `agent.id`,
`rule.id`, SSH `data.srcip`, `data.srcuser`, `data.dstuser` and PERS
`syscheck.path`, `syscheck.mode` as text with keyword multifields. Username
and mode fields exist only to prove the absence of corresponding restrictions.
Every rule ID is a string. Object paths inherit strict dynamic mapping.
Nulls and absent leaves are intentional semantic fixtures, not unmapped fields.

Requests use `timestamp_field=timestamp`, `event_category_field=type.keyword`,
`size=10`, plus the per-scenario timestamp filter; no tiebreaker is specified.
Two or three documents per partition cannot exhaust the sequence result limit.
Every scenario uses create-only document writes, refresh, exact ordered sequence
IDs, complete responses, exact stored-source verification and field capabilities.
The report distinguishes predeclared assertions from unknown equal-time cases.
HTTP 200 alone never establishes successful detection.

Resource samples are taken initially, before every scenario and finally.
The inherited host stop thresholds are 512 MiB available memory minimum and
512 MiB swap use maximum, plus running/non-OOM/non-restarting container status.
Phase 6B additionally stops at container memory >=90% and on pending tasks.
Cluster health must remain green or yellow without timeout. HTTP timeout is 15s.
Sampling does not measure continuous instantaneous memory peaks.

Evidence files:

- `results.json`: full requests, responses, rules' SHA-256, fixture/mapping
  definitions and hashes, stored sources, field capabilities, resources,
  initial/final index inventory with UUIDs and sequence classifications.
- `integrity.json`: original publication and pre-existing Phase 6A file checks,
  all 14 rule hashes and local historical tag identity.
- `regression.json`: command outputs and return codes, including safe rerun refusal.
- `REPORT.md`: full A–P report printed directly to the terminal after validation.

No Phase 6A engine rerun is required or performed. Its retained assertions and
qualification tests are evaluated offline. All Phase 6A evidence is preserved.
Production telemetry, native Wazuh mapping compatibility, scheduled execution,
multivalued fields and detection efficacy remain outside these synthetic tests.

Development content validation retains the frozen restrictions with one explicit
exception: the two documentation-only source-IP literals may appear only in
`6b-scenarios.json` and this run's `results.json`. Other addresses and the same
literals in other paths remain rejected. The historical validator is unchanged.
