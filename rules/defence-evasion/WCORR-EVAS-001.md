# WCORR-EVAS-001 — sudo → audit configuration change → audit daemon stopped

- Rule identifier: `WCORR-EVAS-001`.
- Detection objective: Detects sudo activity followed by an audit configuration change and an audit daemon stop event.
- Severity: High. Risk score: 80.
- Source status: COMPLETE_SOURCE; UNCHANGED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `data.audit.type.keyword`, `rule.id.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 20m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: Legitimate audit-service maintenance can match this potentially significant defence-evasion sequence.
- Deployment prerequisites: Collect sudo plus audit CONFIG_CHANGE and daemon-stop alerts; ensure audit telemetry is available. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-EVAS-001.eql](WCORR-EVAS-001.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
