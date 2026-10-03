from __future__ import annotations
from pathlib import Path
from .core import read_text
from .findings import analyze_text

def analyze_directory(path: str, pattern: str="*.log", limit: int=100) -> dict:
    root=Path(path)
    if not root.is_dir(): raise ValueError(f"Directory not found: {root}")
    results=[]; errors=[]
    for p in sorted(root.rglob(pattern))[:limit]:
        try: results.append({"file":str(p.relative_to(root)),"analysis":analyze_text(read_text(str(p)))})
        except (ValueError,OSError) as exc: errors.append({"file":str(p.relative_to(root)),"error":str(exc)})
    return {"schema":"cyberiq.batch/v1","root":str(root),"pattern":pattern,"processed":len(results),"errors":errors,"results":results}
