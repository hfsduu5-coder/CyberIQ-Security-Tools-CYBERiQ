from __future__ import annotations
import html, json
from collections import Counter
from pathlib import Path

def _load_reports(root: Path) -> list[tuple[Path,dict]]:
    reports=[]
    for p in sorted(root.glob("*.json"))[:250]:
        try:
            data=json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data,dict): reports.append((p,data))
        except (OSError,json.JSONDecodeError): continue
    return reports

def build_dashboard(report_dir: str, output: str="cyberiq-dashboard.html") -> Path:
    root=Path(report_dir)
    if not root.is_dir(): raise ValueError(f"Directory not found: {root}")
    reports=_load_reports(root); severities=Counter(); finding_count=0
    for _,data in reports:
        findings=data.get("findings",[])
        if isinstance(findings,list):
            finding_count+=len(findings)
            for f in findings:
                if isinstance(f,dict): severities[str(f.get("severity","info")).lower()]+=1
    cards=[]
    for p,data in reports:
        schema=html.escape(str(data.get("schema","unversioned")))
        cards.append(f"<article><div class='card-head'><h2>{html.escape(p.name)}</h2><span>{schema}</span></div><pre>{html.escape(json.dumps(data,indent=2,ensure_ascii=False))}</pre></article>")
    body="".join(cards) or "<article><p>No JSON reports found.</p></article>"
    sev=" ".join(f"<span class='pill'>{html.escape(k)} {v}</span>" for k,v in sorted(severities.items())) or "<span class='pill'>no normalized findings</span>"
    page=f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>CyberIQ Dashboard</title><style>
:root{{--bg:#07080a;--panel:#101216;--line:#351019;--red:#e01839;--muted:#9aa0aa;--text:#f2f3f5}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px system-ui}}header{{position:sticky;top:0;background:#08090bea;border-bottom:1px solid var(--line);backdrop-filter:blur(10px)}}.wrap{{max-width:1180px;margin:auto;padding:22px}}h1{{margin:0;color:var(--red);font-size:28px}}.sub{{color:var(--muted);margin-top:5px}}.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:22px 0}}.metric,article{{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px}}.metric strong{{display:block;font-size:26px}}.pill{{display:inline-block;border:1px solid #4b1822;border-radius:999px;padding:5px 9px;margin:3px;color:#ddd}}.card-head{{display:flex;justify-content:space-between;gap:12px;align-items:center}}.card-head span{{color:var(--muted)}}article{{margin:14px 0}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#090a0d;padding:14px;border-radius:10px;max-height:460px;overflow:auto}}footer{{color:var(--muted);padding:30px 0}}</style></head><body><header><div class="wrap"><h1>CyberIQ Security Tools</h1><div class="sub">Local • read-only • offline-first dashboard</div></div></header><main class="wrap"><section class="metrics"><div class="metric"><span>Reports</span><strong>{len(reports)}</strong></div><div class="metric"><span>Findings</span><strong>{finding_count}</strong></div><div class="metric"><span>Directory</span><strong>{html.escape(root.name or ".")}</strong></div></section><section>{sev}</section>{body}<footer>CyberIQ • Defensive analysis workspace</footer></main></body></html>"""
    out=Path(output); out.write_text(page,encoding="utf-8"); return out
