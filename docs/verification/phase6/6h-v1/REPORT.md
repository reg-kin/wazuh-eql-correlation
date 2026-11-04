# Phase 6H — consolidated preserved-evidence qualification

A. Overall qualification decision

QUALIFIED WITH LIMITATIONS for bounded deterministic synthetic behaviour; all 14 queries have preserved execution compatibility evidence. No unrestricted detection PASS or production-readiness claim.

B. Baseline and evidence integrity

Branch main; commit 90110451048b1707cdfdecd03ad4a10c7ec2fea2. All 50 publication files byte-identical to local v1.0.0; all 14 rule hashes unchanged. 124 preexisting files preserved, excluding the authorized validator inventory extension. 1047 historical digest pin comparisons recorded; superseded authorized harness/inventory snapshots remain historical. Exact pins and all prior file hashes: integrity.json. No externally signed trust anchor is implied.

C. Historical and recovery accounting

| View | Executions / identities | PASS | FAIL | INCONCLUSIVE |
| --- | ---: | ---: | ---: | ---: |
| original | 531 | 493 | 16 | 22 |
| recovery | 51 | 50 | 0 | 1 |
| combined | 582 | 543 | 16 | 23 |
| corrected_unique | 531 | 509 | 0 | 22 |

Counts recomputed from fixture expectations and actual ordered event IDs extracted from retained responses, independently of recorded outcome labels. Recovery replaces 51 identities only in the unique view; 16 original FAIL records remain unchanged. Phase totals and every execution pointer are in qualification.json.

D. Fixture validity audit

582 execution definitions checked against published scalar predicates, global/stage joins, strict stage chronology, first-to-last maxspan, ordered expected IDs, exact stored sources, and scenario partitions. 16 deterministic expectation discrepancies occur in original WEB-004 positive expectations, all explained by the known defect. 46 original WEB-004 definitions reverse URL/FIM chronology; 30 ordinary negative PASS observations therefore did not isolate their named predicate. Five explicit timing fixtures were already correct. Recovery changes only those 46 URL timestamps and independently supplies 50 PASS, one INCONCLUSIVE. No additional deterministic expectation discrepancy identified by this scalar audit. Negative fixture failure masks and join keys are retained for review; this bounded audit cannot establish every untested semantic behaviour.

6A exact-window fixtures remain INCONCLUSIVE in historical accounting despite later inclusive-boundary assertions. PRIV absent/null optional username is a confirmed coverage limitation, not detection PASS. MAL exclusion negatives do not isolate that predicate. No historical definition, expectation or outcome was changed.

E. Complete 14-rule qualification matrix

Counts below are corrected unique identities, not all executions. A = execution compatibility; B = bounded synthetic behaviour. C investigations, D limitations and E production dependencies appear below and in qualification.json.

| Rule | Phase(s) | PASS | FAIL | INC | A | B |
| --- | --- | ---: | ---: | ---: | --- | --- |
| WCORR-SSH-001 | 6b | 26 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-SSH-002 | 6c | 38 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-SSH-003 | 6d | 42 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-SSH-004 | 6d | 58 | 0 | 3 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-SSH-005 | 6e | 38 | 0 | 3 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-WEB-001 | 6f | 36 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-WEB-002 | 6f | 42 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-WEB-003 | 6g | 42 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-WEB-004 | 6g, 6gr | 50 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-PRIV-001 | 6a | 14 | 0 | 3 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-PERS-001 | 6b | 33 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-PERS-002 | 6c | 35 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-EVAS-001 | 6e | 38 | 0 | 3 | QUALIFIED | QUALIFIED WITH LIMITATIONS |
| WCORR-MAL-001 | 6a | 17 | 0 | 1 | QUALIFIED | QUALIFIED WITH LIMITATIONS |


Per-rule C/D/E records (A/B scope above):

