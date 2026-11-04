PHASE 6E — SSH-005 AND EVAS-001 REAL-ENGINE VALIDATION

A. Overall outcome
PARTIAL: 82 scenarios; 76 PASS, 0 FAIL, 6 INCONCLUSIVE. Exact published queries executed on Elasticsearch 8.19.20. Timestamp-tie investigations retain their original classification. No production readiness claim.

B. Baseline and preconditions
Branch main; commit 90110451048b1707cdfdecd03ad4a10c7ec2fea2. Initial tracked tree unchanged. Existing untracked development files matched the explicit inventory. Historical release and development validators each passed 14 checks with one optional external-source skip; all 21 prior offline/evidence checks passed. Prior reports, qualification, fixtures, harness adapters and retained responses reviewed. All 50 publication files match v1.0.0; all 14 published EQL hashes agree. Prior integrity pins verified. All 41 prior index UUIDs/counts/exact sources verified before writes and after execution. Both intended index names and the evidence directory were absent. No previous engine scenario rerun. Green cluster, zero pending tasks, version 8.19.20, 2 GiB container limit confirmed before writes.

C. SSH-005 rule analysis
Three ordered any stages: rule 5715; rule 92603 AND data.audit.command.keyword exactly "scp"; rule 550 OR 554. Global join agent.id.keyword; no stage-specific joins or optional fields. maxspan=30m from first to final event. Required predicate fields: rule.id.keyword at each stage, agent.id.keyword at each stage and data.audit.command.keyword at stage two. Timestamp is the configured date ordering field; type.keyword is configured for categories but any stages impose no category predicate. No path, mode, user, transfer-file, destination, process or session restriction. No exclusion. The final stage represents FIM alert telemetry, not proven SCP write attribution. Legitimate transfers and scheduled/unrelated FIM can correlate.

D. EVAS-001 rule analysis
Three ordered any stages: rule 5402 OR 5407; rule 80705 AND data.audit.type.keyword exactly "CONFIG_CHANGE"; rule 80703. Global join agent.id.keyword; no stage-specific or optional joins. maxspan=20m first to last. Required predicate fields: agent.id.keyword, rule.id.keyword, stage-two data.audit.type.keyword, configured timestamp. type.keyword configures category but any has no category condition. No command, path, mode, root-target, username, process, session or explicit exclusion predicate. Companion metadata interprets these IDs as sudo, audit configuration change and audit daemon stop. Synthetic rule IDs do not prove those real-world actions or a common actor. Legitimate audit maintenance can match.

E. Harness and mapping changes
Added suite adapter, five offline/evidence tests, strict mapping and 82 predeclared fixtures. Reused shared HTTP client/run/resources, 6B/6C source contracts and green-health adapter. No second HTTP implementation. Nine exact development inventory additions; no other prior source changes. Strict date/keyword multifield mappings add data.audit.command and data.audit.type; retain inert fields for absence-of-predicate probes. One primary, zero replicas, create-only document writes, sequential execution, 246 synthetic documents. Each scenario uses a unique UTC day plus an explicit timestamp range. Events occur within 1801 seconds of midnight, leaving over 23 hours between partitions, exceeding both maxspans; filters independently isolate each day. Equal timestamps have no tiebreaker. Expectations and fixture hashes were fixed before execution; no query/expectation changed or scenario rerun.

F. SSH-005 scenario results
41 scenarios: 38 PASS, 0 FAIL, 3 INCONCLUSIVE. Literal ordered IDs below; ? means predeclared null expectation.

