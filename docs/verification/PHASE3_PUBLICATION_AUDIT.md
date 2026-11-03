# Phase 3 — open-source publication readiness audit

Audit date: 3 November 2026. Scope: this development repository and offline checks only.

## 1. Executive verdict

**PUBLICATION READY as an experimental open-source reference implementation.** All 14 intended source definitions are complete. No remaining source-publication blocker or identified sensitive material remains. Publication has not occurred.

| Classification | Verdict | Evidence boundary |
| --- | --- | --- |
| SOURCE COMPLETE | Yes | Exactly 14 nonempty EQL definitions and corresponding metadata |
| OFFLINE VERIFIED | Yes | Repository consistency, source digests, configuration, links and security checks pass |
| PUBLICATION READY | Yes | Sanitised experimental source with explicit limitations and Apache-2.0 licence |
| DETECTION VALIDATED | No | Final-expression Elasticsearch and reproducible synthetic execution pending |
| PRODUCTION READY | No | Operational deployment and detection behaviour have not been established |

Publication readiness does not imply detection validation or production readiness. Historical execution counts cannot validate revised expressions. No rule installation, enabling or operational efficacy is claimed.

## 2. Exact files modified or created

Modified:

- `.gitignore`: editor and scratch exclusions.
- `README.md`: experimental publication verdict, current audit links, independence and reference-port clarification.
- `docs/architecture.md`: reference-specific endpoint clarification.
- `docs/installation.md`: reference port scope.
- `docs/security.md`: current publication verdict and actual scan/Git scope.
- `docs/troubleshooting.md`: configurable endpoint wording.
- `docs/validation-results.md`: separate synthetic-test and operational-activation evidence categories.
- `docs/verification/PHASE2_REPORT.md`: historical-snapshot notice only.
- `tests/validate_repository.py`: current status assertions, preserve the 46-file historical inventory as a subset, and add current publication-manifest integrity verification.

Created:

- `CONTRIBUTING.md`.
- `docs/verification/PUBLICATION_MANIFEST.json`.
- `docs/verification/PHASE3_PUBLICATION_AUDIT.md`.

No existing file was deleted. All 14 EQL files, all 14 rule entries, the rule metadata manifest, Logstash configuration and licence remain byte-for-byte unchanged. Initial and final SHA-256 inventories are in the publication manifest.

## 3. Repository inventory

Initial inventory: 46 regular files. Final inventory: 49 regular files. No symlinks, Git metadata, raw alerts, database files, runtime logs, bytecode, generated runtime artefacts or embedded certificate/key files were found. No executable application service is supplied; Python is used only for offline repository tests.

| Category | Exact scope | Count |
| --- | --- | --- |
| EQL source | `rules/**/*.eql` | 14 |
| Per-rule documentation | `rules/**/*.md` | 14 |
| Rule metadata | `tests/rule-manifest.json` | 1 |
| Offline test source | `tests/validate_repository.py` | 1 |
| Logstash examples | `config/logstash/logstash.conf`, `config/logstash/pipelines.yml`, `config/logstash/environment.example` | 3 |
| Main guides | Eight Markdown files directly in `docs/` | 8 |
| Verification reports | Phase 1, Phase 2 and this report | 3 |
| Publication manifest | `docs/verification/PUBLICATION_MANIFEST.json` | 1 |
| Top-level publication files | `.gitignore`, `LICENSE`, `README.md`, `CONTRIBUTING.md` | 4 |

The manifest enumerates every exact path, every documentation path, the initial file checksums and final SHA-256 checksums for every file except itself. Self-hashing is deliberately excluded to avoid a recursive digest; its path remains in the complete inventory. The report is hashed by the manifest.

## 4. Fourteen-rule completeness

All identifiers use the existing `WCORR-` prefix. The complete set is SSH-001–005, WEB-001–004, PRIV-001, PERS-001–002, EVAS-001 and MAL-001; no extra rule exists. Every entry has a nonempty EQL sequence, name, detection description, severity, risk score, correlation window, required fields, limitations, deployment prerequisites and explicit evidence status. No pending-source placeholder remains.