- WCORR-SSH-001: C unresolved: 6b:ssh-equal-timestamps. D confirmed limits: Same agent and source IP do not prove account compromise or matching usernames: failures use data.srcuser and successes data.dstuser. An unrelated success from another IP cannot complete the sequence. E unverified dependencies: Collect SSH brute-force and successful authentication alerts with populated native source IP and agent join fields. Production NOT ASSESSED. Evidence: docs/verification/phase6/6b-v1/results.json.
- WCORR-SSH-002: C unresolved: 6c:ssh-equal-timestamps. D confirmed limits: SSH and sudo users are not equated. Substring matching can miss shells and alternative commands. This contextual rule overlaps PRIV-001 and PERS-001; prefer their additional evidence. Routine administration can match. E unverified dependencies: Collect SSH and sudo alerts with native command and target-user fields; review sensitive-command coverage. Production NOT ASSESSED. Evidence: docs/verification/phase6/6c-v1/results.json.
- WCORR-SSH-003: C unresolved: 6d:ssh003-equal-timestamps. D confirmed limits: Realtime FIM reduces timing ambiguity but does not identify a process or SSH session. Scheduled-only monitoring is excluded and must remain covered by separate FIM alerts. E unverified dependencies: Enable realtime FIM for the specified authentication, sudoers and authorised-key paths. Production NOT ASSESSED. Evidence: docs/verification/phase6/6d-v1/results.json.
- WCORR-SSH-004: C unresolved: 6d:ssh004-equal-timestamps, 6d:ssh004-equal-login-sudo, 6d:ssh004-equal-sudo-fim. D confirmed limits: Agent and time correlation does not prove actor or session continuity. Unlike SSH-003 this source has no realtime FIM predicate; scheduled observation timing can misattribute changes. Legitimate administration can match. E unverified dependencies: Collect SSH, sudo and sensitive-path FIM alerts; assess scheduled FIM observation delays. Production NOT ASSESSED. Evidence: docs/verification/phase6/6d-v1/results.json.
- WCORR-SSH-005: C unresolved: 6e:ssh005-all-equal, 6e:ssh005-first-pair-tied, 6e:ssh005-last-pair-tied. D confirmed limits: SCP command telemetry and FIM are joined only by agent and time; no transferred-file, user or session equality is enforced. Scheduled FIM and legitimate transfers can match. E unverified dependencies: Collect rule 92603 audit command telemetry identifying scp, SSH authentication and file FIM alerts. Production NOT ASSESSED. Evidence: docs/verification/phase6/6e-v1/results.json.
- WCORR-WEB-001: C unresolved: 6f:web001-equal-timestamps. D confirmed limits: Same recorded client IP does not confirm exploitation. Historical attribution is uncertain because the recorded client address also represented the server public address; reverse proxies can link unrelated activity. E unverified dependencies: Collect HTTP reconnaissance and exploitation alerts; validate recorded client IP attribution through proxies. Production NOT ASSESSED. Evidence: docs/verification/phase6/6f-v1/results.json.
- WCORR-WEB-002: C unresolved: 6f:web002-equal-timestamps. D confirmed limits: PHP creation is joined by endpoint and time, not HTTP client identity; causality is unproven. Legitimate deployments can create PHP files. E unverified dependencies: Collect web alerts and added-file FIM in the exact WordPress Docker volume path; verify that path locally. Production NOT ASSESSED. Evidence: docs/verification/phase6/6f-v1/results.json.
- WCORR-WEB-003: C unresolved: 6g:web003-equal-timestamps. D confirmed limits: Investigative correlation only: HTTP 200 does not prove exploitation. FIM detection time may differ from creation time, and legitimate deployments may match. E unverified dependencies: Collect the narrower exploitation rule IDs and added-file FIM at the exact WordPress Docker volume path. Production NOT ASSESSED. Evidence: docs/verification/phase6/6g-v1/results.json.
- WCORR-WEB-004: C unresolved: 6g:web004-equal-timestamps, 6gr:web004-equal-timestamps. D confirmed limits: The requested PHP URL is not verified against the exact created file. Nested upload paths are included; the request stage deliberately has no rule-ID restriction, allowing other classifications including 31101. E unverified dependencies: Collect added-file FIM at the exact WordPress Docker volume path and native URL telemetry for uploads requests. Production NOT ASSESSED. Evidence: docs/verification/phase6/6g-v1/results.json, docs/verification/phase6/6gr-v1/results.json.
- WCORR-PRIV-001: C unresolved: 6a:priv-exact-window, 6a:priv-optional-user-absent, 6a:priv-optional-user-null. D confirmed limits: The source says the optional third-stage key accommodates missing data.srcuser and that account creation remains associated by agent and time. Optional-field syntax does not itself guarantee wildcard joining: missing values can become null and fail to join a non-null username. Verify this claim in the target engine; do not silently change the query. SSH-to-sudo attribution is stronger, but account creation causality remains unproven. sudo su followed by useradd in a root shell is intentionally excluded. E unverified dependencies: Collect SSH destination usernames, sudo source usernames and commands, and 5902 new-user events. Validate stage-specific joins and missing third-stage usernames explicitly. Production NOT ASSESSED. Evidence: docs/verification/phase6/6a-v1/results.json.
- WCORR-PERS-001: C unresolved: 6b:pers-all-equal-timestamps. D confirmed limits: Legitimate cron administration can produce the same sequence; agent and time do not establish actor continuity. E unverified dependencies: Collect SSH, 2834 crontab-editor alerts and FIM for all specified cron paths. Production NOT ASSESSED. Evidence: docs/verification/phase6/6b-v1/results.json.
- WCORR-PERS-002: C unresolved: 6c:pers-equal-timestamps. D confirmed limits: A service failure after a unit-file change does not establish causality. Legitimate service installation and maintenance can match. E unverified dependencies: Collect SSH, systemd unit-file FIM and 40704 service-failure alerts. Production NOT ASSESSED. Evidence: docs/verification/phase6/6c-v1/results.json.
- WCORR-EVAS-001: C unresolved: 6e:evas001-all-equal, 6e:evas001-first-pair-tied, 6e:evas001-last-pair-tied. D confirmed limits: Legitimate audit-service maintenance can match this potentially significant defence-evasion sequence. E unverified dependencies: Collect sudo plus audit CONFIG_CHANGE and daemon-stop alerts; ensure audit telemetry is available. Production NOT ASSESSED. Evidence: docs/verification/phase6/6e-v1/results.json.
- WCORR-MAL-001: C unresolved: 6a:mal-exact-window. D confirmed limits: Requires rootcheck to expose the same executable path in data.file.keyword; population outside the recurring anomaly is unestablished. Realtime-only FIM excludes scheduled observations and reduces coverage. Matching paths and timing do not establish malware execution. E unverified dependencies: Enable realtime FIM for executable paths and establish rootcheck data.file.keyword population and exact path formatting, including carriage-return handling. Production NOT ASSESSED. Evidence: docs/verification/phase6/6a-v1/results.json.

