# CyberIQ Security Tools Architecture

CyberIQ Security Tools is intentionally **offline-first**. Inputs are local files or directories. Core analyzers produce dictionaries, normalized findings use versioned schema identifiers, reporting serializes results, and the dashboard renders local JSON reports.

## Layers
1. **Core** — hashing, headers, logs, URLs, indicator patterns.
2. **Metadata** — local file and directory observations.
3. **Findings** — normalized defensive review signals.
4. **Workspace** — case folders and evidence manifests.
5. **Batch** — bounded directory processing.
6. **Plugins** — small registry-based extension interface.
7. **Reporting** — JSON, Markdown, HTML, CSV.
8. **Dashboard** — static local read-only presentation.

No layer performs target scanning, exploitation, reputation lookup, credential testing, persistence, or evasion.
