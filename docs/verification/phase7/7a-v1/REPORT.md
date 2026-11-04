# Phase 7A — native telemetry contract assessment

A. Overall assessment

All 14 frozen queries are inventoried: 34 ordered stages, 13 EQL leaf fields plus timestamp/category metadata (15 total), and 26 distinct Wazuh rule IDs. Native compatibility is UNVERIFIED; production readiness is NOT ASSESSED. This development-only assessment used repository evidence only. No EQL or Elasticsearch request was executed.

B. Publication integrity

All 50 publication files, including the manifest, are byte-identical to local v1.0.0. All 14 exact EQL byte hashes are retained in field-contract.json. The local tag is a historical repository anchor, not an external signed attestation. Preexisting untracked Phase 6 files were present at baseline; they were included in the preservation digest inventory. The only existing file authorized for modification is the development validator, with six explicit inventory additions.

C. Complete 14-rule telemetry matrix

Every stage below is `any`; no category value, HTTP status or method is implicitly required. ID sets are alternatives within the stage. The exact predicates below govern requirements, independently of names. All production availability is UNVERIFIED.

| Rule | Ordered stage IDs | Global joins | Stage joins | Maxspan |
| --- | --- | --- | --- | --- |
| WCORR-EVAS-001 | 5402, 5407 → 80705 → 80703 | agent.id.keyword | none | 20m |
| WCORR-MAL-001 | 550, 554 → 510, 521 | agent.id.keyword | 1: syscheck.path.keyword; 2: data.file.keyword | 60m |
| WCORR-PERS-001 | 5715 → 2834 → 550, 554 | agent.id.keyword | none | 30m |
| WCORR-PERS-002 | 5715 → 550, 554 → 40704 | agent.id.keyword | none | 30m |
| WCORR-PRIV-001 | 5715 → 5402, 5407 → 5902 | agent.id.keyword | 1: data.dstuser.keyword; 2: data.srcuser.keyword; 3: ?data.srcuser.keyword | 30m |
| WCORR-SSH-001 | 5712, 5763 → 5715 | agent.id.keyword, data.srcip.keyword | none | 15m |
| WCORR-SSH-002 | 5715 → 5402, 5407 | agent.id.keyword | none | 15m |
| WCORR-SSH-003 | 5715 → 550, 554 | agent.id.keyword | none | 30m |
| WCORR-SSH-004 | 5715 → 5402, 5407 → 550, 554 | agent.id.keyword | none | 30m |
| WCORR-SSH-005 | 5715 → 92603 → 550, 554 | agent.id.keyword | none | 30m |
| WCORR-WEB-001 | 31151, 31515, 31516 → 31103, 31104, 31105, 31110, 31164, 31166, 31168 | agent.id.keyword, data.srcip.keyword | none | 10m |
| WCORR-WEB-002 | 31151, 31103, 31104, 31105 → 554 | agent.id.keyword | none | 10m |
| WCORR-WEB-003 | 31106, 31110, 31166, 31168 → 554 | agent.id.keyword | none | 10m |
| WCORR-WEB-004 | 554 → unrestricted ID; URL predicate | agent.id.keyword | none | 30m |

Complete stage predicates (all stages also require their global join, timestamp ordering and configured metadata):

WCORR-EVAS-001:

```eql
sequence by agent.id.keyword with maxspan=20m
  [any where rule.id.keyword in ("5402", "5407")]
  [any where rule.id.keyword == "80705"
    and data.audit.type.keyword == "CONFIG_CHANGE"]
  [any where rule.id.keyword == "80703"]
```

WCORR-MAL-001:

```eql
sequence by agent.id.keyword with maxspan=60m
  [any where
    rule.id.keyword in ("550", "554") and
    syscheck.mode.keyword == "realtime" and
    (
      syscheck.path.keyword like "/usr/bin/*" or
      syscheck.path.keyword like "/usr/sbin/*" or
      syscheck.path.keyword like "/bin/*" or
      syscheck.path.keyword like "/sbin/*"
    )
  ] by syscheck.path.keyword
  [any where
    rule.id.keyword in ("510", "521") and
    data.file.keyword != null and
    data.file.keyword != "/dev/null\r"
  ] by data.file.keyword
```

