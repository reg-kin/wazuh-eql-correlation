# Phase 6A qualification and repository integration

This addendum supersedes the repository-integration blocker in the retained
[execution report](REPORT.md). The original report, results, regression log,
fixtures, harness and integrity snapshot remain unchanged. Their statements
about the original run remain historical facts. No engine rerun was performed.

## Validation contract and commands

The frozen Phase 4 manifest contains exactly 50 publication paths. Its SHA-256
map covers the other 49 files, excluding itself. The original validator requires
exact candidate-set equality, exact Markdown inventory, every listed digest,
rule-manifest equality and publication/readiness flags. Candidate scanning
excludes only Git internals and Python bytecode directories. The manifest's own
bytes are additionally compared to the local v1.0.0 tag by development validation.

The original validator is itself hashed by the manifest. It remains unchanged.
New Phase 6 files caused an inventory mismatch; this was not a rule or hash
failure. The historical validator must still reject those files in a purported
release tree. Running it directly on development therefore still fails by design.

Run these offline commands from the repository root:

```bash
python3 tests/validate_development.py --historical
python3 tests/validate_development.py
python3 -m unittest discover -s tests -p 'test_phase6*.py' -v
```

Historical mode copies the entire local v1.0.0 tag into a temporary directory
and runs the original validator there. It does not filter tag contents against
the manifest, so unexpected release files remain errors. Development mode runs
all inherited repository checks over the entire current tree. Only the
publication test first requires exact equality to the frozen inventory plus an
explicit list of 13 development paths, then applies the original publication
checks to the historical subset. No prefix or wildcard exempts new files. All
49 historical digests are still mandatory. This preserves every release byte,
including the old validator, metadata, detection descriptions and manifest.
The optional external-source check remains skipped without WCORR_SOURCE_FILE.

## Qualification expectations

[qualification.json](../../../tests/fixtures/phase6/qualification.json) pins the
retained results digest and separately defines offline regression assertions.
These expectations were written after observation; they are not independent
predeclared engine tests. The original 35 outcomes remain 31 PASS, four
INCONCLUSIVE and zero FAIL. All 35 retained observations now have explicit
qualification assertions; assertion success is separate from detection coverage.

For priv-exact-window, the three ordered event IDs match at exactly 1800 seconds.
For mal-exact-window, the two ordered event IDs match at exactly 3600 seconds.
Both are explicit inclusive-boundary regression expectations for these fixtures
on Elasticsearch 8.19.20. Existing inside/outside fixtures match at 1799/3599
seconds and return no match at 1801/3601 seconds. No general claim about other
versions, equal timestamps or scheduling is made.

PRIV optional-username coverage limitation: priv-optional-user-absent and
priv-optional-user-null both return zero sequences despite preceding stages
sharing the non-null username labuser. The third-stage optional join does not
provide a wildcard match for that username. The separate qualification assertion
expects absence, classified as known_semantic_limitation. Its success confirms
the limitation; neither scenario is successful detection. Intended detection
coverage when the final username is absent or null remains unachieved. This is
fixture-scoped evidence, not proof of all possible null-join combinations.
Published PRIV-001 remains unchanged.

The two MAL /dev/null plus carriage-return cases retain their successful
no-sequence assertions. They do not independently validate the exclusion
predicate: stage-2-only substitution also breaks the path join; substitution in
both stages violates the executable-directory predicate. Isolated exclusion
coverage remains unproven for scalar paths. Multivalued paths were not tested.
No predicate rewrite or additional engine query was used.

## Preservation, scope and readiness

Qualification tests check retained response status/completeness, ordered event
IDs, exact stored fixture sources, refresh success, field capabilities, rule
hashes and retained index inventory. Negative offline tests verify rejection of
unexpected release files, missing release files, corrupted release bytes and
unlisted development files. Temporary test copies are the only modified copies
of release artifacts; retained evidence and Elasticsearch indices are untouched.

This qualification is limited to the two published queries and synthetic local
fixtures. Production efficacy, native Wazuh mappings, deployment scheduling,
equal-timestamp ordering and other rules remain unqualified. Phase 6B can be
considered only as a separately authorized next phase with these limitations
carried forward. This work does not begin Phase 6B or establish production
readiness. No production connection, service change, Docker change, restart,
package installation, credential retrieval, commit, push, publication or tag is
part of qualification.

## Recorded qualification results

Historical validation: 15 tests, 14 passed, one optional external-source skip.
Development validation: 15 tests, 14 passed, the same optional skip.
Offline Phase 6 tests: eight passed, including four new qualification tests.
The 35 retained scenario assertions all agree with qualification expectations.
The original validator on the development tree still produces its expected
publication-inventory failure; it is now explicitly a release-only entry point.
There are no failures in the applicable historical, development or qualification
suites. No overall detection PASS is claimed: optional-username coverage and
isolated MAL exclusion coverage remain limitations.

All 50 publication files compare byte-for-byte with the local v1.0.0 tag; all
49 manifest-covered SHA-256 values agree. All 14 EQL files and their companion
metadata, tests/rule-manifest.json and the frozen publication manifest remain
unchanged. Git diff --check succeeds, and no tracked file was modified.
