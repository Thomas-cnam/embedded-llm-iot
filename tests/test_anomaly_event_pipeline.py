"""Host-side tests for detector-to-JSON anomaly event flow."""

import json
import os
import sys
import unittest


REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from firmware.anomaly.alert_policy import AnomalyAlertPolicy  # noqa: E402
from firmware.anomaly.detector import PhotoresistorAnomalyDetector  # noqa: E402
from firmware.anomaly.event_formatter import AnomalyEventFormatter  # noqa: E402
from firmware.anomaly.integration import (  # noqa: E402
    AnomalyIntegrationController,
)


class FakeAlarmController:
    def __init__(self):
        self.actions = []

    def show_normal(self):
        self.actions.append("normal")

    def trigger(self, anomaly_type):
        self.actions.append("trigger_" + anomaly_type)

    def safe_off(self):
        self.actions.append("off")
        return {
            "successful": True,
            "rgb_error": None,
            "buzzer_error": None,
        }


def create_pipeline(with_alarm=False):
    alarm = FakeAlarmController() if with_alarm else None
    integration = AnomalyIntegrationController(
        PhotoresistorAnomalyDetector(),
        AnomalyAlertPolicy(),
        alarm,
    )
    return integration, AnomalyEventFormatter(), alarm


def process_json(integration, formatter, value, timestamp_ms):
    result = integration.process(value, timestamp_ms)
    return result, formatter.serialize_event(result)


class AnomalyEventPipelineTests(unittest.TestCase):
    def test_normal_reading_produces_no_json(self):
        integration, formatter, _ = create_pipeline()

        result, payload = process_json(integration, formatter, 24368, 0)

        self.assertEqual(result["detector_result"]["anomaly_type"], "normal")
        self.assertFalse(result["policy_decision"]["should_emit_alert"])
        self.assertIsNone(payload)

    def test_first_low_light_alert_produces_one_json_object(self):
        integration, formatter, _ = create_pipeline()
        process_json(integration, formatter, 24368, 0)

        result, payload = process_json(integration, formatter, 48, 500)
        event = json.loads(payload)

        self.assertTrue(result["policy_decision"]["should_emit_alert"])
        self.assertEqual(event["event_id"], 1)
        self.assertEqual(event["anomaly_type"], "low_light")
        self.assertEqual(event["value"], 48)

    def test_suppressed_low_light_produces_no_json(self):
        integration, formatter, _ = create_pipeline()
        process_json(integration, formatter, 24368, 0)
        process_json(integration, formatter, 48, 500)

        result, payload = process_json(integration, formatter, 40, 1000)

        self.assertEqual(
            result["policy_decision"]["decision_reason"],
            "suppressed_same_anomaly",
        )
        self.assertIsNone(payload)

    def test_cooldown_repeat_produces_next_json_event(self):
        integration, formatter, _ = create_pipeline()
        process_json(integration, formatter, 24368, 0)
        _, first_payload = process_json(integration, formatter, 48, 500)
        process_json(integration, formatter, 40, 1000)

        result, repeated_payload = process_json(integration, formatter, 45, 5500)

        self.assertEqual(
            result["policy_decision"]["decision_reason"], "cooldown_repeat"
        )
        self.assertEqual(json.loads(first_payload)["event_id"], 1)
        self.assertEqual(json.loads(repeated_payload)["event_id"], 2)

    def test_threshold_recovery_produces_no_json(self):
        integration, formatter, _ = create_pipeline()
        process_json(integration, formatter, 24368, 0)
        process_json(integration, formatter, 48, 500)

        result, payload = process_json(integration, formatter, 24300, 1000)

        self.assertTrue(result["policy_decision"]["recovered"])
        self.assertEqual(
            result["policy_decision"]["decision_reason"], "recovered"
        )
        self.assertIsNone(payload)

    def test_high_light_after_recovery_produces_json(self):
        integration, formatter, _ = create_pipeline()
        process_json(integration, formatter, 24368, 0)
        process_json(integration, formatter, 48, 500)
        process_json(integration, formatter, 24300, 1000)

        _, payload = process_json(integration, formatter, 39546, 1500)
        event = json.loads(payload)

        self.assertEqual(event["event_id"], 2)
        self.assertEqual(event["anomaly_type"], "high_light")

    def test_anomaly_change_emits_immediately(self):
        integration, formatter, _ = create_pipeline()
        process_json(integration, formatter, 48, 0)

        result, payload = process_json(integration, formatter, 39546, 500)

        self.assertEqual(
            result["policy_decision"]["decision_reason"], "anomaly_changed"
        )
        self.assertEqual(json.loads(payload)["event_id"], 2)

    def test_pipeline_without_alarm_reports_local_alarm_false(self):
        integration, formatter, _ = create_pipeline()

        _, payload = process_json(integration, formatter, 48, 0)

        self.assertFalse(json.loads(payload)["local_alarm"])

    def test_pipeline_with_alarm_reports_local_alarm_true(self):
        integration, formatter, alarm = create_pipeline(with_alarm=True)

        _, payload = process_json(integration, formatter, 48, 0)

        self.assertEqual(alarm.actions, ["trigger_low_light"])
        self.assertTrue(json.loads(payload)["local_alarm"])

    def test_json_payload_is_compact_and_has_no_line_break(self):
        integration, formatter, _ = create_pipeline()

        _, payload = process_json(integration, formatter, 48, 0)

        self.assertTrue(payload.startswith("{"))
        self.assertTrue(payload.endswith("}"))
        self.assertNotIn("\n", payload)
        self.assertNotIn(": ", payload)
        self.assertNotIn(", ", payload)

    def test_representative_sequence_emits_only_requested_events(self):
        integration, formatter, _ = create_pipeline()
        samples = (
            (24368, 0),
            (48, 500),
            (40, 1000),
            (45, 5500),
            (24300, 6000),
            (39546, 6500),
            (39000, 7000),
            (24350, 7500),
        )

        payloads = []
        for value, timestamp_ms in samples:
            _, payload = process_json(
                integration, formatter, value, timestamp_ms
            )
            if payload is not None:
                payloads.append(json.loads(payload))

        self.assertEqual([event["event_id"] for event in payloads], [1, 2, 3])
        self.assertEqual(
            [event["anomaly_type"] for event in payloads],
            ["low_light", "low_light", "high_light"],
        )


if __name__ == "__main__":
    unittest.main()
