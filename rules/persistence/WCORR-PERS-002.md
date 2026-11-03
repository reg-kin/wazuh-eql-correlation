# WCORR-PERS-002 — SSH login → systemd unit modification → service failure

- Rule identifier: `WCORR-PERS-002`.
- Detection objective: Detects an SSH login followed by modification or creation of a systemd service unit and a subsequent service-failure alert.
- Severity: Medium. Risk score: 60.
- Source status: COMPLETE_SOURCE; UNCHANGED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `rule.id.keyword`, `syscheck.path.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 30m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: A service failure after a unit-file change does not establish causality. Legitimate service installation and maintenance can match.
- Deployment prerequisites: Collect SSH, systemd unit-file FIM and 40704 service-failure alerts. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-PERS-002.eql](WCORR-PERS-002.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
