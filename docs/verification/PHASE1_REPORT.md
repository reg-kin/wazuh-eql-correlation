> Historical Phase 1 snapshot. Source gaps and inventory below describe that phase only; superseded by [Phase 2](PHASE2_REPORT.md).

# Phase 1 verification report

Construction date: 3 November 2026. Scope: local, offline repository construction only.

## Overall verdict

Repository construction is complete within the available source material. The collection is **not publication-ready**: five required SSH definitions remain missing-source status. Nine supplied definitions are preserved as EQL sources, not activated detection rules. No production environment was accessed or modified.

## Exact files created

- `.gitignore`
- `LICENSE`
- `README.md`
- `config/logstash/environment.example`
- `config/logstash/logstash.conf`
- `config/logstash/pipelines.yml`
- `docs/architecture.md`
- `docs/configuration.md`
- `docs/correlation-rule-catalogue.md`
- `docs/ecs-normalisation-decision.md`
- `docs/installation.md`
- `docs/security.md`
- `docs/troubleshooting.md`
- `docs/validation-results.md`
- `docs/verification/PHASE1_REPORT.md`
- `rules/defence-evasion/WCORR-EVAS-001.eql`
- `rules/defence-evasion/WCORR-EVAS-001.md`
- `rules/malware/WCORR-MAL-001.eql`
- `rules/malware/WCORR-MAL-001.md`
- `rules/persistence/WCORR-PERS-001.eql`
- `rules/persistence/WCORR-PERS-001.md`
- `rules/persistence/WCORR-PERS-002.eql`
- `rules/persistence/WCORR-PERS-002.md`
- `rules/privilege-escalation/WCORR-PRIV-001.eql`
- `rules/privilege-escalation/WCORR-PRIV-001.md`
- `rules/ssh/WCORR-SSH-001.md`
- `rules/ssh/WCORR-SSH-002.md`
- `rules/ssh/WCORR-SSH-003.md`
- `rules/ssh/WCORR-SSH-004.md`
- `rules/ssh/WCORR-SSH-005.md`
- `rules/web/WCORR-WEB-001.eql`
- `rules/web/WCORR-WEB-001.md`
- `rules/web/WCORR-WEB-002.eql`
- `rules/web/WCORR-WEB-002.md`
- `rules/web/WCORR-WEB-003.eql`
- `rules/web/WCORR-WEB-003.md`
- `rules/web/WCORR-WEB-004.eql`
- `rules/web/WCORR-WEB-004.md`
- `tests/rule-manifest.json`
- `tests/validate_repository.py`

## Completed components

Apache-2.0 licence, ignore policy, sanitised Logstash pipeline, pipeline selector and environment example; architecture, installation, configuration, mapping verification, ECS decision, catalogue, historical evidence, troubleshooting and security documentation; 14 catalogue entries; nine supplied EQL definitions; a machine-readable integrity manifest and standard-library offline checks.

Configuration retains JSON file ingestion, native fields, the persistent sincedb path, daily index naming and full TLS verification. Variables cover alert path, Elasticsearch URL, identity, password and CA path. Persistent queue settings are documented separately and are not enabled by the pipeline. No index template is invented. Field-capabilities guidance distinguishes template simulation from existing native mapping provenance. Elasticsearch on 9201 is separate from Wazuh Indexer on 9200; Elastic Agent telemetry and rules are independent. There are no SOC Automation Service, SOAR or remediation dependencies.

## Missing definitions and activation status

WCORR-SSH-001, WCORR-SSH-002, WCORR-SSH-003, WCORR-SSH-004 and WCORR-SSH-005 lack original EQL source, exact windows and predicate/join fields. No executable placeholders were created. Their five historical counts are documented without reconstructed logic.

WEB-001 through WEB-004, PRIV-001, PERS-001, PERS-002, EVAS-001 and MAL-001 have supplied EQL files. MAL-001 is blocked for refinement. The other eight supplied rules require lab validation; all five SSH rules are source-blocked. No rule activation in Kibana is claimed.

## Offline test results

Validation command: `python3 tests/validate_repository.py` from the repository root, using only the Python standard library. Result: **PASS — 10 tests run, 0 failures, 0 errors** (final execution on 3 November 2026). The checks cover structure, exact catalogue/source counts, source digests, metadata, pending-source safety, configuration variables, sensitive-content patterns, address/payload/dependency hygiene, documentation links/consistency and this exact inventory.

Source hashes pin the supplied definitions for regression review; they are not an independent EQL parser or a guarantee against coordinated source/manifest edits. No offline check proves Elasticsearch query execution, Logstash plugin compatibility, mappings, detection efficacy, timing semantics or Kibana rule creation. No Logstash configuration test or live integration test was run.

## Security findings

Manual content review and offline checks found no embedded usable credentials, private IP addresses, actual host/user identifiers, private keys, certificate material, production event payloads or private repository dependencies. Only localhost endpoints, supplied reference paths and deployment-specific detection paths are included. User `root` is an intentional query predicate; `web_wp_data` is supplied deployment context. Environment values use CHANGE_ME placeholders. Secrets are never printed by the scanner on failure. Pattern scanning has finite coverage and is not a formal secrecy guarantee.

No network calls, package installation, SSH, production access, service changes, Elasticsearch/Kibana API calls, automatic remediation, remote initialisation, Git staging, commit, push or publication were performed. All lasting files are inside the project directory.

## Documentation and historical evidence status

All requested documentation is present in UK English, except the canonical Apache licence text. All 14 supplied historical counts are documented as returned sequences with query size limited to 10, not exhaustive totals or efficacy evidence. Per-rule caveats include username mismatch, maintenance, observation time, reverse-proxy attribution, agent/actor ambiguity, unlinked created/requested PHP files and the MAL-001 rootcheck anomaly involving /dev/null and a carriage return. Zero results have not demonstrated positive efficacy. Historical time ranges, raw requests/responses and complete provenance were not supplied. The journald feedback-loop incident is described without invented incident details.

## Publication blockers

Five SSH source definitions and metadata are missing. Historical reproduction evidence is incomplete. MAL-001 needs refinement before activation; all complete queries still need isolated lab tests, mapping and runtime verification, and false-positive review. Deployment-specific WordPress paths and installed plugin compatibility need lab confirmation. No claim of a fully validated, publication-ready rule collection is made, and publication was not requested or performed.

## Exact recommended next step

Recover the original EQL definitions and timestamp/category/index/window metadata for WCORR-SSH-001 through WCORR-SSH-005 from the authorised source, without accessing production during this task. Add reviewed source files and update the manifest, catalogue and offline expectations in a separate revision. Then plan an independently authorised isolated-lab validation, including MAL-001 refinement, before considering activation or publication.
