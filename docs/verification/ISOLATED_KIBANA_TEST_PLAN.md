# Isolated Kibana import and activation test plan

Status: **planned; not executed**. This plan qualifies the exact disabled package from v1.1.0, tagged at merge commit `aafd896b8323f04a5653c25199e39b21646681c9`. Experimental source publication qualification is complete; isolated import and activation qualification of this unchanged export remains outstanding. Follow the [authoritative installation procedure](../installation.md#authoritative-public-release-procedure), [export configuration guidance](../public-release-configuration.md) and [integration reconciliation](PUBLIC_RELEASE_INTEGRATION.md). This plan adds no execution or production-readiness claim.

## Objectives and historical boundary

Demonstrate that all 14 published records import without identity or content changes, remain disabled, use the required native time/category configuration and, after controlled isolated activation, produce attributable scheduled detection alerts for labelled fixtures. Measure negative behaviour, timing, duplication and execution health before deciding whether this particular lab configuration passes.

Completed evidence is separate: [Phase 7B](phase7/7b-v1/REPORT.md) records bounded native execution of 14 frozen queries, with three positive and eleven valid zero-match rules. The [5 November scheduled report](scheduled-kibana-validation/REPORT.md) records user-confirmed synthetic scheduled alerts for all 14, using a PRIV-001 agent-only candidate. Its primary exports, execution logs and fixtures are not supplied. The historical username-correlated PRIV-001 source remains unchanged; the portable export uses a different agent-only expression without the candidate’s presence guards. Historical candidate success cannot qualify those exact export bytes. Historical MAL-001 Low/21 alert attributes do not replace the export’s High/75 metadata. Preserve all historical results and limitations.

## Prerequisites and isolation gate

Record operator, reviewer, UTC test period, cluster identity, selected space, exact Elasticsearch/Kibana versions, feature/licence availability and privileges. Use 8.19.20 for the initial reference test; other versions need independent qualification. Prepare disposable Elasticsearch/Kibana infrastructure, snapshots or equivalent recoverable state, a dedicated lab identity, synchronised clocks and an evidence directory outside the repository. Read [native configuration](../configuration.md) and [security guidance](../security.md).

A Kibana space alone does not isolate Elasticsearch data. Require no production ingestion, routing, credentials, connectors or automation, and prove `wazuh-alerts-4.x-*` resolves only to disposable synthetic lab indices, including aliases/data streams. Separate lab pipelines, checkpoints and queues from production. Retain empty actions, filters and exception lists; keep suppression disabled for baseline tests. Do not run attacks or privileged commands: generate authorised synthetic documents representing the stages.

If the unchanged index pattern or deployment-specific paths cannot safely be represented, stop exact-package qualification. Prepare a separately reviewed lab variant with its own hashes and evidence; never alter the preserved package. Missing native settings, incompatible mappings, identity conflicts or unexpected production reach block activation. Obtain lab operational authorisation before service changes or activation; this document is a future procedure, not an authorisation to operate a target.

## Verify the exact published package

Download the complete v1.1.0 source from the trusted public repository and confirm its tag resolves to the merge commit above. Record source reference, retrieval time and payload hashes; do not infer the presence of a separately uploaded release asset. Use a Git checkout with repository history and tags for the full validators (an extracted source archive lacks required Git metadata). From its root run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_public_release.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_development.py --historical
PYTHONDONTWRITEBYTECODE=1 python3 scripts/stage2a.py validate
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
(cd deployment/public-release && sha256sum -c MANIFEST.sha256)
```

Require 16 manifest entries to pass, 14 unique UUID `rule_id` values and WCORR names, and disabled records with no actions/filters/exceptions. Retain the manifest digest and NDJSON digest. Match query-string SHA-256 values and UUIDs to [machine-readable reconciliation](PUBLIC_RELEASE_RECONCILIATION.json); hash decoded query UTF-8 bytes without newline normalisation. Companion `.eql` files normalise the final newline and are not the import payload. Bundled checksums establish consistency, not independent authenticity or live-export provenance; the original archive is absent. The optional external-source check may be explicitly skipped when unavailable.

On a later documentation checkout, the unchanged validator’s explicit file inventory may reject new documentation. Record that failure separately from package integrity; do not regenerate frozen manifests or weaken validators. Run the commands on the exact tag as well to establish its baseline.

## Pre-import inventory and disabled import

1. Capture a complete paginated inventory of the selected space, including disabled rules, total counts and UUIDs. Save sanitised exports/read-back where permitted. Check all 14 UUIDs, WCORR names and equivalent queries under other IDs, especially Stage 2A copies. Stop on conflict; do not overwrite, regenerate IDs or run both variants.
2. Record a before-state snapshot and a cleanup ledger for every resource the test will create. Confirm no concurrent operator changes can invalidate the inventory.
3. In Security → Rules → Import rules, select only `deployment/public-release/kibana-rules.ndjson`. Do not use saved-object import, individual EQL sources or Stage 2A API-create bodies. Decline overwrite and automatic ID regeneration.
4. Save every import result. Require 14 successes, no partial failures and exactly 14 expected new identities. Read back every rule before enabling any. Partial import fails the gate and requires cleanup before retry.

## Identity, content, schedule and native configuration

Compare sanitised rule read-back against every NDJSON record and reconciliation entry: UUID `rule_id` (distinct from a server-assigned object ID), WCORR name, exact decoded query bytes, index, type/language, severity/risk, interval, from/to, result cap, disabled state and empty actions/filters/exceptions. Investigate all changes introduced by import or server defaults. PERS-002 is High/60 in this export; SSH-002 adds destination-user and command presence guards; PRIV-001 joins only by agent and cannot establish same-user/session causality. Twelve other queries reconcile lexically to historical sources, but all query bytes differ in formatting.

All rules use `wazuh-alerts-4.x-*`, interval `5m`, `to=now`; verify each `from` against the package:

| Rules | Maxspan | From |
| --- | --- | --- |
| WEB-001/002/003 | 10m | now-16m |
| SSH-001/002 | 15m | now-21m |
| EVAS-001 | 20m | now-26m |
| SSH-003/004/005, PERS-001/002, PRIV-001, WEB-004 | 30m | now-36m |
| MAL-001 | 60m | now-66m |

The export omits explicit `timestamp_field`, `timestamp_override`, fallback policy and `event_category_override`. Verify effective EQL ordering **and** range filtering use native `timestamp`, category uses `type.keyword`, and fallback cannot silently use incompatible ECS defaults. Retain read-back and execution evidence, not just a UI screenshot. If these settings are absent, unobservable or wrong, record unchanged-package qualification as blocked. A corrected rule is a separately reviewed variant with fresh hashes and requalification; importing a disabled record successfully does not resolve this gate.

Inspect field capabilities across every resolved target index: date `timestamp`, searchable keyword categories, agent and stage-specific join/predicate fields with doc values and populated values. Use the complete inventory in configuration guidance and derive dependencies from each exact export query. Check conflicting/unmapped fields, ignored long values and source coverage for SSH, sudo, audit, FIM, web, cron/systemd and rootcheck. Verify exact WEB-002/003/004 WordPress paths. Empty `required_fields` metadata is not evidence of optional telemetry. Missing source/mapping coverage blocks affected activation.

## Controlled activation and synthetic matrix

After all prior gates and lab authorisation pass, retain a disabled baseline export. Enable one rule at a time, recording UTC activation and execution times; keep actions absent. Identify fixtures by unique run ID and synthetic agent/document identities, and avoid overlap between cases. Record all source IDs, timestamps, ingestion times, stage labels, joins and expected outcomes before running each case. Refresh lab ingestion and confirm documents are searchable before interpreting a result. Test all 14 rules, then a bounded concurrent run to assess interference and capacity.

For each rule require a complete ordered positive sequence using exact export predicates, including a positive near its full maxspan. Use safely synthesised path/command values rather than executing their represented actions. Include these labelled negatives and edge cases:

| Case | Expected assessment |
| --- | --- |
| Missing stage, failed predicate, reversed event order, span beyond maxspan | No matching sequence; investigate any alert |
| Different agent; different IP, user or file/path at actual query join boundaries | No match where the query enforces that join; record unsupported attribution explicitly |
| Missing/null join and predicate fields | Measure exact query behaviour; SSH-002 guards require explicit missing-field negatives |
| Same-agent unrelated users for PRIV-001 | May match by design; assess as false-positive/attribution risk, not a same-user guarantee |
| WEB-001 cross-source mixing and MAL-001 mismatched file paths | Verify actual join isolation and path correlation |
| Legitimate SSH/sudo administration, account creation, maintenance and web deployments | Label analyst disposition; measure matches and explain tuning needs |
| Equal timestamps and out-of-order ingestion | Record ordering ambiguity and actual behaviour; do not assume a tie-breaker absent from the export |

Use query-specific expectations; never impose a username or IP join the export does not contain. Record positive and negative denominators per rule, not only aggregate PASS counts. A direct EQL response or preview helps diagnosis but cannot substitute for scheduled detection alerts.

## Alerts, errors, boundaries and deduplication

For every positive save the scheduled alert ID, rule UUID, execution reference, alert timestamp, severity/risk and original source-event ancestry. Verify stages and join values against fixtures and rule identity, including intermediate signals if present. Record expected versus actual sequence and alert counts and detection latency. A zero result requires confirmation that the rule executed successfully over the intended searchable documents; absence of an alert alone is not a negative PASS.

Capture execution status/history, warnings, parser/schema/mapping/privilege failures, timeouts, task delays, gaps and result-cap/truncation indicators. Observe multiple scheduled runs after ingestion becomes searchable and until the documented observation period ends. Set and record the timeout/observation budget before each run using maxspan, search window, ingestion delay and measured scheduling latency. Missing executions, unexplained errors or incomplete evidence fail the case rather than establishing a negative.

Exercise just-inside, equal and just-outside maxspan; search-window edges; arrivals immediately before/after a scheduled run; full-span sequences crossing runs; late and out-of-order arrival; and a controlled scheduler gap. Record timestamp precision and actual request bounds to assess inclusivity. Export windows are maxspan + 6m: a 5m interval leaves only a provisional 1m lateness allowance. Test delay below, at and above that allowance; it is not a measured guarantee. Contrast with Stage 2A’s separate maxspan + 10m proposal without changing the export. Test concurrent runtime and caps with bounded synthetic volume; do not claim unbounded capacity.

Repeat executions over overlapping windows with unchanged source IDs, then replay the same content under new document IDs. Count alerts by rule/sequence/run to distinguish engine deduplication from duplicate ingestion. Keep suppression off to expose baseline behaviour. Review shared/proxy IPs, same-agent unrelated actions and common maintenance with an analyst; report false-positive counts and dispositions. Synthetic results cannot estimate representative production precision/recall.

## Rollback and evidence

On any safety breach, unexpected actions, uncontrolled alert volume or gate failure, disable the newly imported rules immediately and confirm read-back. Capture execution/error evidence before cleanup. Delete only the 14 newly created identities verified against the cleanup ledger; never delete a pre-existing rule or use a broad name wildcard. Remove only test-created alerts, fixtures, indices, pipelines/checkpoints and temporary identities after retaining sanitised evidence. Reconcile the complete paginated after-inventory with the baseline, including other spaces/resources touched. Confirm no test tasks/actions remain and production was untouched. Record rollback outcome; retain failed-attempt evidence separately from retries.

Keep an evidence bundle outside frozen historical directories: run manifest, source/commit and payload digests, versions/licence, isolation approval, pre/post inventories, import results, effective settings, field capabilities, fixture definitions and expected outcomes, execution histories, alert ancestry, timing measurements, deduplication/analyst assessments and rollback ledger. Redact credentials, API keys, operator/personal identities and real telemetry before sharing; retain enough synthetic identity linkage to reproduce results. Hash collected artefacts and distinguish operator attestations from primary exports.

## Acceptance and remaining qualification

Report separate verdicts for offline package verification, disabled import, native configuration, controlled activation, per-rule efficacy/timing and rollback. Mark each PASS, FAIL, BLOCKED or NOT RUN with evidence references; do not infer later gates from earlier successes.

Require all 14 exact UUIDs and query/settings comparisons to pass; all rules initially disabled; verified native time/category and mappings; all planned positives producing attributable scheduled alerts; expected negatives and documented query limitations; healthy executions without unexplained gaps/truncation; measured boundary/deduplication results; reviewed false positives; and successful rollback to the baseline. Unexplained discrepancies prevent a full lab PASS. Define acceptable latency, duplicate volume and bounded load with the reviewer before execution; report measured limits rather than inventing production thresholds.

A successful isolated run qualifies only the recorded package, version and lab conditions. Representative Wazuh telemetry, field/source compatibility, realistic timing/capacity, coverage and accuracy assessment, and separate operational approval remain necessary before production deployment. SOC Automation, Cases, remediation and external SOC handoff are outside this project’s qualification scope.
