============================================================
PHASE 6A — REAL-ENGINE EQL VALIDATION REPORT
============================================================

A. OVERALL OUTCOME
PARTIAL. Both exact published queries parse and execute on Elasticsearch 8.19.20. All 31 predeclared sequence/absence assertions PASS; four semantic investigations remain labelled INCONCLUSIVE because no result was predeclared. No engine scenario failed. Static publication inventory fails because Phase 6 adds files outside the frozen Phase 4 manifest. This is not an unqualified repository-wide PASS.

B. ENGINE BASELINE
Version: 8.19.20; cluster: docker-cluster; UUID: Nw-VMeIvT5qL_77Vk2EaWw; node: 23a801c61d6a.
Endpoint: http://127.0.0.1:19200. Initial/final health: green/green. Initial indices: 0; retained final indices: 35.
Execution UTC: 2026-11-04T09:34:19.277405+00:00. Host total RAM: 4055916544 bytes; container limit: 2147483648 bytes.
Infrastructure was not reprovisioned. No service was restarted.

C. REPOSITORY BASELINE
Branch: main; commit: 90110451048b1707cdfdecd03ad4a10c7ec2fea2. Working tree was clean before implementation.
No pre-existing fixtures or separate real-engine Python harness were found. Existing Python tests use standard-library unittest in tests/validate_repository.py. Rule metadata is in companion Markdown, tests/rule-manifest.json and the frozen docs/verification/PUBLICATION_MANIFEST.json. Existing verification documentation is in docs/verification/.
rules/malware/WCORR-MAL-001.eql: f2764d7b25baccfcdf0788abcbee70b12e0bc47ff83a3207a8e3a7b8e30d1d6a
rules/privilege-escalation/WCORR-PRIV-001.eql: 60908232bf5d32c872bdfaa87bbb1177cc7be8fd867d815918ee0483c7484bc2

D. HARNESS IMPLEMENTATION
Created tests/phase6_engine.py; tests/test_phase6_engine.py; tests/fixtures/phase6/mappings.json; tests/fixtures/phase6/scenarios.json; and docs/verification/phase6/ evidence/documentation.
Standard-library urllib HTTP, fixed 15-second timeouts, no dependencies, no credentials, proxy bypass, redirect rejection, checked/pinned loopback endpoints by default, explicit alternative-origin authorization flag. Deterministic scenario IDs, timestamps and per-scenario index names. Conflicts abort before any writes. Existing evidence is never overwritten. Indices are retained.
Queries are read from the original EQL paths for each execution and hashed again. POST /<index>/_eql/search uses JSON-body timestamp_field=timestamp, event_category_field=type.keyword, size=10. Every observed EQL HTTP status is 200. Index creation, document creation, refresh and exact stored-source verification succeeded for every scenario.
35 indices, 87 synthetic documents total; each index has one primary shard, zero replicas and two or three documents. Each result includes response, field capabilities and indexed sources for diagnosis.

E. ELASTICSEARCH MAPPINGS
Exact mappings follow; both use dynamic=strict and _meta ownership marker. All .keyword fields are explicit keyword multifields under text base fields. timestamp is date. This mapping works without changing any EQL.
priv:
```json
{
  "dynamic": "strict",
  "_meta": {
    "owner": "wcorr-phase6-synthetic",
    "schema": 1
  },
  "properties": {
    "timestamp": {
      "type": "date"
    },
    "type": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "agent": {
      "properties": {
        "id": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    },
    "rule": {
      "properties": {
        "id": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    },
    "data": {
      "properties": {
        "dstuser": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        },
        "srcuser": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        },
        "command": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }
}
```
mal:
```json
{
  "dynamic": "strict",
  "_meta": {
    "owner": "wcorr-phase6-synthetic",
    "schema": 1
  },
  "properties": {
    "timestamp": {
      "type": "date"
    },
    "type": {
      "type": "text",
      "fields": {
        "keyword": {
          "type": "keyword"
        }
      }
    },
    "agent": {
      "properties": {
        "id": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    },
    "rule": {
      "properties": {
        "id": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    },
    "data": {
      "properties": {
        "file": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    },
    "syscheck": {
      "properties": {
        "mode": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        },
        "path": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        }
      }
    }
  }
}
```

F. PRIV-001 RESULTS
Every actual sequence lists Elasticsearch _id values in returned stage order. [] means no sequences. Unknown means semantic investigation with no predeclared expected outcome.

- priv-positive: expected [["priv-positive-s1", "priv-positive-s2", "priv-positive-s3"]]; actual [["priv-positive-s1", "priv-positive-s2", "priv-positive-s3"]]; PASS; HTTP 200.
  Populated matching third-stage username.
