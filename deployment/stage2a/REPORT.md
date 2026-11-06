# Stage 2A — scheduled Elastic Security preparation

Date: 6 November 2026. Baseline: main at `4fafdb021dd2d7814299418acd11edcde4d47411`, confirmed before changes; working tree was clean.

Verdict: **READY for offline review and controlled lab qualification; NOT READY for production activation.** Fourteen disabled API create bodies are prepared. Thirteen are eligible for staged qualification. WCORR-SSH-001 is the initial deployment candidate. WCORR-PRIV-001 is held: the published username-correlated query has not completed qualification. No deployment, activation, production connection, ECS normalisation or SOC Automation was performed.

## Deliverables and API contract

`definitions/*.json` are individual request bodies for `POST /api/detection_engine/rules`, not saved-object exports or NDJSON import files. Each uses its published WCORR identifier as stable `rule_id`; Kibana assigns the separate server `id`. Names include that identifier and the catalogue title. Catalogue description, severity, risk, limitations and field dependencies come from `tests/rule-manifest.json`; historical validation-status fields there are not used as current readiness claims. All rules have `enabled: false`, `actions: []`, no suppression configuration, version 1 and `max_signals: 100` as a provisional per-run cap. Names, author, category tags, required native fields and setup prerequisites supply metadata. The cap is not an assurance against dropped matches: verify effective Kibana/Elasticsearch limits, sequence intermediate alerts and truncation warnings in the target lab.

Queries decode to exactly the UTF-8 bytes of the published `.eql` files, including their final newline. Source SHA-256 values are checked against the frozen manifest. No query, join, optional field, path, predicate or maxspan was rewritten. PRIV-001's held body deliberately contains its published query, not the successful agent-only candidate.

Every rule sets `type` and `language` to `eql`, `index` to `["wazuh-alerts-4.x-*"]`, EQL ordering `timestamp_field` to `timestamp`, range-filter `timestamp_override` to `timestamp`, fallback disabled, and `event_category_override` to `type.keyword`. Ordering and range filtering are separate settings; setting only the range override is insufficient. No data view, ECS rename or timestamp transformation is introduced. No tiebreaker is invented: equal-timestamp ordering needs explicit lab qualification.

