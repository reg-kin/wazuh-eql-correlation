# Phase 6F — WEB-001 and WEB-002 real-engine validation

A. Overall outcome

80 synthetic scenarios: **78 PASS, 0 FAIL, 2 INCONCLUSIVE** on Elasticsearch 8.19.20. Both exact published queries executed successfully. Equal-timestamp cases remain unresolved. This establishes bounded synthetic query behaviour only; no production readiness is claimed. WEB-003 and WEB-004 were not executed.

B. Baseline and preconditions

Branch main; commit 90110451048b1707cdfdecd03ad4a10c7ec2fea2. The starting tree had only the existing untracked Phase 6 development files and no tracked modifications. Before writes: historical release and development validators passed (14 passed, one optional external-source skip each); all 26 prior offline/evidence tests passed. All 50 publication files matched v1.0.0 byte-for-byte, all 14 published rule hashes matched, previous evidence pins passed, and the explicit development inventory passed. All 43 retained indices matched UUIDs, counts and exact indexed sources. Both target names and evidence directory were absent. The endpoint was loopback, version 8.19.20, green with zero pending tasks, and the container limit was 2147483648 bytes. No earlier engine scenarios were rerun. Qualification limitations were carried forward.

C. WEB-001 rule analysis

Intended sequence: reconnaissance alert followed by an exploitation indicator. Stage 1 permits IDs 31151, 31515, 31516; stage 2 permits 31103, 31104, 31105, 31110, 31164, 31166, 31168. Both stages are `any`, require non-null data.srcip.keyword, and share global joins agent.id.keyword and data.srcip.keyword. There are no stage-specific joins, destination-IP joins, URL/method/status/request predicates, optional fields or exclusions. Required query fields are the stage rule IDs and joins; metadata additionally specifies timestamp and type.keyword. Maxspan is 10 minutes from first to last event. Medium severity/risk 55 and historical 10 returned sequences are preserved metadata, not efficacy evidence. Shared proxy/NAT source attribution cannot establish actor identity or successful exploitation.

D. WEB-002 rule analysis

Intended sequence: a web alert followed by added PHP-file FIM. Stage 1 permits IDs 31151, 31103, 31104, 31105. Stage 2 requires ID 554, syscheck.event.keyword == "added", and case-sensitive `like` path `/var/lib/docker/volumes/web_wp_data/_data/wp-content/uploads/*.php`. Both `any` stages join globally on agent.id.keyword only, within 10 minutes. There are no stage-specific joins, source/destination-IP joins, HTTP predicates, optional fields or exclusions. Required query fields are agent/rule IDs plus stage-2 syscheck event/path; metadata also specifies timestamp/type.keyword. High severity/risk 82 and zero historical sequences remain unchanged. Agent/time proximity cannot establish that a web request caused a file creation; legitimate deployment can match.

E. Harness and mapping changes

The Phase 6F suite reuses the established HTTP client, sequential execution, create-only document writes, conflict rejection, fixture validator, resource guards and green-health extension. The shared harness is unchanged. Nine authorized paths were explicitly added to development inventory; unexpected-file rejection remains enabled. Both mappings use dynamic=strict, timestamp=date, native nested Wazuh paths and explicit text/keyword multifields. Each new index has one primary and zero replicas. Each scenario occupies an independent UTC day with an explicit timestamp filter and more than 23 hours between partitions, exceeding maxspan. Fixtures and exact ordered IDs were fixed before execution and checked for changes during the run. No fixture corrections or retrospective expectation changes occurred. There are only two stages, so no separate partial-tie configuration exists.

F. WEB-001 scenario results

37 scenarios: 36 PASS, 0 FAIL, 1 INCONCLUSIVE.

For each row, S denotes the complete ordered IDs `[["web001-<case>-s1", "web001-<case>-s2"]]`; ∅ denotes `[]`; ? denotes predeclared null expectation. Literal IDs and full responses are in results.json.

