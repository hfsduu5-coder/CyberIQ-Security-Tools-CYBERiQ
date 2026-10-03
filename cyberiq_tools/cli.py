from __future__ import annotations
import argparse, json
from . import __version__
from .core import file_hashes, header_review, indicators, log_summary, read_text, url_inventory, verify_hash
from .metadata import directory_inventory, file_metadata
from .reporting import save_report
from .dashboard import build_dashboard
from .workspace import add_evidence, add_note, case_status, case_timeline, create_case, set_status
from .findings import analyze_headers, analyze_text
from .batch import analyze_directory
from .builtin_plugins import load_builtin_plugins
from .plugins import list_plugins, run_plugin
from .doctor import doctor
from .templates import executive_report

def add_output(p):
    p.add_argument("--output"); p.add_argument("--format",choices=("json","md","html","csv"),default="json")

def main():
    p=argparse.ArgumentParser(prog="cyberiq-tools",description="CyberIQ offline defensive security utilities.")
    p.add_argument("--version",action="version",version=f"%(prog)s {__version__}")
    sub=p.add_subparsers(dest="command",required=True)
    sub.add_parser("doctor")
    ex=sub.add_parser("executive-report"); ex.add_argument("path"); ex.add_argument("--output",default="cyberiq-executive-report.md")
    for name in ("hashcheck","headers","logsummary","urls","indicators","metadata","inventory"):
        x=sub.add_parser(name); x.add_argument("path"); add_output(x)
    v=sub.add_parser("verify-hash"); v.add_argument("path"); v.add_argument("expected"); v.add_argument("--algorithm",choices=("md5","sha1","sha256","sha512"),default="sha256"); add_output(v)
    d=sub.add_parser("dashboard"); d.add_argument("report_dir"); d.add_argument("--output",default="cyberiq-dashboard.html")
    pl=sub.add_parser("plugin"); ps=pl.add_subparsers(dest="plugin_command",required=True); ps.add_parser("list"); pr=ps.add_parser("run"); pr.add_argument("name"); pr.add_argument("path"); add_output(pr)
    bt=sub.add_parser("batch"); bt.add_argument("path"); bt.add_argument("--pattern",default="*.log"); bt.add_argument("--limit",type=int,default=100); add_output(bt)
    an=sub.add_parser("analyze"); an.add_argument("path"); an.add_argument("--type",choices=("text","headers"),default="text"); add_output(an)
    case=sub.add_parser("case"); cs=case.add_subparsers(dest="case_command",required=True)
    cn=cs.add_parser("new"); cn.add_argument("name"); cn.add_argument("--root",default="cases")
    ca=cs.add_parser("add"); ca.add_argument("case_path"); ca.add_argument("evidence_path")
    ct=cs.add_parser("status"); ct.add_argument("case_path")
    ctl=cs.add_parser("timeline"); ctl.add_argument("case_path")
    cnn=cs.add_parser("note"); cnn.add_argument("case_path"); cnn.add_argument("text")
    cst=cs.add_parser("set-status"); cst.add_argument("case_path"); cst.add_argument("status",choices=("open","review","closed"))
    a=p.parse_args()
    try:
        if a.command=="executive-report":
            data=json.loads(read_text(a.path)); from pathlib import Path; Path(a.output).write_text(executive_report(data),encoding="utf-8"); print(f"Executive report saved: {a.output}"); return 0
        if a.command=="doctor":
            print(json.dumps(doctor(),indent=2)); return 0
        if a.command=="plugin":
            load_builtin_plugins()
            if a.plugin_command=="list":
                for x in list_plugins(): print(f"{x.name:12} {x.description}")
            else:
                data=run_plugin(a.name,read_text(a.path))
                if a.output: print(f"Report saved: {save_report(data,a.output,a.format)}")
                else: print(json.dumps(data,indent=2,ensure_ascii=False))
            return 0
        if a.command=="batch":
            data=analyze_directory(a.path,a.pattern,a.limit)
            if a.output: print(f"Report saved: {save_report(data,a.output,a.format)}")
            else: print(json.dumps(data,indent=2,ensure_ascii=False))
            return 0
        if a.command=="analyze":
            data=analyze_headers(read_text(a.path)) if a.type=="headers" else analyze_text(read_text(a.path))
            if a.output: print(f"Report saved: {save_report(data,a.output,a.format)}")
            else: print(json.dumps(data,indent=2,ensure_ascii=False))
            return 0
        if a.command=="case":
            if a.case_command=="new": print(f"Case created: {create_case(a.name,a.root)}")
            elif a.case_command=="add": print(json.dumps(add_evidence(a.case_path,a.evidence_path),indent=2))
            elif a.case_command=="timeline": print(json.dumps(case_timeline(a.case_path),indent=2))
            elif a.case_command=="note": print(json.dumps(add_note(a.case_path,a.text),indent=2))
            elif a.case_command=="set-status": print(json.dumps(set_status(a.case_path,a.status),indent=2))
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