Schema references reviewed on 6 November 2026: [Elastic v8 create-rule API](https://www.elastic.co/docs/api/doc/kibana/v8/operation/operation-createrule) and [Elastic EQL field reference](https://www.elastic.co/docs/solutions/security/detect-and-alert/eql). These document the request fields and distinguish EQL timestamp ordering from range filtering. Documentation browsing was limited to public vendor documentation; deployment compatibility findings below use repository evidence only.

Compatibility uncertainty: published v8 documentation is not a pinned 8.19.20 OpenAPI artefact. No matching server-side schema or actual API round-trip export for these new bodies exists in this repository. The local validator enforces the selected field contract, types, catalogue values and exact generated bodies; it is not a complete Kibana OpenAPI validator and does not parse or execute EQL. Verify acceptance and read-back of all fields, especially timestamp ordering, timestamp fallback, event category, required-fields metadata and schedule interpretation, in an isolated matching-version lab before production approval. Do not remove unsupported fields silently or accept a fallback to ECS defaults. Any adjustments require regenerated definitions and repeat review.

## Schedule and coverage assumptions

All intervals are 5 minutes, `to: now`. Set the total search window W = M + D + I, where M is maxspan, provisional maximum event ingestion lateness D = 5 minutes, and I = 5 minutes between successful executions. Thus additional look-back (W minus I) is M + 5 minutes. Additional look-back is represented by `from`, not a separate API field. The historical 5-minute interval plus 1-minute additional look-back would search only 6 minutes and cannot cover any of the published complete maxspans.

| Rule | Maxspan M | Total W / from | Additional look-back | Severity / risk | Rollout |
| --- | --- | --- | --- | --- | --- |
| WCORR-SSH-001 | 15m | 25m / `now-25m` | 20m | High / 73 | Initial |
| WCORR-SSH-002 | 15m | 25m / `now-25m` | 20m | Medium / 47 | Later |
| WCORR-SSH-003 | 30m | 40m / `now-40m` | 35m | High / 70 | Later |
| WCORR-SSH-004 | 30m | 40m / `now-40m` | 35m | High / 78 | Later |
| WCORR-SSH-005 | 30m | 40m / `now-40m` | 35m | Medium / 62 | Later |
| WCORR-WEB-001 | 10m | 20m / `now-20m` | 15m | Medium / 55 | Later |
| WCORR-WEB-002 | 10m | 20m / `now-20m` | 15m | High / 82 | Later |
| WCORR-WEB-003 | 10m | 20m / `now-20m` | 15m | High / 85 | Later |
| WCORR-WEB-004 | 30m | 40m / `now-40m` | 35m | High / 80 | Later |
| WCORR-PRIV-001 | 30m | 40m / `now-40m` | 35m | High / 82 | HOLD |
| WCORR-PERS-001 | 30m | 40m / `now-40m` | 35m | High / 78 | Later |
| WCORR-PERS-002 | 30m | 40m / `now-40m` | 35m | Medium / 60 | Later |
| WCORR-EVAS-001 | 20m | 30m / `now-30m` | 25m | High / 80 | Later |
| WCORR-MAL-001 | 60m | 70m / `now-70m` | 65m | High / 75 | Later |

For a last-stage event at t and first-stage event at t−M, all stages are available by t+D if every event's ingestion lateness is bounded by D. The next successful run occurs by t+D+I, so the first event remains inside W. This also covers stages arriving out of order within the bound. Offline enumeration checks all 300 second offsets within an interval at delays 0, 1, 299 and 300 seconds, with sequences spanning the complete maxspan. This is a mathematical window check, not proof of the server's execution boundaries or detection engine state. Test exact boundaries and milliseconds in the lab; add measured clock/jitter margin if necessary.

Assumptions: clocks are aligned, timestamps represent the intended event time, every stage remains searchable, lateness is bounded, successful runs stay at most five minutes apart, and searches finish without timeout/truncation. The five-minute delay is unmeasured. Measure real delay and scheduler gaps; increase W or change schedule only after capacity testing. Future timestamps, longer delays, outages, event retention loss and capped results fall outside this guarantee. Long overlapping searches increase cost and possible alert duplication; they do not provide durable cross-run sequence state. Maintain at least the complete W of searchable source history, with operational margin. Gap recovery/backfill must be bounded, separately approved and audited.

## Repository-only configuration assessment

- `README.md` and `docs/verification/scheduled-kibana-validation/REPORT.md` identify Elasticsearch/Kibana 8.19.20 and user-confirmed synthetic scheduled alerts for 14 candidates. The report explicitly lacks primary exports, fixtures and execution logs. PRIV-001 used an altered expression; this does not validate its published username joins. MAL-001's synthetic Low/21 differs from the catalogue High/75; this pack preserves catalogue values.
- `config/logstash/logstash.conf` retains native fields, writes `wazuh-alerts-4.x-*`, supplies type `wazuh-alerts`, disables ECS compatibility and uses verified TLS. `manage_template: false` means it supplies no mapping assurance. Its output has no deterministic document ID, so retries/replay can duplicate source events. No ingestion changes are included.
- `docs/configuration.md` lists required native mappings but explicitly does not verify all live mappings. `docs/verification/phase7/7a-v1/` documents the complete field contract and dependencies; `phase7/7b-v1/REPORT.md` records bounded native EQL execution distinct from positive scheduled testing. These support feasibility, not current production compatibility.
- No effective Kibana configuration, encryption-key verification, licence/feature check, Task Manager capacity evidence, target-space privilege inventory or current production field-capabilities export is supplied. Therefore configuration support is **plausible and previously demonstrated in synthetic tests, but not established for these production definitions**. No production endpoint was contacted.

## Initial SSH-001 deployment procedure (future authorised work only)

1. Run `python3 scripts/stage2a.py validate` and `python3 -m unittest discover -s tests -p test_stage2a.py -v`. Review the source hash, High/73 metadata, same-agent/same-IP joins, 15-minute maxspan, 5-minute interval and 25-minute total search window. Same IP does not prove same user or compromise.
2. First use an isolated 8.19.20 lab. Its lab-only reviewed copy must target an isolated synthetic index, never production ingestion. Preserve the query and time fields. Record that the index differs from the production-target body. Run positive sequences, different-agent/IP negatives, missing-field cases, reversed order, legitimate successes, full-span/run-boundary cases, late/out-of-order ingestion and equal timestamps. Retain sanitised request/response and alert ancestry evidence.
3. Before any subsequently authorised production action, satisfy all prerequisites below. Select exactly one Kibana space and approved endpoint. Use trusted TLS, a protected credential outside this repository, JSON content type and `kbn-xsrf: true`. For non-default spaces prefix API paths with `/s/{space_id}`. Do not send credentials to Elasticsearch's endpoint when calling Kibana.
4. A separately authorised operator obtains the complete, freshly paginated rule inventory via `GET /api/detection_engine/rules/_find` in that space. Merge all pages into a local JSON object with `total` and `data`; verify the total stays stable across collection and restart collection if it changes. Do not filter to enabled rules or project tags: disabled and unmanaged test rules can conflict. Store snapshots outside version control. Run `python3 scripts/stage2a.py plan --snapshot /protected/path/rules.json --rule-id WCORR-SSH-001`. This command is offline and prints a proposal only.
5. Review potential equivalent detections with different whitespace, names, indices or rewritten predicates, including earlier synthetic copies. The planner catches exact query text (outer whitespace ignored), same stable IDs and exact-name conflicts, but cannot prove semantic equivalence or discover rules missing from a snapshot. Resolve conflicts explicitly; do not automatically delete, disable or overwrite existing rules. Use an exclusive operational deployment lock and recheck the inventory immediately before creation to avoid concurrent deployments.
6. If the proposal is `CREATE_DISABLED`, the authorised operator submits exactly `definitions/WCORR-SSH-001.json` to `POST /api/detection_engine/rules` in the selected space. Only SSH-001 is selected initially: never bulk-create the directory. A conflict response or ambiguous timeout requires GET by `rule_id` and reconciliation; never retry with a new ID, use overwrite imports, or regenerate IDs. If an exact disabled definition exists, the planner returns `NOOP`. Any drift, active rule or duplicate is a stop requiring explicit review. It never PATCHes existing rules.
7. Read back via `GET /api/detection_engine/rules?rule_id=WCORR-SSH-001`. Verify `enabled: false` and every effective body field, especially query bytes, index, timestamps, category, interval and from/to. Retain the returned server `id`, response, space, operator, body checksum and deployment time. Regenerate a complete snapshot and re-run the planner: expect NOOP. Server defaults or normalisation can cause a conservative drift failure; inspect it rather than automatically accepting it.
8. Activation is a separate authorised change after lab evidence and production prerequisites are approved. Use the target version's reviewed update-rule API (`PATCH /api/detection_engine/rules` with stable `rule_id` and `enabled: true`) only then; read back enabled state. No enabled request body or executable activation tool is supplied here. The first run may search recent history; review expected backlog and alert-volume risk before enabling.
9. Observe at least a full 25-minute source window plus ingestion allowance and several successful runs, extending to representative workloads and maintenance. Require no execution gaps, timeout/truncation warnings or unexplained duplicates; verify positive/negative outcomes and source ancestry. Monitor runtime relative to interval, source lateness, alert counts and analyst workload. Halt on unexpected joins, duplicate storms or missing expected alerts.
10. Roll back by separately authorised disable of this stable rule ID, followed by read-back and confirmation that new executions stop. Preserve existing alerts, snapshots and audit evidence; do not delete/recreate to reset identity. Already queued executions may need observation. Define recovery/backfill and requalification before resuming.

## Duplicate and idempotency safeguards

The offline planner has no networking, credentials, deployment, update or enable capability. It rejects incomplete inventory totals, repeated server IDs, duplicate stable IDs, same-name conflicts, matching query text under a different ID, enabled-rule conflicts and any body drift. PRIV-001 is always rejected. Repeat planning against an exact disabled installation is NOOP. Run Python normally; the tool refuses `-O`, which disables assertions. Inventory freshness and exclusive deployment ownership are operational prerequisites; a local snapshot cannot enforce remote atomicity.

Overlapping-window alert deduplication must be tested on the exact target version and query: execute the same source sequence over several runs and assert the expected single correlated alert, inspecting intermediate sequence alerts separately. Repeat the test after disable/re-enable and rule edits without assuming the same result. Do not assume a stable rule ID eliminates alert duplicates. Replayed source documents with different Elasticsearch IDs can produce distinct ancestry and alerts; the current Logstash configuration permits this. Record source `_index`/`_id` ancestry (and a sanitised source identity where available), investigate duplicate ingestion, and do not add suppression or change queries to conceal it. Suppression remains unconfigured; no exactly-once claim is made.

## Remaining controlled rollout

After SSH-001's observation gate, qualify and activate one rule at a time within these suggested waves, retaining before/after inventories and rollback ownership:

1. SSH-002 through SSH-005: establish sudo, FIM realtime/scheduled differences, audit scp coverage and legitimate administration. Inspect overlapping detections across the SSH rules; distinguish intended separate hypotheses from duplicate alerts.
2. WEB-001 through WEB-004: verify source-IP continuity where queried, deployment-specific WordPress container paths, FIM additions and URL coverage. The fixed paths are preserved and may not describe the target estate. Any path change is separate detection engineering work.
3. PERS-001 and PERS-002, then EVAS-001: verify cron/systemd/audit sources and maintenance negatives. Agent-only joins can correlate unrelated activity on an endpoint.
4. MAL-001: validate exact file-path joins, the excluded carriage-return `/dev/null` string, positive and negative paths, and the 70-minute total window under realistic load. Long-window cost needs its own gate.

There are twelve eligible later rules in these waves, plus initial SSH-001. PRIV-001 remains disabled and outside every wave until published username-correlation positives, cross-user negatives and optional/missing username semantics are qualified. Do not substitute its agent-only candidate silently. Each wave requires representative telemetry, delay/gap measurements, API read-back, runtime headroom, alert ancestry, deduplication checks, analyst acceptance and an agreed observation period before advancement. No calendar-based automatic activation is planned.

## Explicit production prerequisites

- Separate deployment and activation authorisation, change window, responsible owner, target space, reviewed endpoints, backup inventory and tested disable procedure.
- Confirm deployed Elasticsearch/Kibana versions and exact API fields in a matching isolated lab; record primary API evidence for these definitions. Confirm Elastic Security feature/licence availability and effective rule/alert limits.
- Confirm TLS/authentication, a persistent `xpack.encryptedSavedObjects.encryptionKey`, healthy Task Manager/alerting and functioning security alert indices. Verify least-privilege source read/view-index-metadata and target-space detection/alert permissions for the operator and the rule execution API key. No credentials or configuration are changed here.
- Verify all required native fields across every targeted index using field capabilities, mappings and representative values, including date `timestamp`, keyword join/predicate fields, doc values, ignore_above limits and unmapped/conflicting indices. Use `docs/verification/phase7/7a-v1/` and per-rule `required_fields` as the inventory. Inspect populated values, scalar/array shape, missing fields, source coverage and retention; do not infer these from templates or synthetic fixtures.
- Measure lateness, clock skew, jitter and maximum successful-run gaps; validate or increase the provisional delay budget and window under load. Confirm full-span positives, strict negatives and equal-timestamp behaviour. Do not introduce ECS normalisation or an unqualified tiebreaker to pass these gates.
- Review false positives, overlapping rules, replay/source duplicates, expected first-run history, capacity and result caps; demonstrate alert deduplication and source ancestry on successive runs. Monitor runtime, gaps and timeouts with a documented escalation/recovery process.
- Collect a fresh complete duplicate inventory, take the deployment lock, review any semantically equivalent unmanaged rules, create only disabled SSH-001, and verify the exact stored settings before any activation request.

## Offline validation results

`python3 scripts/stage2a.py validate`: PASS — 14 disabled definitions, source SHA-256 and query preservation, exact selected API field contract, catalogue metadata and maxspan preservation, unique stable IDs and bounded schedule enumeration.

`python3 -m unittest discover -s tests -p test_stage2a.py -v`: PASS — 8 tests: complete definitions/window checks, create-to-NOOP idempotency, incomplete inventory rejection, duplicate stable ID rejection, alternate-ID query detection, active/drift rejection, PRIV-001 hold and rejection of the legacy six-minute window as sufficient maxspan coverage.

These are offline checks. They do not establish live schema acceptance, EQL execution, ingestion timing, duplicate-alert behaviour or production configuration. Final regression results are recorded below after running the existing repository validator.

Existing repository regression: `python3 tests/validate_development.py` PASS — 16 checks, one expected skip for the unavailable external source file (`WCORR_SOURCE_FILE`). Frozen source hashes and repository inventory passed. The validator inventory was extended explicitly for Stage 2A artefacts; historical evidence was preserved.

Full offline unit suite: `python3 -m unittest discover -s tests` PASS — 49 tests. `git diff --check` PASS. Diff of `rules/` against the expected baseline is empty. `python3 -O scripts/stage2a.py validate` correctly refuses execution with a safety-validation error (expected negative check). No external source comparison or live service checks were attempted.

Final Stage 2A readiness verdict: **definition preparation and offline validation COMPLETE; controlled lab qualification READY; production deployment/activation BLOCKED pending the explicit prerequisites. SSH-001 is the sole initial candidate, twelve additional rules await controlled qualification, and PRIV-001 remains held.**