| Case | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| positive | S | S | PASS |
| alternate-1-31515 | S | S | PASS |
| alternate-1-31516 | S | S | PASS |
| alternate-2-31104 | S | S | PASS |
| alternate-2-31105 | S | S | PASS |
| alternate-2-31110 | S | S | PASS |
| alternate-2-31164 | S | S | PASS |
| alternate-2-31166 | S | S | PASS |
| alternate-2-31168 | S | S | PASS |
| agent-id-missing-1 | ∅ | ∅ | PASS |
| agent-id-null-1 | ∅ | ∅ | PASS |
| rule-id-missing-1 | ∅ | ∅ | PASS |
| rule-id-null-1 | ∅ | ∅ | PASS |
| data-srcip-missing-1 | ∅ | ∅ | PASS |
| data-srcip-null-1 | ∅ | ∅ | PASS |
| wrong-id-1 | ∅ | ∅ | PASS |
| agent-id-missing-2 | ∅ | ∅ | PASS |
| agent-id-null-2 | ∅ | ∅ | PASS |
| rule-id-missing-2 | ∅ | ∅ | PASS |
| rule-id-null-2 | ∅ | ∅ | PASS |
| data-srcip-missing-2 | ∅ | ∅ | PASS |
| data-srcip-null-2 | ∅ | ∅ | PASS |
| wrong-id-2 | ∅ | ∅ | PASS |
| different-agent | ∅ | ∅ | PASS |
| different-source | ∅ | ∅ | PASS |
| different-destination | S | S | PASS |
| inside | S | S | PASS |
| boundary | S | S | PASS |
| outside | ∅ | ∅ | PASS |
| reversed | ∅ | ∅ | PASS |
| equal-timestamps | ? | S | INCONCLUSIVE |
| http-valid | S | S | PASS |
| http-invalid-case-path | S | S | PASS |
| category-different | S | S | PASS |
| proxy-shared-source | S | S | PASS |
| source-text-case | ∅ | ∅ | PASS |
| empty-source | S | S | PASS |

G. WEB-002 scenario results

43 scenarios: 42 PASS, 0 FAIL, 1 INCONCLUSIVE.

For each row, S denotes the complete ordered IDs `[["web002-<case>-s1", "web002-<case>-s2"]]`; ∅ denotes `[]`; ? denotes predeclared null expectation. Literal IDs and full responses are in results.json.

| Case | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| positive | S | S | PASS |
| alternate-1-31103 | S | S | PASS |
| alternate-1-31104 | S | S | PASS |
| alternate-1-31105 | S | S | PASS |
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

H. EQL semantic findings

Both complete positives and every alternative allowed ID matched. Missing/null agent or rule IDs prevented correlation at each stage. WEB-001 also rejected missing/null or different source IPs; an empty but equal source string matched because it is non-null. Case-different source strings failed equality. Different destination IPs had no effect. WEB-002 matched different or absent source addresses. Both matched valid HTTP fields and invalid/unrelated HTTP values because neither query constrains them. Different event categories matched under `any`.

Both queries matched at 599.999 and exactly 600 seconds; 600.001 seconds and reversed stages did not match. Both equal-time observations returned S, but remain INCONCLUSIVE without a specified tiebreaker. WEB-002 rejected missing/null event/path, modified/deleted/uppercase ADDED, alternate roots, uppercase path/extension, query-string suffixes, non-PHP and .php.txt. Its wildcard accepted nested paths and an empty filename stem (.php). These are fixture-scoped observations of the exact expressions.

I. Regression results

Final historical and development validators each passed 14 tests with one optional external-source skip. All 30 offline/evidence tests passed: 26 previous and four new. Phase 6F engine results are the separate 78 PASS/0 FAIL/2 INCONCLUSIVE counts. All rule/publication and prior file/index preservation checks passed. Git diff --check and the explicit tracked/untracked whitespace scan passed. regression.json retains command outputs. An interim evidence assertion ran at 23/80 scenarios and failed on incomplete result count; the completed evidence passed final regression. No engine expectations were changed.

J. Resource utilisation

