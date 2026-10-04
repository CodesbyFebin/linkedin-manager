import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "approval_gate.py"


class ApprovalGateTests(unittest.TestCase):
    def run_gate(self, text, fmt="comment"):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as handle:
            handle.write(text)
            path = handle.name
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--format", fmt, path],
            capture_output=True, text=True,
        )
        return proc.returncode, proc.stdout

    def test_secret_closes_gate(self):
        code, out = self.run_gate("A note with sk_live_abc123 and no link. " * 8)
        self.assertEqual(code, 1)
        self.assertIn("GATE: closed", out)
        self.assertIn("secrets", out)

    def test_clean_comment_can_open(self):
        text = "The gate failed on length. We kept the draft and waited for a yes. " * 4
        code, out = self.run_gate(text, "comment")
        self.assertIn("GATE:", out)
        self.assertNotIn("secrets", out.split("PASS | secrets")[-1][:20])


if __name__ == "__main__":
    unittest.main()
