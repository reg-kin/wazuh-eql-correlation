# Phase 6G — final two rules real-engine validation

A. Overall outcome

Coverage incomplete due to a post-execution-discovered WEB-004 fixture timestamp defect. 94 deterministic synthetic scenarios on Elasticsearch 8.19.20: 76 PASS, 16 FAIL, 2 INCONCLUSIVE. This establishes bounded synthetic engine compatibility. It does not establish detection efficacy or production readiness; no unrestricted PASS is claimed.

B. Baseline and preconditions

Branch main, commit 90110451048b1707cdfdecd03ad4a10c7ec2fea2. Starting tree: existing untracked Phase 6 files, no tracked changes. Before repository/index writes, all 50 historical publication files matched v1.0.0, all 14 rule digests matched, previous evidence pins passed, all 45 prior indices matched UUID/count/exact sources, target names and evidence directory were absent. Historical/development validators each passed 14 tests with one optional external-source skip. All 30 previous offline/evidence tests passed. Local engine was 8.19.20, green with zero pending tasks, safe resource measurements and 2147483648-byte container limit. The suite repeated mandatory engine/preservation preflight before engine writes. No Phase 6A–6F engine scenarios were rerun.

C. WEB-003 exact rule analysis

Two ordered `any` stages: rule.id.keyword in (31106, 31110, 31166, 31168), followed by rule.id.keyword == 554 AND syscheck.event.keyword == "added" AND syscheck.path.keyword like "/var/lib/docker/volumes/web_wp_data/_data/wp-content/uploads/*.php". Global join: agent.id.keyword only. Maxspan: 10m from first to last stage. Required stage fields are those predicates and agent join; metadata additionally specifies timestamp and type.keyword. There are no stage-specific joins, source/destination IP joins, HTTP URL/request/method/status constraints, command/audit predicates, optional-field syntax or exclusions. High severity/risk 85, COMPLETE_SOURCE/UNCHANGED, historical zero returned sequences (size 10, earlier expressions), LAB_VALIDATION_REQUIRED remain frozen metadata. The query cannot attribute file creation to an individual HTTP request/client or prove exploitation; unrelated alerts plus legitimate deployment can match. Missing joins, alternate IDs/path/case, delayed FIM or outside-window ingestion can miss related activity.

D. WEB-004 exact rule analysis