- priv-alternate-rule-command: expected [["priv-alternate-rule-command-s1", "priv-alternate-rule-command-s2", "priv-alternate-rule-command-s3"]]; actual [["priv-alternate-rule-command-s1", "priv-alternate-rule-command-s2", "priv-alternate-rule-command-s3"]]; PASS; HTTP 200.
- priv-different-agent: expected []; actual []; PASS; HTTP 200.
- priv-mismatched-stage2-user: expected []; actual []; PASS; HTTP 200.
- priv-mismatched-stage3-user: expected []; actual []; PASS; HTTP 200.
- priv-reversed-order: expected []; actual []; PASS; HTTP 200.
- priv-invalid-command: expected []; actual []; PASS; HTTP 200.
- priv-non-root-target: expected []; actual []; PASS; HTTP 200.
- priv-missing-dstuser: expected []; actual []; PASS; HTTP 200.
- priv-missing-srcuser: expected []; actual []; PASS; HTTP 200.
- priv-missing-command: expected []; actual []; PASS; HTTP 200.
- priv-missing-agent: expected []; actual []; PASS; HTTP 200.
- priv-outside-window: expected []; actual []; PASS; HTTP 200.
- priv-inside-window: expected [["priv-inside-window-s1", "priv-inside-window-s2", "priv-inside-window-s3"]]; actual [["priv-inside-window-s1", "priv-inside-window-s2", "priv-inside-window-s3"]]; PASS; HTTP 200.
- priv-exact-window: expected UNKNOWN; actual [["priv-exact-window-s1", "priv-exact-window-s2", "priv-exact-window-s3"]]; INCONCLUSIVE; HTTP 200.
  Investigate equality at maxspan boundary.
- priv-optional-user-absent: expected UNKNOWN; actual []; INCONCLUSIVE; HTTP 200.
  Investigate optional join: absence must not be assumed wildcard.
- priv-optional-user-null: expected UNKNOWN; actual []; INCONCLUSIVE; HTTP 200.
  Investigate explicit null optional join.

G. MAL-001 RESULTS
Every actual sequence lists Elasticsearch _id values in returned stage order. [] means no sequences. Unknown means semantic investigation with no predeclared expected outcome.

- mal-positive: expected [["mal-positive-s1", "mal-positive-s2"]]; actual [["mal-positive-s1", "mal-positive-s2"]]; PASS; HTTP 200.
- mal-alternate-rules: expected [["mal-alternate-rules-s1", "mal-alternate-rules-s2"]]; actual [["mal-alternate-rules-s1", "mal-alternate-rules-s2"]]; PASS; HTTP 200.
- mal-directory-usr-sbin: expected [["mal-directory-usr-sbin-s1", "mal-directory-usr-sbin-s2"]]; actual [["mal-directory-usr-sbin-s1", "mal-directory-usr-sbin-s2"]]; PASS; HTTP 200.
- mal-directory-bin: expected [["mal-directory-bin-s1", "mal-directory-bin-s2"]]; actual [["mal-directory-bin-s1", "mal-directory-bin-s2"]]; PASS; HTTP 200.
- mal-directory-sbin: expected [["mal-directory-sbin-s1", "mal-directory-sbin-s2"]]; actual [["mal-directory-sbin-s1", "mal-directory-sbin-s2"]]; PASS; HTTP 200.
- mal-different-agent: expected []; actual []; PASS; HTTP 200.
- mal-different-path: expected []; actual []; PASS; HTTP 200.
- mal-scheduled: expected []; actual []; PASS; HTTP 200.
- mal-unsupported-path: expected []; actual []; PASS; HTTP 200.
- mal-reversed-order: expected []; actual []; PASS; HTTP 200.
- mal-outside-window: expected []; actual []; PASS; HTTP 200.
- mal-inside-window: expected [["mal-inside-window-s1", "mal-inside-window-s2"]]; actual [["mal-inside-window-s1", "mal-inside-window-s2"]]; PASS; HTTP 200.
- mal-exact-window: expected UNKNOWN; actual [["mal-exact-window-s1", "mal-exact-window-s2"]]; INCONCLUSIVE; HTTP 200.
  Investigate equality at maxspan boundary.
- mal-missing-path: expected []; actual []; PASS; HTTP 200.
- mal-missing-file: expected []; actual []; PASS; HTTP 200.
- mal-missing-mode: expected []; actual []; PASS; HTTP 200.
- mal-dev-null-cr-stage2: expected []; actual []; PASS; HTTP 200.
  No match cannot isolate exclusion: path join also fails.
- mal-dev-null-cr-both: expected []; actual []; PASS; HTTP 200.
  No match cannot isolate exclusion: executable directory predicate also fails.