WCORR-PERS-001:

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where rule.id.keyword == "5715"]
  [any where rule.id.keyword == "2834"]
  [any where rule.id.keyword in ("550", "554") and (
    syscheck.path.keyword like "/var/spool/cron/*" or
    syscheck.path.keyword like "/var/spool/cron/crontabs/*" or
    syscheck.path.keyword like "/etc/cron.d/*" or
    syscheck.path.keyword == "/etc/crontab"
  )]
```

WCORR-PERS-002:

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where rule.id.keyword == "5715"]
  [any where rule.id.keyword in ("550", "554") and (
    syscheck.path.keyword like "/etc/systemd/system/*.service" or
    syscheck.path.keyword like "/usr/lib/systemd/system/*.service" or
    syscheck.path.keyword like "/lib/systemd/system/*.service"
  )]
  [any where rule.id.keyword == "40704"]
```

WCORR-PRIV-001:

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where
    rule.id.keyword == "5715" and
    data.dstuser.keyword != null
  ] by data.dstuser.keyword
  [any where
    rule.id.keyword in ("5402", "5407") and
    data.dstuser.keyword == "root" and
    data.srcuser.keyword != null and
    (
      data.command.keyword like "*useradd*" or
      data.command.keyword like "*adduser*"
    )
  ] by data.srcuser.keyword
  [any where
    rule.id.keyword == "5902"
  ] by ?data.srcuser.keyword
```

WCORR-SSH-001:

```eql
sequence by agent.id.keyword, data.srcip.keyword with maxspan=15m
  [any where
    rule.id.keyword in ("5712", "5763") and
    data.srcip.keyword != null
  ]
  [any where
    rule.id.keyword == "5715" and
    data.srcip.keyword != null
  ]
```

WCORR-SSH-002:

```eql
sequence by agent.id.keyword with maxspan=15m
  [any where
    rule.id.keyword == "5715"
  ]
  [any where
    rule.id.keyword in ("5402", "5407") and
    data.dstuser.keyword == "root" and
    (
      data.command.keyword like "*useradd*" or
      data.command.keyword like "*usermod*" or
      data.command.keyword like "*passwd*" or
      data.command.keyword like "*visudo*" or
      data.command.keyword like "*systemctl disable*" or
      data.command.keyword like "*systemctl stop*" or
      data.command.keyword like "*crontab*" or
      data.command.keyword like "*chmod*" or
      data.command.keyword like "*chown*"
    )
  ]
```

WCORR-SSH-003:

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where rule.id.keyword == "5715"]
  [any where
    rule.id.keyword in ("550", "554") and
    syscheck.mode.keyword == "realtime" and
    (
      syscheck.path.keyword in (
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/gshadow",
        "/etc/sudoers"
      ) or
      syscheck.path.keyword like "/etc/sudoers.d/*" or
      syscheck.path.keyword like "/home/*/.ssh/authorized_keys" or
      syscheck.path.keyword == "/root/.ssh/authorized_keys"
    )
  ]
```

WCORR-SSH-004:

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where rule.id.keyword == "5715"]
  [any where rule.id.keyword in ("5402", "5407")]
  [any where
    rule.id.keyword in ("550", "554") and
    (
      syscheck.path.keyword in (
        "/etc/passwd",
        "/etc/shadow",
        "/etc/group",
        "/etc/gshadow",
        "/etc/sudoers"
      ) or
      syscheck.path.keyword like "/etc/sudoers.d/*" or
      syscheck.path.keyword like "/home/*/.ssh/authorized_keys" or
      syscheck.path.keyword == "/root/.ssh/authorized_keys"
    )
  ]
```

WCORR-SSH-005:

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where rule.id.keyword == "5715"]
  [any where
    rule.id.keyword == "92603" and
    data.audit.command.keyword == "scp"
  ]
  [any where rule.id.keyword in ("550", "554")]
```

WCORR-WEB-001:

```eql
sequence by agent.id.keyword, data.srcip.keyword
with maxspan=10m
  [any where rule.id.keyword in
    ("31151", "31515", "31516")
    and data.srcip.keyword != null]
  [any where rule.id.keyword in
    ("31103", "31104", "31105", "31110",
     "31164", "31166", "31168")
    and data.srcip.keyword != null]
```