| Scenario | Expected ordered IDs | Actual ordered IDs | Outcome |
| --- | --- | --- | --- |
| ssh005-positive | [["ssh005-positive-s1", "ssh005-positive-s2", "ssh005-positive-s3"]] | [["ssh005-positive-s1", "ssh005-positive-s2", "ssh005-positive-s3"]] | PASS |
| ssh005-alternate-id | [["ssh005-alternate-id-s1", "ssh005-alternate-id-s2", "ssh005-alternate-id-s3"]] | [["ssh005-alternate-id-s1", "ssh005-alternate-id-s2", "ssh005-alternate-id-s3"]] | PASS |
| ssh005-wrong-id-1 | [] | [] | PASS |
| ssh005-agent-mismatch-1 | [] | [] | PASS |
| ssh005-agent-missing-1 | [] | [] | PASS |
| ssh005-agent-null-1 | [] | [] | PASS |
| ssh005-rule-missing-1 | [] | [] | PASS |
| ssh005-rule-null-1 | [] | [] | PASS |
| ssh005-wrong-id-2 | [] | [] | PASS |
| ssh005-agent-mismatch-2 | [] | [] | PASS |
| ssh005-agent-missing-2 | [] | [] | PASS |
| ssh005-agent-null-2 | [] | [] | PASS |
| ssh005-rule-missing-2 | [] | [] | PASS |
| ssh005-rule-null-2 | [] | [] | PASS |
| ssh005-wrong-id-3 | [] | [] | PASS |
| ssh005-agent-mismatch-3 | [] | [] | PASS |
| ssh005-agent-missing-3 | [] | [] | PASS |
| ssh005-agent-null-3 | [] | [] | PASS |
| ssh005-rule-missing-3 | [] | [] | PASS |
| ssh005-rule-null-3 | [] | [] | PASS |
| ssh005-inside | [["ssh005-inside-s1", "ssh005-inside-s2", "ssh005-inside-s3"]] | [["ssh005-inside-s1", "ssh005-inside-s2", "ssh005-inside-s3"]] | PASS |
| ssh005-boundary | [["ssh005-boundary-s1", "ssh005-boundary-s2", "ssh005-boundary-s3"]] | [["ssh005-boundary-s1", "ssh005-boundary-s2", "ssh005-boundary-s3"]] | PASS |
| ssh005-outside | [] | [] | PASS |
| ssh005-adjacent-total-outside | [] | [] | PASS |
| ssh005-reversed | [] | [] | PASS |
| ssh005-first-pair-reversed | [] | [] | PASS |
| ssh005-last-pair-reversed | [] | [] | PASS |
| ssh005-all-equal | ? | [["ssh005-all-equal-s1", "ssh005-all-equal-s2", "ssh005-all-equal-s3"]] | INCONCLUSIVE |
| ssh005-first-pair-tied | ? | [["ssh005-first-pair-tied-s1", "ssh005-first-pair-tied-s2", "ssh005-first-pair-tied-s3"]] | INCONCLUSIVE |
| ssh005-last-pair-tied | ? | [["ssh005-last-pair-tied-s1", "ssh005-last-pair-tied-s2", "ssh005-last-pair-tied-s3"]] | INCONCLUSIVE |
| ssh005-predicate-case | [] | [] | PASS |
| ssh005-predicate-prefix | [] | [] | PASS |
| ssh005-predicate-suffix | [] | [] | PASS |
| ssh005-predicate-path | [] | [] | PASS |
| ssh005-predicate-null | [] | [] | PASS |
| ssh005-predicate-empty | [] | [] | PASS |
| ssh005-predicate-missing | [] | [] | PASS |
| ssh005-audit-missing | [] | [] | PASS |
| ssh005-predicate-wrong-stage | [] | [] | PASS |
| ssh005-unrelated-users-path-mode | [["ssh005-unrelated-users-path-mode-s1", "ssh005-unrelated-users-path-mode-s2", "ssh005-unrelated-users-path-mode-s3"]] | [["ssh005-unrelated-users-path-mode-s1", "ssh005-unrelated-users-path-mode-s2", "ssh005-unrelated-users-path-mode-s3"]] | PASS |
| ssh005-category-different | [["ssh005-category-different-s1", "ssh005-category-different-s2", "ssh005-category-different-s3"]] | [["ssh005-category-different-s1", "ssh005-category-different-s2", "ssh005-category-different-s3"]] | PASS |

G. EVAS-001 scenario results
41 scenarios: 38 PASS, 0 FAIL, 3 INCONCLUSIVE. Literal ordered IDs below; ? means predeclared null expectation.

