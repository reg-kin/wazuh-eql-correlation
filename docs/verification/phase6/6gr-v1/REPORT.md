# Phase 6G-R — WEB-004 fixture recovery

A. Overall recovery outcome

51 WEB-004 scenarios: **50 PASS, 0 FAIL, 1 INCONCLUSIVE** on Elasticsearch 8.19.20. All 16 original fixture-induced failures recovered to PASS. Complete scoped coverage of the requested 51 fixtures is restored. The original WEB-004 34 PASS, 16 FAIL, 1 INCONCLUSIVE and whole Phase 6G 76 PASS, 16 FAIL, 2 INCONCLUSIVE remain historical facts. No other rule was rerun. This is bounded synthetic validation, not production readiness.

B. Baseline and preconditions

Branch main, commit 90110451048b1707cdfdecd03ad4a10c7ec2fea2. Existing Phase 6 work was untracked; no commit was made. Mandatory read-only preflight passed before recovery repository writes: all 50 frozen publication bytes, 14 rule hashes, prior evidence pins, all 47 index UUIDs/counts/exact indexed sources, historical and development validation (14 passed plus one optional external-source skip each), and 35 previous offline/evidence tests. Recovery index and evidence directory were absent. The adapter repeated publication/evidence/index, version, green-health, zero-pending-task, resource and 2 GiB limit checks before execution. Initial preflight observations and all 47 identities are retained in results.json. Original definitions and prior integrity reports were independently read. The original shared validator checked schema, partitions, IDs and expectation shape but did not check semantic stage chronology or isolated negative predicates.

C. Original fixture defect and root cause

All 51 original WEB-004 definitions were independently checked against the exact published two-stage query. In 46 ordinary/default definitions, FIM is at 01:00:00 UTC and URL at 00:59:00 UTC: stage 2 is 60 seconds before stage 1. This default event timestamp assignment contradicts WEB-004's FIM-then-URL order. Original expected positives were semantically correct but could not match those reversed definitions; negatives also carried an unintended ordering mismatch and therefore did not isolate their named condition. The schema-only fixture gate allowed this systematic timestamp assignment error to reach the engine. No generator implementation is retained, so no unobserved generator history is asserted.

The exact 46 affected cases are: positive, agent-id-missing-1, agent-id-null-1, rule-id-missing-1, rule-id-null-1, syscheck-event-missing-1, syscheck-event-null-1, syscheck-path-missing-1, syscheck-path-null-1, agent-id-missing-2, agent-id-null-2, data-url-missing-2, data-url-null-2, different-agent, different-srcip, different-dstip, fim-uppercase-extension, fim-nested-path, fim-empty-stem, fim-alternate-root, fim-suffix, fim-uppercase-path, fim-query-suffix, fim-non-php, fim-event-added-case, fim-event-modified, fim-event-deleted, fim-event-empty, url-nested, url-query, url-suffix, url-empty-stem, url-uppercase-extension, url-uppercase-path, url-absolute, url-other-root, url-non-php, url-empty, url-different-file, request-rule-missing, request-rule-null, request-rule-other, wrong-fim-id, http-post-500, different-category, source-absent.

Five explicit timing cases: inside +1799.999 seconds; boundary +1800; outside +1800.001; reversed -60; equal-timestamps 0. These were already correctly defined. Independent checks of joins, FIM rule/event/path predicates, URL predicate, original expectations, strict source schema, UTC-day containment, unique partitions and ordered IDs found no additional defect. Each original predicate-negative case has exactly one intended predicate failure, plus the unintended original chronology defect. The five timing cases have all predicates satisfied. Equal timestamps retain null expectation and INCONCLUSIVE classification.

D. Corrected fixture design

Separate versioned file: tests/fixtures/phase6/6gr-scenarios.json. Exactly 46 URL timestamps changed to FIM +60 seconds, strictly inside 30 minutes. No other definitions or expectations changed. All 51 scenario identities and IDs are retained under a separate recovery index. Five timing exceptions are byte-equivalent to their original definitions. Each scenario retains its isolated UTC day and explicit timestamp range filter. Original file remains untouched.

Original fixture SHA-256: cd7605c106178f5abd845fe2b834c46f82d78f6e95658366e27034421355001e

Corrected fixture SHA-256: 9d373e8afbf8d87f7d5e74d871a3df9afe4ebd5f2275e44687b94d84c1085de9

E. Pre-execution fixture validation

51/51 passed before index creation. The offline gate checks strict schema, UTC/day isolation, exact intended interval, stage predicates and required non-null agent equality, exact intended failed predicate set for each negative, query-derived expected ordered IDs and unchanged original expectations. Positive spans must be positive and <=1800 seconds. Outside/reversed negatives isolate time/order; all other negatives have valid +60-second order. Equal timestamps explicitly remain semantic investigation without a deterministic order claim. Canonical comparison permits only the specified timestamp repairs. The complete suite rejects on any defect and is revalidated before each create-only document write. Automated mutation tests reject every one of the 46 original reversed cases, including negatives; additional tests reject extra predicate mismatches, reversed expected IDs, expectation changes and partition collisions. Offline expectations and checks were persisted in the initial evidence save before engine writes.

