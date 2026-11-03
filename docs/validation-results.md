# Validation status

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

**WCORR-MAL-001:** Scheduled FIM observations were correlated with repeated rootcheck anomalies involving /dev/null and a carriage return character. These observations do not establish malware execution; the Phase 2 revision addresses these weaknesses, but requires lab validation.

All rules with zero historical matches have not demonstrated positive detection efficacy. All five SSH definitions have now been recovered. PRIV-001 and MAL-001 have revised source definitions; their historical counts do not validate those revisions. No rules have been activated in Kibana as part of this repository.

## Future evidence record

For each separately authorised lab test record rule source digest/revision, service/plugin versions, field capabilities, timestamp/category settings, index scope, query range, size/limits, synthetic test labels, expected versus observed sequences, timing/ingestion effects and analyst disposition. Preserve sanitised aggregate results only. Review legitimate maintenance and adversarial negatives as well as positive chains. Offline checks validate repository integrity and consistency, not Elasticsearch parsing, runtime semantics, detection efficacy or Kibana readiness.

## B. Offline validation of final expressions

All 14 source definitions have repository integrity, metadata, field-inventory and source-token preservation checks. Unchanged queries retain their Phase 1 bytes. Structural checks are not full Elasticsearch syntax validation; no EQL parser is available in the repository workflow. The external authoritative source can optionally be supplied to the checker for direct comparison without copying it into the repository.

## C. Final-expression live or isolated-lab execution

NOT_PERFORMED for all 14. No new positive detections are claimed. Source WEB-001 reports 10 historical matches, with source attribution ambiguity; WEB-002 reports zero historical sequences and earlier synthetic positive/negative tests; WEB-003 and WEB-004 report zero. These supplied summaries lack complete requests, responses, dates and reproducible fixtures. The revised source provides no new execution evidence for PRIV-001 or MAL-001, nor complete evidence for the SSH revisions. Earlier Phase 1 counts remain historical only.

## Source inconsistencies and evidence gaps

SSH-002 standalone adds two null predicates absent in Dev Tools; Dev Tools is designated, with the complete alternative recorded in its entry. Its same-user recommendation is unimplemented. SSH-003 standalone and Dev Tools differ only in layout. PERS-002 contains a stray cron heading; its actual systemd title, description and expression are retained. PRIV-001's claim that an optional third-stage field permits missing usernames is unverified: optional fields can yield null rather than wildcard joins. Preserve the source and test missing-field semantics before interpreting matches. SSH-004 and SSH-005 lack SSH-003's realtime restriction; this difference is retained. MAL-001's rootcheck path population outside the recurring anomaly is unestablished. No contradictory predicates have been silently reconciled.

## D. Synthetic positive and negative detection tests

No reproducible synthetic test suite or final-expression positive/negative execution evidence is included for this complete pack. Earlier WEB-002 test summaries are historical context only. The Python repository tests are not detection tests. All 14 require labelled positive and negative lab cases, including missing-field behaviour, timing boundaries and join negatives.

## E. Operational Kibana activation

No rules are claimed installed or enabled. Disabled rule creation, effective timestamp/category settings, sequence coverage, execution windows, overlapping searches, duplicate alerts and suppression all require separate operational verification. No activation occurred during this audit.
