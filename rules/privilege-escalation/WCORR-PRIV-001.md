# WCORR-PRIV-001 — SSH access → privileged account creation

- Rule identifier: `WCORR-PRIV-001`.
- Detection objective: Detects a successful SSH login followed by sudo activity targeting root and a subsequent new-user event on the same monitored endpoint.
- Severity: High. Risk score: 82.
- Source status: COMPLETE_SOURCE; REVISED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `data.command.keyword`, `data.dstuser.keyword`, `data.srcuser.keyword`, `rule.id.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 30m.
- Historical match count: 2 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: The source says the optional third-stage key accommodates missing data.srcuser and that account creation remains associated by agent and time. Optional-field syntax does not itself guarantee wildcard joining: missing values can become null and fail to join a non-null username. Verify this claim in the target engine; do not silently change the query. SSH-to-sudo attribution is stronger, but account creation causality remains unproven. sudo su followed by useradd in a root shell is intentionally excluded.
- Deployment prerequisites: Collect SSH destination usernames, sudo source usernames and commands, and 5902 new-user events. Validate stage-specific joins and missing third-stage usernames explicitly. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. Historical positives are not new positive detections.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-PRIV-001.eql](WCORR-PRIV-001.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