Two ordered `any` stages: the identical 554/added/uploads/*.php FIM predicate above, followed by data.url.keyword != null AND data.url.keyword like "/wp-content/uploads/*.php*". Global join: agent.id.keyword only. Maxspan: 30m. Required stage-1 fields: agent/rule ID, syscheck event/path; stage 2: agent ID and non-null matching URL. Metadata also lists timestamp and type.keyword; its rule-ID requirement applies only to FIM. No stage-specific joins, IP joins, request rule-ID restriction, method/status/request predicates, command/audit predicates, optional-field syntax or exclusions. High severity/risk 80; historical zero (earlier expression, size 10), COMPLETE_SOURCE/UNCHANGED and LAB_VALIDATION_REQUIRED remain frozen. No equality connects URL basename to FIM path. Any matching URL telemetry can correlate regardless of HTTP success or causal relation. Alternate roots, case, missing URL/join, FIM delays, or reversed/outside timestamps can miss related activity.

E. Harness and mapping changes

New suite adapter reuses unchanged shared runner/HTTP implementation, existing fixture contract and green-health adapter pattern. Nine authorized paths were added explicitly to development inventory; historical validator and manifest are unchanged. Both indices use dynamic=strict, timestamp=date and native nested Wazuh text/keyword multifields; one primary and zero replicas. Create-only writes and conflict checks are retained. Each two-event scenario has its own isolated UTC day with an exact timestamp range filter and more than 23 hours separating partitions, exceeding both maxspans. Expectations were declared before execution and unchanged. A WEB-004 timestamp defect was discovered after execution began: 46 default cases put stage 2 sixty seconds before stage 1. Their original definitions and expectations are preserved unchanged. No corrected rerun was attempted because the authorized namespace is retained and preexisting conflicts must be refused. Positive expectations in those cases remain FAIL; negative observations cannot isolate their intended predicate. Only the five explicitly timestamped WEB-004 cases have valid timing for their named investigation. Two stages admit only all-equal ties; a distinct partial tie is inapplicable.

F. WEB-003 scenario results

43 scenarios: 42 PASS, 0 FAIL, 1 INCONCLUSIVE.

S means the exact ordered IDs [["web003-<case>-s1", "web003-<case>-s2"]]; ∅ means []; ? means predeclared null. Full literal IDs and HTTP responses are retained in results.json.

| Case | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| positive | S | S | PASS |
| alternate-1-31110 | S | S | PASS |
| alternate-1-31166 | S | S | PASS |
| alternate-1-31168 | S | S | PASS |
| agent-id-missing-1 | ∅ | ∅ | PASS |
| agent-id-null-1 | ∅ | ∅ | PASS |
| rule-id-missing-1 | ∅ | ∅ | PASS |
| rule-id-null-1 | ∅ | ∅ | PASS |
| wrong-id-1 | ∅ | ∅ | PASS |
| agent-id-missing-2 | ∅ | ∅ | PASS |
| agent-id-null-2 | ∅ | ∅ | PASS |
| rule-id-missing-2 | ∅ | ∅ | PASS |
| rule-id-null-2 | ∅ | ∅ | PASS |
| wrong-id-2 | ∅ | ∅ | PASS |
| different-agent | ∅ | ∅ | PASS |
| different-source | S | S | PASS |
| different-destination | S | S | PASS |
| inside | S | S | PASS |
| boundary | S | S | PASS |
| outside | ∅ | ∅ | PASS |
| reversed | ∅ | ∅ | PASS |
| equal-timestamps | ? | S | INCONCLUSIVE |
| http-valid | S | S | PASS |
| http-invalid-case-path | S | S | PASS |
| category-different | S | S | PASS |
| event-missing | ∅ | ∅ | PASS |
| event-null | ∅ | ∅ | PASS |
| path-missing | ∅ | ∅ | PASS |
| path-null | ∅ | ∅ | PASS |
| uppercase-extension | ∅ | ∅ | PASS |
| nested-path | S | S | PASS |
| empty-stem | S | S | PASS |
| alternate-root | ∅ | ∅ | PASS |
| suffix | ∅ | ∅ | PASS |
| uppercase-path | ∅ | ∅ | PASS |
| query-suffix | ∅ | ∅ | PASS |
| non-php | ∅ | ∅ | PASS |
| event-added-case | ∅ | ∅ | PASS |
| event-modified | ∅ | ∅ | PASS |
| event-deleted | ∅ | ∅ | PASS |
| event-empty | ∅ | ∅ | PASS |
| legitimate-deployment | S | S | PASS |
| source-absent | S | S | PASS |

G. WEB-004 scenario results

51 scenarios: 34 PASS, 16 FAIL, 1 INCONCLUSIVE.

S means the exact ordered IDs [["web004-<case>-s1", "web004-<case>-s2"]]; ∅ means []; ? means predeclared null. Full literal IDs and HTTP responses are retained in results.json.

| Case | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| positive | S | ∅ | FAIL |
| agent-id-missing-1 | ∅ | ∅ | PASS |
| agent-id-null-1 | ∅ | ∅ | PASS |
| rule-id-missing-1 | ∅ | ∅ | PASS |
| rule-id-null-1 | ∅ | ∅ | PASS |
| syscheck-event-missing-1 | ∅ | ∅ | PASS |
| syscheck-event-null-1 | ∅ | ∅ | PASS |
| syscheck-path-missing-1 | ∅ | ∅ | PASS |
| syscheck-path-null-1 | ∅ | ∅ | PASS |
| agent-id-missing-2 | ∅ | ∅ | PASS |
| agent-id-null-2 | ∅ | ∅ | PASS |
| data-url-missing-2 | ∅ | ∅ | PASS |
| data-url-null-2 | ∅ | ∅ | PASS |
| different-agent | ∅ | ∅ | PASS |
| different-srcip | S | ∅ | FAIL |
| different-dstip | S | ∅ | FAIL |
| inside | S | S | PASS |
| boundary | S | S | PASS |
| outside | ∅ | ∅ | PASS |
| reversed | ∅ | ∅ | PASS |
| equal-timestamps | ? | S | INCONCLUSIVE |
| fim-uppercase-extension | ∅ | ∅ | PASS |
| fim-nested-path | S | ∅ | FAIL |
| fim-empty-stem | S | ∅ | FAIL |
| fim-alternate-root | ∅ | ∅ | PASS |
| fim-suffix | ∅ | ∅ | PASS |
| fim-uppercase-path | ∅ | ∅ | PASS |
| fim-query-suffix | ∅ | ∅ | PASS |
| fim-non-php | ∅ | ∅ | PASS |
| fim-event-added-case | ∅ | ∅ | PASS |
| fim-event-modified | ∅ | ∅ | PASS |
| fim-event-deleted | ∅ | ∅ | PASS |
| fim-event-empty | ∅ | ∅ | PASS |
| url-nested | S | ∅ | FAIL |
| url-query | S | ∅ | FAIL |
| url-suffix | S | ∅ | FAIL |
| url-empty-stem | S | ∅ | FAIL |
| url-uppercase-extension | ∅ | ∅ | PASS |
| url-uppercase-path | ∅ | ∅ | PASS |
| url-absolute | ∅ | ∅ | PASS |
| url-other-root | ∅ | ∅ | PASS |
| url-non-php | ∅ | ∅ | PASS |
| url-empty | ∅ | ∅ | PASS |
| url-different-file | S | ∅ | FAIL |
| request-rule-missing | S | ∅ | FAIL |
| request-rule-null | S | ∅ | FAIL |
| request-rule-other | S | ∅ | FAIL |
| wrong-fim-id | ∅ | ∅ | PASS |
| http-post-500 | S | ∅ | FAIL |
| different-category | S | ∅ | FAIL |
| source-absent | S | ∅ | FAIL |

H. EQL semantic findings

All allowed WEB-003 alert alternatives matched. WEB-003 matched exact maxspan and 1 ms inside, rejected 1 ms outside and reversed stages. Its missing/null predicate/join fields prevented matches; IP differences did not constrain joins. Its FIM pattern accepted nested paths and empty stems, rejected uppercase extension/path, alternate roots, non-PHP and suffix/query additions. Unrelated HTTP values and legitimate-deployment fixtures matched.

WEB-004 matched its explicitly timed 1799.999-second and exact 1800-second positives, rejected 1800.001 seconds and reversed stages. Equal-time observations for both rules remain INCONCLUSIVE. Most WEB-004 fixtures accidentally reversed request/FIM times; their empty responses cannot establish the intended URL, optional request-ID, method/status, FIM, category or IP semantics. Their FAIL classifications are retained and attributed to the fixture defect, not demonstrated engine incompatibility. No expectations were changed. URL wildcard/no-filename-equality and no-method/status/request-ID limitations follow directly from published syntax; they are not claimed as independently engine-confirmed by defective cases.

I. Regression results

Final historical and development validators each passed 14 tests with one optional external-source skip. All 35 offline/evidence tests passed (30 prior, five Phase 6G). Phase 6G engine outcomes are the separate scenario counts above. Publication/rule hashes, prior byte preservation and all 45 prior index audits passed. Tracked diff --check and explicit tracked/untracked whitespace scan passed. Full command outputs are in regression.json.

J. Resource utilisation

Minimum sampled host available RAM 1514.30 MiB; maximum sampled swap use 536576 bytes; maximum sampled container memory 74.86% of 2 GiB. Every recorded container state was running, OOMKilled=false, Restarting=false; initial/final health green, pending tasks empty. Guards require >=512 MiB available host RAM, <=512 MiB swap used, container <90%, green health, no pending tasks. No guard triggered. Samples do not establish instantaneous peaks.

K. Rule and publication integrity

All 50 publication files and all 14 published rule hashes match frozen evidence. Prior Phase 6A–6F candidate/evidence bytes are unchanged; the sole authorized preexisting-file modification adds nine explicit inventory paths. All 45 previous index UUIDs/counts/exact sources were audited again after execution. Full SHA-256 values and index checks are in integrity.json.

rules/web/WCORR-WEB-003.eql: b81834c7c28348dca9a4be421a4c251f572f593de82001f041a1b456e24af428

rules/web/WCORR-WEB-004.eql: b67180707b02050e1333c9c3938506da02a5ada66c9369476e6f662cc94b2c03

L. Evidence inventory

Evidence: docs/verification/phase6/6g-v1/REPORT.md, README.md, results.json, integrity.json, regression.json. Suite/tests: tests/phase6g_engine.py and tests/test_phase6g_engine.py. Definitions: tests/fixtures/phase6/6g-mappings.json and 6g-scenarios.json. Results retain original query text/hash, fixture/mapping hashes and definitions, request parameters/filter, complete HTTP status/responses, ordered expected/actual IDs, classifications, stored sources, field capabilities, index inventories and resource measurements. README gives reproduction commands and conflict constraints.

phase6-wcorr-6g-v1-web003: UUID mLd8to9rTMiNjDRgedqI5Q, documents 86.

phase6-wcorr-6g-v1-web004: UUID pIszrS0RSFyEVFDkjtrb7Q, documents 102.

M. Confirmed detection limitations

Agent/time joins permit unrelated alerts, legitimate deployments and requests for unrelated filenames to correlate. No actor identity, causality, exploitation success, PHP execution or HTTP success is established. Published WEB-004 syntax permits .php.txt URLs and does not require a request rule ID; defective fixtures leave those specific engine behaviors unvalidated. Case-sensitive exact roots/extensions and added-only FIM restrict coverage. Missing required predicate/join fields, alternate roots and timing/order changes can cause misses. FIM timestamps may differ from creation time. Native Wazuh mappings/population, missing/null timestamp/category, multivalued fields, competing sequences, ingestion delays, scheduling, deduplication, scale and real-world efficacy remain unverified. Timestamp ties remain unresolved. Earlier optional-username and isolated MAL-exclusion coverage limitations remain intact.

N. Cumulative Phase 6A–6G progress

| Phase | Scenarios | PASS | FAIL | INCONCLUSIVE |
| --- | --- | --- | --- | --- |
| 6A | 35 | 31 | 0 | 4 |
| 6B | 61 | 59 | 0 | 2 |
| 6C | 75 | 73 | 0 | 2 |
| 6D | 104 | 100 | 0 | 4 |
| 6E | 82 | 76 | 0 | 6 |
| 6F | 80 | 78 | 0 | 2 |
| 6G | 94 | 76 | 16 | 2 |
| Total | 531 | 493 | 16 | 22 |

All 14 published rules now have bounded synthetic real-engine evidence. Offline assertions are not additional engine scenarios. Prior classifications remain unchanged.

O. Readiness for consolidated qualification

The final two exact queries executed; WEB-003 has complete scoped fixture results and WEB-004 has bounded temporal positive/negative evidence only. WEB-004 predicate and limitation coverage needs corrected, independently predeclared fixtures in a separately authorized conflict-free run. The 46 reversed default fixtures prevent this phase from satisfying its full intended validation coverage. Consolidated qualification has not begun and requires a separate assessment of cumulative coverage and unresolved limitations. No production readiness, activation approval or unrestricted PASS follows from this phase.

P. Safety and production non-interference

Only repository files, loopback laboratory Elasticsearch and read-only Docker inspect/stats were accessed. Synthetic writes were confined to the two authorized new indices. No production infrastructure, credentials, package installation, Docker/host configuration, firewall/kernel settings, service restarts, existing-index deletion, live attacks, published EQL/metadata/descriptions, historical manifest, commit, push, tag or publication were involved. Existing 2 GiB limit and all prior evidence/indices were preserved. Phases 6A–6F were not rerun; consolidated qualification did not begin.
