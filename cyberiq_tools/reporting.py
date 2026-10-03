from __future__ import annotations
import csv, html, json
from pathlib import Path

def save_report(data: dict, output: str, fmt: str="json") -> Path:
    p=Path(output); p.parent.mkdir(parents=True,exist_ok=True); fmt=fmt.lower()
    if fmt=="json":
        p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    elif fmt=="md":
        lines=["# CyberIQ Security Tools Report",""]
        for k,v in data.items(): lines.append(f"- **{k}**: `{v}`")
        p.write_text("\n".join(lines)+"\n",encoding="utf-8")
    elif fmt=="html":
        rows="".join(f"<tr><th>{html.escape(str(k))}</th><td><pre>{html.escape(str(v))}</pre></td></tr>" for k,v in data.items())
        p.write_text(f"<!doctype html><meta charset='utf-8'><title>CyberIQ Report</title><h1>CyberIQ Security Tools Report</h1><table>{rows}</table>",encoding="utf-8")
    elif fmt=="csv":
        with p.open("w",newline="",encoding="utf-8") as fh:
            w=csv.writer(fh); w.writerow(["key","value"]); [w.writerow([k,json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v]) for k,v in data.items()]
    else: raise ValueError("Unsupported report format.")
    return p
