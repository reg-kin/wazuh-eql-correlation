# WCORR-WEB-002 — Web attack followed by suspicious PHP file creation

- Rule identifier: `WCORR-WEB-002`.
- Detection objective: This rule detects web attack indicators followed by the creation of a PHP file in the WordPress uploads directory.
- Severity: High. Risk score: 82.
- Source status: COMPLETE_SOURCE; UNCHANGED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `rule.id.keyword`, `syscheck.event.keyword`, `syscheck.path.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 10m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: PHP creation is joined by endpoint and time, not HTTP client identity; causality is unproven. Legitimate deployments can create PHP files.
- Deployment prerequisites: Collect web alerts and added-file FIM in the exact WordPress Docker volume path; verify that path locally. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-WEB-002.eql](WCORR-WEB-002.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
