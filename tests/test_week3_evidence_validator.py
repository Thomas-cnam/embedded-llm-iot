"""Tests for the Week 3 evidence validator."""

import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_week3_evidence import DIAG_END, DIAG_START, parse_evidence

PHASES = ("ambient", "covered", "ambient recovery", "phone flashlight", "final ambient recovery")


def make_event(event_id, kind, value):
    return {"schema_version": "1.0", "event_type": "anomaly", "sensor": "photoresistor",
            "event_id": event_id, "anomaly_type": kind, "detector_method": "threshold",
            "value": value, "previous_value": 16000, "delta": value - 16000,
            "history": [16000, value], "timestamp_ms": event_id * 1000,
            "local_alarm": True, "low_threshold": 5000, "high_threshold": 32000,
            "delta_threshold": 8000}


def complete_lines(test_markers=False):
    lines = ["TEST_START week3_anomaly_serial_event_test" if test_markers else DIAG_START]
    event_id = 0
    for phase_number, phase in enumerate(PHASES, 1):
        lines.append("DIAG Phase %d of 5 : %s" % (phase_number, phase))
        for index in range(1, 13):
            value, state, decision, alarm, emitted = 16000, "normal", "normal", "none", None
            if phase in ("covered", "phone flashlight"):
                kind = "low_light" if phase == "covered" else "high_light"
                value = 1000 if kind == "low_light" else 40000
                state = kind
                if index == 1:
                    decision = "entered_anomaly"
                elif index == 11:
                    decision = "cooldown_repeat"
                else:
                    decision = "suppressed_same_anomaly"
                alarm = "trigger_" + kind if index in (1, 11) else "none"
                if index in (1, 11):
                    event_id += 1
                    emitted = make_event(event_id, kind, value)
            lines.append("DIAG Sample %d of 12 value= %d state= %s decision= %s alarm= %s" %
                         (index, value, state, decision, alarm))
            if emitted:
                lines.append(json.dumps(emitted, separators=(",", ":")))
    lines.append("DIAG Guided anomaly hardware integration sequence completed.")
    lines.append("TEST_END week3_anomaly_serial_event_test" if test_markers else DIAG_END)
    return lines


class ValidatorTests(unittest.TestCase):
    def validate(self, lines):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "raw.txt"
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            return parse_evidence(path)

    def test_valid_diag_boundaries_and_low_high_events(self):
        result = self.validate(complete_lines())
        self.assertEqual(result["errors"], [])
        self.assertEqual([e["event_id"] for e in result["events"]], [1, 2, 3, 4])

    def test_valid_test_markers(self):
        self.assertEqual(self.validate(complete_lines(True))["errors"], [])

    def test_missing_start(self):
        self.assertIn("missing start boundary", self.validate(complete_lines()[1:])["errors"])

    def test_missing_end(self):
        self.assertIn("missing end boundary", self.validate(complete_lines()[:-1])["errors"])

    def test_missing_phase(self):
        result = self.validate([line for line in complete_lines() if "Phase 3 of 5" not in line])
        self.assertTrue(any("missing phase" in error for error in result["errors"]))

    def modify_first_event(self, update):
        lines = complete_lines()
        index = next(i for i, line in enumerate(lines) if line.startswith("{"))
        event = json.loads(lines[index]); update(event)
        lines[index] = json.dumps(event, separators=(",", ":"))
        return self.validate(lines)

    def test_malformed_json(self):
        lines = complete_lines(); index = next(i for i, line in enumerate(lines) if line.startswith("{")); lines[index] = "{bad"
        self.assertTrue(any("malformed JSON" in error for error in self.validate(lines)["errors"]))

    def test_invalid_schema(self):
        self.assertTrue(any("schema_version" in e for e in self.modify_first_event(lambda x: x.update(schema_version="2.0"))["errors"]))

    def test_duplicate_event_id(self):
        lines = complete_lines(); indexes = [i for i, line in enumerate(lines) if line.startswith("{")]
        event = json.loads(lines[indexes[1]]); event["event_id"] = 1; lines[indexes[1]] = json.dumps(event)
        self.assertTrue(any("strictly increasing" in e for e in self.validate(lines)["errors"]))

    def test_decreasing_event_id(self):
        lines = complete_lines(); indexes = [i for i, line in enumerate(lines) if line.startswith("{")]
        for index, value in zip(indexes, (2, 1)):
            event = json.loads(lines[index]); event["event_id"] = value; lines[index] = json.dumps(event)
        self.assertTrue(any("strictly increasing" in e for e in self.validate(lines)["errors"]))

    def test_invalid_adc_value(self):
        self.assertTrue(any("value must" in e for e in self.modify_first_event(lambda x: x.update(value=70000))["errors"]))

    def test_boolean_event_id(self):
        self.assertTrue(any("event_id" in e for e in self.modify_first_event(lambda x: x.update(event_id=True))["errors"]))

    def test_diag_and_summary_ignored(self):
        lines = complete_lines(); lines[1:1] = ["DIAG note", "SUMMARY note"]
        self.assertEqual(self.validate(lines)["errors"], [])

    def test_cleanup_recognized(self):
        self.assertEqual(self.validate(complete_lines())["boundary_style"], "DIAG start/cleanup")


if __name__ == "__main__":
    unittest.main()
