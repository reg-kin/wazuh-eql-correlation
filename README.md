# Wazuh EQL Correlation

Multi-stage security alert correlation for Wazuh using Elasticsearch EQL, with Logstash ingestion, detection rules and deployment guidance.

Project identifier: `wazuh-eql-correlation`. Apache-2.0; UK English documentation. No GitHub location or publication is claimed.

**Experimental reference implementation — all 14 rules passed user-confirmed synthetic scheduled Kibana detection tests on 5 November 2026 (Elasticsearch/Kibana 8.19.20), generating scheduled security alerts.** PRIV-001 used a validated agent-only candidate; its published username-correlated expression remains unchanged. See the [scheduled validation report](docs/verification/scheduled-kibana-validation/REPORT.md) for provenance, alert ancestry and limitations. This is not a production-validated rule pack. Production qualification remains pending for representative Wazuh telemetry, field compatibility, event coverage and detection accuracy. See the [publication audit](docs/verification/PHASE3_PUBLICATION_AUDIT.md) and [checksum manifest](docs/verification/PUBLICATION_MANIFEST.json).

```text
Wazuh Manager 4.14.7
  /var/ossec/logs/alerts/alerts.json
    -> Logstash 8.19.20 (JSON, native fields, persistent sincedb, verified TLS)
    -> Elasticsearch 8.19.20 https://localhost:9201
       wazuh-alerts-4.x-*
    -> Kibana 8.19.20 / Elastic Security EQL
```

Reference host: Ubuntu 24.04 LTS. The separate Wazuh Indexer on port 9200 is not the Elasticsearch EQL engine. Elastic Agent supplies separate SOC telemetry; Wazuh alerts add an independent correlation stream. Wazuh EQL Correlation is independent; SOC Automation is separate. Project scope covers Wazuh ingestion, field normalisation and mapping compatibility, EQL correlation, scheduled detection and production qualification. SOC integration, Case publication, remediation and external SOC handoff are not qualification requirements.

Wazuh already supports native matching and correlation. Elastic EQL was selected for the required ordered multi-event sequences across Wazuh alerts, alongside those capabilities.

Start with [architecture](docs/architecture.md), [installation](docs/installation.md) and [configuration](docs/configuration.md). The [rule catalogue](docs/correlation-rule-catalogue.md) links all 14 entries. Read [historical results](docs/validation-results.md), the [ECS decision](docs/ecs-normalisation-decision.md), [troubleshooting](docs/troubleshooting.md) and [security](docs/security.md) before lab evaluation.

Run the reproducible offline checks from the repository root:

```sh
python3 tests/validate_public_release.py
```

Python's standard library is sufficient. Checks do not contact services, install packages, stage files or prove EQL execution on Elasticsearch. The Phase 1 and Phase 2 reports are historical snapshots; the Phase 3 publication audit is preserved as historical evidence. The [Phase 4 rename report](docs/verification/PHASE4_RENAME_REPORT.md) records the historical rename verdict and next step. The scheduled validation report supplies the current scheduled-test status; frozen historical evidence remains unchanged.

For direct read-only comparison with the authorised source kept outside the repository:

```sh
WCORR_SOURCE_FILE=/tmp/wazuh-correlation-rules-source.txt python3 tests/validate_public_release.py
```

The authoritative current validation and import procedure is [installation](docs/installation.md#authoritative-public-release-procedure). It takes precedence over the preserved package README and older commands in CONTRIBUTING.md or historical reports.

Without that variable, the external comparison is explicitly skipped; manifest integrity and all other offline checks still run. Current public-release checks validate the integrated inventory and scheduled report, while checking historical release hashes against the original tag for explicitly evolving documentation. Run `python3 tests/validate_development.py --historical` to validate the complete frozen release with its unchanged validator; `tests/validate_repository.py` applies to that historical tree. Do not copy the source document into the repository.

This independent project is not officially affiliated with or endorsed by Wazuh or Elastic. Elasticsearch/Kibana 8.19.20 is user-confirmed for the scheduled synthetic tests; the other reference versions are not established as a tested compatibility matrix by those tests. Port 9201 is specific to that reference deployment; configure your own Elasticsearch endpoint.

Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md). Source publication does not establish detection validation or production readiness.

The [portable public-release package](deployment/public-release/kibana-rules.ndjson) contains 14 disabled import records with original UUID rule IDs. Read the [integration report](docs/verification/PUBLIC_RELEASE_INTEGRATION.md) before import: its queries and schedules differ from the historical sources and Stage 2A. Run `python3 tests/validate_public_release.py` for the current integration checks; this extends the frozen development inventory without changing the staged validator.