| Scenario | Expected ordered IDs | Actual ordered IDs | Outcome |
| --- | --- | --- | --- |
| evas001-positive | [["evas001-positive-s1", "evas001-positive-s2", "evas001-positive-s3"]] | [["evas001-positive-s1", "evas001-positive-s2", "evas001-positive-s3"]] | PASS |
| evas001-alternate-id | [["evas001-alternate-id-s1", "evas001-alternate-id-s2", "evas001-alternate-id-s3"]] | [["evas001-alternate-id-s1", "evas001-alternate-id-s2", "evas001-alternate-id-s3"]] | PASS |
| evas001-wrong-id-1 | [] | [] | PASS |
| evas001-agent-mismatch-1 | [] | [] | PASS |
| evas001-agent-missing-1 | [] | [] | PASS |
| evas001-agent-null-1 | [] | [] | PASS |
| evas001-rule-missing-1 | [] | [] | PASS |
| evas001-rule-null-1 | [] | [] | PASS |
| evas001-wrong-id-2 | [] | [] | PASS |
| evas001-agent-mismatch-2 | [] | [] | PASS |
| evas001-agent-missing-2 | [] | [] | PASS |
| evas001-agent-null-2 | [] | [] | PASS |
| evas001-rule-missing-2 | [] | [] | PASS |
| evas001-rule-null-2 | [] | [] | PASS |
| evas001-wrong-id-3 | [] | [] | PASS |
| evas001-agent-mismatch-3 | [] | [] | PASS |
| evas001-agent-missing-3 | [] | [] | PASS |
| evas001-agent-null-3 | [] | [] | PASS |
| evas001-rule-missing-3 | [] | [] | PASS |
| evas001-rule-null-3 | [] | [] | PASS |
| evas001-inside | [["evas001-inside-s1", "evas001-inside-s2", "evas001-inside-s3"]] | [["evas001-inside-s1", "evas001-inside-s2", "evas001-inside-s3"]] | PASS |
| evas001-boundary | [["evas001-boundary-s1", "evas001-boundary-s2", "evas001-boundary-s3"]] | [["evas001-boundary-s1", "evas001-boundary-s2", "evas001-boundary-s3"]] | PASS |
| evas001-outside | [] | [] | PASS |
| evas001-adjacent-total-outside | [] | [] | PASS |
| evas001-reversed | [] | [] | PASS |
| evas001-first-pair-reversed | [] | [] | PASS |
| evas001-last-pair-reversed | [] | [] | PASS |
| evas001-all-equal | ? | [["evas001-all-equal-s1", "evas001-all-equal-s2", "evas001-all-equal-s3"]] | INCONCLUSIVE |
| evas001-first-pair-tied | ? | [["evas001-first-pair-tied-s1", "evas001-first-pair-tied-s2", "evas001-first-pair-tied-s3"]] | INCONCLUSIVE |
| evas001-last-pair-tied | ? | [["evas001-last-pair-tied-s1", "evas001-last-pair-tied-s2", "evas001-last-pair-tied-s3"]] | INCONCLUSIVE |
| evas001-predicate-case | [] | [] | PASS |
| evas001-predicate-prefix | [] | [] | PASS |
| evas001-predicate-suffix | [] | [] | PASS |
| evas001-predicate-path | [] | [] | PASS |
| evas001-predicate-null | [] | [] | PASS |
| evas001-predicate-empty | [] | [] | PASS |
| evas001-predicate-missing | [] | [] | PASS |
| evas001-audit-missing | [] | [] | PASS |
| evas001-predicate-wrong-stage | [] | [] | PASS |
| evas001-unrelated-users-path-mode | [["evas001-unrelated-users-path-mode-s1", "evas001-unrelated-users-path-mode-s2", "evas001-unrelated-users-path-mode-s3"]] | [["evas001-unrelated-users-path-mode-s1", "evas001-unrelated-users-path-mode-s2", "evas001-unrelated-users-path-mode-s3"]] | PASS |
| evas001-category-different | [["evas001-category-different-s1", "evas001-category-different-s2", "evas001-category-different-s3"]] | [["evas001-category-different-s1", "evas001-category-different-s2", "evas001-category-different-s3"]] | PASS |

H. EQL semantic findings
Both positive sequences and all alternate allowed rule IDs match. Wrong IDs, agent mismatches and missing/null agent or rule IDs at every stage prevent matching. Missing/null audit predicates, missing audit objects, case changes, prefixes/suffixes and wrong-stage placement prevent matching. SSH-005 requires bare lowercase scp; /usr/bin/scp does not match. EVAS-001 requires uppercase CONFIG_CHANGE. Reordered stages fail. Inside and exact maxspan boundaries match; outside fails. Adjacent gaps within maxspan do not overcome a first-to-last span outside it. All-equal and both partial-tie scenarios remain INCONCLUSIVE regardless of observed results. Different users, non-root targets, unrelated paths, scheduled modes and different categories still match. These are omitted predicates, not additional requirements. No optional fields or exclusions exist in either published expression.

