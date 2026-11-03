# WCORR-SSH-001 — Brute-force followed by authentication from the same IP

- Rule identifier: `WCORR-SSH-001`.
- Detection objective: Detects an SSH brute-force alert followed by successful authentication on the same Wazuh agent within 15 minutes.
- Severity: High. Risk score: 73.
- Source status: COMPLETE_SOURCE; RECOVERED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `data.srcip.keyword`, `rule.id.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 15m.
- Historical match count: 1 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: Same agent and source IP do not prove account compromise or matching usernames: failures use data.srcuser and successes data.dstuser. An unrelated success from another IP cannot complete the sequence.
- Deployment prerequisites: Collect SSH brute-force and successful authentication alerts with populated native source IP and agent join fields. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. Historical positives are not new positive detections.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-SSH-001.eql](WCORR-SSH-001.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.
