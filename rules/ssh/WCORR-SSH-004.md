# WCORR-SSH-004 — SSH login, sudo and sensitive file modification

- Rule identifier: `WCORR-SSH-004`.
- Detection objective: Detects a three-stage sequence involving remote access, privilege use and modification of security-sensitive files.
- Severity: High. Risk score: 78.
- Source status: COMPLETE_SOURCE; RECOVERED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `rule.id.keyword`, `syscheck.path.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 30m.
- Historical match count: 0 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: Agent and time correlation does not prove actor or session continuity. Unlike SSH-003 this source has no realtime FIM predicate; scheduled observation timing can misattribute changes. Legitimate administration can match.
- Deployment prerequisites: Collect SSH, sudo and sensitive-path FIM alerts; assess scheduled FIM observation delays. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. With zero historical matches, positive detection efficacy has not been demonstrated.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-SSH-004.eql](WCORR-SSH-004.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
