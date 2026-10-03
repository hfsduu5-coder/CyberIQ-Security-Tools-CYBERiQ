from __future__ import annotations
from datetime import datetime, timezone

def executive_report(data: dict) -> str:
    findings=data.get("findings",[]) if isinstance(data,dict) else []
    counts={}
    for item in findings:
        severity=str(item.get("severity","info")).lower()
        counts[severity]=counts.get(severity,0)+1
    lines=[
        "# CyberIQ Executive Security Report","",
        "Generated: "+datetime.now(timezone.utc).isoformat(),"",
        "## Executive Summary",
        "- Normalized findings: **"+str(len(findings))+"**",
        "- Severity distribution: **"+str(counts or {"info":0})+"**","",
        "## Scope",
        "Offline analysis of user-supplied or local evidence. This report is not an external target scan.","",
        "## Findings"
    ]
    if not findings: lines.append("No normalized findings were present in the supplied analysis.")
    for i,item in enumerate(findings,1):
        lines.extend([
            "### "+str(i)+". "+str(item.get("title","Finding")),
            "- Severity: `"+str(item.get("severity","info"))+"`",
            "- Kind: `"+str(item.get("kind","unknown"))+"`",
            "- Evidence: `"+str(item.get("evidence",{}))+"`",""
        ])
    lines.extend(["## Interpretation","Findings are review signals and require analyst validation before conclusions are drawn.","","## CyberIQ","Defensive • Offline-first • Evidence-driven"])
    return "\n".join(lines)+"\n"
