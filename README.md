# Wazuh EQL Correlation

Multi-stage security alert correlation for Wazuh using Elasticsearch EQL, with Logstash ingestion, detection rules and deployment guidance.

Project identifier: `wazuh-eql-correlation`. Apache-2.0; UK English documentation. No GitHub location or publication is claimed.

**Experimental reference implementation — source complete, offline verified, and suitable for source publication.** All 14 EQL definitions and metadata are present. Final-expression Elasticsearch execution and reproducible synthetic detection tests remain pending; this is not a production-validated rule pack. No Kibana installation or activation is claimed. See the [publication audit](docs/verification/PHASE3_PUBLICATION_AUDIT.md) and [checksum manifest](docs/verification/PUBLICATION_MANIFEST.json).

```text
Wazuh Manager 4.14.7
  /var/ossec/logs/alerts/alerts.json
    -> Logstash 8.19.20 (JSON, native fields, persistent sincedb, verified TLS)
    -> Elasticsearch 8.19.20 https://localhost:9201
       wazuh-alerts-4.x-*
    -> Kibana 8.19.20 / Elastic Security EQL
```

Reference host: Ubuntu 24.04 LTS. The separate Wazuh Indexer on port 9200 is not the Elasticsearch EQL engine. Elastic Agent supplies separate SOC telemetry; Wazuh alerts add an independent correlation stream. There is no dependency on the Python SOC Automation Service, the Automated Cybersecurity Remediation Platform, SOAR or automatic remediation.

Wazuh already supports native matching and correlation. Elastic EQL was selected for the required ordered multi-event sequences across Wazuh alerts, alongside those capabilities.

Start with [architecture](docs/architecture.md), [installation](docs/installation.md) and [configuration](docs/configuration.md). The [rule catalogue](docs/correlation-rule-catalogue.md) links all 14 entries. Read [historical results](docs/validation-results.md), the [ECS decision](docs/ecs-normalisation-decision.md), [troubleshooting](docs/troubleshooting.md) and [security](docs/security.md) before lab evaluation.

Run the reproducible offline checks from the repository root:

```sh
python3 tests/validate_repository.py
```

Python's standard library is sufficient. Checks do not contact services, install packages, stage files or prove EQL execution on Elasticsearch. The Phase 1 and Phase 2 reports are historical snapshots; the Phase 3 publication audit is preserved as historical evidence. The [Phase 4 rename report](docs/verification/PHASE4_RENAME_REPORT.md) records the current verdict and next step.

For direct read-only comparison with the authorised source kept outside the repository:

```sh
WCORR_SOURCE_FILE=/tmp/wazuh-correlation-rules-source.txt python3 tests/validate_repository.py
```

Without that variable, the external comparison is explicitly skipped; manifest integrity and all other offline checks still run. Do not copy the source document into the repository.

This independent project is not officially affiliated with or endorsed by Wazuh or Elastic. Reference versions above describe the intended deployment, not a tested compatibility matrix. Port 9201 is specific to that reference deployment; configure your own Elasticsearch endpoint.

Contributions: see [CONTRIBUTING.md](CONTRIBUTING.md). Source publication does not establish detection validation or production readiness.
