# WCORR-SSH-005 — SSH login, SCP execution and file modification

- Rule identifier: `WCORR-SSH-005`.
- Detection objective: Detects an SSH login followed by SCP execution and a file creation or modification event.
- Severity: Medium. Risk score: 62.
- Source status: COMPLETE_SOURCE; RECOVERED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `data.audit.command.keyword`, `rule.id.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 30m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: SCP command telemetry and FIM are joined only by agent and time; no transferred-file, user or session equality is enforced. Scheduled FIM and legitimate transfers can match.
- Deployment prerequisites: Collect rule 92603 audit command telemetry identifying scp, SSH authentication and file FIM alerts. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-SSH-005.eql](WCORR-SSH-005.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
