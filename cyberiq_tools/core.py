from __future__ import annotations
import hashlib, re
from collections import Counter
from pathlib import Path
MAX_BYTES=5_000_000

def read_text(path: str) -> str:
    p=Path(path)
    if not p.is_file(): raise ValueError(f"File not found: {p}")
    if p.stat().st_size>MAX_BYTES: raise ValueError("Input file exceeds 5 MB safety limit.")
    return p.read_text(encoding="utf-8",errors="replace")

def file_hashes(path: str) -> dict:
    p=Path(path)
    if not p.is_file(): raise ValueError(f"File not found: {p}")
    hs={n:hashlib.new(n) for n in ("md5","sha1","sha256","sha512")}
    with p.open("rb") as fh:
        for chunk in iter(lambda:fh.read(65536),b""):
            for h in hs.values(): h.update(chunk)
    return {n:h.hexdigest() for n,h in hs.items()}

def header_review(text: str) -> dict:
    observed={}
    for line in text.replace("\r\n","\n").splitlines():
        if ":" in line:
            k,v=line.split(":",1); observed[k.strip().lower()]=v.strip()
    wanted=("content-security-policy","strict-transport-security","x-content-type-options","referrer-policy","permissions-policy")
    return {"present":sorted(x for x in wanted if x in observed),"missing":sorted(x for x in wanted if x not in observed),"note":"Missing headers are review signals, not proof of a vulnerability."}

def log_summary(text: str) -> dict:
    lines=[x for x in text.splitlines() if x.strip()]; levels=Counter()
    for line in lines:
        m=re.search(r"\b(ERROR|WARN|WARNING|INFO|DEBUG|CRITICAL)\b",line,re.I)
        if m: levels[m.group(1).upper()]+=1
    ips=set(re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])",text))
    return {"lines":len(lines),"levels":dict(sorted(levels.items())),"unique_ipv4_like_values":len(ips),"note":"Offline summary only; addresses are not contacted."}
