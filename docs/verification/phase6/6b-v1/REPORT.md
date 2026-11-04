============================================================
PHASE 6B — REAL-ENGINE VALIDATION REPORT
============================================================

A. OVERALL OUTCOME
PARTIAL: 59 predeclared assertions PASS, 2 semantic investigations INCONCLUSIVE, zero FAIL. Both exact published rules parse and execute successfully on Elasticsearch 8.19.20. Synthetic assertions are successful; production detection efficacy and equal-timestamp ordering remain unqualified. No blanket detection or production-readiness PASS is claimed.

B. BASELINE
Commit: 90110451048b1707cdfdecd03ad4a10c7ec2fea2; branch: main.
Expected post-qualification state verified before writes: 13 explicit development paths, all untracked; no tracked modifications. Phase 6A report, qualification report, harness, tests, fixtures, development inventory, historical publication manifest and companion rule documentation inspected. Historical/development checks each passed 14 tests with one optional external-source skip; all eight existing Phase 6 offline/qualification tests passed.
Local endpoint: http://127.0.0.1:19200; engine: 8.19.20; cluster UUID: Nw-VMeIvT5qL_77Vk2EaWw.
Initial/final cluster health: green/green. Initial indices: 35; final: 37. Execution started: 2026-11-04T09:59:27.161030+00:00.
No Phase 6A implementation, engine execution or evidence generation was repeated; retained evidence was checked offline. Existing Phase 6A indices received no writes.

C. RULE ANALYSIS
Authority: the original published EQL files, read verbatim for every execution.
SSH: rules/ssh/WCORR-SSH-001.eql
SHA-256: 3dfada3fd2d79dc3952022922fa737e7d5877dec2802da142244ea3cea4beb91
Objective: a Wazuh brute-force alert followed by successful SSH authentication. Exactly two ordered any-category stages: rule.id.keyword in ("5712", "5763"), then rule.id.keyword == "5715". Both explicitly require data.srcip.keyword != null. Global joins are agent.id.keyword and data.srcip.keyword. There are no stage-specific joins, optional-field operators, username checks, exclusions or raw failure-count thresholds. maxspan=15m spans the first and last event. A positive needs equal populated agent/IP values, correct IDs and order within the window. Different agent/IP, missing/null joins, incorrect IDs, reversed stages and excessive span must produce no sequences. Required query fields: agent.id.keyword, data.srcip.keyword, rule.id.keyword; request timestamp_field=timestamp and event_category_field=type.keyword. Missing/null mandatory joins are not wildcards.

