# Public-release integration — 6 November 2026

Verdict: suitable for offline release review and isolated import qualification; **not ready for production activation**. No services were contacted, packages installed, commits made or files staged.

## Preconditions and preservation

Confirmed `release/kibana-publication`, no unstaged changes and exactly 18 existing staged files identical to their index bytes before integration. The archive contained 14 unique WCORR names and 14 unique UUID rule IDs. All 16 SHA-256 manifest entries passed after extraction. The original archive SHA-256, manifest digest and all 18 staged-file digests are recorded in [reconciliation data](PUBLIC_RELEASE_RECONCILIATION.json).

The [package](../../deployment/public-release/README.md), including its README and manifest, is copied byte for byte from the archive. All 14 rules are disabled; actions, filters and exception lists are empty. The export already omits environment-specific server IDs, creator/updater identities, API keys, space IDs and execution metadata; none needed further removal. Original UUID rule IDs are retained as detection identity. No metadata was added to the import records. The WordPress volume paths remain deliberate detection predicates, not portable defaults.

Historical canonical EQL, source manifest, publication manifest and verification evidence remain unchanged. All staged Stage 2A definitions, report, script, tests and development validator remain index-identical. Stage 2A is a distinct API-create proposal with WCORR IDs, explicit native timestamp/category configuration, longer windows and a PRIV-001 hold. It is not regenerated from this export. Do not install both variants without resolving duplicate detections.

## Reconciliation

All 14 exported query strings differ in bytes from the canonical sources due to formatting and final-newline representation. The companion archive EQL files equal each exported query with its final newline normalised to one newline. Twelve have identical lexical tokens to the canonical definitions. SSH-002 adds `data.dstuser.keyword != null` and `data.command.keyword != null`; this can narrow missing-field behaviour and needs qualification. PRIV-001 removes per-stage username joins and the SSH/sudo username presence guards. It correlates only by agent over 30 minutes and cannot attribute the actions to the same user or session. Do not transfer historical username-query counts to this revision.

All original export UUIDs, query bytes, native index patterns, maxspans, severity/risk and scheduling are retained. Risk scores match the historical catalogue (including MAL-001 High/75). PERS-002 exports High/60 versus canonical and Stage 2A Medium/60; this severity change is preserved and requires analyst review. Names/descriptions and sparse author/tags/required-fields metadata differ from Stage 2A and are retained. Empty required-fields metadata does not remove telemetry dependencies. The machine-readable reconciliation lists every UUID, canonical path/hash, export-query hash and schedule.

| WCORR ID | Maxspan | Export interval | Export from | Stage 2A from | Query reconciliation |
| --- | --- | --- | --- | --- | --- |
| WCORR-EVAS-001 | 20m | 5m | now-26m | now-30m | formatting only |
| WCORR-MAL-001 | 60m | 5m | now-66m | now-70m | formatting only |
| WCORR-PERS-001 | 30m | 5m | now-36m | now-40m | formatting only |
| WCORR-PERS-002 | 30m | 5m | now-36m | now-40m | formatting only |
| WCORR-PRIV-001 | 30m | 5m | now-36m | now-40m | agent-level joins; username joins and presence guards removed |
| WCORR-SSH-001 | 15m | 5m | now-21m | now-25m | formatting only |
| WCORR-SSH-002 | 15m | 5m | now-21m | now-25m | destination username and command presence guards added |
| WCORR-SSH-003 | 30m | 5m | now-36m | now-40m | formatting only |
| WCORR-SSH-004 | 30m | 5m | now-36m | now-40m | formatting only |
| WCORR-SSH-005 | 30m | 5m | now-36m | now-40m | formatting only |
| WCORR-WEB-001 | 10m | 5m | now-16m | now-20m | formatting only |
| WCORR-WEB-002 | 10m | 5m | now-16m | now-20m | formatting only |
| WCORR-WEB-003 | 10m | 5m | now-16m | now-20m | formatting only |
| WCORR-WEB-004 | 30m | 5m | now-36m | now-40m | formatting only |

The export total search window is maxspan + 6 minutes, versus maxspan + 10 minutes in Stage 2A. With a five-minute execution interval this leaves a provisional one-minute lateness allowance rather than Stage 2A's five minutes. WEB-002 is explicitly confirmed as `interval=5m`, `from=now-16m`. Neither bound has been measured for production; preserve the supplied schedule and qualify capacity, delay and execution gaps before approving any revision.

