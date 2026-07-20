"""Validate Week 3 ESP32-C6 console evidence without modifying it."""

import argparse
import json
import re
import sys
from pathlib import Path

TEST_START = "TEST_START week3_anomaly_serial_event_test"
TEST_END = "TEST_END week3_anomaly_serial_event_test"
DIAG_START = "DIAG ESP32-C6 anomaly hardware integration test"
DIAG_END = "DIAG Safety cleanup complete: RGB LED and buzzer are off."
COMPLETION = "DIAG Guided anomaly hardware integration sequence completed."
PHASES = ("ambient", "covered", "ambient recovery", "phone flashlight", "final ambient recovery")
PHASE_RE = re.compile(r"^DIAG Phase \d+ of \d+ : (.+)$")
SAMPLE_RE = re.compile(
    r"^DIAG Sample (\d+) of (\d+) value= (\d+) state= (\S+) "
    r"decision= (\S+) alarm= (\S+)$"
)


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def validate_event(event):
    errors = []
    if not isinstance(event, dict):
        return ["event must be a JSON object"]
    for key, expected in (("schema_version", "1.0"), ("event_type", "anomaly"), ("sensor", "photoresistor")):
        if event.get(key) != expected:
            errors.append("%s must equal %r" % (key, expected))
    if not is_int(event.get("event_id")) or event["event_id"] < 0:
        errors.append("event_id must be a non-negative integer")
    if event.get("anomaly_type") not in ("low_light", "high_light"):
        errors.append("invalid anomaly_type")
    if event.get("detector_method") not in ("threshold", "delta"):
        errors.append("invalid detector_method")
    value = event.get("value")
    if not is_int(value) or not 0 <= value <= 65535:
        errors.append("value must be an ADC integer")
    for key in ("previous_value", "delta"):
        if event.get(key) is not None and not is_int(event.get(key)):
            errors.append("%s must be an integer or null" % key)
    history = event.get("history")
    if not isinstance(history, list) or any(not is_int(v) or not 0 <= v <= 65535 for v in history):
        errors.append("history must contain ADC integers")
    if not is_int(event.get("timestamp_ms")) or event["timestamp_ms"] < 0:
        errors.append("timestamp_ms must be a non-negative integer")
    if not isinstance(event.get("local_alarm"), bool):
        errors.append("local_alarm must be a boolean")
    for key in ("low_threshold", "high_threshold", "delta_threshold"):
        if not is_int(event.get(key)):
            errors.append("%s must be an integer" % key)
    return errors


def parse_evidence(path):
    path = Path(path)
    result = {"path": str(path), "errors": [], "events": [], "samples": [], "phases": [], "boundary_style": None}
    if not path.exists():
        result["errors"].append("file does not exist")
        return result
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        result["errors"].append("file is empty")
        return result
    if TEST_START in lines and TEST_END in lines:
        result["boundary_style"] = "TEST_START/TEST_END"
    elif DIAG_START in lines and DIAG_END in lines:
        result["boundary_style"] = "DIAG start/cleanup"
    else:
        if TEST_START not in lines and DIAG_START not in lines:
            result["errors"].append("missing start boundary")
        if TEST_END not in lines and DIAG_END not in lines:
            result["errors"].append("missing end boundary")
    if COMPLETION not in lines:
        result["errors"].append("missing completion line")
    if any("Traceback (most recent call last)" in line for line in lines):
        result["errors"].append("unhandled traceback present")

    phase = None
    last_sample = None
    for number, line in enumerate(lines, 1):
        match = PHASE_RE.match(line)
        if match:
            phase = match.group(1)
            result["phases"].append(phase)
            last_sample = None
            continue
        match = SAMPLE_RE.match(line)
        if match:
            last_sample = {
                "line_number": number, "phase": phase,
                "reading_index": int(match.group(1)), "sample_total": int(match.group(2)),
                "value": int(match.group(3)), "detected_state": match.group(4),
                "policy_reason": match.group(5), "alarm": match.group(6), "event": None,
            }
            result["samples"].append(last_sample)
            continue
        if line.lstrip().startswith("{"):
            try:
                event = json.loads(line)
            except json.JSONDecodeError as error:
                result["errors"].append("line %d: malformed JSON: %s" % (number, error.msg))
                last_sample = None
                continue
            result["errors"].extend("line %d: %s" % (number, error) for error in validate_event(event))
            result["events"].append(event)
            if last_sample is None or number != last_sample["line_number"] + 1:
                result["errors"].append("line %d: JSON does not immediately follow a sample" % number)
            else:
                last_sample["event"] = event
            last_sample = None
        elif line.strip():
            last_sample = None

    for expected in PHASES:
        if expected not in result["phases"]:
            result["errors"].append("missing phase: %s" % expected)
        count = sum(sample["phase"] == expected for sample in result["samples"])
        if count != 12:
            result["errors"].append("phase %s: expected 12 samples, found %d" % (expected, count))
    if len(result["samples"]) != 60:
        result["errors"].append("expected 60 samples, found %d" % len(result["samples"]))
    ids = [event.get("event_id") for event in result["events"]]
    if len(result["events"]) != 4:
        result["errors"].append("expected 4 JSON events, found %d" % len(result["events"]))
    if ids and ids[0] != 1:
        result["errors"].append("event identifiers must start at 1")
    if any(current <= previous for previous, current in zip(ids, ids[1:])):
        result["errors"].append("event identifiers are not strictly increasing")
    if ids and ids != list(range(1, len(ids) + 1)):
        result["errors"].append("event identifiers are not continuous")
    for sample in result["samples"]:
        event = sample["event"]
        if sample["phase"] in ("ambient", "ambient recovery", "final ambient recovery") and event:
            result["errors"].append("line %d: recovery or ambient emitted JSON" % sample["line_number"])
        if sample["policy_reason"] == "suppressed_same_anomaly" and event:
            result["errors"].append("line %d: suppressed reading emitted JSON" % sample["line_number"])
        if sample["policy_reason"] in ("entered_anomaly", "cooldown_repeat") and event is None:
            result["errors"].append("line %d: emitted decision has no JSON" % sample["line_number"])
    types = [event.get("anomaly_type") for event in result["events"]]
    if "low_light" not in types:
        result["errors"].append("no low_light event found")
    if "high_light" not in types:
        result["errors"].append("no high_light event found")
    if types and types != ["low_light", "low_light", "high_light", "high_light"]:
        result["errors"].append("unexpected anomaly event sequence")
    return result


def print_report(result):
    ids = [event.get("event_id") for event in result["events"]]
    types = [event.get("anomaly_type") for event in result["events"]]
    print(result["path"])
    print("  Boundary:", result["boundary_style"] or "invalid")
    print("  Samples:", len(result["samples"]))
    print("  JSON events:", len(result["events"]))
    print("  Event IDs:", ids)
    print("  Anomaly types:", types)
    print("  IDs strictly increasing:", all(b > a for a, b in zip(ids, ids[1:])))
    for error in result["errors"]:
        print("  ERROR:", error)
    if not result["errors"]:
        print("  Validation: PASS")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+")
    results = [parse_evidence(path) for path in parser.parse_args(argv).paths]
    for result in results:
        print_report(result)
    return 0 if all(not result["errors"] for result in results) else 1


if __name__ == "__main__":
    sys.exit(main())
