# WCORR-SSH-003 — SSH followed by realtime sensitive file modification

- Rule identifier: `WCORR-SSH-003`.
- Detection objective: Correlates remote access with subsequent modification of sensitive Linux authentication or access-control files. This SSH-linked rule is restricted to realtime FIM events
- Severity: High. Risk score: 70.
- Source status: COMPLETE_SOURCE; RECOVERED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `rule.id.keyword`, `syscheck.mode.keyword`, `syscheck.path.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 30m.
- Historical match count: 1 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: Realtime FIM reduces timing ambiguity but does not identify a process or SSH session. Scheduled-only monitoring is excluded and must remain covered by separate FIM alerts.
- Deployment prerequisites: Enable realtime FIM for the specified authentication, sudoers and authorised-key paths. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. Historical positives are not new positive detections.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-SSH-003.eql](WCORR-SSH-003.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
