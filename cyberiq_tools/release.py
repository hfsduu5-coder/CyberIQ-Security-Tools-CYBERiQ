from __future__ import annotations
import json
from pathlib import Path
from . import __version__
from .doctor import doctor

def release_check() -> dict:
    required=["README.md","CHANGELOG.md","LICENSE","SECURITY.md","pyproject.toml","docs/ARCHITECTURE.md","docs/PLUGINS.md","docs/MIGRATION-v9.md"]
    files={name:Path(name).is_file() for name in required}
    diag=doctor()
    return {"version":__version__,"required_files":files,"all_required_files":all(files.values()),"environment":diag,
            "ready":all(files.values()) and diag.get("python_supported",False),
            "note":"Local release readiness check only; CI status and remote repository settings are not asserted."}
