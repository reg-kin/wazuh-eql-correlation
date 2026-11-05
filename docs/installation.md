# Installation and safe lab evaluation

Project: **Wazuh EQL Correlation** (`wazuh-eql-correlation`); see the [project overview](../README.md).

Reference versions: Ubuntu 24.04 LTS; Wazuh Manager 4.14.7; Logstash, Elasticsearch and Kibana 8.19.20. Port 9201 is reference-specific, not a universal Elasticsearch default; port 9200 identifies the separate Wazuh Indexer in this deployment. Elasticsearch/Kibana 8.19.20 was used in user-confirmed scheduled synthetic tests on 5 November 2026; other reference versions are not independently verified by those tests. Plugin versions, Elastic Security feature availability and licence entitlement must be checked in the target lab. No packages or services are installed by this repository.

1. Review [security](security.md) and the [source catalogue](correlation-rule-catalogue.md). Use an isolated lab and authorised synthetic events, with no connection to production ingestion. Keep lab indices and checkpoints separate from production. The reference configuration's index name must be deliberately changed in a reviewed lab copy if isolation requires another namespace.
2. Provision the reference services through an independently reviewed installation procedure. Keep Wazuh Indexer on 9200 separate from Elasticsearch on 9201. Establish certificate trust and a dedicated ingest identity; verify mappings as described in [configuration](configuration.md).
3. Install the configuration files to the paths selected in `pipelines.yml` on that lab host. Ensure the selected pipeline is not also loaded by another `path.config` wildcard. Configure environment injection, file/ACL access, the sincedb directory and any separately approved persistent queue settings. Inspect existing Logstash pipeline settings before adding another pipeline.
4. In the lab, run Logstash's `--config.test_and_exit` using the intended settings and environment, with secrets protected. This checks configuration parsing, not delivery, EQL validity or privileges. The repository's offline checks do not invoke Logstash. Start ingestion only with separate operational approval and verify new lab events arrive with native fields and the intended `timestamp`.
5. Check field capabilities across all target indices. Run one supplied EQL definition against a bounded lab interval with explicit `timestamp_field = timestamp`, `event_category_field = type.keyword` and `size = 10`. Record time range, effective mappings, versions, request settings and sanitised returned sequence counts. API examples describe future lab work; no API calls were made here.
6. Build labelled synthetic positive and negative sequences for each complete rule, including out-of-order ingestion, equal timestamps, missing fields, cross-agent negatives and legitimate maintenance. WEB-001 also needs cross-source negatives. Test timing boundaries and deployment-specific paths. Do not store production alerts in the repository. A zero historical result requires a positive test; historical matches require analyst review rather than an efficacy claim.

## Kibana detection-rule creation and activation

No importable enabled rules are supplied. The `.eql` files are query sources, not full Kibana detection-rule exports. In a lab, choose Elastic Security → Rules → Create new rule → Event correlation (EQL), select `wazuh-alerts-4.x-*` (or the isolated lab equivalent), and use the reviewed query. UI labels can differ; confirm exact 8.19.20 capabilities in the lab. Set the timestamp override to `timestamp` and the event category override to `type.keyword`. If the UI does not expose both, use a reviewed, version-compatible rule-creation API procedure with `timestamp_override` and `event_category_override`; verify the effective values rather than accepting defaults. No Kibana API call is executed here.

Assign an appropriate reviewed severity, risk score, name, stable identifier and ownership. Scheduling interval and additional look-back must cover the query maxspan plus measured ingestion delay; the schedule window is separate from maxspan. Test boundary coverage, duplicate alert handling, execution time and gap monitoring. Do not invent production values from historical counts. Create disabled initially and retain evidence of preview/execution settings, false positives, negative tests and operational capacity before any separately authorised activation. Check alert field behaviour with native data, including absent ECS enrichment.

All 14 rules generated scheduled synthetic Kibana alerts (user-confirmed); see the [scheduled validation report](verification/scheduled-kibana-validation/REPORT.md). PRIV-001 used an agent-only candidate, while the published username-correlated source remains unchanged. Tests used isolated indices without modifying production rules or Wazuh configuration. Production qualification still requires representative telemetry, field compatibility, event coverage and detection accuracy review. The procedures here remain guidance for each target deployment, not evidence that all operational checks have passed. SOC Automation integration, Case publication, remediation and external SOC handoff are outside this independent project's qualification requirements.

## Source-recommended initial Kibana settings

| Setting | Initial value |
| --- | --- |
| Rule type | Event Correlation (EQL) |
| Name / description / severity / risk | Preserve each source entry and manifest |
| Index | `wazuh-alerts-4.x-*` |
| Timestamp field | `timestamp` |
| Event category field | `type.keyword` |
| Schedule | 5 minutes |
| Additional look-back | 1 minute |
| Alert suppression | Disabled initially |
| Actions | None initially |
| Tags | Wazuh, EQL, Multi-stage, rule category |

Schedule and look-back are starting values, not proof of complete sequence coverage. EQL maxspan limits elapsed time between sequence events inside the documents searched; it does not automatically enlarge the scheduled detection search window. A 60-minute MAL-001 chain can be missed if an execution sees only a short interval. Validate effective query-window coverage for every maxspan, ingestion delays and run boundaries. Review overlapping-window deduplication, document duplicates and alert suppression before activation. Keep suppression disabled and actions absent during initial tests. Verify actual version-specific rule settings and record evidence before enabling anything.
