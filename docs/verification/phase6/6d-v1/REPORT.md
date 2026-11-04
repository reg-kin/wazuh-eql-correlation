============================================================
PHASE 6D — REAL-ENGINE VALIDATION REPORT
============================================================

A. OVERALL OUTCOME
PARTIAL — 104 scenarios: 100 PASS, 0 FAIL, 4 INCONCLUSIVE. Both exact published rules parse and execute on Elasticsearch 8.19.20. Four timestamp-tie investigations remain unresolved. No production-readiness claim.

B. BASELINE AND PRECONDITIONS
Branch main; commit 90110451048b1707cdfdecd03ad4a10c7ec2fea2. Initial tracked tree unchanged; prior Phase 6 development files were untracked and matched the explicit inventory. Historical and development validators passed (14 pass, one optional external-source skip each); all 16 existing offline/qualification/evidence tests passed. Reviewed prior reports, qualification, harnesses, fixtures, mappings, tests and integrity/regression evidence. Prior total: 171 scenarios, 163 PASS, 8 INCONCLUSIVE, 0 FAIL. No prior engine scenario rerun.
All 50 publication files match the local v1.0.0 tag byte-for-byte, all 14 rule hashes agree, prior pinned evidence agrees. All 39 retained index UUIDs, document counts and exact indexed sources verified read-only before writes and again afterward. Neither target index existed. Baseline audit rejects unexpected/missing indices. Elasticsearch 8.19.20, loopback endpoint, green health, zero pending tasks; 2 GiB container limit confirmed. Storage sizes are observational and may change through background merges; UUID/count/source identity is authoritative.

C. SSH-003 RULE ANALYSIS
Objective: SSH authentication followed by realtime modification of sensitive Linux access-control files. Exactly two ordered any stages: rule 5715; then rule 550 or 554, mode exactly realtime and an allowed sensitive path. Global join agent.id.keyword only, no stage-specific or optional joins. Predicate fields: rule.id.keyword, syscheck.mode.keyword, syscheck.path.keyword, with populated agent join at both stages. Timestamp orders events; request category field type.keyword is configured, but any stages impose no category predicate. maxspan=30m, first to last.
Allowed paths: exactly /etc/passwd, /etc/shadow, /etc/group, /etc/gshadow, /etc/sudoers; or like /etc/sudoers.d/*; or like /home/*/.ssh/authorized_keys; or exactly /root/.ssh/authorized_keys. No command predicate, explicit exclusion, username, process or SSH-session join. Scheduled FIM is excluded by the positive realtime condition. Agent/time proximity cannot establish the actor responsible.

D. SSH-004 RULE ANALYSIS
Objective: SSH authentication, sudo alert, then sensitive file modification. Exactly three ordered any stages: 5715; 5402 or 5407; 550 or 554 with the identical path alternatives listed in C. Global join agent.id.keyword only; no stage-specific or optional joins. Predicate fields: rule.id.keyword and final-stage syscheck.path.keyword plus agent join at all stages. Timestamp/category configuration as above. maxspan=30m measures first to last, not each adjacent gap. No realtime FIM restriction, command condition, root-target requirement, explicit exclusion or user/session/process join. All companion documentation inspected; no alternative expression substituted. Scheduled FIM and unrelated administrative sudo activity can correlate.

E. HARNESS AND MAPPING CHANGES
Added phase6d_engine.py suite configuration, test_phase6d_engine.py and 6d fixture/mapping JSON under tests. Reused phase6_engine.run, Client, resources, create-only writes, conflict refusal and 6B/6C contract validation. The adapter relabels suite keys only for existing two-/three-stage fixture validation. GreenClient strengthens the shared health check to green throughout; no new HTTP framework. Preflight audits historical publication, prior pins, 39 exact index identities/sources, engine version and resources before any write.
Two strict mappings explicitly map date timestamp and keyword multifields on type, agent.id, rule.id, syscheck.path/mode and data.srcuser/dstuser/command. Data fields support absence-of-predicate tests; they do not add joins. One primary and zero replicas. Retrieved live mappings equal definitions. Each scenario uses a unique UTC day and an explicit range filter; >23-hour inter-partition gaps also exceed maxspan. Stored sources and field capabilities verified for every scenario.
Offline validation caught underscores in path-derived IDs. IDs alone were corrected before engine writes; original fixture, hashes and correction retained in integrity.json. No event source, expected classification or query changed during execution. No failing query rewritten and no scenario rerun. Extended nine explicit development inventory paths; narrow exact synthetic home-path allowances in three Phase 6D files retain all other content and unexpected-file checks.

