# WCORR-WEB-004 — PHP file creation followed by HTTP access attempt

- Rule identifier: `WCORR-WEB-004`.
- Detection objective: This is the revised version. Instead of accepting general suspicious web activity after PHP creation, it requires a subsequent HTTP request targeting a PHP URL within the WordPress uploads directory.
- Severity: High. Risk score: 80.
- Source status: COMPLETE_SOURCE; UNCHANGED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `data.url.keyword`, `rule.id.keyword`, `syscheck.event.keyword`, `syscheck.path.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 30m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: The requested PHP URL is not verified against the exact created file. Nested upload paths are included; the request stage deliberately has no rule-ID restriction, allowing other classifications including 31101.
- Deployment prerequisites: Collect added-file FIM at the exact WordPress Docker volume path and native URL telemetry for uploads requests. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-WEB-004.eql](WCORR-WEB-004.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
