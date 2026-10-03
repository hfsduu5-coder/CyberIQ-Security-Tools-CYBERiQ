import tempfile, unittest
from pathlib import Path
from cyberiq_tools.core import file_hashes, header_review, log_summary
class CoreTests(unittest.TestCase):
    def test_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.txt"; p.write_text("CyberIQ",encoding="utf-8")
            self.assertEqual(len(file_hashes(str(p))["sha256"]),64)
    def test_headers(self):
        r=header_review("Content-Security-Policy: default-src 'self'\nX-Content-Type-Options: nosniff")
        self.assertIn("content-security-policy",r["present"])
        self.assertIn("strict-transport-security",r["missing"])
    def test_logs(self):
        r=log_summary("INFO start\nERROR failed 192.0.2.1\n")
        self.assertEqual(r["levels"]["ERROR"],1); self.assertEqual(r["unique_ipv4_like_values"],1)
if __name__=="__main__": unittest.main()