F. SSH-003 SCENARIO RESULTS
43 scenarios: 42 PASS, 0 FAIL, 1 INCONCLUSIVE. Each row uses its full scenario ID as prefix. S = the complete ordered IDs [<scenario>-s1, <scenario>-s2]; [] = no sequences; ? = no predeclared deterministic outcome. Full literal IDs and responses in results.json. All HTTP statuses 200; responses complete.

| Scenario | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| ssh003-positive | S | S | PASS |
| ssh003-alternate-fim-id | S | S | PASS |
| ssh003-wrong-id-1 | [] | [] | PASS |
| ssh003-different-agent-1 | [] | [] | PASS |
| ssh003-agent-id-missing-1 | [] | [] | PASS |
| ssh003-agent-id-null-1 | [] | [] | PASS |
| ssh003-rule-id-missing-1 | [] | [] | PASS |
| ssh003-rule-id-null-1 | [] | [] | PASS |
| ssh003-wrong-id-2 | [] | [] | PASS |
| ssh003-different-agent-2 | [] | [] | PASS |
| ssh003-agent-id-missing-2 | [] | [] | PASS |
| ssh003-agent-id-null-2 | [] | [] | PASS |
| ssh003-rule-id-missing-2 | [] | [] | PASS |
| ssh003-rule-id-null-2 | [] | [] | PASS |
| ssh003-reversed | [] | [] | PASS |
| ssh003-inside | S | S | PASS |
| ssh003-boundary | S | S | PASS |
| ssh003-outside | [] | [] | PASS |
| ssh003-equal-timestamps | ? | S | INCONCLUSIVE |
| ssh003-path-etc-shadow | S | S | PASS |
| ssh003-path-etc-group | S | S | PASS |
| ssh003-path-etc-gshadow | S | S | PASS |
| ssh003-path-etc-sudoers | S | S | PASS |
| ssh003-path-etc-sudoersd-lab | S | S | PASS |
| ssh003-path-home-lab-ssh-authorized-keys | S | S | PASS |
| ssh003-path-root-ssh-authorized-keys | S | S | PASS |
| ssh003-path-unrelated | [] | [] | PASS |
| ssh003-path-suffix | [] | [] | PASS |
| ssh003-path-case | [] | [] | PASS |
| ssh003-path-sudoers-no-slash | [] | [] | PASS |
| ssh003-path-sudoers-empty | S | S | PASS |
| ssh003-path-sudoers-nested | S | S | PASS |
| ssh003-path-home-nested | S | S | PASS |
| ssh003-path-home-empty | S | S | PASS |
| ssh003-path-keys-suffix | [] | [] | PASS |
| ssh003-path-other-home | [] | [] | PASS |
| ssh003-path-missing | [] | [] | PASS |
| ssh003-path-null | [] | [] | PASS |
| ssh003-mode-scheduled | [] | [] | PASS |
| ssh003-mode-case | [] | [] | PASS |
| ssh003-mode-missing | [] | [] | PASS |
| ssh003-mode-null | [] | [] | PASS |
| ssh003-login-user-missing | S | S | PASS |

G. SSH-004 SCENARIO RESULTS
61 scenarios: 58 PASS, 0 FAIL, 3 INCONCLUSIVE. Each row uses its full scenario ID as prefix. S = the complete ordered IDs [<scenario>-s1, <scenario>-s2, <scenario>-s3]; [] = no sequences; ? = no predeclared deterministic outcome. Full literal IDs and responses in results.json. All HTTP statuses 200; responses complete.