F. All 51 WEB-004 scenario results

S = literal ordered pair [["web004-<case>-s1", "web004-<case>-s2"]]; ∅ = []; ? = predeclared null. Full literal expected/actual IDs and HTTP responses are in results.json. Every EQL response was HTTP 200, nonpartial, completed, without timeout. Counts: 50 PASS, 0 FAIL, 1 INCONCLUSIVE.

| Case | Original 6G | Recovery expected | Recovery actual | Recovery outcome |
| --- | --- | --- | --- | --- |
| positive | FAIL | S | S | PASS |
| agent-id-missing-1 | PASS | ∅ | ∅ | PASS |
| agent-id-null-1 | PASS | ∅ | ∅ | PASS |
| rule-id-missing-1 | PASS | ∅ | ∅ | PASS |
| rule-id-null-1 | PASS | ∅ | ∅ | PASS |
| syscheck-event-missing-1 | PASS | ∅ | ∅ | PASS |
| syscheck-event-null-1 | PASS | ∅ | ∅ | PASS |
| syscheck-path-missing-1 | PASS | ∅ | ∅ | PASS |
| syscheck-path-null-1 | PASS | ∅ | ∅ | PASS |
| agent-id-missing-2 | PASS | ∅ | ∅ | PASS |
| agent-id-null-2 | PASS | ∅ | ∅ | PASS |
| data-url-missing-2 | PASS | ∅ | ∅ | PASS |
| data-url-null-2 | PASS | ∅ | ∅ | PASS |
| different-agent | PASS | ∅ | ∅ | PASS |
| different-srcip | FAIL | S | S | PASS |
| different-dstip | FAIL | S | S | PASS |
| inside | PASS | S | S | PASS |
| boundary | PASS | S | S | PASS |
| outside | PASS | ∅ | ∅ | PASS |
| reversed | PASS | ∅ | ∅ | PASS |
| equal-timestamps | INCONCLUSIVE | ? | S | INCONCLUSIVE |
| fim-uppercase-extension | PASS | ∅ | ∅ | PASS |
| fim-nested-path | FAIL | S | S | PASS |
| fim-empty-stem | FAIL | S | S | PASS |
| fim-alternate-root | PASS | ∅ | ∅ | PASS |
| fim-suffix | PASS | ∅ | ∅ | PASS |
| fim-uppercase-path | PASS | ∅ | ∅ | PASS |
| fim-query-suffix | PASS | ∅ | ∅ | PASS |
| fim-non-php | PASS | ∅ | ∅ | PASS |
| fim-event-added-case | PASS | ∅ | ∅ | PASS |
| fim-event-modified | PASS | ∅ | ∅ | PASS |
| fim-event-deleted | PASS | ∅ | ∅ | PASS |
| fim-event-empty | PASS | ∅ | ∅ | PASS |
| url-nested | FAIL | S | S | PASS |
| url-query | FAIL | S | S | PASS |
| url-suffix | FAIL | S | S | PASS |
| url-empty-stem | FAIL | S | S | PASS |
| url-uppercase-extension | PASS | ∅ | ∅ | PASS |
| url-uppercase-path | PASS | ∅ | ∅ | PASS |
| url-absolute | PASS | ∅ | ∅ | PASS |
| url-other-root | PASS | ∅ | ∅ | PASS |
| url-non-php | PASS | ∅ | ∅ | PASS |
| url-empty | PASS | ∅ | ∅ | PASS |
| url-different-file | FAIL | S | S | PASS |
| request-rule-missing | FAIL | S | S | PASS |
| request-rule-null | FAIL | S | S | PASS |
| request-rule-other | FAIL | S | S | PASS |
| wrong-fim-id | PASS | ∅ | ∅ | PASS |
| http-post-500 | FAIL | S | S | PASS |
| different-category | FAIL | S | S | PASS |
| source-absent | FAIL | S | S | PASS |

G. Original versus recovery comparison

Original WEB-004: 34 PASS, 16 FAIL, 1 INCONCLUSIVE. Recovery: 50 PASS, 0 FAIL, 1 INCONCLUSIVE. All 16 original failures were fixture-induced and recovered to PASS. Of the 34 original PASS cases, 30 ordinary negatives now have independent correctly ordered predicate evidence, while four explicit temporal cases retain PASS. One equal-timestamp investigation remains INCONCLUSIVE. No genuine unexpected FAIL occurred. All 51 comparison records, original definitions, spans and predicate checks are in integrity.json. Original classifications and totals are unchanged.

H. EQL semantic findings