H. EQL SEMANTIC FINDINGS
PRIV: agent equality and stage-specific username equality are enforced. Changing either stage-2 or stage-3 username prevents a match. A populated matching stage-3 srcuser matches. Missing and explicit-null stage-3 srcuser do not match a non-null username from earlier stages. Optional-field syntax therefore does not provide wildcard matching in these observed fixtures. The documented source claim that absent third-stage users remain associated by agent/time is not supported on this engine; the companion rule documentation already warns of this limitation.
MAL: agent and path equality are enforced; realtime, executable-directory and temporal restrictions behave as asserted. All four allowed directory alternatives and both rule-ID alternatives were exercised.
Ordering: reversing relevant stages returns no match. Windows: 1799s/3599s match; 1801s/3601s do not. The exact 1800s and 3600s boundaries both match. These observations resolve the boundary experiments for these fixtures; they are not retroactively classified PASS. Equal-timestamp tie ordering was not tested.
Both exact EQL files are parser/execution compatible with this mapping on 8.19.20. No parser error, query rewrite or substitute query was used.
MAL /dev/null plus carriage return: in a scalar path sequence, matching the stage-2 exclusion value requires stage-1 syscheck.path to equal /dev/null\r, which is outside every allowed executable directory. Keeping /usr/bin/labtool at stage 1 instead fails the path join. Both synthetic investigations return no match but neither independently tests the exclusion. The exclusion branch cannot be isolated in a complete positive scalar-path sequence under the published restrictions; this redundancy is not proof of a detection defect. Multivalued path semantics were not investigated. No standalone rewritten predicate query was executed.

I. REGRESSION TEST RESULTS
New offline harness tests: 4/4 PASS (endpoint authorization, write-scope guard, fixture contracts, resource stop). Real engine: 31 PASS, 4 INCONCLUSIVE, 0 FAIL; 35/35 scenarios executed. Re-running the retained run ID correctly refuses before writes. git diff --check passes.
Existing validation: 15 tests, 13 PASS, 1 FAIL, 1 SKIP. The sole failure is test_publication_manifest: exact frozen Phase 4 file inventory excludes the added Phase 6 files. The optional external-source comparison remains skipped because WCORR_SOURCE_FILE was not supplied; no source credentials were sought.
No existing validator or publication manifest was changed to suppress this failure. Independent verification confirms all hashed Phase 4 files, all 14 published rules and all rule metadata are byte-for-byte unchanged. regression.json records command output; integrity.json records frozen-file integrity.

J. RESOURCE UTILISATION
Available host RAM: initial 1791021056 bytes; minimum sampled 1757315072; final 1762430976.
Swap used: initial 536576 bytes; maximum sampled 536576; final 536576.
Container memory: initial 1.411GiB / 2GiB; final 1.447GiB / 2GiB; maximum sampled memory percentage 72.36%.
Every sampled container state was running, OOMKilled=false, Restarting=false. No safeguard triggered. Sampling is before each scenario and at completion, not continuous peak monitoring. Elasticsearch final health green, no unassigned shards.

K. RULE INTEGRITY
Original and final SHA-256 values are identical for both target EQL files (see section C and results.json). All frozen publication-file hashes independently match. No tracked file was modified.

L. EVIDENCE
Harness: tests/phase6_engine.py
Offline tests: tests/test_phase6_engine.py
Synthetic fixture definitions: tests/fixtures/phase6/scenarios.json
Exact mappings: tests/fixtures/phase6/mappings.json
Machine-readable engine evidence: docs/verification/phase6/6a-v1/results.json
Regression evidence: docs/verification/phase6/regression.json
Integrity evidence: docs/verification/phase6/integrity.json
Reproduction instructions: docs/verification/phase6/README.md
This report: docs/verification/phase6/REPORT.md
Retained Elasticsearch indices: phase6-wcorr-6a-v1-<scenario-id>; complete names and UUIDs are in results.json.

M. DEFECTS OR OPEN QUESTIONS
Confirmed semantic limitation: absent/null third-stage PRIV username does not complete the sequence. Any intended agent/time-only fallback is absent in the observed rule behavior. No rule change was made.
Confirmed repository integration issue: frozen publication inventory rejects additive Phase 6 work. A separately authorized publication audit should decide how to represent later verification evidence without rewriting historical claims.
Unverified: native Wazuh field availability, realistic rootcheck file population, deployment mappings, scheduled search coverage, real-world detection efficacy, multivalued paths, equal-timestamp order, and other rules. No fixture/source mismatch or engine rejection was observed. The MAL exclusion investigation is not a proven defect.

N. NEXT STEP
Recommend WCORR-SSH-001 and WCORR-PERS-001 for the next separately authorized synthetic real-engine phase. Do not infer validation of the remaining 12 rules; none was executed here.

O. SAFETY CONFIRMATION
Only the existing local Elasticsearch laboratory endpoint and read-only Docker inspection/stats were accessed. Production VPS, Elasticsearch, Wazuh and Kibana were not accessed. No production credentials or telemetry were used. No attacks were simulated.
Authorized local modifications consist solely of new harness/tests, synthetic fixtures, and Phase 6 documentation/evidence, plus the 35 dedicated retained laboratory indices and their 87 synthetic documents. No unrelated index existed initially; final inventory contains exactly this run’s dedicated indices.
No Docker configuration, network or volume changes; no cleanup, restart, package installation, firewall/kernel changes, PostgreSQL/Redis modifications, branch switch, commit, push or publication. Published rule files, metadata, manifests, existing tests and other tracked files remain unchanged.
