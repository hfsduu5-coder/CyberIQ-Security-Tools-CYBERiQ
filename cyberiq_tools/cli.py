from __future__ import annotations
import argparse, json
from . import __version__
from .core import file_hashes, header_review, indicators, log_summary, read_text, url_inventory, verify_hash
from .metadata import directory_inventory, file_metadata
from .reporting import save_report
from .dashboard import build_dashboard
from .workspace import add_evidence, case_status, create_case
from .findings import analyze_headers, analyze_text

def add_output(p):
    p.add_argument("--output"); p.add_argument("--format",choices=("json","md","html","csv"),default="json")

def main():
    p=argparse.ArgumentParser(prog="cyberiq-tools",description="CyberIQ offline defensive security utilities.")
    p.add_argument("--version",action="version",version=f"%(prog)s {__version__}")
    sub=p.add_subparsers(dest="command",required=True)
    for name in ("hashcheck","headers","logsummary","urls","indicators","metadata","inventory"):
        x=sub.add_parser(name); x.add_argument("path"); add_output(x)
    v=sub.add_parser("verify-hash"); v.add_argument("path"); v.add_argument("expected"); v.add_argument("--algorithm",choices=("md5","sha1","sha256","sha512"),default="sha256"); add_output(v)
    d=sub.add_parser("dashboard"); d.add_argument("report_dir"); d.add_argument("--output",default="cyberiq-dashboard.html")
    an=sub.add_parser("analyze"); an.add_argument("path"); an.add_argument("--type",choices=("text","headers"),default="text"); add_output(an)
    case=sub.add_parser("case"); cs=case.add_subparsers(dest="case_command",required=True)
    cn=cs.add_parser("new"); cn.add_argument("name"); cn.add_argument("--root",default="cases")
    ca=cs.add_parser("add"); ca.add_argument("case_path"); ca.add_argument("evidence_path")
    ct=cs.add_parser("status"); ct.add_argument("case_path")
    a=p.parse_args()
    try:
        if a.command=="analyze":
            data=analyze_headers(read_text(a.path)) if a.type=="headers" else analyze_text(read_text(a.path))
            if a.output: print(f"Report saved: {save_report(data,a.output,a.format)}")
            else: print(json.dumps(data,indent=2,ensure_ascii=False))
            return 0
        if a.command=="case":
            if a.case_command=="new": print(f"Case created: {create_case(a.name,a.root)}")
            elif a.case_command=="add": print(json.dumps(add_evidence(a.case_path,a.evidence_path),indent=2))
            else: print(json.dumps(case_status(a.case_path),indent=2))
            return 0
        if a.command=="dashboard":
            print(f"Dashboard saved: {build_dashboard(a.report_dir,a.output)}"); return 0
        if a.command=="hashcheck": data=file_hashes(a.path)
        elif a.command=="verify-hash": data=verify_hash(a.path,a.expected,a.algorithm)
        elif a.command=="headers": data=header_review(read_text(a.path))
        elif a.command=="logsummary": data=log_summary(read_text(a.path))
        elif a.command=="urls": data=url_inventory(read_text(a.path))
        elif a.command=="indicators": data=indicators(read_text(a.path))
        elif a.command=="metadata": data=file_metadata(a.path)
        else: data=directory_inventory(a.path)
        if a.output: print(f"Report saved: {save_report(data,a.output,a.format)}")
        else: print(json.dumps(data,indent=2,ensure_ascii=False))
        return 0
    except (ValueError,OSError) as exc: p.exit(1,f"Error: {exc}\n")

if __name__=="__main__": raise SystemExit(main())
