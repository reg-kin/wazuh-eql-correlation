# Phase 7B proposed native inspection — NOT EXECUTED

Development-only plan. Obtain the independently confirmed production Elasticsearch endpoint, product/version and approved time window from the operator. Do not reuse the laboratory endpoint, credentials or index namespace. No endpoint or credential is embedded here. If the service is Wazuh Indexer/OpenSearch rather than Elasticsearch, stop and reassess API/EQL compatibility separately. Use an existing least-privilege read/view-metadata identity without disclosing authentication material. This document authorizes no execution in Phase 7A.

Use only mapping, field-capability and bounded search reads. POST below is a read-only search/capability request, not an index write. No EQL, scripts, runtime mappings, refresh, PIT creation, scroll, template simulation, ingest or mutation APIs are needed.

1. Scope and mappings

Published pattern: `wazuh-alerts-4.x-*`. Resolve only that pattern on the confirmed production service, then record an explicit allowlist of concrete indices for the approved retention dates. No wildcard across all cluster indices and no laboratory `wcorr-*` indices. If native alerts use a different name, record that discrepancy and obtain the correct scope before searching; do not silently substitute ECS indices. Inspect recent and retained/rollover mappings individually; preserve absent/conflicting indices. Requests use `APPROVED_INDICES` as a non-executable placeholder for the reviewed comma-separated index list.

```http
GET /_resolve/index/wazuh-alerts-4.x-*?expand_wildcards=open
GET /APPROVED_INDICES/_mapping
POST /APPROVED_INDICES/_field_caps?include_unmapped=true
{
  "fields": [
    "agent.id.keyword",
    "data.audit.command.keyword",
    "data.audit.type.keyword",
    "data.command.keyword",
    "data.dstuser.keyword",
    "data.file.keyword",
    "data.srcip.keyword",
    "data.srcuser.keyword",
    "data.url.keyword",
    "rule.id.keyword",
    "syscheck.event.keyword",
    "syscheck.mode.keyword",
    "syscheck.path.keyword",
    "timestamp",
    "type.keyword",
    "@timestamp",
    "event.ingested",
    "wazuh.event.created"
  ]
}
```

Do not include global templates or unrelated mappings. Mapping responses may be large: request at most five concrete indices per call, reduce to one if needed, and keep the raw snapshot in a protected evidence store. Field capabilities: inspect type-specific index lists, searchable/aggregatable flags, unmapped and nonaggregatable indices. Map every exact leaf and all parents: type, fields.keyword, format, normalizer, ignore_above, null_value, index/doc_values, enabled, nested/object/flattened and runtime/alias definitions. A parent keyword without its `.keyword` leaf is a mismatch. Mapping cannot establish enabled Wazuh rules or field population.

2. Minimal population and rule-ID coverage

After confirming `timestamp` is a searchable date, select a fixed UTC half-open interval, initially one hour in one concrete index. Widen deliberately up to 24 hours only if coverage is absent and the operator approves resource scope; absence in a sampled window is UNOBSERVED, never proof of disabled telemetry. Use a common fixed interval for comparable counts. The following body is a template; replace START_UTC and END_UTC with that interval. Run one request at a time, timeout 10s, size 0, no document hits, total hits capped at 10000. All aggregation counts are over the bounded search; record timeout, shard success/failure and count relation. Partial/timeout results are incomplete evidence and must not be accepted as zero.