| Scenario | Expected | Actual | Outcome |
| --- | --- | --- | --- |
| ssh004-positive | S | S | PASS |
| ssh004-alternate-fim-id | S | S | PASS |
| ssh004-alternate-sudo-id | S | S | PASS |
| ssh004-wrong-id-1 | [] | [] | PASS |
| ssh004-different-agent-1 | [] | [] | PASS |
| ssh004-agent-id-missing-1 | [] | [] | PASS |
| ssh004-agent-id-null-1 | [] | [] | PASS |
| ssh004-rule-id-missing-1 | [] | [] | PASS |
| ssh004-rule-id-null-1 | [] | [] | PASS |
| ssh004-wrong-id-2 | [] | [] | PASS |
| ssh004-different-agent-2 | [] | [] | PASS |
| ssh004-agent-id-missing-2 | [] | [] | PASS |
| ssh004-agent-id-null-2 | [] | [] | PASS |
| ssh004-rule-id-missing-2 | [] | [] | PASS |
| ssh004-rule-id-null-2 | [] | [] | PASS |
| ssh004-wrong-id-3 | [] | [] | PASS |
| ssh004-different-agent-3 | [] | [] | PASS |
| ssh004-agent-id-missing-3 | [] | [] | PASS |
| ssh004-agent-id-null-3 | [] | [] | PASS |
| ssh004-rule-id-missing-3 | [] | [] | PASS |
| ssh004-rule-id-null-3 | [] | [] | PASS |
| ssh004-reversed | [] | [] | PASS |
| ssh004-fim-before-sudo | [] | [] | PASS |
| ssh004-sudo-before-login | [] | [] | PASS |
| ssh004-inside | S | S | PASS |
| ssh004-boundary | S | S | PASS |
| ssh004-outside | [] | [] | PASS |
| ssh004-adjacent-within-total-outside | [] | [] | PASS |
| ssh004-equal-timestamps | ? | S | INCONCLUSIVE |
| ssh004-equal-login-sudo | ? | S | INCONCLUSIVE |
| ssh004-equal-sudo-fim | ? | S | INCONCLUSIVE |
| ssh004-path-etc-shadow | S | S | PASS |
| ssh004-path-etc-group | S | S | PASS |
| ssh004-path-etc-gshadow | S | S | PASS |
| ssh004-path-etc-sudoers | S | S | PASS |
| ssh004-path-etc-sudoersd-lab | S | S | PASS |
| ssh004-path-home-lab-ssh-authorized-keys | S | S | PASS |
| ssh004-path-root-ssh-authorized-keys | S | S | PASS |
| ssh004-path-unrelated | [] | [] | PASS |
| ssh004-path-suffix | [] | [] | PASS |
| ssh004-path-case | [] | [] | PASS |
| ssh004-path-sudoers-no-slash | [] | [] | PASS |
| ssh004-path-sudoers-empty | S | S | PASS |
| ssh004-path-sudoers-nested | S | S | PASS |
| ssh004-path-home-nested | S | S | PASS |
| ssh004-path-home-empty | S | S | PASS |
| ssh004-path-keys-suffix | [] | [] | PASS |
| ssh004-path-other-home | [] | [] | PASS |
| ssh004-path-missing | [] | [] | PASS |
| ssh004-path-null | [] | [] | PASS |
| ssh004-mode-scheduled | S | S | PASS |
| ssh004-mode-case | S | S | PASS |
| ssh004-mode-missing | S | S | PASS |
| ssh004-mode-null | S | S | PASS |
| ssh004-arbitrary-command | S | S | PASS |
| ssh004-command-missing | S | S | PASS |
| ssh004-command-null | S | S | PASS |
| ssh004-non-root | S | S | PASS |
| ssh004-dstuser-missing | S | S | PASS |
| ssh004-dstuser-null | S | S | PASS |
| ssh004-unrelated-users | S | S | PASS |

H. EQL SEMANTIC FINDINGS
Missing/null agent and rule IDs prevent correlation at every stage; differing agents fail. Missing/null path fails. SSH-003 requires exact lowercase realtime; scheduled, case-changed, missing and null mode fail. SSH-004 matches all four mode variants because no mode predicate exists. Every path alternative and rule-ID alternative tested successfully. Path case, disallowed directory, backup suffix and missing sudoers.d slash fail. Wildcards admit nested paths, an empty sudoers.d remainder and an empty home component.
Reverse order fails. SSH-004 also fails FIM-before-sudo and sudo-before-login. 1799s and exactly 1800s first-to-last match; 1801s does not. SSH-004 at 0/1000/2000s fails despite both adjacent gaps fitting. Positive three-stage ordered IDs and first-to-last spans independently checked offline. Equal timestamps yielded the observed S rows above; three-stage all-equal and individual tied-stage cases remain INCONCLUSIVE without a tiebreaker guarantee.
SSH-004 matches arbitrary/missing/null commands, non-root/missing/null targets and different users. SSH-003 matches without login username. These are agent/time correlations; no other join key exists to mismatch. No optional-field syntax or exclusion branch exists to investigate in these two published queries.

