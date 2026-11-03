# Troubleshooting and recovery

The following are lab investigation steps, not actions performed against production.

| Symptom | Checks and safe recovery direction |
| --- | --- |
| No events | Confirm file path, valid JSON lines, parent-directory traversal, file ACL mask, service identity and post-rotation access. Check whether start_position=end correctly skipped old lines. |
| Missing environment variable | Confirm injection into the service process; a shell export or example file alone does not configure systemd. Never dump the process environment into public output. |
| TLS or authentication failure | Verify the configured Elasticsearch endpoint (9201 in the reference deployment), CA readability, hostname/SAN, certificate chain and identity permissions. Port 9200 belongs to the separate Wazuh Indexer. Do not disable certificate verification. |
| Wrong index name | Inspect ILM/data-stream settings, other pipelines and date interpolation. The explicit daily name uses @timestamp, which may differ from native timestamp. |
| EQL type error or no matches | Check field capabilities on all indices, keyword subfields, timestamp population, date range, join values and stage prerequisites. A zero result is not proof of a working detector. |
| Duplicate or missing documents | Review checkpoint persistence, inode/rotation behaviour, outage length, source retention and queue state. Do not delete sincedb or queues as a first response. |
| Backpressure or high disk use | Monitor output failures, queue capacity and source retention. Preserve recovery evidence and plan a bounded lab replay with a separate checkpoint/index. |
| Configuration fails to parse | Check installed Logstash plugin versions and TLS option support with a lab config test. The production ssl/cacert options were expressed using current ssl_enabled/ssl_certificate_authorities names. |

## Historical journald feedback-loop lesson

A historical Logstash/Wazuh journald feedback-loop incident was reported. Detailed logs, exact trigger, dates and an independently verified root-cause analysis were not supplied. Do not invent them. A possible recursive ingestion path is: Logstash diagnostic output reaches journald; Wazuh monitors that journal and produces alerts; Logstash ingests those alerts and emits further diagnostics. This is a risk model, not a reconstructed incident trace.

Avoid recursive ingestion: review journal collection scope, diagnostic destinations and Wazuh monitoring rules together. Do not add a verbose stdout/rubydebug output for live Wazuh events into a journal Wazuh monitors. Test diagnostic routing in an isolated lab, keep sensitive payloads out of service logs and monitor unexpected ingestion/alert-rate growth. Any exclusion must be narrowly reviewed to avoid hiding unrelated security telemetry. During an incident follow an approved containment plan to interrupt the recursive path, preserve sanitised evidence, correct routing and verify bounded rates before recovery. This repository changes no journal, Wazuh or Logstash service settings.

Sincedb is a read checkpoint, while the optional persistent queue buffers events after input. Neither prevents recursive ingestion. Queue deletion can discard data; checkpoint deletion can replay or skip events depending on file discovery settings. Keep recovery plans separate from routine installation.
