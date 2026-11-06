# Wazuh EQL Correlation — portable rule export

This package contains 14 Kibana Elastic Security EQL detection rules exported from a deployed configuration on 6 November 2026. The EQL expressions are preserved exactly.

## Contents
- `kibana-rules.ndjson`: 14 rules, **disabled by default** for safe review before activation.
- `rules/`: individual EQL expressions.

## Prerequisites
- Wazuh alerts ingested into Elasticsearch with native Wazuh fields, mapped as expected by the rules.
- Elasticsearch/Kibana with Elastic Security EQL detection rule support. The source deployment used Elasticsearch/Kibana 8.19.20; compatibility elsewhere is not established.
- An index matching `wazuh-alerts-4.x-*`, with relevant fields searchable as `.keyword`.
- Rule time settings are 5-minute execution intervals and search windows of `maxspan + 6 minutes`.
- Verify the effective timestamp and event-category configuration in the target Kibana installation before enabling. The exported objects do not explicitly specify timestamp override or event-category override settings.

## Installation
In Kibana's Default space, navigate to Security > Rules > Detection rules (SIEM), then use the import option and select `kibana-rules.ndjson`. Review imported rules, adapt index and environment-specific predicates, validate the expected telemetry, then enable only suitable rules. Existing rule IDs may cause overwrite prompts: do not overwrite operational rules without review.

## Important limitations
- The rule definitions are not a substitute for Wazuh, Logstash, Elasticsearch or Kibana configuration.
- `WCORR-PRIV-001` uses host-level correlation and does **not** establish that the same user performed each action.
- WEB-002/003/004 contain a deployment-specific WordPress Docker volume path; adjust it to match your monitored environment.
- Successful execution does not prove detection coverage or absence of false positives.
- No production alerts, credentials, hostnames or operator identities are included in the portable package.
- This is a prepared release artefact, not yet committed or published to GitHub.
