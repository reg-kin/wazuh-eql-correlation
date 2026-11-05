# Validation status

## Current scheduled validation — 5 November 2026

All 14 rules passed synthetic scheduled Kibana detection tests and generated scheduled security alerts on Elasticsearch/Kibana 8.19.20 (user-confirmed). PRIV-001 used a validated agent-only candidate, not the unchanged published username-correlated expression. Tests used isolated synthetic indices, preserved original source-event ancestry and did not modify production rules or Wazuh configuration. See the [scheduled validation report](verification/scheduled-kibana-validation/REPORT.md) for the matrix, supplied alert details, candidate digest and evidence limitations.

The [Phase 7B report](verification/phase7/7b-v1/REPORT.md) records bounded native execution of all 14 frozen rules (three positive, eleven zero-match). Production qualification remains pending for representative Wazuh telemetry, field compatibility, event coverage and detection accuracy. The new report supersedes historical scheduled-alert readiness conclusions, not historical test results or integrity records.

The sections below retain earlier evidence context with current qualifications.

## A. Historical execution of earlier versions

These are supplied historical query-execution results, not measurements made during repository construction and not proof of detection efficacy. Each query used size limited to 10; returned sequence counts are not exhaustive index-wide totals. Counts of 10 may reflect the request cap. Dates, time ranges, full query requests, raw responses, effective mappings and result provenance beyond the supplied summary were not provided. No precision, recall or coverage claim can be calculated from them.

| Rule | Returned sequences (size limited to 10) |
| --- | --- |
| WCORR-SSH-001 | 1 |
| WCORR-SSH-002 | 10 |
| WCORR-SSH-003 | 1 |
| WCORR-SSH-004 | 0 |
| WCORR-SSH-005 | 0 |
| WCORR-WEB-001 | 10 |
| WCORR-WEB-002 | 0 |
| WCORR-WEB-003 | 0 |
| WCORR-WEB-004 | 0 |
| WCORR-PRIV-001 | 2 |
| WCORR-PERS-001 | 0 |
| WCORR-PERS-002 | 0 |
| WCORR-EVAS-001 | 0 |
| WCORR-MAL-001 | 7 |

## Analyst qualifications

**WCORR-SSH-001:** Different usernames were involved in the failed and successful SSH authentication events. Actor continuity is unproven.

**WCORR-SSH-002:** Routine SSH administration and sudo may match.

**WCORR-SSH-003:** File modification and observation timestamps may differ.

**WCORR-SSH-004:** No historical matches; positive detection efficacy has not been demonstrated.

**WCORR-SSH-005:** No historical matches; positive detection efficacy has not been demonstrated.

**WCORR-WEB-001:** Reverse-proxy source IP attribution is uncertain. Shared proxy addresses may link unrelated activity.

**WCORR-WEB-002:** Agent-level correlation does not establish the same attacker. Legitimate deployments can add PHP files.

**WCORR-WEB-003:** Agent-level correlation does not establish the same attacker. Legitimate deployments can add PHP files.

**WCORR-WEB-004:** The PHP file created is not necessarily the same PHP file subsequently requested. Benign uploads and requests may coincide.

**WCORR-PRIV-001:** Two historical sequences included account creation and potentially legitimate maintenance. Same-agent matching does not prove same-session or same-actor activity.

**WCORR-PERS-001:** Legitimate cron maintenance may coincide with authentication activity; agent-level joins do not identify an actor.

**WCORR-PERS-002:** Legitimate service installation and maintenance may match; agent-level joins do not identify an actor.

**WCORR-EVAS-001:** Authorised audit configuration and administration may match; agent-level joins do not identify an actor.

**WCORR-MAL-001:** Scheduled FIM observations were correlated with repeated rootcheck anomalies involving /dev/null and a carriage return character. These observations do not establish malware execution; the Phase 2 revision addresses these weaknesses, and later user-confirmed positive/negative file-path and scheduled alert tests are recorded in the new report.

Zero historical matches do not establish production detection efficacy; the later user-confirmed synthetic scheduled positives are recorded above. All five SSH definitions have now been recovered. PRIV-001 and MAL-001 have revised source definitions; their historical counts do not validate those revisions. Scheduled synthetic activation is now user-confirmed as recorded above; production activation is not established.

## Future evidence record

For each separately authorised lab test record rule source digest/revision, service/plugin versions, field capabilities, timestamp/category settings, index scope, query range, size/limits, synthetic test labels, expected versus observed sequences, timing/ingestion effects and analyst disposition. Preserve sanitised aggregate results only. Review legitimate maintenance and adversarial negatives as well as positive chains. Offline checks validate repository integrity and consistency, not Elasticsearch parsing, runtime semantics, detection efficacy or Kibana readiness.

## B. Offline validation of final expressions

All 14 source definitions have repository integrity, metadata, field-inventory and source-token preservation checks. Unchanged queries retain their Phase 1 bytes. Structural checks are not full Elasticsearch syntax validation; no EQL parser is available in the repository workflow. The external authoritative source can optionally be supplied to the checker for direct comparison without copying it into the repository.

## C. Final-expression live or isolated-lab execution

The earlier NOT_PERFORMED status is superseded by bounded Phase 7B native execution and the user-confirmed scheduled synthetic results above. The following supplied source summaries remain historical context. Source WEB-001 reports 10 historical matches, with source attribution ambiguity; WEB-002 reports zero historical sequences and earlier synthetic positive/negative tests; WEB-003 and WEB-004 report zero. These supplied summaries lack complete requests, responses, dates and reproducible fixtures. The revised source provides no new execution evidence for PRIV-001 or MAL-001, nor complete evidence for the SSH revisions. Earlier Phase 1 counts remain historical only.

## Source inconsistencies and evidence gaps

SSH-002 standalone adds two null predicates absent in Dev Tools; Dev Tools is designated, with the complete alternative recorded in its entry. Its same-user recommendation is unimplemented. SSH-003 standalone and Dev Tools differ only in layout. PERS-002 contains a stray cron heading; its actual systemd title, description and expression are retained. PRIV-001's claim that an optional third-stage field permits missing usernames is unverified: optional fields can yield null rather than wildcard joins. Preserve the source and test missing-field semantics before interpreting matches. SSH-004 and SSH-005 lack SSH-003's realtime restriction; this difference is retained. MAL-001's rootcheck path population outside the recurring anomaly is unestablished. No contradictory predicates have been silently reconciled.

## D. Synthetic positive and negative detection tests

Phase 6 contains historical synthetic fixtures and semantic test evidence; those records remain unchanged. Primary scheduled-test fixtures and execution exports for the current 14-rule programme are not included. Earlier WEB-002 test summaries remain historical context. Repository integrity checks alone do not establish detection efficacy. The later scheduled results establish user-confirmed synthetic positives for all 14 (PRIV-001 candidate), with positive/negative file-path tests specifically confirmed for MAL-001. Comprehensive labelled negative cases, missing-field behaviour, timing boundaries and join negatives remain qualification work.

## E. Operational Kibana activation

All 14 generated scheduled synthetic alerts (user-confirmed); this does not establish production installation or enablement. Disabled rule creation, effective timestamp/category settings, sequence coverage, execution windows, overlapping searches, duplicate alerts and suppression all require separate operational verification. No production activation is established by this documentation update.
