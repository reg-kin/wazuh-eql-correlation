# WCORR-WEB-003 — Server-side exploitation indicator followed by PHP file creation

- Rule identifier: `WCORR-WEB-003`.
- Detection objective: This rule uses a narrower selection of web exploitation indicators followed by PHP file creation.
- Severity: High. Risk score: 85.
- Source status: COMPLETE_SOURCE; UNCHANGED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `rule.id.keyword`, `syscheck.event.keyword`, `syscheck.path.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 10m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: Investigative correlation only: HTTP 200 does not prove exploitation. FIM detection time may differ from creation time, and legitimate deployments may match.
- Deployment prerequisites: Collect the narrower exploitation rule IDs and added-file FIM at the exact WordPress Docker volume path. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-WEB-003.eql](WCORR-WEB-003.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
