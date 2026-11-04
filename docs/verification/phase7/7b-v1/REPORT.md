# Phase 7B — native Elasticsearch qualification

Native execution qualification is COMPLETE for all 14 frozen v1.0.0 rules in the recorded production window: **14 successful executions, 3 positive rules, 11 valid zero-match rules, 0 blocked or incompatible rules**. Seventeen sequences were returned. This establishes native execution compatibility; complete positive coverage and production readiness remain unqualified.

Recorded in a fixed bounded historical production window; exact execution/event dates and dated index references are withheld for publication. Logical index pattern: `wazuh-alerts-4.x-*`.

## Integrity and authenticated access

Reviewed the existing Phase 7A report, inspection plan and prior Phase 7B reports. All 14 SHA-256 hashes match the frozen manifest and query bytes match local tag v1.0.0. The manifest also matches the tag. Revalidated again after execution. No frozen sources or manifest were modified. The local tag is an integrity anchor, not independent attestation.

TLS chain and hostname verification and authenticated native access succeeded. Root and detailed mapping inspection were permission-denied; server version remains operator-supplied and independently unconfirmed. Infrastructure and credential-source details are withheld. No credential or permission changes were attempted.

## Request scope and completeness

Each final EQL request uses the exact frozen source text, timestamp_field=timestamp and event_category_field=type.keyword. All joins, stage ordering and maxspan remain unchanged. A fixed outer timestamp filter bounds production scope. Requests ran sequentially with size=10, fetch_size=100, allow_partial_search_results=false and allow_partial_sequence_results=false. Initial wait was bounded by wait_for_completion_timeout=45s and client socket timeout=55s; the initial-wait setting is not a hard engine-runtime timeout. All queries completed synchronously with explicit timed_out=false, is_partial=false and is_running=false. All final EQL responses were HTTP 200.

Initial request wrappers were rejected before EQL execution: 15 requests rejected unsupported timeout (including one diagnostic), followed by 14 rejecting unsupported _source. Removing those wrapper properties resolved the harness errors without editing any query. These are not rule incompatibilities. Sanitised historical request bodies are in results.json; exact time filters and execution timings are withheld. They are not replayable requests.

Population and field-capability inspection was performed. Production population sizes, agent cardinality, shard/index details and retention dates are withheld for publication; no inference of continuous retention is supported.

## Per-rule results

| Rule | Execution | Qualification | Returned sequences  |
| --- | --- | --- | ---:  |
| WCORR-SSH-001 | PASS | POSITIVE | 1  |
| WCORR-SSH-002 | PASS | POSITIVE | 6  |
| WCORR-SSH-003 | PASS | ZERO_MATCHES | 0  |
| WCORR-SSH-004 | PASS | ZERO_MATCHES | 0  |
| WCORR-SSH-005 | PASS | ZERO_MATCHES | 0  |
| WCORR-WEB-001 | PASS | POSITIVE | 10  |
| WCORR-WEB-002 | PASS | ZERO_MATCHES | 0  |
| WCORR-WEB-003 | PASS | ZERO_MATCHES | 0  |
| WCORR-WEB-004 | PASS | ZERO_MATCHES | 0  |
| WCORR-PRIV-001 | PASS | ZERO_MATCHES | 0  |
| WCORR-PERS-001 | PASS | ZERO_MATCHES | 0  |
| WCORR-PERS-002 | PASS | ZERO_MATCHES | 0  |
| WCORR-EVAS-001 | PASS | ZERO_MATCHES | 0  |
| WCORR-MAL-001 | PASS | ZERO_MATCHES | 0  |

Zero matches are valid executions, not rule failures. WEB-001 reached the size=10 cap; its hits.total=10/relation=eq describes the bounded response and does not prove only ten sequences exist. Counts are returned sequences, not exhaustive detection volumes.

## Positive evidence and preserved historical qualification

- **WCORR-SSH-001**: representative ordered IDs 5712 → 5715; exact timestamps withheld.
- **WCORR-SSH-002**: representative ordered IDs 5715 → 5402; exact timestamps withheld.
- **WCORR-WEB-001**: representative ordered IDs 31151 → 31105; exact timestamps withheld.

The prior user-established SSH-001 PASS is preserved separately in results.json: ordered IDs 5712 → 5715, same agent/source IP, approximately 850 seconds within 15 minutes, different usernames. Its exact production date and identifiers are withheld. The original historical response remains unavailable. The current native result corroborates the ordered IDs and approximately 850.496-second interval. Account compromise is not established.

Production event IDs, join values (including deterministic hashes), exact timestamps and concrete index dates are withheld without replacement aliases. Ordered event rule IDs and sequence structure remain. Relative event offsets in results.json are calculated from original timestamps and preserve sequence timing without exposing absolute event times. No full event payload is published. Historical provenance, interval and account-compromise limitations remain explicit.

## Native field evidence

