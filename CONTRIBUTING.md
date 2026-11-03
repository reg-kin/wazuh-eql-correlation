# Contributing to Wazuh EQL Correlation

Project identifier: `wazuh-eql-correlation`. This is an experimental Apache-2.0 reference implementation. Keep changes focused and explain the intended behaviour and limitations. No official Wazuh or Elastic affiliation is implied.

Run `python3 tests/validate_repository.py` before submitting changes. Use only sanitised synthetic examples; never contribute production alerts, credentials, certificates, private identifiers or operational logs. Report security concerns privately to the repository maintainer using an available private channel; do not disclose secrets in public issues. No dedicated private reporting address is configured here.

For rule changes, review predicates and join keys explicitly, update the rule metadata and tests/rule-manifest.json checksums, and record the evidence level accurately. Re-run the publication audit and regenerate its manifest when publication files change. Repository checks do not validate EQL in Elasticsearch. Keep historical counts separate from final-expression results, and record reproducible labelled positive/negative lab evidence before making detection claims. Do not enable actions or remediation as part of source contributions.
