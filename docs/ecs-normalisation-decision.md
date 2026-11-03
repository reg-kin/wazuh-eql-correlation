# Decision: preserve native Wazuh fields

Status: accepted for this integration.

Additional ECS normalisation was removed from this integration's design so native Wazuh alert fields remain directly available to the supplied EQL predicates. The historical transformation implementation and its change history were not supplied; this repository does not reconstruct them or claim a production removal was performed.

Mapping `rule.id`, `agent.id`, source data and FIM attributes into a second schema would add transformation and validation work and could change the meaning of the existing native queries. There is no active ECS transformation filter. File input, JSON codec, pipeline and output ECS compatibility are explicitly disabled. Existing ECS-looking fields are retained rather than stripped; preservation does not mean no Logstash ingestion metadata is added.

This is a scoped design choice, not a claim that ECS is unsuitable. Elastic Agent continues to supply its separate telemetry and rules. Native fields require explicit mapping checks and may not populate ECS-based Security views or prebuilt rules. This repository does not claim compatibility with every Elastic Security feature. Future normalisation would need versioned mappings, reviewed queries and independent validation.
