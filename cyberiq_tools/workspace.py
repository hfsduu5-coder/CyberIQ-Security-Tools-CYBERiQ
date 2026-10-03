from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path
from .core import file_hashes

def _safe_name(name: str) -> str:
    value=re.sub(r"[^A-Za-z0-9._-]+","-",name.strip()).strip("-")
    if not value or value in {".",".."}: raise ValueError("Invalid case name.")
    return value

def create_case(name: str, root: str="cases") -> Path:
    base=Path(root)/_safe_name(name)
    if base.exists(): raise ValueError(f"Case already exists: {base}")
    for part in ("evidence","reports","notes"): (base/part).mkdir(parents=True,exist_ok=True)
    meta={"schema":"cyberiq.case/v1","name":base.name,"created_utc":datetime.now(timezone.utc).isoformat(),"evidence":[]}
    (base/"case.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    return base

def add_evidence(case_path: str, evidence_path: str) -> dict:
    case=Path(case_path); meta_path=case/"case.json"
    if not meta_path.is_file(): raise ValueError("Not a CyberIQ case workspace.")
    src=Path(evidence_path)
    if not src.is_file(): raise ValueError(f"File not found: {src}")
    meta=json.loads(meta_path.read_text(encoding="utf-8"))
    record={"name":src.name,"source_path":str(src.resolve()),"bytes":src.stat().st_size,"sha256":file_hashes(str(src))["sha256"],"recorded_utc":datetime.now(timezone.utc).isoformat()}
    meta["evidence"].append(record); meta_path.write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")
    return record

def case_status(case_path: str) -> dict:
    p=Path(case_path); f=p/"case.json"
    if not f.is_file(): raise ValueError("Not a CyberIQ case workspace.")
    data=json.loads(f.read_text(encoding="utf-8"))
    return {"name":data.get("name"),"created_utc":data.get("created_utc"),"evidence_count":len(data.get("evidence",[])),"reports":len(list((p/"reports").glob("*"))) if (p/"reports").is_dir() else 0}
