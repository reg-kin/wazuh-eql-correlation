============================================================
PHASE 6C — REAL-ENGINE VALIDATION REPORT
============================================================

A. OVERALL OUTCOME
PARTIAL — synthetic execution completed: 73 PASS, 0 FAIL, 2 INCONCLUSIVE. Equal-timestamp investigations remain inconclusive. No production-readiness claim.

B. BASELINE
Branch main; commit 90110451048b1707cdfdecd03ad4a10c7ec2fea2. Initial Git state contained the existing untracked Phase 6 framework and evidence; no tracked changes. Historical release, development and 13 existing offline/qualification/evidence tests passed before work. Every pinned prior file hash agrees. All 37 prior index UUIDs, counts and exact document IDs/sources verified read-only. Two 6B storage sizes drifted since retained evidence (73.6kb to 74.4kb; 85.8kb to 37.2kb); immutable identity and content agree. Elasticsearch 8.19.20 on loopback; green, one node, zero pending tasks; container limit 2 GiB, running, no OOM. Neither 6C target index existed.

C. RULE ANALYSIS
SSH-002: objective is SSH authentication followed by sensitive sudo activity. Exactly two ordered stages: rule 5715, then rule 5402 or 5407 with data.dstuser.keyword == "root" and data.command.keyword matching one of *useradd*, *usermod*, *passwd*, *visudo*, *systemctl disable*, *systemctl stop*, *crontab*, *chmod*, *chown*. Global join is agent.id.keyword; no stage-specific joins, optional-field syntax or exclusions. Window 15m from first to last event. Predicate fields are rule.id.keyword at both stages and command/dstuser at stage two; agent join values must be present. Login username is not required. timestamp is the ordering field; type.keyword is configured as category field, but both stages use any and impose no category predicate. Metadata declares both timestamp and category fields; their missing/null behaviour was not investigated here. Published EQL, rather than the stricter alternative displayed in metadata, was executed.
PERS-002: objective is SSH login followed by service-unit modification and service-failure alert. Exactly three ordered stages: 5715; 550 or 554 with syscheck.path.keyword like /etc/systemd/system/*.service OR /usr/lib/systemd/system/*.service OR /lib/systemd/system/*.service; then 40704. Global join agent.id.keyword only; no stage-specific joins, optional-field syntax or exclusions. Window 30m first to last. Required predicate fields are rule IDs at every stage and path at stage two. timestamp orders; category is configured but no category predicate is present. No service-name, username, session or process join.

D. HARNESS CHANGES
Added tests/phase6c_engine.py, tests/test_phase6c_engine.py, tests/fixtures/phase6/6c-mappings.json and tests/fixtures/phase6/6c-scenarios.json. Extended only the explicit inventory in tests/validate_development.py. Reused phase6_engine.run and phase6b_engine.validate_fixtures; no independent HTTP client. Added five evidence files in docs/verification/phase6/6c-v1/. Existing harnesses, rules, metadata, manifest and historical validator remain byte-identical. Loopback pinning, bounded 15-second requests, strict write namespace, create-only IDs, conflict refusal, sequential execution, resources and exact ID/source checks retained.

E. MAPPINGS
Two explicit dynamic:strict mappings, date timestamp, text fields with keyword multifields for type, agent.id, rule.id, data.srcuser/dstuser/command, syscheck.path and service.name. The last fields permit explicit omission tests; they do not add rule predicates. No dynamic mapping or keyword ignore_above truncation. Retrieved _mapping equals each fixture definition. Per-scenario field capabilities confirm every referenced keyword field. Each index has one shard and zero replicas. Exact definitions and live verification are retained in results.json and integrity.json.

F. SSH-002 RESULTS
Each row uses its full scenario ID as prefix. S means the exact ordered IDs `[<scenario>-s1, <scenario>-s2]`; [] means no sequences. ? means no deterministic expectation was predeclared. All requests returned HTTP 200, complete responses.

| Scenario | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| ssh-positive | S | S | PASS |
| ssh-alternate-id | S | S | PASS |
| ssh-wrong-id-1 | [] | [] | PASS |
| ssh-different-agent-1 | [] | [] | PASS |
| ssh-agent-missing-1 | [] | [] | PASS |
| ssh-agent-null-1 | [] | [] | PASS |
| ssh-rule-missing-1 | [] | [] | PASS |
| ssh-rule-null-1 | [] | [] | PASS |
| ssh-wrong-id-2 | [] | [] | PASS |
| ssh-different-agent-2 | [] | [] | PASS |
| ssh-agent-missing-2 | [] | [] | PASS |
| ssh-agent-null-2 | [] | [] | PASS |
| ssh-rule-missing-2 | [] | [] | PASS |
| ssh-rule-null-2 | [] | [] | PASS |
| ssh-reversed | [] | [] | PASS |
| ssh-inside | S | S | PASS |
| ssh-boundary | S | S | PASS |
| ssh-outside | [] | [] | PASS |
| ssh-equal-timestamps | ? | S | INCONCLUSIVE |
| ssh-command-usermod | S | S | PASS |
| ssh-command-passwd | S | S | PASS |
| ssh-command-visudo | S | S | PASS |
| ssh-command-systemctl-disable | S | S | PASS |
| ssh-command-systemctl-stop | S | S | PASS |
| ssh-command-crontab | S | S | PASS |
| ssh-command-chmod | S | S | PASS |
| ssh-command-chown | S | S | PASS |
| ssh-dstuser-missing | [] | [] | PASS |
| ssh-dstuser-null | [] | [] | PASS |
| ssh-command-missing | [] | [] | PASS |
| ssh-command-null | [] | [] | PASS |
| ssh-non-root | [] | [] | PASS |
| ssh-root-case | [] | [] | PASS |
| ssh-invalid-command | [] | [] | PASS |
| ssh-command-case | [] | [] | PASS |
| ssh-substring | S | S | PASS |
| ssh-spacing | [] | [] | PASS |
| ssh-unjoined-users | S | S | PASS |
| ssh-login-user-null | S | S | PASS |

G. PERS-002 RESULTS
Each row uses its full scenario ID as prefix. S means the exact ordered IDs `[<scenario>-s1, <scenario>-s2, <scenario>-s3]`; [] means no sequences. ? means no deterministic expectation was predeclared. All requests returned HTTP 200, complete responses.

| Scenario | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| pers-positive | S | S | PASS |
| pers-alternate-id | S | S | PASS |
| pers-wrong-id-1 | [] | [] | PASS |
| pers-different-agent-1 | [] | [] | PASS |
| pers-agent-missing-1 | [] | [] | PASS |
| pers-agent-null-1 | [] | [] | PASS |
| pers-rule-missing-1 | [] | [] | PASS |
| pers-rule-null-1 | [] | [] | PASS |
| pers-wrong-id-2 | [] | [] | PASS |
| pers-different-agent-2 | [] | [] | PASS |
| pers-agent-missing-2 | [] | [] | PASS |
| pers-agent-null-2 | [] | [] | PASS |
| pers-rule-missing-2 | [] | [] | PASS |
| pers-rule-null-2 | [] | [] | PASS |
| pers-wrong-id-3 | [] | [] | PASS |
| pers-different-agent-3 | [] | [] | PASS |
| pers-agent-missing-3 | [] | [] | PASS |
| pers-agent-null-3 | [] | [] | PASS |
| pers-rule-missing-3 | [] | [] | PASS |
| pers-rule-null-3 | [] | [] | PASS |
| pers-reversed | [] | [] | PASS |
| pers-failure-before-fim | [] | [] | PASS |
| pers-inside | S | S | PASS |
| pers-boundary | S | S | PASS |
| pers-outside | [] | [] | PASS |
| pers-equal-timestamps | ? | S | INCONCLUSIVE |
| pers-usr-lib | S | S | PASS |
| pers-lib | S | S | PASS |
| pers-wrong-directory | [] | [] | PASS |
| pers-wrong-suffix | [] | [] | PASS |
| pers-path-case | [] | [] | PASS |
| pers-nested | S | S | PASS |
| pers-path-missing | [] | [] | PASS |
| pers-path-null | [] | [] | PASS |
| pers-unrelated-service | S | S | PASS |
| pers-empty-unit-basename | S | S | PASS |

H. SEMANTIC FINDINGS
Missing/null agent IDs and rule IDs prevent correlation at every tested stage. Different agents do not join. Stage-two missing/null target user, command or path prevents matches as applicable. Reverse order fails; PERS failure before FIM fails. First-to-last windows match at 899/900 seconds for SSH and 1799/1800 for PERS; 901/1801 seconds do not match. Both exact-boundary expectations were declared before execution. All nine command alternatives, both sudo IDs, both FIM IDs and all three service directories match. Case changes, invalid commands, doubled spaces, wrong directory/suffix fail as declared. Substring command text, nested unit paths and empty unit basename match. Different users and unrelated service names still match because those joins are absent. Equal timestamps are observational only; see rows above and retained responses. No expectation changed and no failing scenario was rerun.

I. REGRESSION RESULTS
Historical release: 15 tests, 14 pass and one optional external-source skip. Development: same. Existing 6A offline: four pass; 6A qualification: four pass; 6B offline/evidence: five pass. New 6C: three pass after execution. Full command outputs and whitespace/preservation checks are recorded in regression.json. Historical validator and frozen publication manifest are preserved. No 6A or 6B engine execution was repeated.

J. RESOURCE UTILISATION
Observed minimum host available memory 1631.3 MiB; maximum container memory 73.98% of 2 GiB. Maximum observed swap consumption was 536576 bytes (about 0.51 MiB). Every recorded container state running, not restarting, OOMKilled=false. Initial/final cluster green; per-scenario health guards and zero-pending-task checks passed. Guards stop below 512 MiB available, above 512 MiB swap, at 90% container usage, unhealthy cluster, pending tasks or OOM/restart. Host has approximately 3.8 GiB RAM. No restart or reconfiguration. Raw observations retained per scenario.

K. RULE INTEGRITY
All 14 expected and actual SHA-256 values agree:

| Rule | SHA-256 |
| --- | --- |
| WCORR-SSH-001 | 3dfada3fd2d79dc3952022922fa737e7d5877dec2802da142244ea3cea4beb91 |
| WCORR-SSH-002 | 6fe2f2fecc882435f94e251e3c18dc36506b95d29594ef627e2e4a77e7501c12 |
| WCORR-SSH-003 | b1b405f98bf6175e816bbd4432ac7b449955e2dc214c506ec75dcb8553321776 |
| WCORR-SSH-004 | cf06bb2906a157801c277065d64ca2d843432427ce408c1df614cebcfdd64a6f |
| WCORR-SSH-005 | d2e1ef87e5bf9f168ac0b64c55f27e2098aa0ae3311a1dfb46b11f20eec3b80c |
| WCORR-WEB-001 | e354480ff7ddc057025538343fe262992156911ba0012de0ea6c33dd1535d03f |
| WCORR-WEB-002 | 26f9d26cdfdc0521ae8d0d3c9fa06c5775d046ff9e2426bcff2c043a1c201aff |
| WCORR-WEB-003 | b81834c7c28348dca9a4be421a4c251f572f593de82001f041a1b456e24af428 |
| WCORR-WEB-004 | b67180707b02050e1333c9c3938506da02a5ada66c9369476e6f662cc94b2c03 |
| WCORR-PRIV-001 | 60908232bf5d32c872bdfaa87bbb1177cc7be8fd867d815918ee0483c7484bc2 |
| WCORR-PERS-001 | fa68921dc320770b8205616aff38b10d84c95518b4a85673d248a8803d9effc9 |
| WCORR-PERS-002 | 3523502f6e1d1b107bd34b9c0d5f00b159972c065552c1f84ce160e4f7d34a3c |
| WCORR-EVAS-001 | 63ab3dc6183ab8c0201288e6a7b5278bdc258f9c3c3240e40e4ff3d36d481f4f |
| WCORR-MAL-001 | f2764d7b25baccfcdf0788abcbee70b12e0bc47ff83a3207a8e3a7b8e30d1d6a |

L. EVIDENCE INVENTORY
Five new retained files: REPORT.md (this report), README.md (reproduction), results.json (exact fixtures/mappings, requests, HTTP response status/body, expected/actual IDs, classifications, resources and inventories), integrity.json (prior file hashes, rule hashes, prior index/source audit and target mapping/settings/counts), regression.json (commands and outputs). No previous report overwritten.

| Index | UUID | Documents |
| --- | --- | --- |
| phase6-wcorr-6c-v1-ssh | obEzIPLYQfWUAghMZo-_iw | 78 |
| phase6-wcorr-6c-v1-pers | F4TbEIjmQq2vDdUbUHTEPg | 108 |

M. DETECTION LIMITATIONS
Confirmed: agent-only attribution permits unrelated users/services and routine administration; SSH substring matches do not prove command execution (echo useradd matches). Case and whitespace variations can miss commands; alternate shells/commands outside the nine patterns are uncovered. PERS wildcard spans nested paths and accepts .service with no basename; unit modification followed by any matching failure does not establish causality. PERS-002 does not exclude scheduled FIM; neither query excludes legitimate administration or unrelated sessions. No additional correlation key exists to mismatch beyond agent ID.
Unverified: native Wazuh mappings/telemetry population, missing/null timestamp/category behaviour, multivalued fields, event ties with explicit tiebreakers, multiple competing sequence selection, production scheduling/window coverage, scale and efficacy. Small fixtures contain one candidate chain per unique UTC day; query range filters prevent cross-scenario correlations. Equal-timestamp observations do not establish a deterministic ordering guarantee. Prior PRIV optional-user and MAL isolated-exclusion limitations remain.

N. CUMULATIVE PHASE 6 PROGRESS
6A: 35 scenarios, 31 PASS, four INCONCLUSIVE, zero FAIL. 6B: 61 scenarios, 59 PASS, two INCONCLUSIVE, zero FAIL. 6C: 75 scenarios, 73 PASS, 2 INCONCLUSIVE, 0 FAIL. Cumulative: 171 scenarios, 163 PASS, 8 INCONCLUSIVE, 0 FAIL. Six of 14 published rules tested: PRIV-001, MAL-001, SSH-001, PERS-001, SSH-002 and PERS-002. Qualification assertions are not extra engine scenarios. Eight rules remain untested.

O. NEXT RECOMMENDATION
Validate WCORR-SSH-003 and WCORR-SSH-004 next in a separately authorized phase, focusing on realtime FIM predicates versus agent/time-only three-stage attribution. Neither was executed here.

P. SAFETY CONFIRMATION
Only local repository changes, loopback Elasticsearch laboratory access and read-only Docker inspections occurred. Writes were confined to the two new 6C synthetic indices. No production access, credentials, live attacks, packages, Docker/firewall/kernel/service changes, index deletion, branch change, commit, push, tag or publication. The remaining eight rules were not executed. Prior evidence and index identities/counts/content preserved; baseline storage-size drift disclosed above. This synthetic validation does not establish production readiness.