WCORR-WEB-002:

```eql
sequence by agent.id.keyword with maxspan=10m
  [any where rule.id.keyword in
    ("31151", "31103", "31104", "31105")]
  [any where rule.id.keyword == "554"
    and syscheck.event.keyword == "added"
    and syscheck.path.keyword like
      "/var/lib/docker/volumes/web_wp_data/_data/wp-content/uploads/*.php"]
```

WCORR-WEB-003:

```eql
sequence by agent.id.keyword with maxspan=10m
  [any where rule.id.keyword in
    ("31106", "31110", "31166", "31168")]
  [any where rule.id.keyword == "554"
    and syscheck.event.keyword == "added"
    and syscheck.path.keyword like
      "/var/lib/docker/volumes/web_wp_data/_data/wp-content/uploads/*.php"]
```

WCORR-WEB-004:

```eql
sequence by agent.id.keyword with maxspan=30m
  [any where rule.id.keyword == "554"
    and syscheck.event.keyword == "added"
    and syscheck.path.keyword like
      "/var/lib/docker/volumes/web_wp_data/_data/wp-content/uploads/*.php"]
  [any where data.url.keyword != null
    and data.url.keyword like
      "/wp-content/uploads/*.php*"]
```

D. Required Elasticsearch field mappings

| Exact Elasticsearch path | Expected type | Source path / multifield |
| --- | --- | --- |
| agent.id.keyword | keyword | agent.id → keyword multifield |
| data.audit.command.keyword | keyword | data.audit.command → keyword multifield |
| data.audit.type.keyword | keyword | data.audit.type → keyword multifield |
| data.command.keyword | keyword | data.command → keyword multifield |
| data.dstuser.keyword | keyword | data.dstuser → keyword multifield |
| data.file.keyword | keyword | data.file → keyword multifield |
| data.srcip.keyword | keyword | data.srcip → keyword multifield |
| data.srcuser.keyword | keyword | data.srcuser → keyword multifield |
| data.url.keyword | keyword | data.url → keyword multifield |
| rule.id.keyword | keyword | rule.id → keyword multifield |
| syscheck.event.keyword | keyword | syscheck.event → keyword multifield |
| syscheck.mode.keyword | keyword | syscheck.mode → keyword multifield |
| syscheck.path.keyword | keyword | syscheck.path → keyword multifield |
| timestamp | date | timestamp |
| type.keyword | keyword | type → keyword multifield |

The expected date baseline and keyword leaves reproduce Phase 6 capabilities. A text parent is fixture design, not mandatory; the exact suffixed leaf is mandatory for unchanged queries. All mappings, populations and Wazuh alert meanings in production remain UNVERIFIED. Inspect searchable/index/doc_values capabilities and conflicts in every concrete index. `date_nanos` requires separate version-specific validation. No ECS or @timestamp substitution is authorized.

Every keyword leaf is subject to ignore_above: source presence does not prove indexed keyword presence. Long commands, URLs and paths are especially exposed. Inspect normalizers, null_value, aliases/runtime fields, object parents and nested structures; no nested query is supplied. Scalars were tested; arrays, empty arrays and arrays of objects need source inspection and later laboratory tests. No query normalizes case, whitespace, paths, usernames or IP strings. MAL compares paths exactly, including carriage-return distinction. No mapping change is proposed.

E. Wazuh rule-ID dependencies

| IDs | Telemetry dependency from publication/evidence | Availability |
| --- | --- | --- |
| 5402, 5407, 5902 | Sudo/privilege | UNVERIFIED |
| 80703, 80705, 92603 | Audit | UNVERIFIED |
| 550, 554 | FIM | UNVERIFIED |
| 510, 521 | Rootcheck | UNVERIFIED |
| 5712, 5715, 5763 | SSH authentication | UNVERIFIED |
| 2834 | Cron editor | UNVERIFIED |
| 40704 | Systemd/service | UNVERIFIED |
| 31103, 31104, 31105, 31106, 31110, 31151, 31164, 31166, 31168, 31515, 31516 | Web-server/application | UNVERIFIED |

