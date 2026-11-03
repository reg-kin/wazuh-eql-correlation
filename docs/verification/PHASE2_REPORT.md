# Phase 2 verification report

Historical snapshot: its inventory and publication conclusions describe Phase 2. The [Phase 3 publication audit](PHASE3_PUBLICATION_AUDIT.md) supersedes the publication decision; historical findings are preserved.

## 1. Overall completion verdict

Source integration COMPLETE: exactly 14 complete EQL definitions, with no pending definitions. Offline repository validation PASS. Final-expression live EQL execution NOT_PERFORMED. Kibana activation readiness NOT_READY. GitHub publication readiness: sanitised source integration is ready for review as an unvalidated reference; publication as a validated detection pack is BLOCKED. No publication was performed.

## 2. Files modified or created

Created five SSH `.eql` files and this report. Modified all 14 rule metadata entries, PRIV-001 and MAL-001 EQL, manifest, offline tests, README, catalogue, validation, installation, configuration and security documentation. The Phase 1 report received only a historical-snapshot notice and replacement of its obsolete status token with descriptive text. Its findings and original inventory are retained. Seven existing EQL files, pipeline configuration, licence and unrelated work were preserved.

## 3. Rule identifiers and statuses

All rows have COMPLETE_SOURCE, offline repository checks PASS and final execution NOT_PERFORMED. Every rule requires lab validation before activation.

| Rule | Phase 2 change | Maxspan | Severity / risk | Activation |
| --- | --- | --- | --- | --- |
| WCORR-SSH-001 | RECOVERED | 15m | High / 73 | LAB_VALIDATION_REQUIRED |
| WCORR-SSH-002 | RECOVERED | 15m | Medium / 47 | LAB_VALIDATION_REQUIRED |
| WCORR-SSH-003 | RECOVERED | 30m | High / 70 | LAB_VALIDATION_REQUIRED |
| WCORR-SSH-004 | RECOVERED | 30m | High / 78 | LAB_VALIDATION_REQUIRED |
| WCORR-SSH-005 | RECOVERED | 30m | Medium / 62 | LAB_VALIDATION_REQUIRED |
| WCORR-WEB-001 | UNCHANGED | 10m | Medium / 55 | LAB_VALIDATION_REQUIRED |
| WCORR-WEB-002 | UNCHANGED | 10m | High / 82 | LAB_VALIDATION_REQUIRED |
| WCORR-WEB-003 | UNCHANGED | 10m | High / 85 | LAB_VALIDATION_REQUIRED |
| WCORR-WEB-004 | UNCHANGED | 30m | High / 80 | LAB_VALIDATION_REQUIRED |
| WCORR-PRIV-001 | REVISED | 30m | High / 82 | LAB_VALIDATION_REQUIRED |
| WCORR-PERS-001 | UNCHANGED | 30m | High / 78 | LAB_VALIDATION_REQUIRED |
| WCORR-PERS-002 | UNCHANGED | 30m | Medium / 60 | LAB_VALIDATION_REQUIRED |
| WCORR-EVAS-001 | UNCHANGED | 20m | High / 80 | LAB_VALIDATION_REQUIRED |
| WCORR-MAL-001 | REVISED | 60m | High / 75 | LAB_VALIDATION_REQUIRED |

## 4. SSH source recovery

All five SSH expressions recovered. SSH-001 preserves same-agent/source-IP joining; SSH-002 uses the designated Dev Tools expression; SSH-003 preserves realtime FIM; SSH-004 preserves its three stages without adding realtime filtering; SSH-005 preserves scp audit telemetry and agent-level joining. Full names, descriptions, windows, severity, risk, required fields, limitations and prerequisites appear in each entry and the manifest. No ECS normalisation was introduced.

## 5. Differences from Phase 1

Five previously missing executable definitions are now present. Seven of the nine existing definitions are token-identical to source and remain byte-for-byte unchanged: WEB-001–004, PERS-001–002 and EVAS-001. PRIV-001 and MAL-001 changed. Metadata, scheduling guidance and tests now cover 14 complete definitions. Historical counts remain explicitly scoped to earlier versions.

## 6. Revised PRIV-001 and MAL-001

PRIV-001 preserves global agent joining, stage-one data.dstuser, stage-two data.srcuser, root target, useradd/adduser command predicates and optional third-stage ?data.srcuser. The source's claim about missing third-stage usernames needs runtime verification: optional fields can yield null, which need not join a non-null username. Do not assume wildcard semantics. sudo su followed by useradd in a root shell is intentionally outside coverage. Historical count 2 is not evidence for this revision.

