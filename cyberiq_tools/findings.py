from __future__ import annotations
from .core import header_review, indicators, log_summary, url_inventory

def finding(kind: str, title: str, evidence: dict, severity: str="info") -> dict:
    return {"schema":"cyberiq.finding/v1","kind":kind,"severity":severity,"title":title,"evidence":evidence}

def analyze_text(text: str) -> dict:
    logs=log_summary(text); urls=url_inventory(text); inds=indicators(text)
    findings=[]
    if logs["levels"].get("CRITICAL",0): findings.append(finding("log","Critical log entries observed",{"count":logs["levels"]["CRITICAL"]},"high"))
    if logs["levels"].get("ERROR",0): findings.append(finding("log","Error log entries observed",{"count":logs["levels"]["ERROR"]},"medium"))
    if urls["urls_found"]: findings.append(finding("inventory","URLs observed in supplied text",{"count":urls["urls_found"],"unique_hosts":urls["unique_hosts"]}))
    if any(inds[k] for k in ("ipv4_like_values","domain_like_values","sha256_like_values","md5_like_values")): findings.append(finding("indicator","Indicator-like patterns observed",inds))
    return {"schema":"cyberiq.analysis/v1","findings":findings,"summary":{"findings":len(findings)},"note":"Offline evidence normalization only; findings are review signals, not threat verdicts."}

def analyze_headers(text: str) -> dict:
    review=header_review(text); findings=[]
    if review["missing"]: findings.append(finding("headers","Security headers absent from supplied response",{"missing":review["missing"]},"low"))
    return {"schema":"cyberiq.analysis/v1","findings":findings,"header_review":review}
