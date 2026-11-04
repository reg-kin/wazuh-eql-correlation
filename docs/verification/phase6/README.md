# Phase 6A local engine validation

This evidence applies only to synthetic fixtures for WCORR-PRIV-001 and WCORR-MAL-001 on Elasticsearch 8.19.20. Published queries, rule metadata, and the Phase 4 publication manifest are preserved. No production efficacy or activation readiness is claimed.

Run from the repository root, with the existing local laboratory already running:

```bash
python3 -m unittest discover -s tests -p 'test_phase6*.py' -v
python3 tests/validate_repository.py
python3 tests/phase6_engine.py --url http://127.0.0.1:19200 --run-id 6a-v2
```

The initial execution uses `6a-v1`. A repeat must use a new explicit run ID because indices and evidence are retained. The harness refuses index conflicts and existing evidence directories. It never deletes indices. All writes use `phase6-wcorr-<run-id>-<scenario>`. Default endpoints must resolve entirely to loopback; connections are pinned to a checked address, bypass environment proxies and reject redirects. `--authorize-non-loopback` explicitly authorizes an alternative laboratory origin; production is outside this task's authorization. Origins containing credentials are rejected. HTTP timeouts are 15 seconds.

Fixtures and mappings are in [scenarios.json](../../../tests/fixtures/phase6/scenarios.json) and [mappings.json](../../../tests/fixtures/phase6/mappings.json). The harness loads published EQL bytes from the paths recorded in results, checks their SHA-256 before every execution, and puts `timestamp_field`, `event_category_field`, and `size` in the JSON request body to `POST /<index>/_eql/search`. The engine itself validates this placement. There is one primary shard and zero replicas per scenario. Every event ID and timestamp is fixed. All rule IDs are strings. Index mappings are strict and carry an ownership marker; only fields needed by each rule and event category are mapped.

The runner executes sequentially with two or three documents per index. It checks host available RAM, swap use, container memory, running/OOM state and cluster health before each scenario. It stops below 512 MiB available RAM, above 512 MiB swap use, on OOM/restart/stopped container, or unacceptable cluster health. Monitoring uses read-only Docker inspect/stats for the established laboratory container. It does not provision or restart services.

Each result preserves EQL HTTP status and structured response, exact expected and actual ordered IDs, indexed-source verification, refresh acknowledgment, field capabilities, resources and notes. Parser/execution errors remain in the response and classify as FAIL; no alternate query is attempted. Unexpected transport failures stop the run. Unknown expectations are JSON null and classify as INCONCLUSIVE regardless of observed matches. This avoids assigning retrospective expectations to semantic experiments. The accompanying report interprets those observations.

The offline publication inventory validator predates Phase 6 and requires the exact frozen Phase 4 file set. New files therefore trigger its inventory check. This is reported openly; the validator and historical manifest are not weakened or rewritten. Rule checks, security/content checks and other existing checks still run.

Read the [execution report](REPORT.md) and [machine-readable evidence](6a-v1/results.json). The evidence records the baseline branch/commit, unchanged rule hashes, cluster identity, per-scenario results and retained index inventory. Reproduction produces different cluster-generated index UUIDs and execution times while preserving fixture IDs, timestamps, query bytes and expected sequences.
