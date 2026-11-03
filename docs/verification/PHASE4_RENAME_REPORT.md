# Phase 4 — project rename and final consistency audit

Audit date: 3 November 2026. Scope: the renamed project tree only; offline review, no external source access.

## 1. Rename completion verdict

**COMPLETE.** Current project identity is consistent. The Phase 3 publication-ready experimental baseline is preserved. Initial review verified every Phase 3 final file digest before edits. The only literal old repository-name reference was the publication manifest's `project_name`; the README also used the former display title. No filenames, configuration examples, scripts, tests or intended GitHub URLs required a repository-name replacement. No GitHub URL was supplied or invented, and no publication occurred.

## 2. New project identity

- Title: **Wazuh EQL Correlation**.
- Project identifier and directory basename: `wazuh-eql-correlation`.
- Description: Multi-stage security alert correlation for Wazuh using Elasticsearch EQL, with Logstash ingestion, detection rules and deployment guidance.

Architecture remains Wazuh JSON alerts → Logstash → Elasticsearch → Elastic Security EQL. Native Wazuh fields, existing index naming, verified TLS, all Logstash configuration bytes, 14 EQL definitions, rule identifiers, rule metadata and Apache-2.0 licensing are preserved. No ECS normalisation was introduced.

## 3. Files modified

- `README.md`: exact title, description, identifier and current report link.
- `CONTRIBUTING.md`: current title and identifier.
- `docs/installation.md`: current project identity and overview link.
- `docs/configuration.md`: current project identity and overview link.
- `docs/architecture.md`: current project identity and overview link.
- `docs/security.md`: current identity and current/historical audit links.
- `tests/validate_repository.py`: identity consistency and Phase 3 preservation checks.
- `docs/verification/PUBLICATION_MANIFEST.json`: current identity, Phase 4 inventory, checksums, verification results and retained Phase 3 baseline metadata.

Created: `docs/verification/PHASE4_RENAME_REPORT.md`. No files were deleted or renamed. Initial inventory: 49 files; final inventory: 50 files.

## 4. Historical references retained

The old identifier `wazuh-elastic-security-correlation` is retained only as the former identity in `phase3_audit_metadata.project_name` and in this traceability explanation. It is not an operational directory or GitHub target. The Phase 1, Phase 2 and Phase 3 reports remain byte-for-byte unchanged, including their historical counts, evidence limitations, inventories and verdicts.

The publication manifest preserves `initial_sha256` as the Phase 3 initial inventory and `phase3_baseline_sha256` as the Phase 3 final inventory. Former created/modified lists and offline results are retained under `phase3_audit_metadata`; top-level lists/results describe Phase 4. The former README display title is recorded by its preserved Phase 3 digest. Generic service paths such as `wazuh-correlation.env` and the optional source-document filename identify deployment/source artefacts, not the former repository, and remain unchanged. Historical technical facts were not altered.

## 5. EQL checksum verification

**PASS: 14/14 EQL files match their recorded Phase 3 SHA-256 digests before and after editing.** No unexpected discrepancy occurred. Tests also compare the unchanged rule-manifest digests with the retained Phase 3 baseline and current source checksums. No EQL expression, whitespace or byte changed.

All 14 rule documentation files, `tests/rule-manifest.json`, the three Logstash files and `LICENSE` also remain byte-for-byte identical to Phase 3. The Apache-2.0 licence SHA-256 remains `5c9817c129b98e7bb966bca028c43c19107102ef8e03fe799bffb4354f4ef015`.

## 6. Publication manifest verification

**PASS.** The manifest identifies the current project and includes all 50 publication paths, the complete documentation inventory, all 14 unchanged rule records and SHA-256 hashes of the other 49 files, including this report. Its own digest is excluded to avoid recursion. Current source-file checksums include the modified test script; unchanged EQL and Logstash digests retain their Phase 3 values. JSON remains sorted, two-space indented UTF-8 with a final newline. Historical hash inventories are explicitly distinguished from current hashes.

## 7. Offline test results

Command: `python3 tests/validate_repository.py`, with `WCORR_SOURCE_FILE` unset.

- Baseline: 13 tests run; 12 passed, 1 optional external-source comparison skipped.
- Final: 15 tests run; 14 passed, the same optional comparison skipped; 0 failures and 0 errors.
- Exactly 14 sources, required metadata, IDs, fields, correlation windows, byte integrity, native configuration contracts, relative documentation links, identity, manifest inventory/checksums and preservation checks pass.
- Whitespace check: all modified/new text files have final newlines and no trailing whitespace.
- `git diff --check`: not applicable; the tree has no Git metadata. No Git repository was initialised.

Standard library only; no dependencies installed or network accessed. These are structural and integrity checks, not Elasticsearch syntax execution or detection-efficacy tests. External documentation URLs were not fetched.

## 8. Security review

**No publication-sensitive material identified in the 50-file tree.** Offline content checks and review found no production IP addresses, usable embedded credentials, private keys/certificate bytes, sensitive logs, real infrastructure identifiers, personal absolute paths or stale operational references to the old repository directory. Relative documentation links resolve inside the project. No symlinks or unexpected runtime artefacts were found.

Only localhost endpoints, reference service paths, unusable CHANGE_ME placeholders and existing detection context remain. The root-account predicates and WordPress volume path are preserved technical source context. Pattern scans and review provide bounded evidence, not proof that every possible secret is absent. Any later additions or Git history require another release-tree review.

No production access, service changes, package installation, network calls, EQL modifications, Git staging/commits/pushes, GitHub repository creation or publication occurred.

## 9. Remaining publication blockers

**None identified for experimental source publication.** No remote publication destination is asserted. Final-expression Elasticsearch execution, reproducible synthetic positive/negative evidence and operational integration remain absent. These prevent detection-validation and production-readiness claims; they do not block publication of this explicitly experimental source.

## 10. Final publication-readiness classification

| Classification | Verdict |
| --- | --- |
| Source complete | Yes — exactly 14 definitions with metadata |
| Offline verified | Yes — structural, integrity, link and security checks |
| Publication ready | Yes — experimental reference implementation with explicit limitations |
| Detection validated | No — final-expression execution and reproducible efficacy tests pending |
| Production ready | No — detection and deployment behaviour unestablished |
| Published | No |

## 11. Exact next step

On a separate explicit publication request, select the actual destination and release the reviewed manifest-listed `wazuh-eql-correlation` tree as an experimental Apache-2.0 reference with its limitations intact. No publication action is authorised by this audit.

For detection evaluation, the next technical step is a separately authorised isolated lab: execute the exact pinned PRIV-001 missing-username and MAL-001 executable-path cases first, then labelled positive/negative cases for all 14 definitions. Verify mappings, ingestion/TLS, query-window coverage and duplicate handling. Keep rules disabled and actions absent until separate evidence supports activation. Publication readiness does not establish detection validation or production readiness.