```http
POST /APPROVED_INDICES/_search?allow_partial_search_results=false
{
  "size": 0,
  "timeout": "10s",
  "track_total_hits": 10000,
  "query": {
    "range": {
      "timestamp": {
        "gte": "START_UTC",
        "lt": "END_UTC"
      }
    }
  },
  "aggs": {
    "required_rule_ids": {
      "filters": {
        "filters": {
          "510": {
            "term": {
              "rule.id.keyword": "510"
            }
          },
          "521": {
            "term": {
              "rule.id.keyword": "521"
            }
          },
          "550": {
            "term": {
              "rule.id.keyword": "550"
            }
          },
          "554": {
            "term": {
              "rule.id.keyword": "554"
            }
          },
          "2834": {
            "term": {
              "rule.id.keyword": "2834"
            }
          },
          "5402": {
            "term": {
              "rule.id.keyword": "5402"
            }
          },
          "5407": {
            "term": {
              "rule.id.keyword": "5407"
            }
          },
          "5712": {
            "term": {
              "rule.id.keyword": "5712"
            }
          },
          "5715": {
            "term": {
              "rule.id.keyword": "5715"
            }
          },
          "5763": {
            "term": {
              "rule.id.keyword": "5763"
            }
          },
          "5902": {
            "term": {
              "rule.id.keyword": "5902"
            }
          },
          "31103": {
            "term": {
              "rule.id.keyword": "31103"
            }
          },
          "31104": {
            "term": {
              "rule.id.keyword": "31104"
            }
          },
          "31105": {
            "term": {
              "rule.id.keyword": "31105"
            }
          },
          "31106": {
            "term": {
              "rule.id.keyword": "31106"
            }
          },
          "31110": {
            "term": {
              "rule.id.keyword": "31110"
            }
          },
          "31151": {
            "term": {
              "rule.id.keyword": "31151"
            }
          },
          "31164": {
            "term": {
              "rule.id.keyword": "31164"
            }
          },
          "31166": {
            "term": {
              "rule.id.keyword": "31166"
            }
          },
          "31168": {
            "term": {
              "rule.id.keyword": "31168"
            }
          },
          "31515": {
            "term": {
              "rule.id.keyword": "31515"
            }
          },
          "31516": {
            "term": {
              "rule.id.keyword": "31516"
            }
          },
          "40704": {
            "term": {
              "rule.id.keyword": "40704"
            }
          },
          "80703": {
            "term": {
              "rule.id.keyword": "80703"
            }
          },
          "80705": {
            "term": {
              "rule.id.keyword": "80705"
            }
          },
          "92603": {
            "term": {
              "rule.id.keyword": "92603"
            }
          }
        }
      }
    },
    "url_stage_without_rule_restriction": {
      "filter": {
        "exists": {
          "field": "data.url.keyword"
        }
      }
    },
    "indexed_field_presence": {
      "filters": {
        "filters": {
          "agent.id.keyword": {
            "exists": {
              "field": "agent.id.keyword"
            }
          },
          "data.audit.command.keyword": {
            "exists": {
              "field": "data.audit.command.keyword"
            }
          },
          "data.audit.type.keyword": {
            "exists": {
              "field": "data.audit.type.keyword"
            }
          },
          "data.command.keyword": {
            "exists": {
              "field": "data.command.keyword"
            }
          },
          "data.dstuser.keyword": {
            "exists": {
              "field": "data.dstuser.keyword"
            }
          },
          "data.file.keyword": {
            "exists": {
              "field": "data.file.keyword"
            }
          },
          "data.srcip.keyword": {
            "exists": {
              "field": "data.srcip.keyword"
            }
          },
          "data.srcuser.keyword": {
            "exists": {
              "field": "data.srcuser.keyword"
            }
          },
          "data.url.keyword": {
            "exists": {
              "field": "data.url.keyword"
            }
          },
          "rule.id.keyword": {
            "exists": {
              "field": "rule.id.keyword"
            }
          },
          "syscheck.event.keyword": {
            "exists": {
              "field": "syscheck.event.keyword"
            }
          },
          "syscheck.mode.keyword": {
            "exists": {
              "field": "syscheck.mode.keyword"
            }
          },
          "syscheck.path.keyword": {
            "exists": {
              "field": "syscheck.path.keyword"
            }
          },
          "timestamp": {
            "exists": {
              "field": "timestamp"
            }
          },
          "type.keyword": {
            "exists": {
              "field": "type.keyword"
            }
          }
        }
      }
    }
  }
}
```

Use fixed filters so zero counts for all 26 IDs are explicit and terms top-N truncation cannot hide IDs. WEB-004 stage 2 must be assessed independently of that ID set; URL presence above is only a population count, not its path predicate. For each rule/stage in rule-dependencies.json, repeat a small size-0 request restricted to that stage's ID set (omit ID filter for WEB-004 stage 2), with exists and must_not exists filter counts for its predicate/join fields. Inspect empty indexed strings using term(field, "") separately for keyword fields, and keyword-missing but parent-present documents using parent exists AND must_not keyword exists where the parent is indexed. These reveal possible ignore_above or backfill issues, not the cause. Do not equate field existence with the complete predicate or stage match. No cross-stage correlation is performed.

Missing/null/unmapped procedure: retain each absent leaf and index name in the incompatibility ledger. Do not create mappings. Partition requests by compatible mapping type; do not set unmapped fields to invented defaults. If rule.id.keyword is absent, the prescribed ID coverage is unavailable; inspect the mapped source rule.id representation through a separately scoped diagnostic and label it as diagnostic only. Exists cannot distinguish absent, explicit null, empty arrays, ignored values or a null_value sentinel; use source samples. If timestamp is absent, the timestamp-bounded body cannot diagnose its absence. Select a concrete daily index from the approved dates and run a size-0 must_not exists(timestamp) count bounded by a verified independent date field if available; otherwise use one small concrete daily index with explicit operator resource review and label the time scope as index-level only. Apply the same approach to null/empty timestamp source samples. Never invent ingest time from an index suffix.

