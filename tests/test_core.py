import json, tempfile, unittest
from pathlib import Path
from cyberiq_tools.batch import analyze_directory
from cyberiq_tools.core import file_hashes, header_review, indicators, log_summary, url_inventory, verify_hash
from cyberiq_tools.findings import analyze_text
from cyberiq_tools.metadata import directory_inventory, file_metadata
from cyberiq_tools.reporting import save_report
from cyberiq_tools.schemas import validate_document
from cyberiq_tools.workspace import add_evidence, case_status, create_case

class RegressionTests(unittest.TestCase):
    def test_core_and_reports(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.log"; p.write_text("ERROR 192.0.2.1 https://lab.example/a.js\n"+"a"*64,encoding="utf-8")
            h=file_hashes(str(p)); self.assertTrue(verify_hash(str(p),h["sha256"])["match"])
            self.assertEqual(file_metadata(str(p))["bytes"],p.stat().st_size)
            self.assertEqual(directory_inventory(d)["files"],1)
            self.assertEqual(log_summary(p.read_text())["levels"]["ERROR"],1)
            self.assertEqual(url_inventory(p.read_text())["urls_found"],1)
            self.assertEqual(indicators(p.read_text())["sha256_like_values"],1)
            out=Path(d)/"r.json"; save_report({"ok":True},str(out)); self.assertTrue(json.loads(out.read_text())["ok"])
    def test_headers_findings_and_batch(self):
        self.assertIn("strict-transport-security",header_review("X-Content-Type-Options: nosniff")["missing"])
        analysis=analyze_text("ERROR 192.0.2.1 https://lab.example/"); self.assertGreater(analysis["summary"]["findings"],0)
        self.assertTrue(validate_document(analysis,"analysis")["valid"])
        with tempfile.TemporaryDirectory() as d:
            Path(d,"a.log").write_text("INFO ok",encoding="utf-8")
            self.assertEqual(analyze_directory(d)["processed"],1)
    def test_case_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            case=create_case("demo",d); e=Path(d)/"evidence.txt"; e.write_text("sample",encoding="utf-8")
            record=add_evidence(str(case),str(e)); self.assertEqual(len(record["sha256"]),64)
            self.assertEqual(case_status(str(case))["evidence_count"],1)

if __name__=="__main__": unittest.main()