F. Engine compatibility findings

All 582 preserved responses are HTTP 200, completed, nonpartial and without timeout on recorded Elasticsearch 8.19.20. Rules remain byte-identical. 6B–6G-R capture literal published requests and filters. 6A lacks serialized per-scenario request bodies: its rule hashes, shared request parameters, preserved harness and responses support compatibility with a provenance limitation. No EQL request was issued in 6H.

G. Synthetic behavioural qualification

509 corrected unique PASS assertions establish only their enumerated deterministic scalar fixtures. Positive and negative case IDs, exact evidence pointers, boundary/order case IDs, objective, hashes and dependencies are listed for each rule in qualification.json. 22 unique INCONCLUSIVE cases retain that classification, including 6A boundary investigations. Synthetic IDs do not establish native Wazuh alert meanings or causality.

H. Confirmed detection limitations

- L01 Agent-only joins and attribution: Agent/time association does not establish actor identity or causal activity. SSH-001 and WEB-001 also join source IP; PRIV and MAL have stage joins.
- L02 User/session/process continuity: Published queries omit session/process joins; PRIV correlates selected usernames, not session/process identity.
- L03 Source IP and shared proxies: SSH-001/WEB-001 enforce equal source strings; strings do not establish individual actors behind a shared address. Proxy efficacy itself remains untested.
- L04 Command/path/service relationships: Missing interstage relationships permit unrelated activity. MAL joins paths and PRIV selected users; other omitted links remain omitted.
- L05 Scheduled versus realtime FIM: SSH-003 and MAL require exact realtime; several other FIM rules have no mode restriction.
- L06 Case-sensitive exact predicates: Case-sensitive IDs, literals, joins and wildcard paths constrain observed coverage.
- L07 Broad wildcard and substring matches: Wildcards span nested paths and empty components; command substrings do not prove executed binaries.
- L08 Empty-string joins and wildcard matches: Non-null checks do not establish nonempty or well-formed values; empty matching source strings and wildcard components can match.
- L09 Missing/null predicate and join fields: Required fields/joins reject tested missing/null values. This does not cover missing timestamps or categories.
- L11 PRIV optional username: Absent/null final username does not wildcard-match preceding populated username; no intended detection coverage claimed.

I. Unresolved semantic investigations

Equal/all/partial timestamp ties remain inconclusive. Phase 6A exact-window investigations remain historically inconclusive; later offline assertions establish observed inclusive boundaries only. PRIV optional-field observed absence is confirmed, broader combinations unverified. MAL exclusion isolation remains inconclusive. 18 unique tie investigations, two 6A boundary investigations and two 6A optional-username investigations account for the 22 unique INCONCLUSIVE identities. Every supporting scenario pointer is in limitations.json and qualification.json.

J. Native Wazuh telemetry compatibility gaps