Minimum sampled host available memory: 1603.10 MiB. Maximum sampled swap used: 536576 bytes. Maximum sampled container memory: 74.74% of 2 GiB. Every sampled container state was running, OOMKilled=false and Restarting=false. Initial/final health was green with zero pending tasks. Guards require at least 512 MiB available host memory, at most 512 MiB swap use, container memory below 90%, green health and no pending tasks. No safeguard triggered. Samples do not establish instantaneous peaks.

K. Rule and publication integrity

All 14 published rule hashes agree with the manifest; all 50 publication files remain byte-identical to v1.0.0, including the historical validator and frozen publication manifest. WEB-001 SHA-256: e354480ff7ddc057025538343fe262992156911ba0012de0ea6c33dd1535d03f. WEB-002 SHA-256: 26f9d26cdfdc0521ae8d0d3c9fa06c5775d046ff9e2426bcff2c043a1c201aff. All preexisting candidate files are unchanged except the nine-entry development inventory extension. Full values and source digests are in integrity.json.

L. Evidence inventory

Directory: docs/verification/phase6/6f-v1/ — REPORT.md, README.md, results.json, integrity.json, regression.json. Results include exact rule hashes, mappings, fixtures, original query text, request parameters, timestamp filters, HTTP status/response, expected/actual ordered IDs, classifications, field capabilities, stored sources and resource samples. Integrity contains target mapping/settings/count responses, source preservation audits and full publication comparisons. Suite: tests/phase6f_engine.py; offline tests: tests/test_phase6f_engine.py; definitions: tests/fixtures/phase6/6f-mappings.json and 6f-scenarios.json. Reproduction commands and conflict constraints are in README.md.

phase6-wcorr-6f-v1-web001: UUID jQTQDh2USUmxmujhXHXvaA; documents 74.

phase6-wcorr-6f-v1-web002: UUID XbwtcA_sSIK9Ib7YiMWfRg; documents 86.

M. Confirmed detection limitations

WEB-001 can link unrelated activity behind shared source addresses; non-null empty strings can correlate. Changing agent/source, missing required joins, reversed times or a span outside 10 minutes prevents a match even when an analyst might regard the activity as related. WEB-002 can link legitimate PHP deployment to unrelated web alerts and cannot attribute a file to an HTTP client. Exact case, event value and volume path constrain coverage; alternative deployment roots and uppercase extensions fail. Nested paths are included by the wildcard. Neither query validates HTTP URL, method, status, request, destination, attack success or causality.

Unverified: native Wazuh mapping/population, missing/null timestamp or category, multivalued fields, competing sequences, ingestion delay, real-world efficacy, scheduling/deduplication and scale. Timestamp ties remain unresolved. Prior PRIV optional-username and isolated MAL-exclusion coverage limitations remain unchanged.

N. Cumulative Phase 6 progress

| Phase | Scenarios | PASS | FAIL | INCONCLUSIVE |
| --- | --- | --- | --- | --- |
| 6A | 35 | 31 | 0 | 4 |
| 6B | 61 | 59 | 0 | 2 |
| 6C | 75 | 73 | 0 | 2 |
| 6D | 104 | 100 | 0 | 4 |
| 6E | 82 | 76 | 0 | 6 |
| 6F | 80 | 78 | 0 | 2 |
| Total | 437 | 417 | 0 | 20 |

Twelve of 14 rules now have bounded synthetic real-engine evidence. All prior classifications are preserved. Offline test assertions are not additional engine scenarios.

O. Readiness for WEB-003 and WEB-004

The retained framework can support a separately scoped phase after exact-query inspection, independent predeclared scenarios, dedicated namespaces and fresh mandatory preflight. WEB-003 and WEB-004 remain unexecuted. This report does not establish production readiness or authorize activation.

P. Safety and production non-interference

Access was limited to local repository files, loopback laboratory Elasticsearch and read-only Docker inspection/stats. Synthetic writes were confined to the two authorized new indices; all 43 previous indices retain exact UUIDs/counts/sources. No production access, credential retrieval, package installation, Docker/host configuration change, firewall/kernel change, service restart, index deletion, live attack, published-rule/metadata edit, historical artifact change, commit, push, tag or publication occurred. Phase 6A–6E evidence remains intact.
