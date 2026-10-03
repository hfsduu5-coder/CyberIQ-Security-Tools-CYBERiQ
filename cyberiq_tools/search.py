from __future__ import annotations
import json
from pathlib import Path

def search_reports(report_dir: str, query: str, severity: str|None=None, limit: int=50) -> dict:
    if limit < 1 or limit > 500: raise ValueError("Search limit must be between 1 and 500.")
    if severity is not None:
        severity=severity.lower().strip()
        if severity not in {"info","low","medium","high","critical"}: raise ValueError("Invalid severity.")
    root=Path(report_dir)
    if not root.is_dir(): raise ValueError(f"Directory not found: {root}")
    q=query.casefold().strip(); matches=[]
    for p in sorted(root.glob("*.json"))[:500]:
        try: data=json.loads(p.read_text(encoding="utf-8"))
        except (OSError,json.JSONDecodeError): continue
        findings=data.get("findings",[]) if isinstance(data,dict) else []
        for item in findings if isinstance(findings,list) else []:
            if not isinstance(item,dict): continue
            sev=str(item.get("severity","info")).lower()
            blob=json.dumps(item,ensure_ascii=False).casefold()
            if (not q or q in blob) and (not severity or sev==severity.lower()):
                matches.append({"report":p.name,"finding":item})
                if len(matches)>=limit: return {"query":query,"severity":severity,"matches":matches,"truncated":True}
    return {"query":query,"severity":severity,"matches":matches,"truncated":False}
