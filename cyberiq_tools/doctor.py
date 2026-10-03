from __future__ import annotations
import sys
from pathlib import Path
from . import __version__
from .builtin_plugins import load_builtin_plugins
from .plugins import list_plugins

def doctor() -> dict:
    load_builtin_plugins()
    return {
      "version":__version__,
      "python":".".join(map(str,sys.version_info[:3])),
      "python_supported":sys.version_info >= (3,10),
      "cwd_writable":Path.cwd().exists() and os_access(Path.cwd()),
      "builtin_plugins":[p.name for p in list_plugins()],
      "status":"ok" if sys.version_info >= (3,10) else "unsupported-python",
    }

def os_access(path: Path) -> bool:
    import os
    return os.access(path,os.W_OK)
