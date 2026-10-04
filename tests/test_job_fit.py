import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "job_fit.py"


class JobFitTests(unittest.TestCase):
    def test_extracts_title_without_network(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write("Title: Systems engineer\nLocation: Kochi\nHybrid role.\n")
            path = handle.name
        proc = subprocess.run([sys.executable, str(SCRIPT), path], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Systems engineer", proc.stdout)
        self.assertIn("Do not apply", proc.stdout)


if __name__ == "__main__":
    unittest.main()
