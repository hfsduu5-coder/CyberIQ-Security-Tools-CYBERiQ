## 9.6.0
- Code milestone; does not by itself imply a published GitHub tag or Release.
- Validate IPv4 observations before counting them in offline log and indicator analysis.
- Add regression coverage for malformed IPv4-like input.

# Changelog

## [9.6.0] - 2026-10-03
### Added
- Local release-readiness audit with explicit CI-status limitation.

## [9.4.0] - 2026-10-03
### Added
- Search across normalized local JSON findings.
- Optional severity filtering and bounded result limits.
- Regression coverage for report search.

## [9.3.0] - 2026-10-03
### Added
- Executive Markdown report generator for normalized analysis JSON.
- Regression tests for case notes, lifecycle status, timeline, and executive reports.

## [9.1.0] - 2026-10-03
### Added
- Responsive CyberIQ local dashboard with report, finding, severity, and schema summaries.
- `doctor` command for offline local environment diagnostics.

## [9.0.0] - 2026-10-03
### Added
- Stable v9 CLI milestone and package metadata.
- Structured local case workspaces and SHA-256 evidence manifests.
- Normalized defensive findings with versioned document identifiers.
- Bounded offline batch analysis.
- Plugin registry SDK with built-in offline analyzers.
- Schema validation helpers.
- Architecture, plugin, and v9 migration documentation.
- Expanded regression coverage.

### Safety model
- Offline-first analysis of supplied/local data.
- No target scanning, exploitation, credential testing, persistence, evasion, or reputation lookup.

## [3.0.0] - 2026-10-03
### Added
- Local file metadata analyzer.
- Recursive directory inventory.
- JSON, Markdown, HTML, and CSV report export.
- Local read-only dashboard for JSON reports.
- Expanded CLI and tests.

## [2.0.0] - 2026-10-03
### Added
- URL inventory and indicator-pattern analysis.
- Hash verification command.
- Installable CLI packaging and safe sample data.

## [1.0.0] - 2026-10-03
### Added
- Initial defensive toolkit foundation: hashing, saved-header review, and offline log summary.

## Road to 9.0.0
- v4: structured case workspaces and evidence manifests.
- v5: richer defensive parsers and normalized findings.
- v6: batch analysis pipelines.
- v7: plugin architecture and extension SDK.
- v8: polished dashboard, schemas, and documentation.
- v9: stable public interface, migration guide, full regression suite, and release hardening.
