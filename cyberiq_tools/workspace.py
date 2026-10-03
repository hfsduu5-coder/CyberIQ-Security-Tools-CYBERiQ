from __future__ import annotations
import json, re
from datetime import datetime, timezone
from pathlib import Path
from .core import file_hashes

def _now(): return datetime.now(timezone.utc).isoformat()
def _safe_name(name: str) -> str:
    value=re.sub(r"[^A-Za-z0-9._-]+","-",name.strip()).strip("-")
    if not value or value in {".",".."}: raise ValueError("Invalid case name.")
    return value
def _load(case: Path) -> tuple[Path,dict]:
    f=case/"case.json"
    if not f.is_file(): raise ValueError("Not a CyberIQ case workspace.")
    return f,json.loads(f.read_text(encoding="utf-8"))
def _save(path: Path,data: dict):
    tmp=path.with_name(path.name+".tmp")
    tmp.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    tmp.replace(path)

def create_case(name: str, root: str="cases") -> Path:
    base=Path(root)/_safe_name(name)
    if base.exists(): raise ValueError(f"Case already exists: {base}")
    for part in ("evidence","reports","notes"): (base/part).mkdir(parents=True,exist_ok=True)
    _save(base/"case.json",{"schema":"cyberiq.case/v2","name":base.name,"created_utc":_now(),"status":"open","evidence":[],"timeline":[{"at":_now(),"event":"case-created"}]})
    return base

def add_evidence(case_path: str, evidence_path: str) -> dict:
    case=Path(case_path); meta_path,meta=_load(case); src=Path(evidence_path)
    if not src.is_file(): raise ValueError(f"File not found: {src}")
    digest=file_hashes(str(src))["sha256"]
    for item in meta.get("evidence",[]):
        if item.get("sha256")==digest: raise ValueError("Duplicate evidence content.")
    record={"id":f"E-{len(meta.get('evidence',[]))+1:03d}","name":src.name,"bytes":src.stat().st_size,"sha256":digest,"recorded_utc":_now()}
    meta.setdefault("evidence",[]).append(record); meta.setdefault("timeline",[]).append({"at":record["recorded_utc"],"event":"evidence-recorded","name":src.name,"sha256":record["sha256"]})
    _save(meta_path,meta); return record

def add_note(case_path: str, note: str) -> dict:
    case=Path(case_path); meta_path,meta=_load(case); event={"at":_now(),"event":"note","text":note[:1000]}
    meta.setdefault("timeline",[]).append(event); _save(meta_path,meta); return event

def set_status(case_path: str, status: str) -> dict:
    if status not in {"open","review","closed"}: raise ValueError("Status must be open, review, or closed.")
    case=Path(case_path); meta_path,meta=_load(case); meta["status"]=status
    meta.setdefault("timeline",[]).append({"at":_now(),"event":"status-changed","status":status}); _save(meta_path,meta)
    return {"name":meta.get("name"),"status":status}

def case_timeline(case_path: str) -> list[dict]:
    _,meta=_load(Path(case_path)); return meta.get("timeline",[])

def case_status(case_path: str) -> dict:
    p=Path(case_path); _,data=_load(p)
    return {"name":data.get("name"),"status":data.get("status","open"),"created_utc":data.get("created_utc"),"evidence_count":len(data.get("evidence",[])),"timeline_events":len(data.get("timeline",[])),"reports":len(list((p/"reports").glob("*"))) if (p/"reports").is_dir() else 0}