MAL-001 now requires realtime FIM on executable paths, joins syscheck.path to rootcheck data.file, requires a non-null rootcheck path and excludes the exact recurring /dev/null finding with a carriage-return escape. Rootcheck path population beyond the anomaly remains unestablished. Scheduled FIM is excluded. Historical count 7 is not evidence for this revision. Neither revised rule has passed live or isolated-lab execution here.

## 7. Source inconsistencies

SSH-002 standalone requires two additional null predicates: SSH destination username and sudo command. Dev Tools omits both and is the designated expression. The complete standalone alternative is documented in the SSH-002 entry. Both lack same-user equality despite the source recommendation. SSH-003's two forms differ only in layout. PERS-002 contains an incorrect cron heading; the systemd name, description and expression are retained. PRIV-001 optional-key prose is an unverified semantic claim. SSH-004/005 retain scheduled-FIM exposure absent in SSH-003. Historical execution summaries lack full requests, responses, dates, mappings and reproducible evidence. No conflict was silently reconciled.

## 8. Metadata completeness and deployment

All 14 entries contain source names/descriptions, severity/risk, windows, field inventory, limitations, prerequisites and evidence status. MAL-001 has no separately labelled source description; its revision rationale is used verbatim. Index wazuh-alerts-4.x-*, timestamp field timestamp, category type.keyword. Recommended initial schedule 5 minutes, additional look-back 1 minute, suppression disabled, actions none. These are starting values only. maxspan bounds sequences within searched events; it does not enlarge a scheduled search window. Validate effective window coverage, ingestion delays, overlaps, deduplication and alert suppression before activation.

## 9. Offline test results

Original Phase 1 suite: 10 tests PASS before changes. Extended suite: 12 tests PASS, including direct source comparison using WCORR_SOURCE_FILE, exactly 14 definitions/identifiers, complete metadata/fields, digests, native predicates and join preservation, absence of pending markers, security scans and documentation links/inventory. The default command also passes, with only the optional external-source comparison skipped. Python standard library only. Structural checks are not full Elasticsearch syntax validation. No EQL parser was invoked; no final-expression runtime or efficacy test was performed.

## 10. Security review

The complete external source was read; its production public address was omitted from repository artefacts. Source remains outside the repository and was not copied in. Offline scans found no non-loopback literal IP addresses, embedded credential patterns, private-key/certificate material, raw alert payloads or user home paths. No production credentials, private hostnames or personal information were introduced. Pattern scans cannot prove absence of every possible secret; publication review remains appropriate.

No network, SSH, package installation, production access, service changes, Elasticsearch/Kibana requests, activation, remediation, Git staging/commit/push or GitHub publication occurred. This workspace has no Git metadata, so a Git diff/status comparison is unavailable; comparison used the initial file inventory, existing query bytes and source tokens.

## 11. Outstanding validation requirements

A: Historical executions of earlier versions remain supplied context only; size 10 caps and incomplete provenance prevent efficacy conclusions. Source WEB-002 mentions earlier synthetic positives/negatives without reproducible fixtures.

B: Offline final-expression integrity and preservation checks pass; they establish repository consistency only.

C: All 14 final expressions still require separately authorised isolated-lab parser/execution testing with labelled positive and negative fixtures, field capabilities, timestamp/category overrides, missing-field joins, timing boundaries and ingestion delays. Verify rootcheck executable paths, realtime monitoring and deployment-specific WordPress paths. No new positive detections or installed/enabled Kibana rules are claimed.

## 12. Publication blockers

No source-recovery blocker remains. Claims of a validated detection pack are blocked by missing final-expression lab evidence, PRIV-001 optional-join uncertainty, MAL-001 rootcheck path availability, effective query-window and deduplication validation, deployment compatibility and false-positive review. Sanitised reference publication requires an explicit review and publication decision; none is authorised here.

## 13. Exact recommended next step

Arrange a separately authorised, disconnected isolated-lab validation of these pinned source digests. First test PRIV-001 with present and absent third-stage usernames and MAL-001 with matching/mismatching executable paths and the excluded anomaly. Then execute all 14 with labelled positive/negative and timing-boundary fixtures, record sanitised evidence, and verify disabled Kibana rule window/deduplication settings before any activation decision.

## Repository inventory after Phase 2

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
- `docs/verification/PHASE2_REPORT.md`
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
- `rules/ssh/WCORR-SSH-001.eql`
- `rules/ssh/WCORR-SSH-001.md`
- `rules/ssh/WCORR-SSH-002.eql`
- `rules/ssh/WCORR-SSH-002.md`
- `rules/ssh/WCORR-SSH-003.eql`
- `rules/ssh/WCORR-SSH-003.md`
- `rules/ssh/WCORR-SSH-004.eql`
- `rules/ssh/WCORR-SSH-004.md`
- `rules/ssh/WCORR-SSH-005.eql`
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
