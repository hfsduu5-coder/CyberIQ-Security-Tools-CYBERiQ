from __future__ import annotations
import mimetypes, os
from datetime import datetime, timezone
from pathlib import Path
from .core import file_hashes

def file_metadata(path: str) -> dict:
    p=Path(path)
    if not p.is_file(): raise ValueError(f"File not found: {p}")
    st=p.stat(); mime,_=mimetypes.guess_type(p.name)
    return {"name":p.name,"extension":p.suffix.lower(),"bytes":st.st_size,"mime_guess":mime or "unknown",
      "modified_utc":datetime.fromtimestamp(st.st_mtime,tz=timezone.utc).isoformat(),
      "executable_by_owner":bool(st.st_mode & 0o100),"sha256":file_hashes(path)["sha256"],
      "note":"Local filesystem metadata only; no file execution or external lookup is performed."}

def directory_inventory(path: str, limit: int=1000) -> dict:
    root=Path(path)
    if not root.is_dir(): raise ValueError(f"Directory not found: {root}")
    files=[]; total=0
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        total+=p.stat().st_size
        if len(files)<limit: files.append({"path":str(p.relative_to(root)),"bytes":p.stat().st_size,"extension":p.suffix.lower()})
    return {"root":str(root),"files":len(files),"total_bytes":total,"items":files,"truncated":len(files)>=limit}
