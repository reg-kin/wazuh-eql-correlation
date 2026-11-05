# Scheduled Kibana detection validation

Validation date: **5 November 2026**. Elasticsearch/Kibana: **8.19.20** (user-confirmed).

## Evidence provenance and outcome

The operator confirmed that all 14 Wazuh EQL rules passed synthetic scheduled Kibana detection testing and all 14 generated scheduled Kibana security alerts. Tests used isolated synthetic Elasticsearch indices. Existing production rules and Wazuh configuration were not modified during validation. Kibana alerts preserved original source-event ancestry.

These programme results, versions, alert identifiers, times and alert attributes are **user-confirmed validation evidence** supplied for this documentation update. Primary Kibana exports, raw execution logs and synthetic fixtures for these scheduled tests are not included in this report. The listed identifiers are references supplied by the operator, not independently retrieved evidence. No missing UUIDs, timestamps or evidence files are inferred. The candidate digest below is computed locally from the displayed expression.

## Fourteen-rule matrix

| Rule | Scheduled synthetic result (user-confirmed) | Scheduled alert generated |
| --- | --- | --- |
| WCORR-SSH-001 | PASS | Yes |
| WCORR-SSH-002 | PASS | Yes |
| WCORR-SSH-003 | PASS | Yes |
| WCORR-SSH-004 | PASS | Yes |
| WCORR-SSH-005 | PASS | Yes |
| WCORR-WEB-001 | PASS | Yes |
| WCORR-WEB-002 | PASS | Yes |
| WCORR-WEB-003 | PASS | Yes |
| WCORR-WEB-004 | PASS | Yes |
| WCORR-PRIV-001 | PASS — revised agent-only expression | Yes |
| WCORR-PERS-001 | PASS | Yes |
| WCORR-PERS-002 | PASS | Yes |
| WCORR-EVAS-001 | PASS | Yes |
| WCORR-MAL-001 | PASS | Yes |

PASS describes the supplied synthetic scheduled test result, not production detection qualification. PRIV-001 used the candidate below; its PASS does not validate the published username-correlated expression in scheduled testing.

## WCORR-WEB-003

The earlier direct-EQL-only result is superseded by successful scheduled Kibana alert generation on **2026-11-05 at 20:01:37 UTC** (user-confirmed).

- Alert UUID: `53e4887e78ca1e9ffe25ed2a20f4f114263deee722b9d6b1aed2da206afd682e`.
- Synthetic index: `wcorr-web003-test`; agent: `991`.
- Severity: high; risk score: 85; alert depth: 2.
- Ancestry: two original source events and two intermediate signals.

## WCORR-MAL-001

Positive and negative file-path correlation tests passed. A scheduled alert was generated at **2026-11-05 19:23:30 UTC** (user-confirmed).

- Alert UUID: `faa41ecaaf5f8fee5ccd9d1f484bafe0fa262900e166af1539eb046b312570f1`.
- Synthetic index: `wcorr-mal001-test`; agent: `985`.
- Severity: low; risk score: 21; alert depth: 2.
- Ancestry: two original source events and two intermediate signals.

These are test-alert attributes. The published catalogue severity/risk of High/75 remains unchanged; the supplied result does not establish why the test used Low/21.

## WCORR-PRIV-001 validated candidate revision

The [published original expression](../../../rules/privilege-escalation/WCORR-PRIV-001.eql) uses username correlation and remains unchanged. The successful scheduled test used this revised agent-only expression (user-confirmed):

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where rule.id.keyword == "5715" and
    data.dstuser.keyword != null]
  [any where rule.id.keyword in ("5402", "5407") and
    data.dstuser.keyword == "root" and
    data.srcuser.keyword != null and
    (data.command.keyword like "*useradd*" or
     data.command.keyword like "*adduser*")]
  [any where rule.id.keyword == "5902" and
    data.dstuser.keyword != null]
```

This is a **validated candidate revision**, not the deployed production rule. Agent-only correlation can join unrelated users' activity on the same endpoint within 30 minutes, increasing false-positive risk. It does not establish actor, session or causal continuity and requires production review before adoption. The published expression's optional/null username semantics remain a separate qualification concern.

### Deterministic SHA-256

Digest: `d60ae1488a113662f23edc51169876cc55d86567cfe6186da184df71b4b885f7`.

Hash exactly the text inside the EQL fence above, excluding the fences: UTF-8 without BOM, LF line endings, the displayed spaces (two spaces before each stage, four before continuation predicates, five before the adduser predicate), no trailing spaces or blank lines, and exactly one final LF after the final `]`. Do not dedent or reformat it. Reproduce from this report with Python's standard library, run from the repository root:

```python
from pathlib import Path
import hashlib
report = Path("docs/verification/scheduled-kibana-validation/REPORT.md").read_bytes()
expression = report.split(b"```eql\n", 1)[1].split(b"```", 1)[0]
print(hashlib.sha256(expression).hexdigest())
```

This digest identifies the documented candidate bytes; it is not independent proof of the expression submitted to Kibana.

## Historical evidence and production qualification

Existing [Phase 6 evidence](../phase6/README.md), integrity records and [Phase 7 evidence review](../phase7/QUALIFICATION_EVIDENCE_REVIEW.md) remain preserved. This report supersedes historical scheduled-alert readiness conclusions, including the earlier WEB-003 direct-EQL-only status, **not historical test results**. It does not rewrite the conditions, limitations or outcomes of those earlier tests.

[Phase 7B](../phase7/7b-v1/REPORT.md) already records bounded native Elasticsearch execution of all 14 frozen rules: 14 successful executions, three positive rules and eleven valid zero-match rules. That evidence establishes bounded native execution compatibility and remains distinct from these synthetic scheduled alerts.

Production qualification remains pending for representative Wazuh telemetry, field compatibility, event coverage and detection accuracy. Synthetic alert generation does not establish precision, recall, production mappings or schedule-window coverage under real ingestion delays. Further review must address legitimate maintenance, join negatives, optional/missing fields, timing boundaries, duplicate handling and deployment-specific telemetry. Full positive/negative coverage for every rule is not inferred from this programme summary; only MAL-001's positive and negative path results are specifically supplied.

## Project boundary

Wazuh EQL Correlation is an independent project. Its scope is Wazuh alert ingestion into Elasticsearch, field normalisation and mapping compatibility, EQL multi-stage correlation, Elastic Security scheduled detection and production detection qualification. SOC Automation is separate. SOC Automation integration, Case publication, remediation and external SOC handoff are not qualification requirements.
