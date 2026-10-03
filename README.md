<p align="center"><img src="assets/cyberiq-logo.svg" width="92" alt="CyberIQ logo"><br><strong>CyberIQ</strong></p>

# CyberIQ Security Tools

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
```

No network scanning is performed by these tools.

## Tests
```bash
python -m unittest discover -s tests -v
```

## Security Philosophy
Authorization first • Offline analysis where practical • Evidence before conclusions • No embedded credentials • Small, readable utilities

## License
MIT.
