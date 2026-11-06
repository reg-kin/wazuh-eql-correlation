# Installation and safe lab evaluation

Project: **Wazuh EQL Correlation** (`wazuh-eql-correlation`); see the [project overview](../README.md).

Reference versions: Ubuntu 24.04 LTS; Wazuh Manager 4.14.7; Logstash, Elasticsearch and Kibana 8.19.20. Port 9201 is reference-specific, not a universal Elasticsearch default; port 9200 identifies the separate Wazuh Indexer in this deployment. Elasticsearch/Kibana 8.19.20 was used in user-confirmed scheduled synthetic tests on 5 November 2026; other reference versions are not independently verified by those tests. Plugin versions, Elastic Security feature availability and licence entitlement must be checked in the target lab. No packages or services are installed by this repository.

1. Review [security](security.md) and the [source catalogue](correlation-rule-catalogue.md). Use an isolated lab and authorised synthetic events, with no connection to production ingestion. Keep lab indices and checkpoints separate from production. The reference configuration's index name must be deliberately changed in a reviewed lab copy if isolation requires another namespace.
2. Provision the reference services through an independently reviewed installation procedure. Keep Wazuh Indexer on 9200 separate from Elasticsearch on 9201. Establish certificate trust and a dedicated ingest identity; verify mappings as described in [configuration](configuration.md).
3. Install the configuration files to the paths selected in `pipelines.yml` on that lab host. Ensure the selected pipeline is not also loaded by another `path.config` wildcard. Configure environment injection, file/ACL access, the sincedb directory and any separately approved persistent queue settings. Inspect existing Logstash pipeline settings before adding another pipeline.
4. In the lab, run Logstash's `--config.test_and_exit` using the intended settings and environment, with secrets protected. This checks configuration parsing, not delivery, EQL validity or privileges. The repository's offline checks do not invoke Logstash. Start ingestion only with separate operational approval and verify new lab events arrive with native fields and the intended `timestamp`.
5. Check field capabilities across all target indices. Run one supplied EQL definition against a bounded lab interval with explicit `timestamp_field = timestamp`, `event_category_field = type.keyword` and `size = 10`. Record time range, effective mappings, versions, request settings and sanitised returned sequence counts. API examples describe future lab work; no API calls were made here.
6. Build labelled synthetic positive and negative sequences for each complete rule, including out-of-order ingestion, equal timestamps, missing fields, cross-agent negatives and legitimate maintenance. WEB-001 also needs cross-source negatives. Test timing boundaries and deployment-specific paths. Do not store production alerts in the repository. A zero historical result requires a positive test; historical matches require analyst review rather than an efficacy claim.

## Historical source creation guidance (separate from export import)

For the integrated public export use the authoritative procedure below. The following describes manual creation from historical query sources only; do not use it to recreate or rename export rules. No importable enabled rules are supplied. The `.eql` files are query sources, not full Kibana detection-rule exports. In a lab, choose Elastic Security → Rules → Create new rule → Event correlation (EQL), select `wazuh-alerts-4.x-*` (or the isolated lab equivalent), and use the reviewed query. UI labels can differ; confirm exact 8.19.20 capabilities in the lab. Set the timestamp override to `timestamp` and the event category override to `type.keyword`. If the UI does not expose both, use a reviewed, version-compatible rule-creation API procedure with `timestamp_field`, `timestamp_override`, the reviewed fallback policy and `event_category_override`; verify the effective values rather than accepting defaults. No Kibana API call is executed here.

Assign an appropriate reviewed severity, risk score, name, stable identifier and ownership. Scheduling interval and additional look-back must cover the query maxspan plus measured ingestion delay; the schedule window is separate from maxspan. Test boundary coverage, duplicate alert handling, execution time and gap monitoring. Do not invent production values from historical counts. Create disabled initially and retain evidence of preview/execution settings, false positives, negative tests and operational capacity before any separately authorised activation. Check alert field behaviour with native data, including absent ECS enrichment.

All 14 rules generated scheduled synthetic Kibana alerts (user-confirmed); see the [scheduled validation report](verification/scheduled-kibana-validation/REPORT.md). PRIV-001 used an agent-only candidate, while the published username-correlated source remains unchanged. Tests used isolated indices without modifying production rules or Wazuh configuration. Production qualification still requires representative telemetry, field compatibility, event coverage and detection accuracy review. The procedures here remain guidance for each target deployment, not evidence that all operational checks have passed. SOC Automation integration, Case publication, remediation and external SOC handoff are outside this independent project's qualification requirements.

## Historical source-recommended initial Kibana settings

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

This table is preserved historical guidance, not an installation preset: its 5 minutes plus 1 minute searches only six minutes and cannot cover the complete supplied maxspans. Do not apply it to the export or Stage 2A. Schedule and look-back are starting values, not proof of complete sequence coverage. EQL maxspan limits elapsed time between sequence events inside the documents searched; it does not automatically enlarge the scheduled detection search window. A 60-minute MAL-001 chain can be missed if an execution sees only a short interval. Validate effective query-window coverage for every maxspan, ingestion delays and run boundaries. Review overlapping-window deduplication, document duplicates and alert suppression before activation. Keep suppression disabled and actions absent during initial tests. Verify actual version-specific rule settings and record evidence before enabling anything.

## Authoritative public-release procedure

This section is the single authoritative validation and import procedure for the integrated experimental source release. It supersedes the Default-space, in-place adaptation and enablement instructions in the **preserved upstream** [package README](../deployment/public-release/README.md). That README remains unchanged because it is checksummed package content. It also supersedes older validation commands in CONTRIBUTING.md and historical reports; those documents remain preserved.

The three source contracts are distinct:

| Location | Authority and format |
| --- | --- |
| `rules/` and `tests/rule-manifest.json` | Frozen historical query sources and metadata; not import records. |
| `deployment/stage2a/` | Separate disabled single-rule API-create bodies using WCORR rule IDs, explicit native time/category settings, maxspan + 10m windows and a PRIV-001 hold. Not NDJSON or saved objects. |
| `deployment/public-release/` | Preserved 14-record Security detection-rule NDJSON export using UUID rule IDs and maxspan + 6m windows. Exact differences are recorded in the [reconciliation](verification/PUBLIC_RELEASE_RECONCILIATION.json) and [integration report](verification/PUBLIC_RELEASE_INTEGRATION.md). |

Run these offline commands from the repository root, using Python's standard library:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_public_release.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/validate_development.py --historical
PYTHONDONTWRITEBYTECODE=1 python3 scripts/stage2a.py validate
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
(cd deployment/public-release && sha256sum -c MANIFEST.sha256)
git diff --check
git diff --cached --check
```

The first command is the validator for the current integrated tree. Direct `tests/validate_development.py` checks the older Stage 2A inventory and rejects these additions; direct `tests/validate_repository.py` targets the frozen release. Use `--historical` above for that complete frozen tree, not either older validator directly on this tree. An optional authorised external source comparison uses `WCORR_SOURCE_FILE=/tmp/wazuh-correlation-rules-source.txt python3 tests/validate_public_release.py`; without the external file one comparison is explicitly skipped. Do not retrieve secrets or add that source document to the repository. The full suite includes Stage 2A's eight unit tests.

Experimental public source publication means the documented artefacts and offline integrity checks are suitable for review. It does not qualify isolated Kibana import or production deployment. No live import of this unchanged export has been qualified here. Checksums verify local payload consistency; the recorded archive hash is historical integration evidence. The original archive is absent from this package, so these checks do not independently authenticate archive origin or prove live-export provenance.

The [isolated Kibana test plan](verification/ISOLATED_KIBANA_TEST_PLAN.md) expands these gates into an evidence and acceptance procedure. Version `v1.1.0` is tagged at `aafd896b8323f04a5653c25199e39b21646681c9`; the preserved package README’s unpublished-status sentence is a preparation snapshot, not current repository status. Historical integration reports likewise describe their original working-tree state.

For separately authorised isolated import qualification:

1. Use an isolated matching-version Elasticsearch/Kibana 8.19.20 lab with no production ingestion. Select its explicitly approved Kibana space; Default is permissible only if that space is itself isolated and approved. Confirm the unchanged index pattern cannot reach production data. If isolation requires different indices or settings, stop unchanged-package qualification and prepare a separately reviewed lab variant with its own hashes and evidence.
2. Collect a complete paginated rule inventory in that space, including disabled rules. Review UUID, WCORR name and semantically equivalent query conflicts, including Stage 2A copies. Stop on conflicts; never overwrite, regenerate IDs or install both variants as duplicate detections.
3. Use Security → Rules → Import rules and select only `deployment/public-release/kibana-rules.ndjson`. This is a detection-rule import, not Stack Management saved-object import, individual `.eql` import or Stage 2A API creation. Decline overwrite and automatic ID regeneration. Inspect every import result; a partial import or schema rejection fails this qualification.
4. Read back all 14 unique UUID rule IDs and WCORR names. Confirm disabled state, empty actions/filters/exceptions, exact query strings, severity/risk, index and interval/from/to against the package and reconciliation. Confirm WEB-002 is 5m / now-16m. Preserve sanitised results. No activation follows import automatically.
5. Verify effective EQL ordering and range filtering both use `timestamp`, category uses `type.keyword`, and fallback cannot silently select incompatible ECS fields. The export omits explicit settings; do not assume defaults. If the target cannot accept or read back the required native configuration, record unchanged-import qualification as blocked. Review any corrective configuration as a separate variant with new integrity evidence; never silently edit the preserved package.
6. Qualify populated native mappings, complete telemetry, full-span positives, cross-agent/IP/user negatives where applicable, missing fields, equal timestamps, delayed/out-of-order events, execution boundaries, deduplication, runtime, caps, gaps and rollback. Review agent-only PRIV-001, SSH-002 guards and PERS-002 High/60 explicitly. Production requires representative evidence and separate deployment/activation approval; isolated synthetic import success alone cannot provide that approval.

### Export settings and adaptations

The [NDJSON package](../deployment/public-release/kibana-rules.ndjson) supplies 14 disabled rules. Follow the [integration report](verification/PUBLIC_RELEASE_INTEGRATION.md) and [export configuration guidance](public-release-configuration.md), and verify integrity with `python3 tests/validate_public_release.py` first. In the chosen isolated Kibana space use Security → Rules → Import rules. Decline overwrite; inventory all existing rules first, including equivalent queries under WCORR or other IDs. Stage 2A and this package use different identities and must not both be deployed as duplicate detections. Confirm all imported records remain disabled, actions empty, and query, UUID, index and schedule match the package. Read back effective EQL ordering, range timestamp and category settings; the export omits explicit overrides. Require `timestamp` and `type.keyword` as described in configuration, never assume ECS defaults are suitable. Preserve the export and review any necessary lab-specific changes separately. No import or activation was performed during integration.

Export windows are maxspan + 6 minutes (5-minute interval plus a provisional 1-minute lateness allowance); WEB-002 is `interval=5m`, `from=now-16m`. Stage 2A uses maxspan + 10 minutes and explicit native time/category fields. Neither schedule is a measured production guarantee. Qualify timing, deduplication, mappings and representative positives/negatives before separately authorised activation. The earlier source-recommended table is historical guidance, not the effective export configuration.
