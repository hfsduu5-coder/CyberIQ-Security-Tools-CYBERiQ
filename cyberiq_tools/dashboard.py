from __future__ import annotations
import html, json
from pathlib import Path

def build_dashboard(report_dir: str, output: str="cyberiq-dashboard.html") -> Path:
    root=Path(report_dir)
    if not root.is_dir(): raise ValueError(f"Directory not found: {root}")
    cards=[]
    for p in sorted(root.glob("*.json"))[:100]:
        try: data=json.loads(p.read_text(encoding="utf-8"))
        except (OSError,json.JSONDecodeError): continue
        cards.append(f"<article><h2>{html.escape(p.name)}</h2><pre>{html.escape(json.dumps(data,indent=2,ensure_ascii=False))}</pre></article>")
    body="".join(cards) or "<p>No JSON reports found.</p>"
    page=f"""<!doctype html><html><head><meta charset="utf-8"><title>CyberIQ Dashboard</title><style>body{{background:#08090b;color:#eee;font:15px system-ui;max-width:1100px;margin:auto;padding:32px}}h1{{color:#e01937}}article{{background:#111318;border:1px solid #3a1018;border-radius:14px;padding:18px;margin:18px 0}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}</style></head><body><h1>CyberIQ Security Tools</h1><p>Local read-only report dashboard</p>{body}</body></html>"""
    out=Path(output); out.write_text(page,encoding="utf-8"); return out
