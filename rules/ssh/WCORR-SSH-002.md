# WCORR-SSH-002 — SSH followed by sensitive sudo activity

- Rule identifier: `WCORR-SSH-002`.
- Detection objective: Detects successful SSH authentication followed by privileged command execution within 15 minutes.
- Severity: Medium. Risk score: 47.
- Source status: COMPLETE_SOURCE; RECOVERED in Phase 2.
- Required event fields: `timestamp`, `type.keyword`, `agent.id.keyword`, `data.command.keyword`, `data.dstuser.keyword`, `rule.id.keyword`. Fields apply to their respective stages; PRIV-001's third-stage username is optional in source syntax.
- Index pattern: `wazuh-alerts-4.x-*`.
- EQL metadata: `timestamp_field = timestamp`; `event_category_field = type.keyword`.
- Correlation window: 15m.
- Historical match count: 10 returned sequences for earlier versions; query size was limited to 10. This is not an exhaustive index-wide total or validation of this final expression.
- False-positive considerations / Detection limitations: SSH and sudo users are not equated. Substring matching can miss shells and alternative commands. This contextual rule overlaps PRIV-001 and PERS-001; prefer their additional evidence. Routine administration can match.
- Deployment prerequisites: Collect SSH and sudo alerts with native command and target-user fields; review sensitive-command coverage. Confirm native mappings and scheduled query-window coverage as described in [installation](../../docs/installation.md).
- Validation limitations: Offline structural and source-preservation checks only. Final-expression Elasticsearch parsing, execution and detection efficacy remain unvalidated. Historical positives are not new positive detections.
- Activation readiness: `LAB_VALIDATION_REQUIRED`. No activation in Kibana is claimed.

EQL definition: [WCORR-SSH-002.eql](WCORR-SSH-002.eql). Supplied predicates and join keys are preserved; whitespace in unchanged Phase 1 files is retained.

## Source discrepancy

The designated definition is the Dev Tools expression. The standalone expression below additionally requires data.dstuser.keyword != null in stage one and data.command.keyword != null in stage two. Neither form equates the SSH user to the sudo user. The recommendation to correlate usernames is not implemented.

```eql
sequence by agent.id.keyword with maxspan=15m
  [any where
    rule.id.keyword == "5715" and
    data.dstuser.keyword != null
  ]
  [any where
    rule.id.keyword in ("5402", "5407") and
    data.dstuser.keyword == "root" and
    data.command.keyword != null and
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
