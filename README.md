<p align="center"><img src="assets/cyberiq-logo.svg" width="92" alt="CyberIQ logo"><br><strong>CyberIQ</strong></p>

# CyberIQ Security Tools

> **Personal cybersecurity project & portfolio work by Muqtada Al-Sadr Jarallah Khalif (Al-Hantooshi)**  
> Developer • Team Leader of CyberIQ

**Project mission:** provide small, auditable, local-first defensive utilities for evidence handling, CTF learning, education, and authorized security work.

![Version](https://img.shields.io/badge/version-9.6.0-B00020) ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-800020)

A collection of small, auditable **defensive cybersecurity utilities** for labs, education, CTF analysis, and authorized security work.

**مقتدى الصدر جارالله خليف — Muqtada Al-Sadr Jarallah Khalif**  
**الحنتوشي — Al-Hantooshi**  
**Developer • Team Leader of CyberIQ**

> [!IMPORTANT]
> Use these tools only with data and systems you own or are explicitly authorized to assess.

## Tools

| Tool | Purpose |
|---|---|
| `hashcheck` | Calculate MD5, SHA-1, SHA-256 and SHA-512 hashes for a local file |
| `headers` | Review saved HTTP response headers offline |
| `logsummary` | Summarize common log levels and basic local indicators offline |
| `verify-hash` | Compare a local file hash against an expected value |
| `urls` | Inventory URLs, hosts, schemes, and file extensions from saved text |
| `indicators` | Count IPv4/domain/hash-like patterns without reputation lookups |
| `metadata` | Inspect local file metadata and SHA-256 offline |
| `inventory` | Build a recursive local directory inventory |
| `dashboard` | Render local JSON reports into a read-only HTML dashboard |
| `case` | Create local case workspaces and evidence hash manifests |
| `analyze` | Produce normalized defensive findings from supplied data |
| `batch` | Run bounded offline analysis across local files |
| `plugin` | List or run registered offline analysis plugins |
| `doctor` | Check local Python support, write access, version, and built-in plugins |

## Architecture at a glance

**Local evidence → integrity/metadata → offline analyzers → normalized findings → case workspace → reports/dashboard**

The toolkit deliberately avoids network scanning and exploitation. Its core workflow is evidence-driven and designed to remain easy to audit.

## Quick Start

```bash
git clone https://github.com/hfsduu5-coder/CyberIQ-Security-Tools-CYBERiQ.git
cd CyberIQ-Security-Tools-CYBERiQ
python -m cyberiq_tools --help
```

Examples:
```bash
python -m cyberiq_tools hashcheck ./sample.bin
python -m cyberiq_tools headers ./headers.txt
python -m cyberiq_tools logsummary ./app.log
python -m cyberiq_tools urls ./examples/sample.log
python -m cyberiq_tools indicators ./examples/sample.log
python -m cyberiq_tools verify-hash ./sample.bin EXPECTED_SHA256
python -m cyberiq_tools metadata ./sample.bin --output report.json
python -m cyberiq_tools inventory ./examples --output inventory.html --format html
python -m cyberiq_tools dashboard ./reports --output cyberiq-dashboard.html
```

No network scanning, exploitation, or reputation lookup is performed by these tools.

## Install as a CLI
```bash
pip install -e .
cyberiq-tools --version
cyberiq-tools --help
```

## Tests
```bash
python -m unittest discover -s tests -v
```

## Security Philosophy
Authorization first • Offline analysis where practical • Evidence before conclusions • No embedded credentials • Small, readable utilities

## Project Status

This repository is maintained as part of my public cybersecurity and software-engineering portfolio. Development focuses on clear documentation, reproducible local workflows, defensive/educational use, and evidence-backed claims. CyberIQ branding uses the official team identity only when the official asset is available; placeholder logo artwork is not presented as official.

## Portfolio & attribution

This repository documents my personal development work on CyberIQ Security Tools. External standards, libraries, and learning references remain credited to their respective authors and are not presented as my own.

## License
MIT.

## v9.6.0
The v9 line adds structured case workspaces, evidence manifests, normalized findings, bounded batch analysis, an extension SDK, versioned document schemas, report exports, a local dashboard, architecture documentation, migration guidance, and expanded regression coverage.

Documentation: `docs/ARCHITECTURE.md` • `docs/PLUGINS.md` • `docs/MIGRATION-v9.md` • `CHANGELOG.md`.

### v9.1–v9.2 improvements
The local dashboard now summarizes report and finding counts, severity distribution, document schemas, and report contents in a responsive CyberIQ dark interface. The new `doctor` command performs local environment diagnostics without contacting external systems.

### Case lifecycle
```bash
cyberiq-tools case new incident-demo
cyberiq-tools case add cases/incident-demo ./evidence.log
cyberiq-tools case note cases/incident-demo "Initial analyst review"
cyberiq-tools case set-status cases/incident-demo review
cyberiq-tools case timeline cases/incident-demo
cyberiq-tools case status cases/incident-demo
```
Case manifests now record lifecycle status and a UTC timeline for evidence, analyst notes, and status changes.

### Executive reporting
Generate an analyst-facing Markdown summary from a normalized JSON analysis:
```bash
cyberiq-tools analyze ./examples/sample.log --output analysis.json
cyberiq-tools executive-report analysis.json --output executive-report.md
```
The template separates observed review signals from analyst conclusions and documents that analysis is offline and based on supplied evidence.

### v9.4–v9.5 polish
Search normalized findings across local JSON reports and optionally filter by severity:
```bash
cyberiq-tools search ./reports "header" --severity low
```
Run a local release-readiness audit:
```bash
cyberiq-tools release-check
```
The release check validates expected project files and the local Python environment. It intentionally does not claim remote CI status.