rule-dependencies.json links every one of the 34 stages to its exact IDs, fields and joins, with a reverse index for every ID. ID meanings follow published evidence; installed Wazuh definitions, enabled rules and actual native population were not inspected. WEB-004 URL stage has no ID requirement; 31101 is an example classification, not a dependency.

F. Join and timestamp requirements

Every rule joins agent.id.keyword. SSH-001 and WEB-001 additionally require the same data.srcip.keyword across stages. PRIV-001 equates stage-1 dstuser with stage-2 srcuser and stage-3 optional-syntax srcuser; stage-2 dstuser must independently equal root. MAL-001 equates syscheck.path.keyword with data.file.keyword. No other stage joins, actor, session, process, service-name or transferred-file equalities are present.

Ordering follows the written stages and first-to-last maxspan: 10m, 15m, 20m, 30m or 60m as shown. Equal and partial timestamp ties remain unresolved; there is no published tiebreaker. Metadata sets timestamp_field=timestamp and event_category_field=type.keyword; all stages use any. Missing/null timestamp/category behavior remains untested, so metadata configuration must not be misrepresented as an explicit per-event category predicate. Arrival order and scheduled search-window coverage are separate from maxspan.

G. Missing/null/optional-field risks

Required predicates and joins reject the tested missing/null cases; unmapped nonoptional fields can also prevent query verification. Explicit null, absent source, ignored long values and empty arrays may all appear as no indexed value. null_value mappings can change that result. Empty strings differ from null: non-null guards and wildcard components do not establish nonempty or valid values. Stage fields apply only to their own events. PRIV optional field syntax does not make its third stage optional or its join a wildcard; absent/null final usernames did not establish intended coverage. Native empty/array/nested behavior is unverified.

All metadata field lists equal query fields plus timestamp/type metadata as sets; none omits a query reference. Differences in scope/claims: SSH-002 Markdown includes a standalone alternative with extra non-null guards absent from its authoritative .eql; PRIV source accommodation claim is not a demonstrated join guarantee; WEB-004 rule.id applies only to stage 1. HTTP 200, method, destination IP, SSH account/session continuity, service-name continuity and exact WEB URL/FIM filename equality are context rather than predicates. Published LAB_VALIDATION_REQUIRED metadata and older offline validation wording remain frozen; Phase 6H adds bounded synthetic qualification without rewriting publication.

H. FIM, audit, SSH and web dependencies

SSH-003 and MAL-001 require exact realtime mode; SSH-004, SSH-005, PERS-001/002 and WEB-002/003/004 impose no FIM mode predicate. SSH-005 accepts any 550/554 path, not necessarily the transferred file. Sensitive authentication, cron, systemd and executable paths are exactly enumerated in C; wildcard patterns admit nested/empty components in observed scalar cases. WEB FIM requires ID 554, event added and the exact WordPress Docker-volume PHP pattern. That deployment-specific root is unverified in production.

EVAS requires sudo then 80705 with exact CONFIG_CHANGE then 80703; it does not constrain command, actor or audit target. SSH-005 requires audit ID 92603 with command exactly scp, not a path/full command. MAL needs rootcheck 510/521 data.file matching the FIM path and excludes the exact /dev/null plus carriage-return value. Its exclusion was not isolated by Phase 6 negatives. SSH uses 5715; only SSH-001 also needs 5712/5763 and source-IP equality. Web stages use their exact ID lists; no HTTP 200/method condition appears, and source IP is required only by WEB-001.

I. Phase 6H limitations carried forward

Phase 6H remains QUALIFIED WITH LIMITATIONS for bounded synthetic behavior. Preserved accounting: 582 executions, 531 corrected unique identities, 509 PASS, zero corrected FAIL and 22 INCONCLUSIVE. Original 16 WEB-004 FAIL records remain; 46 reversed definitions and 51 separate recovery executions are not rewritten. 6A lacks serialized per-scenario request capture. All 20 limitation records retain their classifications:

| ID / subject | Classification | Finding | Inspection needed |
| --- | --- | --- | --- |
| L01 Agent-only joins and attribution | CONFIRMED | Agent/time association does not establish actor identity or causal activity. SSH-001 and WEB-001 also join source IP; PRIV and MAL have stage joins. | Representative events/provenance + later laboratory tests |
| L02 User/session/process continuity | CONFIRMED | Published queries omit session/process joins; PRIV correlates selected usernames, not session/process identity. | Representative events/provenance + later laboratory tests |
| L03 Source IP and shared proxies | CONFIRMED | SSH-001/WEB-001 enforce equal source strings; strings do not establish individual actors behind a shared address. Proxy efficacy itself remains untested. | Representative events/provenance + later laboratory tests |
| L04 Command/path/service relationships | CONFIRMED | Missing interstage relationships permit unrelated activity. MAL joins paths and PRIV selected users; other omitted links remain omitted. | Representative events/provenance + later laboratory tests |
| L05 Scheduled versus realtime FIM | CONFIRMED | SSH-003 and MAL require exact realtime; several other FIM rules have no mode restriction. | Representative events/provenance + later laboratory tests |
| L06 Case-sensitive exact predicates | CONFIRMED | Case-sensitive IDs, literals, joins and wildcard paths constrain observed coverage. | Mapping + representative sources; laboratory semantics remain open |
| L07 Broad wildcard and substring matches | CONFIRMED | Wildcards span nested paths and empty components; command substrings do not prove executed binaries. | Representative events/provenance + later laboratory tests |
| L08 Empty-string joins and wildcard matches | CONFIRMED | Non-null checks do not establish nonempty or well-formed values; empty matching source strings and wildcard components can match. | Representative events/provenance + later laboratory tests |
| L09 Missing/null predicate and join fields | CONFIRMED | Required fields/joins reject tested missing/null values. This does not cover missing timestamps or categories. | Mapping + representative sources; laboratory semantics remain open |
| L10 Equal-timestamp ordering | INCONCLUSIVE | 18 unique equal/partial timestamp investigations remain INCONCLUSIVE. Two Phase 6A boundary and two optional-username investigations also remain historically INCONCLUSIVE, totaling 22. Recovery repeats one tie identity without resolving it. | Representative events/provenance + later laboratory tests |
| L11 PRIV optional username | CONFIRMED | Absent/null final username does not wildcard-match preceding populated username; no intended detection coverage claimed. | Representative events/provenance + later laboratory tests |
| L12 MAL exclusion isolation | INCONCLUSIVE | No-sequence observations confound exclusion with path join or first-stage directory predicate. Isolated scalar exclusion effectiveness unproven. | Representative events/provenance + later laboratory tests |
| L13 Missing/null timestamps and categories | UNTESTED | Different category values tested for some rules; missing/null ordering/category fields not covered. | Mapping + representative sources; laboratory semantics remain open |
| L14 Multivalued fields | UNTESTED | Scalar fixture evidence does not establish multivalued predicate/join behaviour. | Mapping + representative sources; laboratory semantics remain open |
| L15 Competing sequences | UNTESTED | One candidate chain per partition; selection under competing events not established. | Representative events/provenance + later laboratory tests |
| L16 Ingestion delay and arrival ordering | UNTESTED | Event timestamp reversals tested; delayed ingestion and scheduling interactions not established. | Representative events/provenance + later laboratory tests |
| L17 Scheduling and deduplication | UNTESTED | No scheduler/overlap/state/deduplication evidence. | Representative events/provenance + later laboratory tests |
| L18 Native Wazuh mappings and field population | UNTESTED | Synthetic strict mappings cannot establish native alert field types, keyword multifields, normalization or population. | Mapping + representative sources; laboratory semantics remain open |
| L19 Production scale and detection efficacy | UNTESTED | No representative load, benign baseline, precision/recall or operational efficacy evidence. | Representative events/provenance + later laboratory tests |
| L20 Stage-specific join mismatch for rules without stage joins | NOT APPLICABLE | Only PRIV and MAL have stage-specific joins; other rules use their stated global joins. | Static query extraction; no added stage joins |