| Identifier | Severity | Risk | Maxspan |
| --- | --- | --- | --- |
| WCORR-SSH-001 | High | 73 | 15m |
| WCORR-SSH-002 | Medium | 47 | 15m |
| WCORR-SSH-003 | High | 70 | 30m |
| WCORR-SSH-004 | High | 78 | 30m |
| WCORR-SSH-005 | Medium | 62 | 30m |
| WCORR-WEB-001 | Medium | 55 | 10m |
| WCORR-WEB-002 | High | 82 | 10m |
| WCORR-WEB-003 | High | 85 | 10m |
| WCORR-WEB-004 | High | 80 | 30m |
| WCORR-PRIV-001 | High | 82 | 30m |
| WCORR-PERS-001 | High | 78 | 30m |
| WCORR-PERS-002 | Medium | 60 | 30m |
| WCORR-EVAS-001 | High | 80 | 20m |
| WCORR-MAL-001 | High | 75 | 60m |

The complete rule metadata and source paths/digests are preserved in both manifests. Structural completeness does not establish executable correctness in Elasticsearch.

## 5. EQL source preservation

All 14 EQL SHA-256 digests agree with the pre-existing rule manifest and initial audit bytes. No predicate, join key, whitespace or source byte was changed. PRIV-001 optional third-stage username semantics remain an explicit uncertainty; MAL-001 rootcheck path population remains unestablished. SSH-002's designated Dev Tools expression and documented alternative are preserved. No external source document was accessed in Phase 3; its optional comparison was skipped.

## 6. Logstash configuration

The example is syntactically plausible for the intended Logstash 8.19.20 deployment based on static inspection. File input and JSON codec are appropriate for line-delimited Wazuh JSON alerts. Input, codec, pipeline and Elasticsearch output explicitly disable ECS compatibility, and no normalisation filter or extra plugin dependency is introduced.

All five substitutions exactly match the example environment and configuration guide: `WAZUH_ALERTS_PATH`, `ELASTICSEARCH_URL`, `ELASTICSEARCH_USERNAME`, `ELASTICSEARCH_PASSWORD`, `ELASTICSEARCH_CA_PATH`. Credentials are unusable placeholders; the example is not automatically loaded. TLS uses full verification and a configurable CA path. The explicit daily output pattern agrees with `wazuh-alerts-4.x-*`; ILM, data streams and template management are disabled. Compatible mappings must be provisioned separately.

Persistent sincedb and `start_position = end` behaviour are documented, including first-discovery skipping, offsets, rotation, replay and duplicate risk. The checkpoint path is a fixed reference path with permissions prerequisites; persistent queues are separate settings, not silently enabled. No live Logstash configuration validation, plugin compatibility test or ingestion test occurred.

## 7. Architecture and portability

README, architecture, installation, configuration, ECS decision, catalogue, validation, troubleshooting and security guides consistently preserve native Wazuh fields. Reference versions are Ubuntu 24.04 LTS, Wazuh Manager 4.14.7 and Logstash/Elasticsearch/Kibana 8.19.20. They describe an intended deployment, not a supported compatibility matrix proven by this audit.

Elasticsearch port 9201 is explicitly reference-specific; Wazuh Indexer port 9200 identifies a separate service in that deployment. Elastic Agent telemetry remains separate. No Python SOC Automation Service, Automated Cybersecurity Remediation Platform, SOAR vendor or remediation dependency exists. The WordPress Docker volume path is deployment-specific and must be evaluated locally without silently editing these source expressions.

Native `timestamp` must have a compatible date mapping; `type.keyword` must have a compatible category mapping. The guides document keyword subfields, all 15 required fields, mapping conflicts, missing-field and optional-join behaviour, ingestion timing and equal-time ordering. No unsupported cross-version or Elastic Security feature compatibility is asserted.

## 8. Documentation corrections and evidence claims

The README now makes experimental status and source-publication suitability prominent, links the current evidence and disclaims official affiliation. Historical reports remain snapshots; Phase 2 explicitly points to this superseding publication decision. No historical count was altered.

Validation evidence is separated into A: earlier-version historical execution; B: offline repository/source checks; C: final-expression Elasticsearch execution (not performed); D: final-expression synthetic positives/negatives (pending, no reproducible suite supplied); E: operational Kibana activation (not performed or claimed). Earlier WEB-002 synthetic summaries are not evidence for the final complete pack.