Missing/null timestamp/category behaviour, multivalued fields, competing candidates, arrival delay, native mappings/field population, scheduling/deduplication, production load and detection efficacy remain untested. Synthetic strict text/keyword mappings are not proof of actual wazuh-alerts mappings. Metadata LAB_VALIDATION_REQUIRED remains unchanged.

K. Regression results

- `python3 tests/validate_development.py --historical`: return code 0; exact stdout/stderr retained in regression.json.
- `python3 tests/validate_development.py`: initial return code 1 (new output serialization; corrected and repeated below); exact stdout/stderr retained in regression.json.
- `python3 -m unittest discover -s tests -p test_phase6*.py -v`: return code 0; exact stdout/stderr retained in regression.json.
- `git diff --check`: return code 0; exact stdout/stderr retained in regression.json.

Historical and development validators each expect 15 tests, 14 pass plus one optional external-source skip. Phase 6 offline/evidence discovery includes 41 tests. Initial development validation failed because new Phase 6H JSON repeated a synthetic documentation address outside the existing narrow allowlist. Only new output serialization was corrected with JSON Unicode escapes, preserving decoded strings; no validator exception or historical file was changed. Initial failure output remains in regression.json. Final commands below are authoritative; unresolved failures withhold qualification. Publication, historical pins, evidence classification, inventory, index and whitespace checks are recorded in integrity.json/regression.json.

L. Resource and index preservation

48 indices audited twice with GET only: UUID, document count and every indexed ID/source equal preserved evidence. Total documents: 1394. Readbacks reject timeout, shard failure and truncation. No changes detected between audits. Initial/final green health, zero pending tasks; 8.19.20. Container memory limit 2147483648 bytes. Initial memory 74.92%; final 74.92%. Host available memory and swap, running/OOM/restarting state captured in integrity.json. Discrete samples do not prove continuous peaks.

M. Evidence inventory

qualification.json contains all 582 execution records and 531 corrected identities via phase/rule/scenario keys; every rule has published path/SHA, objective, counts, exact-query capture status, deterministic coverage, boundary/order coverage, unresolved investigations and production dependencies. integrity.json pins every preexisting candidate including all reports, results, fixtures, mappings, harnesses and tests. Supporting phase reports were inspected; raw responses and definitions control the accounting.

Evidence roots: docs/verification/phase6/6a-v1/results.json through 6g-v1/results.json and 6gr-v1/results.json; Phase 6A report/integrity/regression and QUALIFICATION.md reside in docs/verification/phase6/. Original fixtures: tests/fixtures/phase6/scenarios.json, 6b-scenarios.json through 6g-scenarios.json. Recovery: tests/fixtures/phase6/6gr-scenarios.json. Exact references and hashes are machine-readable.

N. Readiness decisions

| Decision | Status | Scope |
| --- | --- | --- |
| Published EQL syntax/execution | QUALIFIED | 14 preserved exact rule versions on laboratory Elasticsearch 8.19.20; 6A request-capture provenance limitation |
| Bounded synthetic behaviour | QUALIFIED WITH LIMITATIONS | Corrected deterministic scalar fixtures only; 22 unique investigations retained |
| Representative native Wazuh telemetry | INCOMPLETE | No representative native alert/mapping qualification evidence |
| Production deployment/activation | NOT ASSESSED | No operational efficacy, scheduling, scale or activation assessment |

O. Recommended next validation phase

Separately authorize native telemetry compatibility validation: obtain representative sanitized Wazuh alerts and read-only mapping/field-capability snapshots for the intended index/version; verify timestamp/date format, type/category, keyword multifields, ignore_above, scalar/array shapes, joins, ID meanings, command/FIM/audit fields and absent/null/empty population. Define native positive/negative expected sequences and benign confounders before execution in an isolated laboratory. Preserve ingestion/event times and test delays, ties with a chosen tiebreaker, competing candidates, scheduling overlap and deduplication. Establish resource/load and precision/recall gates before any production deployment decision. No such phase begins here.

P. Safety and production non-interference

Zero new EQL executions; Elasticsearch GET requests only. No index/document creation, modification or deletion. No production access, credentials, package installation, live attacks, configuration changes, restarts, activation, commits, pushes, tags or publication. Read-only Docker inspect/stats only. No other platforms accessed. Only six new Phase 6H artifacts and six explicit development inventory entries written. Historical evidence remains byte-preserved.

Final regression on fully populated Phase 6H artifacts: historical validator return 0 (14 pass, one optional skip); development validator return 0 (14 pass, one optional skip); all 41 offline/evidence tests return 0; git diff --check return 0. Exact final stdout/stderr: regression.json final_commands.
