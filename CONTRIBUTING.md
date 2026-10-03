# Contributing

Thanks for helping improve CyberIQ Security Tools.

## Scope
Contributions must remain defensive, local-first, educational, or explicitly authorized. Do not add credential attacks, persistence, malware behavior, stealth/evasion, indiscriminate scanning, or exploit automation.

## Workflow
1. Open an issue describing the change and its defensive use case.
2. Keep changes small and auditable.
3. Add or update tests for behavior changes.
4. Never commit credentials, private evidence, target data, or secrets.
5. Run `python -m unittest discover -s tests -v` before proposing a change.

## Quality
Prefer Python standard-library solutions where practical, deterministic output, clear error handling, and evidence-backed documentation.
