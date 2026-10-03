import tempfile, unittest
from pathlib import Path
from cyberiq_tools.core import file_hashes, header_review, indicators, log_summary, url_inventory, verify_hash

class CoreTests(unittest.TestCase):
    def test_hashes_and_verify(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"x.txt"; p.write_text("CyberIQ",encoding="utf-8")
            hashes=file_hashes(str(p))
            self.assertEqual(len(hashes["sha256"]),64)
            self.assertTrue(verify_hash(str(p),hashes["sha256"])["match"])
            self.assertFalse(verify_hash(str(p),"0"*64)["match"])
    def test_headers(self):
        r=header_review("Content-Security-Policy: default-src 'self'\nX-Content-Type-Options: nosniff")
        self.assertIn("content-security-policy",r["present"]); self.assertIn("strict-transport-security",r["missing"])
    def test_logs(self):
        r=log_summary("INFO start\nERROR failed 192.0.2.1\n")
        self.assertEqual(r["levels"]["ERROR"],1); self.assertEqual(r["unique_ipv4_like_values"],1)
    def test_urls(self):
        r=url_inventory("https://lab.example/a.js http://lab.example/b.css")
        self.assertEqual(r["urls_found"],2); self.assertEqual(r["unique_hosts"],1)
    def test_indicators(self):
        r=indicators("192.0.2.1 example.org "+"a"*64)
        self.assertEqual(r["ipv4_like_values"],1); self.assertEqual(r["sha256_like_values"],1)

if __name__=="__main__": unittest.main()