PERS: rules/persistence/WCORR-PERS-001.eql
SHA-256: fa68921dc320770b8205616aff38b10d84c95518b4a85673d248a8803d9effc9
Objective: SSH login, crontab-editor alert, then cron-related FIM. Exactly three ordered any-category stages: rule.id.keyword == "5715"; then "2834"; then in ("550", "554") plus syscheck.path.keyword matching /var/spool/cron/*, /var/spool/cron/crontabs/*, /etc/cron.d/*, or exactly /etc/crontab. Global join: agent.id.keyword only. No stage-specific joins, optional-field operators, explicit exclusions, realtime/mode, user, source-IP, session, file-event-kind or command predicates exist. Thus a stage-specific join mismatch scenario is inapplicable; separate fixtures instead vary the real global join at each stage. maxspan=30m spans first to final stage. Required query fields: agent.id.keyword, rule.id.keyword and final-stage syscheck.path.keyword, plus configured timestamp/category paths. A positive needs correct IDs, order, same populated agent, allowed final path and bounded span. Wrong/missing agent/IDs, invalid path, reversed stages and excessive span must not match. Path is required only at the final stage; absence at earlier stages is intentionally valid.

D. HARNESS CHANGES
Modified tests/phase6_engine.py: optional suite configuration reuses the existing request, indexing, refresh, evidence, resource and exact-source logic; grouped indices use day-range filters for EQL and stored-source verification. Default Phase 6A invocation remains supported and refuses its retained namespace. Added selected-run write scope, fixture/mapping hashes and definitions in new evidence, request capture, repeated precreation conflict checks, container memory and pending-task guards for grouped execution.
Added tests/phase6b_engine.py: fixed 6b-v1 run namespace, loopback-only endpoint, all-14-rule hash preflight, strict source contracts and unique day partitions.
Added tests/test_phase6b_engine.py and tests/fixtures/phase6/6b-mappings.json, 6b-scenarios.json.
Modified tests/validate_development.py: nine exact new paths, without directory wildcards; preserves exact historical/development inventory and frozen tag checks. Its content check explicitly allows only the two documentation-only synthetic address literals in the new fixture and results paths. All other inherited content restrictions remain; rejection tests cover another address and an allowed literal in the wrong path. The original historical validator remains byte-for-byte unchanged.
Added this run's README.md, REPORT.md, results.json, integrity.json and regression.json. No shared-harness defect required changing Phase 6A fixtures or evidence.

E. MAPPING VALIDATION
Both mappings are dynamic=strict with explicit date timestamp and text fields with keyword multifields for type, agent.id and rule.id. SSH additionally maps data.srcip, data.srcuser and data.dstuser; PERS maps syscheck.path and syscheck.mode. Every rule ID is a string. The added username/mode fields test restrictions absent from the queries. Strictness is inherited by nested objects. Fixture validation rejects unknown fields, non-string scalars, duplicate IDs and partition violations before writes.
All indexed sources equal the fixtures exactly; field capabilities confirm every referenced keyword field. Live _mapping, _settings and _count readbacks are preserved in integrity.json. Each dedicated index has one primary shard and zero replicas. No malformed payload was sent to Elasticsearch; malformed-fixture rejection is tested offline.

F. SSH-001 RESULTS
Expected and actual values below are ordered Elasticsearch document IDs. [] means no sequences. UNKNOWN denotes a predeclared semantic investigation, never a detection PASS.
- ssh-positive: expected [["ssh-positive-s1", "ssh-positive-s2"]]; actual [["ssh-positive-s1", "ssh-positive-s2"]]; PASS; HTTP 200.
  One aggregated brute-force alert suffices; no raw failure count predicate.
- ssh-alternate-5763: expected [["ssh-alternate-5763-s1", "ssh-alternate-5763-s2"]]; actual [["ssh-alternate-5763-s1", "ssh-alternate-5763-s2"]]; PASS; HTTP 200.
- ssh-different-ip: expected []; actual []; PASS; HTTP 200.
- ssh-different-agent: expected []; actual []; PASS; HTTP 200.
- ssh-reversed-order: expected []; actual []; PASS; HTTP 200.
- ssh-wrong-first-id: expected []; actual []; PASS; HTTP 200.
- ssh-wrong-success-id: expected []; actual []; PASS; HTTP 200.
- ssh-missing-data-srcip-s1: expected []; actual []; PASS; HTTP 200.
- ssh-missing-agent-id-s1: expected []; actual []; PASS; HTTP 200.
- ssh-missing-rule-id-s1: expected []; actual []; PASS; HTTP 200.
- ssh-null-data-srcip-s1: expected []; actual []; PASS; HTTP 200.
- ssh-null-agent-id-s1: expected []; actual []; PASS; HTTP 200.
- ssh-missing-data-srcip-s2: expected []; actual []; PASS; HTTP 200.
- ssh-missing-agent-id-s2: expected []; actual []; PASS; HTTP 200.
- ssh-missing-rule-id-s2: expected []; actual []; PASS; HTTP 200.
- ssh-null-data-srcip-s2: expected []; actual []; PASS; HTTP 200.
- ssh-null-agent-id-s2: expected []; actual []; PASS; HTTP 200.
- ssh-both-ip-missing: expected []; actual []; PASS; HTTP 200.
- ssh-both-ip-null: expected []; actual []; PASS; HTTP 200.
- ssh-both-agent-missing: expected []; actual []; PASS; HTTP 200.
- ssh-both-agent-null: expected []; actual []; PASS; HTTP 200.
- ssh-inside-window: expected [["ssh-inside-window-s1", "ssh-inside-window-s2"]]; actual [["ssh-inside-window-s1", "ssh-inside-window-s2"]]; PASS; HTTP 200.
  Inclusive boundary expectation informed by Phase 6A; independently asserted for this query.
- ssh-outside-window: expected []; actual []; PASS; HTTP 200.
  Inclusive boundary expectation informed by Phase 6A; independently asserted for this query.
- ssh-exact-window: expected [["ssh-exact-window-s1", "ssh-exact-window-s2"]]; actual [["ssh-exact-window-s1", "ssh-exact-window-s2"]]; PASS; HTTP 200.
  Inclusive boundary expectation informed by Phase 6A; independently asserted for this query.
- ssh-different-usernames: expected [["ssh-different-usernames-s1", "ssh-different-usernames-s2"]]; actual [["ssh-different-usernames-s1", "ssh-different-usernames-s2"]]; PASS; HTTP 200.
  No username join exists.
- ssh-empty-ip: expected [["ssh-empty-ip-s1", "ssh-empty-ip-s2"]]; actual [["ssh-empty-ip-s1", "ssh-empty-ip-s2"]]; PASS; HTTP 200.
  Non-null predicate does not require a valid or nonempty IP string.
- ssh-equal-timestamps: expected UNKNOWN; actual [["ssh-equal-timestamps-s1", "ssh-equal-timestamps-s2"]]; INCONCLUSIVE; HTTP 200.
  No tiebreaker configured; observed order is not a portable guarantee.

G. PERS-001 RESULTS
- pers-positive: expected [["pers-positive-s1", "pers-positive-s2", "pers-positive-s3"]]; actual [["pers-positive-s1", "pers-positive-s2", "pers-positive-s3"]]; PASS; HTTP 200.
- pers-alternate-554: expected [["pers-alternate-554-s1", "pers-alternate-554-s2", "pers-alternate-554-s3"]]; actual [["pers-alternate-554-s1", "pers-alternate-554-s2", "pers-alternate-554-s3"]]; PASS; HTTP 200.
- pers-crontabs: expected [["pers-crontabs-s1", "pers-crontabs-s2", "pers-crontabs-s3"]]; actual [["pers-crontabs-s1", "pers-crontabs-s2", "pers-crontabs-s3"]]; PASS; HTTP 200.
- pers-cron-d: expected [["pers-cron-d-s1", "pers-cron-d-s2", "pers-cron-d-s3"]]; actual [["pers-cron-d-s1", "pers-cron-d-s2", "pers-cron-d-s3"]]; PASS; HTTP 200.
- pers-crontab: expected [["pers-crontab-s1", "pers-crontab-s2", "pers-crontab-s3"]]; actual [["pers-crontab-s1", "pers-crontab-s2", "pers-crontab-s3"]]; PASS; HTTP 200.
- pers-nested-path: expected [["pers-nested-path-s1", "pers-nested-path-s2", "pers-nested-path-s3"]]; actual [["pers-nested-path-s1", "pers-nested-path-s2", "pers-nested-path-s3"]]; PASS; HTTP 200.
- pers-different-agent-s1: expected []; actual []; PASS; HTTP 200.
- pers-missing-agent-s1: expected []; actual []; PASS; HTTP 200.
- pers-missing-rule-s1: expected []; actual []; PASS; HTTP 200.
- pers-wrong-rule-s1: expected []; actual []; PASS; HTTP 200.
- pers-different-agent-s2: expected []; actual []; PASS; HTTP 200.
- pers-missing-agent-s2: expected []; actual []; PASS; HTTP 200.
- pers-missing-rule-s2: expected []; actual []; PASS; HTTP 200.
- pers-wrong-rule-s2: expected []; actual []; PASS; HTTP 200.
- pers-different-agent-s3: expected []; actual []; PASS; HTTP 200.
- pers-missing-agent-s3: expected []; actual []; PASS; HTTP 200.
- pers-missing-rule-s3: expected []; actual []; PASS; HTTP 200.
- pers-wrong-rule-s3: expected []; actual []; PASS; HTTP 200.
- pers-both-agent-null: expected []; actual []; PASS; HTTP 200.
- pers-all-agent-missing: expected []; actual []; PASS; HTTP 200.
- pers-editor-before-login: expected []; actual []; PASS; HTTP 200.
- pers-fim-before-editor: expected []; actual []; PASS; HTTP 200.
- pers-missing-path: expected []; actual []; PASS; HTTP 200.
- pers-null-path: expected []; actual []; PASS; HTTP 200.
- pers-unsupported-path: expected []; actual []; PASS; HTTP 200.
- pers-prefix-lookalike: expected []; actual []; PASS; HTTP 200.
- pers-crontab-suffix: expected []; actual []; PASS; HTTP 200.
- pers-case-mismatch: expected []; actual []; PASS; HTTP 200.
- pers-inside-window: expected [["pers-inside-window-s1", "pers-inside-window-s2", "pers-inside-window-s3"]]; actual [["pers-inside-window-s1", "pers-inside-window-s2", "pers-inside-window-s3"]]; PASS; HTTP 200.
  maxspan covers first to final stage, not adjacent gaps.
- pers-outside-window: expected []; actual []; PASS; HTTP 200.
  maxspan covers first to final stage, not adjacent gaps.
- pers-exact-window: expected [["pers-exact-window-s1", "pers-exact-window-s2", "pers-exact-window-s3"]]; actual [["pers-exact-window-s1", "pers-exact-window-s2", "pers-exact-window-s3"]]; PASS; HTTP 200.
  maxspan covers first to final stage, not adjacent gaps.
- pers-scheduled-mode: expected [["pers-scheduled-mode-s1", "pers-scheduled-mode-s2", "pers-scheduled-mode-s3"]]; actual [["pers-scheduled-mode-s1", "pers-scheduled-mode-s2", "pers-scheduled-mode-s3"]]; PASS; HTTP 200.
  Published query has no realtime predicate.
- pers-different-event-categories: expected [["pers-different-event-categories-s1", "pers-different-event-categories-s2", "pers-different-event-categories-s3"]]; actual [["pers-different-event-categories-s1", "pers-different-event-categories-s2", "pers-different-event-categories-s3"]]; PASS; HTTP 200.
  All stages use any; no stage-specific joins exist to mismatch.
- pers-all-equal-timestamps: expected UNKNOWN; actual [["pers-all-equal-timestamps-s1", "pers-all-equal-timestamps-s2", "pers-all-equal-timestamps-s3"]]; INCONCLUSIVE; HTTP 200.
  Equal-time ordering investigated without tiebreaker.

H. EQL SEMANTIC FINDINGS
Global agent/IP equality is enforced for SSH; global agent equality is enforced at every PERS stage. Missing and explicit-null joins produce no sequence, including all-null agent fixtures. SSH null/missing IP also fails its explicit non-null predicates. Neither query has optional join syntax or stage-specific joins. SSH different usernames still matches because no username correlation is present. A shared empty IP string matches: non-null is not a valid-IP check.
PERS all four listed path branches and both FIM IDs match. The broad /var/spool/cron/* branch includes the crontabs subdirectory; the branches are overlapping. Nested /etc/cron.d/nested/job matches, demonstrating wildcard traversal in this fixture. A case-changed exact /ETC/CRONTAB and suffix /etc/crontab.bak do not match. Scheduled FIM matches because there is no realtime restriction. Different populated event categories match because each stage uses any. No rewritten predicate queries were needed.
Reversed relevant stages do not match. SSH 899s and exactly 900s match; 901s does not. PERS 1799s and exactly 1800s match; 1801s does not. Boundary expectations were predeclared, informed by 6A's same-engine findings; these are independent assertions for the two target queries.
Both equal-time investigations returned their complete stage sequences on this run. They remain INCONCLUSIVE: no expected outcome was predeclared, and an observed result without a tiebreaker does not establish stable tie ordering. No parser or execution errors occurred; all 61 EQL HTTP statuses were 200 and all responses complete. There are no explicit exclusion clauses in either query to isolate.

I. REGRESSION RESULTS
- Historical release verification: PASS (exit 0). 14 pass, one optional external-source skip.
- Development-tree validation: PASS (exit 0). 14 pass, one optional external-source skip.
- Phase 6A offline tests: PASS (exit 0). Four tests.
- Phase 6A qualification tests: PASS (exit 0). Four tests; no engine rerun.
- Phase 6B offline and retained engine tests: PASS (exit 0). Five tests; verifies all 61 retained engine responses.
- Retained namespace overwrite refusal: PASS (exit 1). Expected refusal before writes; evidence directory already exists.
- Git whitespace check: PASS (exit 0). Tracked changes; untracked paths scanned separately.
- All development-file whitespace scan and final preservation audit: PASS (exit 0). 22 explicit development files; protected files and 35 prior index entries unchanged.
Historical and development validation each comprise 15 tests: 14 pass and one optional external-source comparison is skipped because WCORR_SOURCE_FILE is not supplied. Existing Phase 6A offline checks: 4/4 pass; qualification: 4/4 pass, covering all 35 retained observations without rerunning the engine. New Phase 6B offline/evidence checks: 5/5 pass. Real engine: 59 PASS, two INCONCLUSIVE, zero FAIL. Initial fixture validation caught duplicate scenario names before writes; those were corrected before the final predeclared fixtures were executed. No failed engine scenario was retried or relabelled.
Git diff --check covers tracked changes; an additional trailing-whitespace scan covers all development files because they are untracked. The original historical validator remains intentionally release-only and was run against the entire local tag, not the expanded development tree. No mandatory regression failure is suppressed; optional external-source evidence remains unavailable.

J. RESOURCE UTILISATION
Host total RAM: 4055916544 bytes. Available host RAM initial/minimum sampled/final: 1771397120/1728339968/1728339968 bytes.
Swap used initial/maximum sampled/final: 536576/536576/536576 bytes.
Container memory initial/final: 1.45GiB / 2GiB / 1.467GiB / 2GiB; maximum sampled memory percentage: 73.33%.
All 63 samples show running, OOMKilled=false, Restarting=false. No resource safeguard triggered. Cluster health was checked before every scenario; final health is green, with zero pending tasks. All per-scenario pending-task lists are empty. Samples are discrete and do not prove continuous peaks. No memory limit increase, restart or configuration change occurred.

K. RULE INTEGRITY
All 14 published EQL SHA-256 hashes match the frozen rule manifest and the pre-task baseline. All 50 historical publication files, including the manifest itself, compare byte-for-byte to local v1.0.0. Tag object: 0236c0c7817e3900b5158001f85fb35e9ceac162. Target rule hashes before and after engine execution are identical. All pre-existing Phase 6A evidence, qualification files, fixtures and tests remain byte-identical. Only the authorized existing shared harness and development validator changed; their before/after hashes are recorded separately. Existing Phase 6A index inventory entries (names, UUIDs, counts, store sizes) are unchanged.

L. EVIDENCE INVENTORY
Directory: docs/verification/phase6/6b-v1/
Files: results.json (raw requests/responses, definitions, hashes, exact documents and field capabilities); integrity.json (publication/6A integrity and live mapping/settings/count readbacks); regression.json (commands, outputs and return codes); README.md (reproduction); REPORT.md (this report).
Fixtures: tests/fixtures/phase6/6b-scenarios.json and 6b-mappings.json.
Runner/test: tests/phase6b_engine.py and tests/test_phase6b_engine.py; shared runner: tests/phase6_engine.py.
- phase6-wcorr-6b-v1-ssh; UUID OVKAueN_TDmGVwnAQ8IW6Q; documents 54; sampled store size 73.6kb.
- phase6-wcorr-6b-v1-pers; UUID hxRzlOI7TO6lKhram5vXEg; documents 102; sampled store size 85.8kb.
Total: two new indices, 156 synthetic documents, 61 scenarios. Names belong exclusively to phase6-wcorr-6b-v1-. Existing indices were checked before creation; no evidence was overwritten. One distinct UTC day per scenario and the exact timestamp filter isolate all requests; day spacing also exceeds maxspan, preventing cross-scenario correlation even for absent/null agent cases. No index deletion occurred.

M. DETECTION LIMITATIONS
Confirmed: SSH matches one qualifying aggregated alert plus a success; it does not establish a raw failure threshold, same username, compromise or valid IP syntax. Missing agent/IP prevents completion. PERS associates only by agent and time, does not identify a user/session/process and admits scheduled FIM; legitimate administration can match. Broad cron wildcard paths include nested entries. These are observed query semantics, not newly asserted production defects.
Unverified: native Wazuh rule meanings/field population and mappings, real authentication/cron causality, alert scheduling and overlap/deduplication, out-of-order ingestion, multi-valued keys, production efficacy and stable equal-time ordering. This synthetic suite does not remove deployment or activation limitations. No optional-field semantics exist in these two queries; Phase 6A's optional PRIV username limitation and inability to independently isolate MAL's exclusion remain unresolved.

N. OVERALL PHASE 6 PROGRESS
Four of 14 exact published rules have synthetic real-engine execution evidence: WCORR-PRIV-001, WCORR-MAL-001 (6A), WCORR-SSH-001, WCORR-PERS-001 (6B). Combined original scenario classifications: 90 PASS, six INCONCLUSIVE, zero FAIL across 96 scenarios. Phase 6A's later offline qualification assertions do not retroactively change its four original investigations to detection PASS.
Ten rules remain unexecuted in Phase 6: SSH-002 through SSH-005, WEB-001 through WEB-004, PERS-002 and EVAS-001. No full-pack, production readiness or unrestricted detection PASS is claimed. Historical published metadata remains frozen; this evidence is additive.

O. NEXT RECOMMENDATION
Validate WCORR-SSH-002 and WCORR-PERS-002 next, under a separately authorized synthetic phase: extend the SSH chain and test the other persistence sequence while reusing the established harness. Neither was executed or otherwise tested against the engine here.

P. SAFETY CONFIRMATION
Only local loopback Elasticsearch laboratory access, read-only Docker inspection/stats, local Git reads and local development files were used. Elasticsearch writes were limited to the two dedicated 6B synthetic indices. No production VPS, Wazuh, Kibana, Elasticsearch or other production service was accessed. No credentials retrieved, live attacks, host packages, configuration/network changes, container restart, memory-limit changes, production changes, index deletion, commit, push, tag or publication occurred. Rules, metadata, published descriptions, frozen publication manifest, historical tag and every existing Phase 6A evidence file and index were preserved. Changes remain local and uncommitted.