3. Sanitised representative examples

Use a source allowlist: timestamp, type, agent.id, rule.id, data.srcip, data.dstuser, data.srcuser, data.command, data.audit.type, data.audit.command, data.file, data.url, syscheck.path, syscheck.mode, syscheck.event. Add data.method, data.status, data.request and data.dstip only for separately needed web context. Retrieve unsuffixed source values; multifields are usually not source keys. After field inspection, include only verified timestamp alternatives such as @timestamp, event.ingested or wazuh.event.created for timing diagnostics; none is presumed to be ingestion time.

For each ID/family and the unrestricted URL stage, fetch at most 3 hits per request, at most 100 total examples for the initial inspection, timeout 10s and total hits false, with the same bounded interval and no highlight or raw log. Use source filtering and a rule-ID filter; sort ascending timestamp only when mapped and populated. Repeat with exists/missing filters for known missing, null, empty, long, array or alternate-shape cases only where necessary, within the total cap. A single example does not establish population rates. Missing events remain UNVERIFIED. Example request:

```http
POST /APPROVED_INDICES/_search?allow_partial_search_results=false
{
  "size": 3,
  "timeout": "10s",
  "track_total_hits": false,
  "_source": [
    "agent.id",
    "data.audit.command",
    "data.audit.type",
    "data.command",
    "data.dstuser",
    "data.file",
    "data.srcip",
    "data.srcuser",
    "data.url",
    "rule.id",
    "syscheck.event",
    "syscheck.mode",
    "syscheck.path",
    "timestamp",
    "type"
  ],
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "timestamp": {
              "gte": "START_UTC",
              "lt": "END_UTC"
            }
          }
        },
        {
          "term": {
            "rule.id.keyword": "5715"
          }
        }
      ]
    }
  },
  "sort": [
    {
      "timestamp": "asc"
    }
  ]
}
```

Inspect: SSH failure/source versus success/destination users; sudo actor/target/command; 5902 optional source username; rootcheck exact data.file including escaped carriage returns; cron and systemd alerts; scp versus full executable paths; CONFIG_CHANGE casing; scheduled/realtime mode; added/modified FIM classification; exact executable/auth/cron/systemd/WordPress roots; relative versus absolute URL, query suffix, URL decoding, filename case and nested directories. The complete stage predicates and ID sets in field-contract.json control this checklist. For WEB-004 obtain URL-bearing events without imposing an ID, HTTP method or status. No requirement that the requested filename equals the created filename is present in the published query.

Redact before export to the repository: credentials, tokens, cookies, authorization headers, raw logs, request bodies/query secrets, personal usernames, tenant/host/agent identifiers, public/private IPs, command arguments and user-controlled paths. Use consistent pseudonyms across related joins, preserving equality/inequality, source scalar/array shape, case, null versus absent versus empty, relative time deltas and escaped control characters. Preserve fixed predicate literals only when safe. Describe any redaction that prevents direct predicate assessment. Keep originals only in the approved protected location; do not embed endpoint URLs or authentication material in the report. Do not export whole source objects or raw production payloads.

4. Timestamp, arrival and semantic checks

From mapping record date formats, precision and timezone parsing; from samples compare event timestamp to independently verified ingestion time only when provenance is documented. A Logstash @timestamp can be processing time but its meaning is unverified here. Report delay distribution only with adequate samples; three examples are descriptive, not a distribution. Record negative deltas, clock skew and timestamp resolution/ties. Inspect bounded missing timestamp/category counts and duplicate IDs where safely observable; they do not establish equal-time EQL ordering. No published tiebreaker exists. Do not invent one or run EQL in Phase 7B's mapping/population inspection.

Read-only mappings can establish field definitions/conflicts, keyword limits and normalizers. Representative sources are needed for actual shape, ID coverage, normalized values, mode, paths, proxy attribution, and timestamp/ingestion provenance. Later separately scoped laboratory tests are needed for optional/null joins, ties/tiebreakers, date_nanos, arrays/nested variants, MAL exclusion isolation, competing candidates, delayed arrival, scheduling, deduplication and resource efficacy. Index readbacks alone cannot establish causality, detection quality or readiness.

5. Completion record

Retain sanitised requests with exact scope/time, version, concrete-index mapping hash, response completeness flags, counts and redaction method. Produce an index-by-field matrix and rule/stage coverage ledger: OBSERVED / UNOBSERVED IN WINDOW / UNMAPPED / CONFLICT / UNVERIFIED. Record ID-set alternatives separately: each stage requires one allowed ID per matching event, not every ID in the set. Do not call absence disabled or claim production readiness. Any mapping/ingest remediation, broader collection or laboratory execution requires separate work; no changes are in this plan.
