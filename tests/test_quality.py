import tempfile, unittest
from pathlib import Path
from cyberiq_tools.doctor import doctor
from cyberiq_tools.release import release_check
from cyberiq_tools.search import search_reports
from cyberiq_tools.dashboard import build_dashboard

class QualityTests(unittest.TestCase):
    def test_doctor_contract(self):
        result=doctor()
        self.assertIn("python_supported",result)
        self.assertIn("builtin_plugins",result)
        self.assertIn(result["status"],{"ok","unsupported-python"})

    def test_release_check_contract(self):
        result=release_check()
        self.assertIn("ready",result)
        self.assertIn("required_files",result)
        self.assertIn("CI status",result["note"])

    def test_search_limits(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): search_reports(d,"",limit=0)
            with self.assertRaises(ValueError): search_reports(d,"",limit=501)
            with self.assertRaises(ValueError): search_reports(d,"",severity="unknown")

    def test_dashboard_output_guard(self):
        with tempfile.TemporaryDirectory() as d:
            reports=Path(d)/"reports"; reports.mkdir()
            out=Path(d)/"nested"/"dashboard.html"
            self.assertEqual(build_dashboard(str(reports),str(out)),out)
            self.assertTrue(out.is_file())
            with self.assertRaises(ValueError): build_dashboard(str(reports),d)

if __name__=="__main__":
    unittest.main()
