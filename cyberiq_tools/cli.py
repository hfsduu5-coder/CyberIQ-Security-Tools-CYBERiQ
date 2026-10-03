from __future__ import annotations
import argparse, json
from .core import file_hashes, header_review, log_summary, read_text

def main():
    p=argparse.ArgumentParser(prog="cyberiq-tools",description="CyberIQ defensive security utilities.")
    sub=p.add_subparsers(dest="command",required=True)
    for name in ("hashcheck","headers","logsummary"):
        x=sub.add_parser(name); x.add_argument("path")
    a=p.parse_args()
    try:
        if a.command=="hashcheck": data=file_hashes(a.path)
        elif a.command=="headers": data=header_review(read_text(a.path))
        else: data=log_summary(read_text(a.path))
        print(json.dumps(data,indent=2,ensure_ascii=False)); return 0
    except (ValueError,OSError) as exc: p.exit(1,f"Error: {exc}\n")

if __name__=="__main__": raise SystemExit(main())