I. Regression results
Final checks PASS: historical and development validators each 14 passed with one optional external-source skip; all 26 Phase 6 offline/evidence tests passed (21 prior, five new). Git diff --check and whitespace checks over all tracked/untracked candidates passed. See regression.json for exact command outputs and return codes. Historical, development, all prior and new offline/evidence tests, publication/rule hashes, prior evidence/index preservation and tracked/untracked whitespace checks are required. The optional external-source check remains skipped. Engine scenario outcomes are independent from offline assertion success.

J. Resource utilisation
Minimum sampled available host memory 1596.2 MiB; maximum swap use 536576 bytes; maximum container memory 74.42% of 2 GiB. All sampled states running, OOMKilled=false, Restarting=false. Green initial/final health, zero pending tasks. Guards: >=512 MiB host available, <=512 MiB swap used, <90% container memory, green/no pending tasks. No safeguard triggered. Sampling does not capture instantaneous peaks.

K. Rule and publication integrity
All 14 expected/actual SHA-256 values agree (full values in integrity.json). All 50 publication files remain identical to v1.0.0, including the historical validator and frozen manifest. Prior evidence preserved byte-for-byte. Only the explicit development inventory changed among preexisting files.

L. Evidence inventory
REPORT.md, README.md, results.json, integrity.json, regression.json. Results retain mappings, fixture definitions, exact query text/requests, HTTP statuses/responses, ordered expected/actual IDs, resource samples and inventories. Integrity retains full rule hashes, prior source hashes, identity audits and live mapping/settings/counts.

phase6-wcorr-6e-v1-ssh005: UUID Sb4skhJ1Trmgfkbl6cA4BA; documents 123.
phase6-wcorr-6e-v1-evas001: UUID qvjH8PZuSVmO_PLc47uLbA; documents 123.

M. Confirmed and unverified detection limitations
Confirmed: agent/time correlation cannot attribute actors, processes, sessions, transferred files or causality; legitimate unrelated maintenance may match. Exact case-sensitive audit values and ID/agent presence constrain coverage. Non-bare SCP command encodings, out-of-order and late observations are missed by these fixtures. No path/mode exclusions exist. Unverified: native Wazuh mappings/population, missing/null timestamps/category, multivalued fields, competing sequence selection, ingestion delay, scheduling/deduplication, real-world efficacy and scale. Six new timestamp-tie investigations remain unresolved. Earlier PRIV optional-username coverage and MAL isolated-exclusion limitations remain unchanged.

N. Cumulative Phase 6 progress
6A: 35 scenarios, 31 PASS, 0 FAIL, 4 INCONCLUSIVE.
6B: 61 scenarios, 59 PASS, 0 FAIL, 2 INCONCLUSIVE.
6C: 75 scenarios, 73 PASS, 0 FAIL, 2 INCONCLUSIVE.
6D: 104 scenarios, 100 PASS, 0 FAIL, 4 INCONCLUSIVE.
6E: 82 scenarios, 76 PASS, 0 FAIL, 6 INCONCLUSIVE.
Cumulative: 357 scenarios, 339 PASS, 0 FAIL, 18 INCONCLUSIVE. Ten of 14 rules now have bounded synthetic engine evidence. All previous classifications preserved. Offline assertions are not additional engine scenarios.

O. Readiness for final WEB-001–WEB-004 validation
Four WEB rules remain unexecuted. The established harness and integrity controls can support a separately authorized final phase after independent inspection of their exact expressions, scenario design, resource preflight and dedicated namespace selection. Current evidence does not validate WEB queries or establish production readiness.

P. Safety and production non-interference
Only local repository and loopback laboratory Elasticsearch accessed; Docker inspect/stats read-only. Writes confined to two named new indices and authorized development artifacts. All 41 prior indices preserved. No production access, credential retrieval, package installation, Docker/host configuration change, service restart, index deletion, live attack, published artifact edit, commit, push, tag or publication. Only SSH-005 and EVAS-001 executed in this phase.
