<p align="center"><img src="assets/cyberiq-logo.svg" width="92" alt="CyberIQ logo"><br><strong>CyberIQ</strong></p>

# CyberIQ Security Tools

![Version](https://img.shields.io/badge/version-0.2.0-B00020) ![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-800020)

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

## License
MIT.
