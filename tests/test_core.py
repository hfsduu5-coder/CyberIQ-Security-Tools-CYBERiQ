import tempfile, unittest
from pathlib import Path
from cyberiq_tools.core import file_hashes, header_review, indicators, log_summary, url_inventory, verify_hash
from cyberiq_tools.metadata import directory_inventory, file_metadata
from cyberiq_tools.reporting import save_report

class CoreTests(unittest.TestCase):
    def test_hashes_verify_metadata_reports(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.txt"; p.write_text("CyberIQ",encoding="utf-8")
            hashes=file_hashes(str(p)); self.assertEqual(len(hashes["sha256"]),64)
            self.assertTrue(verify_hash(str(p),hashes["sha256"])["match"])
            self.assertEqual(file_metadata(str(p))["bytes"],7)
            self.assertEqual(directory_inventory(d)["files"],1)
            out=Path(d)/"report.json"; save_report({"ok":True},str(out)); self.assertTrue(out.exists())
    def test_headers(self):
        r=header_review("Content-Security-Policy: default-src 'self'\nX-Content-Type-Options: nosniff")
        self.assertIn("content-security-policy",r["present"]); self.assertIn("strict-transport-security",r["missing"])
    def test_logs_urls_indicators(self):
        text="INFO start\nERROR 192.0.2.1 https://lab.example/a.js\n"+"a"*64
        self.assertEqual(log_summary(text)["levels"]["ERROR"],1)
        self.assertEqual(url_inventory(text)["urls_found"],1)
        self.assertEqual(indicators(text)["sha256_like_values"],1)

if __name__=="__main__": unittest.main()