Mapping inspection alone can establish definitions, conflicts, keyword limits, normalizers and object structure. It cannot prove enabled ID coverage, field values, source attribution, mode/path population, ingestion provenance or join behavior. Sources establish representative observations; later laboratory tests must address ties, PRIV null combinations, MAL exclusion isolation, arrays, competing candidates, delayed ingestion and scheduler/deduplication behavior. 18 unique timestamp ties, two 6A boundaries and two optional-username investigations remain historically inconclusive.

J. Native compatibility unknowns

Actual production host/product/version and indices; per-index mappings and source structure; all 26 ID populations; keyword limits and backfill; timestamp/category population and clock precision; ingest-time meaning and delay; proxy/client attribution; rootcheck path population outside the recurring anomaly; optional usernames; exact Docker volume roots; realtime coverage; normalization; multi-value semantics; competing chains; scheduling/deduplication; benign activity and load are unverified. Neither native compatibility nor production readiness is claimed.

K. Proposed Phase 7B read-only inspections

The separate phase7b-inspection-plan.md specifies confirmed endpoint and index scope, resolve/mapping/field-capability reads for all 15 fields, bounded size-0 fixed-filter ID/population counts, and at most three source-filtered hits per request (100 initial examples total). Start with one concrete index and one hour; timeout 10s, no scripts or EQL. Inspect every mapped generation in batches of at most five indices. Handle absent timestamp/keyword fields explicitly and reject partial results. Preserve null/empty/array/control-character and join relationships during sanitization. No plan request was executed.

L. Validation results

- Historical validator: PASS, 15 tests (14 passed; one expected optional external-source skip).
- Development validator: PASS, 15 tests (14 passed; the same optional skip).
- Independent extraction audit: PASS, 14 exact queries, 34 stages, every one of 13 query fields and all global/stage joins; 15 total metadata-inclusive fields; 26 rule IDs; metadata manifest field sets and maxspans agree for all rules.
- All 20 Phase 6H limitations preserved in the contract; all stage production availabilities explicitly UNVERIFIED.
- Preservation: 150 baseline files hashed; 149 byte-identical. Only tests/validate_development.py changed, proven to be exactly the six authorized literal inventory additions. All publication and Phase 6 files remain unchanged.
- Publication: 50 local-tag byte comparisons pass. Five Phase 6H non-self artifact hashes pass. Of 1047 retained historical pin records, 1044 match current bytes; three authorized superseded snapshots or the authorized validator exception are retained without rewriting their historical values.
- Git whitespace check and explicit whitespace scan of all six new files: PASS.
- No Phase 6 engine scenario or EQL query rerun. No external source was supplied for the optional validator comparison; that skip limits only the independent external-source check.

M. Evidence inventory

The six new artifacts are REPORT.md, README.md, field-contract.json, rule-dependencies.json, mapping-requirements.json and phase7b-inspection-plan.md. README.md inventories every baseline file with SHA-256; all Phase 6 evidence, fixtures and mapping files are covered. JSON contracts include exact published queries and their hashes, all stage fields/joins/IDs, metadata differences, all 20 Phase 6H limitations and observed fixture mapping leaves.

Primary evidence: local v1.0.0; docs/verification/PUBLICATION_MANIFEST.json; tests/rule-manifest.json; all rules/*/*.eql and corresponding .md; docs/correlation-rule-catalogue.md; docs/configuration.md; docs/installation.md; docs/troubleshooting.md; docs/ecs-normalisation-decision.md; Phase 6H REPORT.md, qualification.json, limitations.json, integrity.json and regression.json; all Phase 6 reports/results/fixtures/mappings and harnesses. No external/production mapping evidence was consulted.

N. Readiness for Phase 7B

READY TO PROPOSE the bounded read-only inspection after the operator identifies the production service, concrete indices, time scope and suitable read permissions. This is a documentation readiness decision only. Native compatibility remains UNVERIFIED and deployment/activation readiness NOT ASSESSED. Laboratory Elasticsearch is not assumed to host production Wazuh data.

O. Safety and non-interference

No production or laboratory service access, EQL execution, Phase 6 scenario rerun, credentials, package installation, index/document writes, restart, published rule/evidence edits, commits, pushes, tags or publication. Only the six new development documents and the explicitly authorized six-entry validator inventory extension were written in the repository. Offline validator execution and local Git/file reads only. The complete final report is printed to terminal after final validation.