Published query requires FIM rule ID 554, added event and case-sensitive uploads/*.php path, followed by non-null uploads/*.php* URL, joined only by agent ID within 30 minutes. Recovery independently confirms agent equality/mismatch and missing/null joins; missing/null FIM ID, event/path and URL; added-only FIM; case and root restrictions; nested PHP paths and empty stems; URL suffix/query acceptance; unrelated FIM/URL filenames; absent/null/unrelated request rule IDs; different source/destination IPs; POST/status 500 and differing event categories. Exact 1800 seconds and 1799.999 seconds match; 1800.001 and reverse order do not. Equal-time observation is S but remains INCONCLUSIVE without deterministic tie-breaking evidence. No filename, IP, request rule, method, status or event-category constraint is inferred beyond the published EQL. No published query or expectation was adjusted after execution.

I. Regression results

Historical release validation and development-tree validation each passed 14 checks with one optional external-source comparison skipped. All 41 Phase 6 offline/evidence tests passed: 35 previous plus six recovery tests. Publication/rule integrity and all 47 prior index UUID/count/source audits passed after execution. Git diff --check and an explicit tracked/untracked UTF-8 whitespace scan passed. Full command outputs, test counts and preservation observations are retained in regression.json. The historical validator and frozen manifest remain unchanged. Development inventory adds only eight explicit authorized recovery paths.

J. Resource utilisation

2 GiB container limit retained. Minimum sampled host available RAM 1618.25 MiB; maximum sampled swap use 536576 bytes; maximum sampled container memory 74.91%. All sampled container states running, OOMKilled=false, Restarting=false. Initial/final cluster green with empty pending task lists; every scenario passed the health/pending/resource guards. Limits: host available >=512 MiB, swap used <=512 MiB, container memory <90%. Samples do not establish instantaneous peaks. No resource guard triggered.

K. Publication and rule integrity

All 50 frozen publication files match v1.0.0 bytes and all 14 published rule SHA-256 values remain unchanged. WEB-004 SHA-256: b67180707b02050e1333c9c3938506da02a5ada66c9369476e6f662cc94b2c03. All preexisting candidate/evidence files were byte-preserved except the explicitly authorized development inventory extension; integrity.json records before/after digests. Original 6G evidence and 47 prior indices were preserved. Historical validator and manifest are unchanged.

L. Evidence inventory

Evidence directory: docs/verification/phase6/6gr-v1/ containing REPORT.md, README.md, results.json, integrity.json and regression.json. Adapter: tests/phase6gr_engine.py; tests: tests/test_phase6gr_engine.py; corrected definitions: tests/fixtures/phase6/6gr-scenarios.json. Existing 6G mappings and shared Phase 6 harness reused unchanged. results.json retains exact corrected definitions and hashes, published query/hash, pre-execution validation, requests/full responses/status, expected/actual IDs, classifications, exact stored documents, resource observations and index inventories. integrity.json retains original definitions and hashes, scenario comparisons, frozen hashes, all previous file preservation digests, and index audits.

Recovery index: phase6-wcorr-6gr-v1-web004; UUID XxELfFDZTtaTTqzPLODxWQ; 102 documents; dynamic=strict, one primary shard, zero replicas. All writes create-only, sequential, synthetic and loopback scoped. No retries with adjusted expectations occurred.

M. Remaining detection limitations

Agent/time correlation does not establish causality, exploitation, actor identity, PHP execution or HTTP success. Different filenames, unrelated requests, legitimate deployments, URL .php suffixes and failed HTTP outcomes can correlate. Exact case/root and added-only requirements, missing predicate/join fields, delays and reversed/outside timestamps can miss activity. Native Wazuh mapping/population, missing/null timestamp/category, multivalued fields, competing sequences, scheduling, deduplication, scale and real-world efficacy remain unverified. Equal-time ordering remains unresolved. Earlier optional-username and isolated MAL-exclusion limitations remain unchanged.

N. Cumulative historical versus qualified coverage

Historical Phase 6A–6G remains **531 scenarios: 493 PASS, 16 FAIL, 22 INCONCLUSIVE**. Recovery adds a distinct execution record of **51: 50 PASS, 0 FAIL, 1 INCONCLUSIVE**. All execution records combined: **582: 543 PASS, 16 FAIL, 23 INCONCLUSIVE**; these are not unique scenarios. For a unique-scenario coverage view using corrected WEB-004 evidence in place of its defective evidence, the 531 identities have **509 PASS, 0 FAIL, 22 INCONCLUSIVE**. This qualified coverage view does not relabel or erase the 16 historical failures and is not consolidated qualification. All 14 rules have bounded synthetic evidence; this recovery executes only WEB-004.

O. Readiness for consolidated qualification

WEB-004's requested fixture coverage is recovered with zero unexpected deterministic failures. Evidence is available for a separately authorized consolidated assessment, subject to unresolved semantic investigations and detection limitations. Consolidated qualification has not begun. No production readiness, activation approval or unrestricted detection efficacy is claimed.

P. Safety and production non-interference

Only repository work, loopback laboratory Elasticsearch and read-only Docker inspect/stats were used. The sole new engine index is phase6-wcorr-6gr-v1-web004; 47 previous indices remain intact. No production infrastructure, credentials, package installation, Docker/host configuration changes, service restarts, index deletion, live attacks, published EQL/metadata changes, historical release changes, commit, push, tag or publication occurred. No other published rule was rerun. The 2 GiB limit remains unchanged.