Production field-capability and population detail is withheld for publication. Required query fields remain documented per rule in results.json and the Phase 7A field contract; requirements do not assert production field availability. Successful cross-index execution does not establish complete per-index population or full stage-predicate qualification. Detailed mapping settings remain unverified because inspection was denied. An absent event does not prove disabled collection.

## Correlation limitations

All rules join agent.id.keyword. Shared identifiers, including shared manager identifiers, can associate unrelated users or services. Agent/time proximity does not prove actor, session, process or causal continuity. Routine administration can match; a positive sequence is an investigative signal rather than a confirmed attack. Timestamp ties lack a published tiebreaker; ingestion delay and scheduled FIM detection times can affect attribution.

- **WCORR-SSH-001**: Same agent and source IP do not prove account compromise or matching usernames: failures use data.srcuser and successes data.dstuser. An unrelated success from another IP cannot complete the sequence.
- **WCORR-SSH-002**: SSH and sudo users are not equated. Substring matching can miss shells and alternative commands. This contextual rule overlaps PRIV-001 and PERS-001; prefer their additional evidence. Routine administration can match.
- **WCORR-SSH-003**: Realtime FIM reduces timing ambiguity but does not identify a process or SSH session. Scheduled-only monitoring is excluded and must remain covered by separate FIM alerts.
- **WCORR-SSH-004**: Agent and time correlation does not prove actor or session continuity. Unlike SSH-003 this source has no realtime FIM predicate; scheduled observation timing can misattribute changes. Legitimate administration can match.
- **WCORR-SSH-005**: SCP command telemetry and FIM are joined only by agent and time; no transferred-file, user or session equality is enforced. Scheduled FIM and legitimate transfers can match.
- **WCORR-WEB-001**: Same recorded client IP does not confirm exploitation. Historical attribution is uncertain because client/server address ambiguity was reported; reverse proxies can link unrelated activity.
- **WCORR-WEB-002**: PHP creation is joined by endpoint and time, not HTTP client identity; causality is unproven. Legitimate deployments can create PHP files.
- **WCORR-WEB-003**: Investigative correlation only: HTTP 200 does not prove exploitation. FIM detection time may differ from creation time, and legitimate deployments may match.
- **WCORR-WEB-004**: The requested PHP URL is not verified against the exact created file. Nested upload paths are included; the request stage deliberately has no rule-ID restriction, allowing other classifications including 31101.
- **WCORR-PRIV-001**: The source says the optional third-stage key accommodates missing data.srcuser and that account creation remains associated by agent and time. Optional-field syntax does not itself guarantee wildcard joining: missing values can become null and fail to join a non-null username. Verify this claim in the target engine; do not silently change the query. SSH-to-sudo attribution is stronger, but account creation causality remains unproven. sudo su followed by useradd in a root shell is intentionally excluded.
- **WCORR-PERS-001**: Legitimate cron administration can produce the same sequence; agent and time do not establish actor continuity.
- **WCORR-PERS-002**: A service failure after a unit-file change does not establish causality. Legitimate service installation and maintenance can match.
- **WCORR-EVAS-001**: Legitimate audit-service maintenance can match this potentially significant defence-evasion sequence.
- **WCORR-MAL-001**: Requires rootcheck to expose the same executable path in data.file.keyword; population outside the recurring anomaly is unestablished. Realtime-only FIM excludes scheduled observations and reduces coverage. Matching paths and timing do not establish malware execution.

## Remaining gaps and exact next phase

Eleven rules lack positive native sequences in this production window; their zero-match results remain valid. Controlled positive and negative coverage remains needed for all rules, particularly PRIV optional/null username joins, MAL exact path equality and exclusion isolation, arrays, equal timestamps, competing candidates, maxspan boundaries and benign collisions. Shared-agent attribution, proxy IP provenance, scheduled FIM, delayed arrival, search scheduling and deduplication require evaluation. WEB-001's exhaustive volume is unknown. Detailed mappings and independent server version confirmation remain permission-limited. No production remediation is proposed.

**Exact recommended next phase: Phase 7C — isolated laboratory semantic and positive/negative sequence validation of the unchanged v1.0.0 catalogue.** Use separately authorized isolated fixtures to close these gaps. Do not proceed to production deployment, detection activation or automatic Kibana Case publication.

Only Phase 7B REPORT.md and results.json were updated in the repository. No production writes, configuration changes, synthetic ingestion, Kibana Cases, rule activation or publication policies were performed. Existing unrelated untracked files were left in place.

## Publication sanitisation

This publication copy withholds operational identifiers and metadata; no replacement evidence or deterministic aliases were created. All 14/14 native executions, three positive and eleven zero-match classifications, returned sequence counts and WEB-001 result-cap limitation are unchanged. Production observations remain distinct from synthetic Phase 6 evidence. Historical recommendations above describe the original phase; the consolidated review supplies the later readiness assessment.
