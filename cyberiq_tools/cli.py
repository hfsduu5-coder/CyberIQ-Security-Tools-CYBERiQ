from __future__ import annotations
import argparse, json
from . import __version__
from .core import file_hashes, header_review, indicators, log_summary, read_text, url_inventory, verify_hash

def main():
    p=argparse.ArgumentParser(prog="cyberiq-tools",description="CyberIQ offline defensive security utilities.")
    p.add_argument("--version",action="version",version=f"%(prog)s {__version__}")
    sub=p.add_subparsers(dest="command",required=True)
    for name in ("hashcheck","headers","logsummary","urls","indicators"):
        x=sub.add_parser(name); x.add_argument("path")
    v=sub.add_parser("verify-hash"); v.add_argument("path"); v.add_argument("expected"); v.add_argument("--algorithm",choices=("md5","sha1","sha256","sha512"),default="sha256")
    a=p.parse_args()
    try:
        if a.command=="hashcheck": data=file_hashes(a.path)
        elif a.command=="verify-hash": data=verify_hash(a.path,a.expected,a.algorithm)
        elif a.command=="headers": data=header_review(read_text(a.path))
        elif a.command=="logsummary": data=log_summary(read_text(a.path))
        elif a.command=="urls": data=url_inventory(read_text(a.path))
        else: data=indicators(read_text(a.path))
        print(json.dumps(data,indent=2,ensure_ascii=False)); return 0
    except (ValueError,OSError) as exc: p.exit(1,f"Error: {exc}\n")

if __name__=="__main__": raise SystemExit(main())
