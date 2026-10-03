# Migration Guide — v3 to v9

The original v3 commands remain available: `hashcheck`, `verify-hash`, `headers`, `logsummary`, `urls`, `indicators`, `metadata`, `inventory`, and `dashboard`.

New stable command groups:
- `case new|add|status` — structured local case workspaces and evidence manifests.
- `analyze` — normalized defensive findings.
- `batch` — bounded offline directory analysis.
- `plugin list|run` — extension registry and built-in analyzers.

Structured documents use versioned identifiers such as `cyberiq.analysis/v1`, `cyberiq.finding/v1`, `cyberiq.batch/v1`, and `cyberiq.case/v1`.
