import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stderr
import io
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "detection_snapshot.py"
SPEC = importlib.util.spec_from_file_location("detection_snapshot", SCRIPT)
detection_snapshot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(detection_snapshot)


class DetectionSnapshotTests(unittest.TestCase):
    def test_snapshot_reports_existing_contracts_without_becoming_a_gate(self):
        snapshot = detection_snapshot.build_snapshot("test-revision")

        self.assertTrue(snapshot["report_only"])
        self.assertEqual(snapshot["revision"], "test-revision")
        self.assertEqual(len(snapshot["fixture_sha256"]), 64)
        self.assertEqual(snapshot["summary"]["contract_failures"], 0)
        self.assertEqual(
            snapshot["summary"]["detected_expected"],
            snapshot["summary"]["expected_detections"],
        )
        self.assertGreater(snapshot["summary"]["tolerated_false_positive_findings"], 0)

    def test_output_file_is_atomic_cli_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "snapshot.json"
            exit_code = detection_snapshot.main(["--revision", "abc123", "--output", str(output)])

            self.assertEqual(exit_code, 0)
            self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["revision"], "abc123")

    def test_operational_error_returns_exit_two_without_traceback(self):
        with mock.patch.object(detection_snapshot, "build_snapshot", side_effect=OSError("fixture vanished")):
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                exit_code = detection_snapshot.main([])
        self.assertEqual(exit_code, 2)
        self.assertIn("fixture vanished", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
