"""Generate labeled Week 3 rows from validated raw console evidence."""

import csv
import sys

from validate_week3_evidence import parse_evidence


HEADER = (
    "run_id", "phase", "reading_index", "timestamp_ms", "value",
    "expected_state", "detected_state", "policy_reason", "json_event_emitted",
    "event_id", "rgb_observation", "buzzer_observation", "correct", "notes",
)


def expected_state(phase):
    if phase == "covered":
        return "low_light"
    if phase == "phone flashlight":
        return "high_light"
    return "normal"


def is_correct(sample, expected):
    if sample["detected_state"] == expected:
        return True
    return (
        sample["phase"] in ("ambient recovery", "final ambient recovery")
        and sample["reading_index"] == 1
        and sample["detected_state"] in ("sudden_rise", "sudden_drop")
        and sample["policy_reason"] == "recovered"
    )


def manual_observations(sample):
    rgb_by_phase = {
        "ambient": "green",
        "covered": "red",
        "ambient recovery": "green",
        "phone flashlight": "blue",
        "final ambient recovery": "green",
    }
    buzzer = "short tone" if sample["event"] else "off"
    return rgb_by_phase[sample["phase"]], buzzer


def build_rows(run_id, result):
    rows = []
    for sample in result["samples"]:
        event = sample["event"]
        expected = expected_state(sample["phase"])
        rgb, buzzer = manual_observations(sample)
        rows.append({
            "run_id": run_id,
            "phase": sample["phase"],
            "reading_index": sample["reading_index"],
            "timestamp_ms": event["timestamp_ms"] if event else "",
            "value": sample["value"],
            "expected_state": expected,
            "detected_state": sample["detected_state"],
            "policy_reason": sample["policy_reason"],
            "json_event_emitted": "true" if event else "false",
            "event_id": event["event_id"] if event else "",
            "rgb_observation": rgb,
            "buzzer_observation": buzzer,
            "correct": "true" if is_correct(sample, expected) else "false",
            "notes": "Phase-level physical observation supplied manually by the operator; event association follows an immediately subsequent JSON line.",
        })
    return rows


def main(argv=None):
    paths = (argv or sys.argv[1:])
    if len(paths) != 3:
        print("usage: generate_week3_labeled_results.py OUTPUT RUN_01 RUN_02")
        return 2
    output, *raw_paths = paths
    results = [parse_evidence(path) for path in raw_paths]
    for result in results:
        if result["errors"]:
            for error in result["errors"]:
                print("%s: %s" % (result["path"], error))
            return 1
    rows = []
    for index, result in enumerate(results, 1):
        rows.extend(build_rows("run_%02d" % index, result))
    with open(output, "w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(rows)
    print("Wrote %d labeled rows to %s" % (len(rows), output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
