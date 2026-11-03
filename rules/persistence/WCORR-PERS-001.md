# WCORR-PERS-001 — SSH login → crontab editor → cron modification

- Rule identifier: `WCORR-PERS-001`.
- Detection objective: Detects an SSH login followed by a crontab editor event and a FIM alert for a cron-related file.
- Severity: High. Risk score: 78.
- Source status: COMPLETE_SOURCE; UNCHANGED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `rule.id.keyword`, `syscheck.path.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 30m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: Legitimate cron administration can produce the same sequence; agent and time do not establish actor continuity.
- Deployment prerequisites: Collect SSH, 2834 crontab-editor alerts and FIM for all specified cron paths. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-PERS-001.eql](WCORR-PERS-001.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