## Import and qualification gates

Use the [installation procedure](../installation.md) in an isolated matching-version lab. Inventory all existing rules across every page in the selected space, including disabled rules and equivalent queries with different IDs. Decline overwrite and automatic ID regeneration. Verify all 14 imported rules remain disabled and read back the effective settings. No import or production change is part of this integration.

The export has no explicit `timestamp_field`, `timestamp_override`, fallback policy or `event_category_override`. Native EQL ordering and range filtering must use `timestamp`, with event category `type.keyword`; do not assume ECS defaults. Verify actual acceptance and read-back in Elasticsearch/Kibana 8.19.20; compatibility elsewhere is unestablished. Any necessary changes belong to a separately reviewed variant with new integrity evidence. The unchanged archive README describes Default-space import; use only the explicitly approved isolated space. This report supplies repository reconciliation and qualification gates in addition to that source README.

Use [export configuration guidance](../public-release-configuration.md) and query-derived field inventory. Validate a date `timestamp` and searchable keyword native joins and predicates across every index, populated fields, doc values, missing/conflicting mappings and full source coverage. Review the exact WordPress Docker volume paths in WEB-002/003/004 against the target estate. Do not rewrite them in the preserved archive. Missing telemetry, field or time configuration blocks activation.

False-positive risks include legitimate SSH/sudo administration and account creation, unrelated same-agent activity, shared/reverse-proxy IP addresses, routine file/cron/systemd maintenance, and legitimate web deployment changes. Agent-only PRIV-001 cannot prove user causality. Long overlapping windows can amplify duplicate source documents and analyst volume. Validate full-span positives, cross-agent/IP/user negatives as applicable, missing fields, equal timestamps, late/out-of-order arrival, run boundaries, repeated-run deduplication, result caps, runtime, gaps and rollback. Preserve sanitised alert ancestry and representative analyst review.

Scheduled synthetic success is user-confirmed historical evidence; no primary live export retrieval or new EQL execution occurred here. Offline JSON checks, token comparisons, hash verification and schedule arithmetic do not parse EQL, establish live API/schema compatibility, demonstrate representative detection accuracy or qualify production. Remaining blockers are native time/category read-back, field/source compatibility, realistic timing/capacity and positive/negative efficacy evidence, duplicate inventory and separately authorised operational approval.

## Reproducible offline validation

Run `python3 tests/validate_public_release.py` for the current inventory, inherited repository checks, package structure/integrity, all JSON, reconciliation and Stage 2A preservation. It extends the explicit inventory and permitted NDJSON/SHA-256 formats while retaining the existing content checks. The existing configuration guide remains byte-identical because historical integrity tests pin it; export-specific configuration guidance is supplied in a separate linked document. No frozen manifest is regenerated.

`tests/validate_development.py` is preserved as staged and describes the pre-integration inventory. Its direct invocation will reject the new files; use the new integration validator for the current tree. `python3 tests/validate_development.py --historical` runs the unchanged repository validator against the frozen release. Run Stage 2A validation and its unit tests separately, then the complete unit suite and `git diff --check`.

Final outcomes:

- Current integration validator: PASS, 18 checks, one expected skip for the unavailable external source document (`WCORR_SOURCE_FILE`). Includes all JSON/NDJSON structure, 14-rule inventory, exact archive integrity, query consistency, scheduling, metadata/content screening and 18-file index preservation.
- Frozen historical repository validator: PASS, 15 checks, one expected external-source skip.
- Stage 2A validator: PASS, 14 disabled definitions with exact source hashes and schedule coverage.
- Stage 2A unit tests: PASS, 8 tests.
- Full unit discovery: PASS, 49 tests.
- `git diff --check`: PASS.

Checks initially exposed an incorrect severity-equality assumption (PERS-002), final-newline differences in companion EQL and two configuration-guide integrity regressions. The severity and newline assertions now check the actual preserved export contract; the configuration guide was restored exactly and supplemental guidance moved to a new document. No archive hash, historical evidence or staged-file check was relaxed. The failures were corrected and the affected checks rerun successfully.

All integration changes remain unstaged. No production readiness is claimed; recommend review of this disabled public package followed by isolated version-matched import qualification.
