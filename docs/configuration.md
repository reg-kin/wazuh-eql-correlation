# Configuration

Project: **Wazuh EQL Correlation** (`wazuh-eql-correlation`); see the [project overview](../README.md).

## Pipeline and variables

[logstash.conf](../config/logstash/logstash.conf) ingests JSON lines from a file, retains native fields and writes daily `wazuh-alerts-4.x-%{+YYYY.MM.dd}` indices. [pipelines.yml](../config/logstash/pipelines.yml) selects its installed path and disables pipeline ECS compatibility. There are no normalisation filters. Output ILM, data streams and automatic template management are disabled to retain the explicit index convention and avoid inventing a template. Deployment must provide verified compatible mappings before ingestion.

| Variable | Reference/example purpose |
| --- | --- |
| WAZUH_ALERTS_PATH | `/var/ossec/logs/alerts/alerts.json` |
| ELASTICSEARCH_URL | `https://localhost:9201` |
| ELASTICSEARCH_USERNAME | Dedicated ingest identity |
| ELASTICSEARCH_PASSWORD | Secret supplied outside version control |
| ELASTICSEARCH_CA_PATH | `/etc/logstash/certs/http_ca.crt` |

No variable has a secret default. `environment.example` contains unusable CHANGE_ME values. Logstash does not load that file automatically. On an authorised lab host, copy it to a protected location outside the repository, replace the placeholders and configure the service manager to inject those variables. For systemd, an administrator can use a service drop-in with `EnvironmentFile=/etc/logstash/wazuh-correlation.env`; the environment file contains `KEY=value` lines (not shell `export` commands), should be root-owned with mode 0600, and is read by the service manager. A separately approved service restart is needed after changes. This repository performs none of those operations. A shell export affects only child processes of that shell, not an already running service. Avoid placing passwords on command lines, in shell history or in shared diagnostic output. Logstash keystore storage is an alternative for the password under the same substitution name; validate precedence in the lab.

The sanitised output uses `ssl_enabled` and `ssl_certificate_authorities` in place of the historical `ssl` and `cacert` spellings. These express the same intended verified TLS connection, with `ssl_verification_mode = full`. Installed plugin versions must be checked with a lab configuration test; no plugin compatibility check was run here. The CA must be readable by Logstash and the certificate SAN must match the configured hostname. Do not disable verification to work around a mismatch. The historical superuser `elastic` is replaced with a dedicated least-privilege identity; no credentials are supplied.

## Permissions and checkpoints

The Logstash service account needs read access to `alerts.json` and traversal (`x`) on every parent directory. Use a narrowly scoped group or named-user ACL rather than world-readable alert files or running Logstash as root. Check effective ACL masks and directory traversal with the actual service identity in a lab. Rotation can replace the file and change access: use an approved default ACL or rotation policy that preserves the minimum access and verify it after rotation. Wazuh must retain the ownership and permissions it needs to write alerts; do not apply broad recursive ownership changes to `/var/ossec`.

The fixed sincedb path is `/var/lib/logstash/plugins/inputs/file/sincedb_wazuh`. Its parent directory must exist and be writable by Logstash; the checkpoint must persist across restarts and container recreation. `start_position = end` applies only to newly discovered files without a usable checkpoint. It does not override an existing offset or guarantee a replay. A new installation intentionally skips pre-existing lines. Do not delete sincedb casually: replay can duplicate events and skipping can lose history. Inode identity, rotation and checkpoint expiry need lab testing. Use a separate checkpoint and index namespace for controlled replay. The supplied output has no deterministic document ID, so retries can duplicate documents.

## Persistent queue: separate Logstash settings

A persistent queue is **not configured in the pipeline** or enabled by this repository. On an approved lab deployment, settings belong in `logstash.yml`, for example:

```yaml
queue.type: persisted
path.queue: /var/lib/logstash/queue
queue.max_bytes: 1gb
```

Size storage against measured event rate and outage duration, ensure service-account access, monitor disk space and verify durability/checkpoint settings against the installed version. Sincedb records file offsets; the queue buffers pipeline events. Neither is an archival copy, a substitute for source retention or an exactly-once guarantee. A full queue backpressures input; source rotation during a prolonged outage can still lose unread data. Protect queue contents as sensitive events.

## Field capabilities and provenance

A read-only template simulation reportedly showed `event.dataset`, `event.kind`, `event.module`, `wazuh.agent.id`, `wazuh.agent.name` and `wazuh.manager.name` as keyword; `host.name` as text with a keyword subfield; `source.ip` as ip; and `wazuh.event.created` as date. This simulation does not establish how existing indices acquired native mappings and does not verify the following fields. No index template is supplied or invented.

| Native EQL field | Required capability |
| --- | --- |
| timestamp | date, consistently mapped and populated; date_nanos requires separate version-specific validation |
| type.keyword | keyword, searchable category field |
| rule.id.keyword | keyword, string identifiers |
| agent.id.keyword | keyword, stable join key |
| data.srcip.keyword | keyword, as used by the supplied predicates and join |
| data.dstuser.keyword | keyword |
| data.audit.type.keyword | keyword |
| data.url.keyword | keyword |
| syscheck.path.keyword | keyword |
| syscheck.event.keyword | keyword |

Keyword fields should retain doc values; review searchability, aggregatability and conflicts across every targeted index. Missing subfields, incompatible types, missing values and keyword ignore_above limits can prevent matching. Do not substitute `source.ip` or `wazuh.agent.id` for native fields merely because a template simulation lists them.

For a separately authorised lab or read-only operational review, this is the field-capabilities request to run in Dev Tools. It was **not executed** during construction:

```http
POST /wazuh-alerts-4.x-*/_field_caps?include_unmapped=true
{
  "fields": ["timestamp", "type.keyword", "rule.id.keyword", "agent.id.keyword", "data.srcip.keyword", "data.dstuser.keyword", "data.audit.type.keyword", "data.url.keyword", "syscheck.path.keyword", "syscheck.event.keyword"]
}
```

Inspect per-type index lists and unmapped entries; do not accept one healthy index as evidence for all indices. Mapping fixes require a separate migration/reindex plan; adding a subfield alone does not backfill existing documents. Verify clocks and representative sanitised values as well as types.

For EQL execution use `timestamp_field = timestamp` and `event_category_field = type.keyword`, not default assumptions. Detection-rule UI support and advanced overrides must be verified on Kibana 8.19.20 before creation; see [installation](installation.md).

## Complete Phase 2 field inventory

`"agent.id.keyword"`, `"data.audit.command.keyword"`, `"data.audit.type.keyword"`, `"data.command.keyword"`, `"data.dstuser.keyword"`, `"data.file.keyword"`, `"data.srcip.keyword"`, `"data.srcuser.keyword"`, `"data.url.keyword"`, `"rule.id.keyword"`, `"syscheck.event.keyword"`, `"syscheck.mode.keyword"`, `"syscheck.path.keyword"`, `"timestamp"`, `"type.keyword"`.

Extend the field-capabilities request above to include every field in this inventory. All `.keyword` fields require compatible native keyword mappings; syscheck.mode, data.command, data.srcuser, data.audit.command and data.file are newly documented dependencies. Stage-specific missing values and optional joins require explicit lab checks.