Kibana guidance retains index `wazuh-alerts-4.x-*`, timestamp `timestamp`, category `type.keyword`, initial schedule 5 minutes, initial additional look-back 1 minute, suppression Disabled initially and actions None initially. These are provisional starting values. `maxspan` does not extend the search window automatically; a short execution window can miss long sequences. Sequence coverage, effective execution window, overlaps, duplicate alerts, suppression, field mappings and missing-field behaviour require lab checks. Version-specific UI/API settings must be confirmed before disabled rule creation.

## 9. Offline verification

Baseline: 12 tests run, 11 passed, 1 optional external-source comparison skipped; no failures or errors. Final suite: 13 tests run, 12 passed, the same 1 skipped; no failures or errors. Standard library only; no dependency installation.

Checks cover exact inventory, rule metadata, required-field extraction, maxspan, source hashes, revised join/filter contracts, configuration variables, licence markers, sensitive-content patterns, address/path/payload hygiene, local documentation links and publication-manifest checksums. Final checksum verification includes the audit report and modified test source. Source checks are structural, not full Elasticsearch syntax validation. Documentation URL targets were not fetched; local relative links were checked offline.

Git diff --check is not applicable because there is no Git repository. An offline whitespace scan found no trailing whitespace or missing final newlines in changed/new text files. No Git staging, commit, push or repository creation occurred.

## 10. Security findings

All 49 publication files were included in content review and offline scanning. No usable embedded password/token, private key, certificate bytes, non-loopback address literal, private infrastructure endpoint, personal contact detail, production hostname, raw Wazuh alert, database content, private repository reference, private user absolute path, shell history or temporary execution log was identified. No sensitive-content removal was required. No Git directory/history/configuration exists to scan. Reference system paths, root account predicates, localhost URLs and the WordPress volume name are intentional source context.

Automated pattern checks and manual review provide bounded evidence, not a guarantee against every possible secret. Re-scan any later added files or Git history before release. Operational secrets, real alerts, keys/certificates, checkpoints, queues, logs, local environments and editor scratch files are publication exclusions; none is required for the reference source distribution.

## 11. Licence and GitHub presentation

Apache-2.0 licence text is present and unchanged. The ignore file covers local secrets, certificate/key extensions, alert/log data, checkpoints, queues, Python artefacts and now editor scratch files. README supplies purpose, architecture, reference versions, guide links, test command, experimental limits and independence. Contributor guidance covers safe evidence, source review and checksum maintenance. No misleading badge or official-affiliation claim is added. Third-party software licensing and feature entitlement remain deployment considerations. No remote repository or publication was created.

## 12. Publication manifest

[PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json) is deterministic UTF-8 JSON with sorted keys, two-space indentation and a final newline. It records the project, reference versions, complete rule metadata, source paths/digests, complete publication inventory, documentation inventory, initial file checksums, final file checksums, offline/live status, limitations, exclusions and readiness verdict. It contains no credentials or production identifiers. The manifest excludes only its own digest; every other publication file is hashed.

## 13. Remaining publication blockers

None identified for experimental source publication. Missing live execution, synthetic efficacy evidence and operational integration are disclosed limitations, not prerequisites to publishing this experimental source. They prevent detection-validated and production-ready claims.

## 14. Separate operational validation requirements

In a separately authorised isolated lab, check installed software/plugins, Logstash configuration parsing, file permissions/rotation, TLS, ingestion, all required mappings and native timestamp/category settings. Execute each exact pinned EQL definition with labelled positive and negative fixtures. Prioritise PRIV-001 present/missing third-stage usernames and MAL-001 matching/mismatching executable paths and the excluded carriage-return anomaly. Test cross-agent/source joins, maintenance negatives, realtime versus scheduled FIM, deployment paths, missing fields, equal timestamps, ingestion delay and maxspan boundaries.

Only after query evidence is recorded, review disabled Kibana rule creation, effective query windows and long-sequence coverage, overlapping searches, duplicate documents/alerts, suppression and execution gaps. Activation and any production-readiness decision require separate evidence and authorisation. This audit made no network, production, SSH, database or service access and no Elasticsearch/Kibana calls, activation or remediation.

## 15. Exact recommended next step

For operational evaluation, arrange a separately authorised isolated-lab validation using the pinned source digests, starting with PRIV-001 missing-username joins and MAL-001 executable-path joins, then all 14 labelled positive/negative cases. Keep rules disabled and actions absent. Source publication can proceed independently as an experimental reference; release the reviewed manifest-listed tree with its explicit limitations when publication is separately requested.