I. REGRESSION RESULTS
Historical release: 15 tests, 14 pass, one optional external-source skip. Development tree: same. Phase 6 offline suite: 21 tests pass (6A four, qualification four, 6B five, 6C three, 6D five). Git diff --check and whitespace checks over every candidate including untracked files pass. Unexpected-file rejection and synthetic-path exception boundaries verified.
An initial evidence-recording check rejected copied Phase 6B-only synthetic address literals in the new integrity file. Prior source equality is now recorded with canonical hashes rather than duplicated raw sources; no address allowance was broadened. The initial failed regression and correction are preserved in regression.json. Historical validator and manifest unchanged. Prior evidence byte-for-byte preserved. Full command outputs and return codes retained in regression.json; fixture defect and correction retained in integrity.json. No previous engine scenarios executed.

J. RESOURCE UTILISATION
Host RAM 3.777 GiB; minimum sampled available 1618.9 MiB. Maximum sampled swap use 536576 bytes. Maximum sampled container memory 74.28% of 2 GiB. Initial/final health green; zero pending tasks. All sampled container states running, OOMKilled=false, Restarting=false. No safeguard triggered.
Guards: >=512 MiB available, <=512 MiB swap use, <90% container memory, green health and no pending tasks. Sequential bounded execution; 269 synthetic documents across two new primary shards. Samples do not measure continuous instantaneous peaks.

K. RULE INTEGRITY
All 14 expected and actual SHA-256 values agree; publication bytes remain identical to v1.0.0.

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
docs/verification/phase6/6d-v1/ contains REPORT.md, README.md, results.json, integrity.json and regression.json. Exact query hashes, mappings, fixtures, requests/responses, sequence IDs, index identities/counts, classifications, resources and reproduction instructions retained. New source files are the suite, offline tests and two fixture JSON files. All earlier evidence preserved.

| Index | UUID | Documents |
| --- | --- | --- |
| phase6-wcorr-6d-v1-ssh003 | -q2fftW4S5y_wgjNLsQJzQ | 86 |
| phase6-wcorr-6d-v1-ssh004 | YSFatdQvR7-EseYNeGJSfQ | 183 |

M. CONFIRMED DETECTION LIMITATIONS
Agent/time association permits unrelated users, sessions and routine administration. SSH-004 imposes no command, root-user or realtime FIM condition and may associate delayed scheduled observations. SSH-003 omits scheduled/non-realtime FIM, missing mode and different-case values. Both omit paths outside the exact case-sensitive allowlist, missing joins/IDs and reordered or late sequences. Broad path wildcards accept nested and empty components. These synthetic matches do not prove compromise, actor continuity, process attribution or causal file modification.
Unverified: native Wazuh mappings/field population, missing/null timestamps/category, multivalued fields, competing sequence selection, ingestion delays, query scheduling/deduplication, real-world efficacy and scale. Equal-time ordering remains unresolved. Earlier optional PRIV username and isolated MAL exclusion limitations remain.

N. CUMULATIVE PHASE 6 PROGRESS
6A: 35 scenarios, 31 PASS, 4 INCONCLUSIVE, 0 FAIL. 6B: 61, 59 PASS, 2 INCONCLUSIVE, 0 FAIL. 6C: 75, 73 PASS, 2 INCONCLUSIVE, 0 FAIL. 6D: 104, 100 PASS, 4 INCONCLUSIVE, 0 FAIL. Cumulative: 275 scenarios, 263 PASS, 12 INCONCLUSIVE, 0 FAIL. Eight of 14 rules now have synthetic engine evidence: PRIV-001, MAL-001, SSH-001 through SSH-004, PERS-001 and PERS-002. Six remain untested. Offline qualification assertions are not extra engine scenarios.

O. NEXT TWO RECOMMENDED RULES
WCORR-SSH-005 and WCORR-EVAS-001 for a separately authorized next phase. They remain unexecuted here; inspect their published expressions before designing fixtures.

P. SAFETY AND PRODUCTION NON-INTERFERENCE
Only local repository work, loopback laboratory Elasticsearch and read-only Docker inspection/stats used. Writes confined to the two named new 6D synthetic indices. All 39 earlier indices verified unchanged in identity/count/source. No production access, credential retrieval, package installation, live attacks, configuration changes, service restart, index deletion, published rule/metadata/manifest edits, commit, push, tag or publication. No other rule executed. This validation does not establish production readiness.
