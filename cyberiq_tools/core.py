from __future__ import annotations
import hashlib, re
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit
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
    return {"file":p.name,"bytes":p.stat().st_size,**{n:h.hexdigest() for n,h in hs.items()}}

def verify_hash(path: str, expected: str, algorithm: str="sha256") -> dict:
    algorithm=algorithm.lower().replace("-","")
    if algorithm not in {"md5","sha1","sha256","sha512"}: raise ValueError("Unsupported hash algorithm.")
    actual=file_hashes(path)[algorithm]
    return {"algorithm":algorithm,"expected":expected.lower(),"actual":actual,"match":actual.lower()==expected.lower()}

def header_review(text: str) -> dict:
    observed={}
    for line in text.replace("\r\n","\n").splitlines():
        if ":" in line:
            k,v=line.split(":",1); observed[k.strip().lower()]=v.strip()
    wanted=("content-security-policy","strict-transport-security","x-content-type-options","referrer-policy","permissions-policy")
    return {"present":sorted(x for x in wanted if x in observed),"missing":sorted(x for x in wanted if x not in observed),"observed":sorted(observed),"note":"Missing headers are review signals, not proof of a vulnerability."}

def log_summary(text: str) -> dict:
    lines=[x for x in text.splitlines() if x.strip()]; levels=Counter()
    for line in lines:
        m=re.search(r"\b(ERROR|WARN|WARNING|INFO|DEBUG|CRITICAL)\b",line,re.I)
        if m: levels[m.group(1).upper()]+=1
    ips=set(re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])",text))
    return {"lines":len(lines),"levels":dict(sorted(levels.items())),"unique_ipv4_like_values":len(ips),"note":"Offline summary only; addresses are not contacted."}

def url_inventory(text: str) -> dict:
    urls=re.findall(r"https?://[^\s\]\[<>'\"]+",text)
    hosts=Counter(); schemes=Counter(); extensions=Counter()
    for raw in urls:
        p=urlsplit(raw)
        if p.hostname: hosts[p.hostname.lower()]+=1
        if p.scheme: schemes[p.scheme.lower()]+=1
        ext=Path(p.path).suffix.lower()
        if ext and len(ext)<=10: extensions[ext]+=1
    return {"urls_found":len(urls),"unique_hosts":len(hosts),"schemes":dict(sorted(schemes.items())),"top_hosts":dict(hosts.most_common(10)),"extensions":dict(extensions.most_common(10)),"note":"Offline inventory only; URLs are not contacted."}

def indicators(text: str) -> dict:
    ipv4=set(re.findall(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])",text))
    domains=set(re.findall(r"(?<![@\w-])(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}(?![\w-])",text))
    sha256=set(re.findall(r"(?i)(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])",text))
    md5=set(re.findall(r"(?i)(?<![0-9a-f])[0-9a-f]{32}(?![0-9a-f])",text))
    return {"ipv4_like_values":len(ipv4),"domain_like_values":len(domains),"sha256_like_values":len(sha256),"md5_like_values":len(md5),"note":"Pattern counts only; no reputation or maliciousness determination is performed."}
