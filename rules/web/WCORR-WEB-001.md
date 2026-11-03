# WCORR-WEB-001 — Web reconnaissance followed by exploitation attempt

- Rule identifier: `WCORR-WEB-001`.
- Detection objective: This rule correlates reconnaissance and exploitation indicators originating from the same recorded HTTP client IP against the same Wazuh-monitored endpoint.
- Severity: Medium. Risk score: 55.
- Source status: COMPLETE_SOURCE; UNCHANGED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `data.srcip.keyword`, `rule.id.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 10m.
- Historical match count: 10 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: Same recorded client IP does not confirm exploitation. Historical attribution is uncertain because the recorded client address also represented the server public address; reverse proxies can link unrelated activity.
- Deployment prerequisites: Collect HTTP reconnaissance and exploitation alerts; validate recorded client IP attribution through proxies. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. Historical positives are not new positive detections.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-WEB-001.eql](WCORR-WEB-001.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
