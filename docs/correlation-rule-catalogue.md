# Correlation rule catalogue

Exactly 14 complete source definitions are integrated. The [manifest](../tests/rule-manifest.json) records full names, descriptions, severity, risk, fields, prerequisites, limitations and source digests; each entry links its executable EQL source. No ECS normalisation is introduced. All final expressions require lab validation; no Kibana installation or activation is claimed.

Historical counts refer to earlier versions, with size limited to 10; they are not final-expression results or exhaustive totals. See [validation](validation-results.md) and [deployment settings](installation.md).

| Rule | Source change | Severity / risk | Maxspan | Earlier returned sequences | Final execution |
| --- | --- | --- | --- | --- | --- |
| [WCORR-SSH-001](../rules/ssh/WCORR-SSH-001.md) | RECOVERED | High / 73 | 15m | 1 | NOT_PERFORMED |
| [WCORR-SSH-002](../rules/ssh/WCORR-SSH-002.md) | RECOVERED | Medium / 47 | 15m | 10 | NOT_PERFORMED |
| [WCORR-SSH-003](../rules/ssh/WCORR-SSH-003.md) | RECOVERED | High / 70 | 30m | 1 | NOT_PERFORMED |
| [WCORR-SSH-004](../rules/ssh/WCORR-SSH-004.md) | RECOVERED | High / 78 | 30m | 0 | NOT_PERFORMED |
| [WCORR-SSH-005](../rules/ssh/WCORR-SSH-005.md) | RECOVERED | Medium / 62 | 30m | 0 | NOT_PERFORMED |
| [WCORR-WEB-001](../rules/web/WCORR-WEB-001.md) | UNCHANGED | Medium / 55 | 10m | 10 | NOT_PERFORMED |
| [WCORR-WEB-002](../rules/web/WCORR-WEB-002.md) | UNCHANGED | High / 82 | 10m | 0 | NOT_PERFORMED |
| [WCORR-WEB-003](../rules/web/WCORR-WEB-003.md) | UNCHANGED | High / 85 | 10m | 0 | NOT_PERFORMED |
| [WCORR-WEB-004](../rules/web/WCORR-WEB-004.md) | UNCHANGED | High / 80 | 30m | 0 | NOT_PERFORMED |
| [WCORR-PRIV-001](../rules/privilege-escalation/WCORR-PRIV-001.md) | REVISED | High / 82 | 30m | 2 | NOT_PERFORMED |
| [WCORR-PERS-001](../rules/persistence/WCORR-PERS-001.md) | UNCHANGED | High / 78 | 30m | 0 | NOT_PERFORMED |
| [WCORR-PERS-002](../rules/persistence/WCORR-PERS-002.md) | UNCHANGED | Medium / 60 | 30m | 0 | NOT_PERFORMED |
| [WCORR-EVAS-001](../rules/defence-evasion/WCORR-EVAS-001.md) | UNCHANGED | High / 80 | 20m | 0 | NOT_PERFORMED |
| [WCORR-MAL-001](../rules/malware/WCORR-MAL-001.md) | REVISED | High / 75 | 60m | 7 | NOT_PERFORMED |
