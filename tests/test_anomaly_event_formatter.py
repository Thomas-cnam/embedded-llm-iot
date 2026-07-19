"""Host-side tests for pure anomaly-event formatting."""

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


def make_detector_result(
    is_anomaly=True,
    anomaly_type="low_light",
    detector_method="threshold",
    value=48,
    previous_value=24320,
    delta=-24272,
    history=None,
    state_before="normal",
    state_after=None,
    secondary_method="sudden_drop",
):
    if history is None:
        history = [24310, 24290, 24340, 24320, value]
    if state_after is None:
        state_after = anomaly_type
    return {
        "is_anomaly": is_anomaly,
        "anomaly_type": anomaly_type,
        "detector_method": detector_method,
        "secondary_method": secondary_method,
        "value": value,
        "previous_value": previous_value,
        "delta": delta,
        "history": history,
        "state_before": state_before,
        "state_after": state_after,
        "low_threshold": 5000,
        "high_threshold": 32000,
        "delta_threshold": 8000,
    }


def make_integration_result(
    detector_result=None,
    should_emit_alert=True,
    timestamp_ms=18250,
    cooldown_active=False,
    alarm_triggered=True,
):
    if detector_result is None:
        detector_result = make_detector_result()
    return {
        "detector_result": detector_result,
        "policy_decision": {
            "should_emit_alert": should_emit_alert,
            "decision_reason": "entered_anomaly",
            "active_anomaly_type": detector_result["anomaly_type"],
            "previous_anomaly_type": None,
            "recovered": False,
            "cooldown_active": cooldown_active,
            "cooldown_remaining_ms": 0,
            "timestamp_ms": timestamp_ms,
        },
        "alarm_action": "trigger_" + detector_result["anomaly_type"],
        "alarm_triggered": alarm_triggered,
        "alarm_error": None,
        "recovery_handled": False,
    }


def make_normal_integration_result():
    detector_result = make_detector_result(
        is_anomaly=False,
        anomaly_type="normal",
        detector_method="none",
        value=24320,
        previous_value=None,
        delta=None,
        history=[24320],
        state_before=None,
        state_after="normal",
        secondary_method=None,
    )
    return make_integration_result(
        detector_result=detector_result,
        should_emit_alert=False,
        timestamp_ms=0,
        alarm_triggered=False,
    )


class AnomalyEventFormatterConstructorTests(unittest.TestCase):
    def test_default_configuration(self):
        formatter = AnomalyEventFormatter()

        self.assertEqual(formatter.schema_version, "1.0")
        self.assertEqual(formatter.starting_event_id, 1)
        self.assertEqual(formatter.next_event_id, 1)

    def test_custom_configuration(self):
        formatter = AnomalyEventFormatter("2.0-test", 0)

        self.assertEqual(formatter.schema_version, "2.0-test")
        self.assertEqual(formatter.next_event_id, 0)

    def test_schema_version_must_be_string(self):
        for value in (None, 1, True, []):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    AnomalyEventFormatter(schema_version=value)

    def test_schema_version_must_not_be_empty(self):
        for value in ("", "   "):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    AnomalyEventFormatter(schema_version=value)

    def test_starting_event_id_rejects_boolean(self):
        with self.assertRaises(TypeError):
            AnomalyEventFormatter(starting_event_id=True)

    def test_starting_event_id_must_be_integer(self):
        for value in (None, 1.0, "1", []):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    AnomalyEventFormatter(starting_event_id=value)

    def test_starting_event_id_must_not_be_negative(self):
        with self.assertRaises(ValueError):
            AnomalyEventFormatter(starting_event_id=-1)


class AnomalyEventFormatterBuildTests(unittest.TestCase):
    def test_builds_complete_schema_event(self):
        formatter = AnomalyEventFormatter()
        event = formatter.build_event(make_integration_result())

        self.assertEqual(
            set(event),
            {
                "schema_version",
                "event_id",
                "event_type",
                "sensor",
                "anomaly_type",
                "detector_method",
                "value",
                "previous_value",
                "delta",
                "history",
                "timestamp_ms",
                "local_alarm",
                "low_threshold",
                "high_threshold",
                "delta_threshold",
                "secondary_method",
                "state_before",
                "state_after",
                "cooldown_active",
            },
        )
        self.assertEqual(event["schema_version"], "1.0")
        self.assertEqual(event["event_id"], 1)
        self.assertEqual(event["event_type"], "anomaly")
        self.assertEqual(event["sensor"], "photoresistor")
        self.assertEqual(event["anomaly_type"], "low_light")
        self.assertEqual(event["detector_method"], "threshold")
        self.assertEqual(event["value"], 48)
        self.assertEqual(event["previous_value"], 24320)
        self.assertEqual(event["delta"], -24272)
        self.assertEqual(event["timestamp_ms"], 18250)
        self.assertTrue(event["local_alarm"])

    def test_event_history_is_copied(self):
        result = make_integration_result()
        event = AnomalyEventFormatter().build_event(result)

        result["detector_result"]["history"].append(99)

        self.assertEqual(event["history"], [24310, 24290, 24340, 24320, 48])

    def test_event_identifiers_increment_only_for_emitted_events(self):
        formatter = AnomalyEventFormatter(starting_event_id=7)

        first = formatter.build_event(make_integration_result())
        suppressed = formatter.build_event(
            make_integration_result(should_emit_alert=False)
        )
        second = formatter.build_event(make_integration_result())

        self.assertEqual(first["event_id"], 7)
        self.assertIsNone(suppressed)
        self.assertEqual(second["event_id"], 8)
        self.assertEqual(formatter.next_event_id, 9)

    def test_normal_result_returns_none(self):
        formatter = AnomalyEventFormatter()

        self.assertIsNone(formatter.build_event(make_normal_integration_result()))
        self.assertEqual(formatter.next_event_id, 1)

    def test_suppressed_anomaly_returns_none(self):
        formatter = AnomalyEventFormatter()

        result = make_integration_result(should_emit_alert=False)

        self.assertIsNone(formatter.build_event(result))
        self.assertEqual(formatter.next_event_id, 1)

    def test_local_alarm_false_is_preserved(self):
        event = AnomalyEventFormatter().build_event(
            make_integration_result(alarm_triggered=False)
        )

        self.assertFalse(event["local_alarm"])

    def test_supported_anomaly_types_are_preserved(self):
        cases = (
            ("low_light", "threshold", 48),
            ("high_light", "threshold", 39546),
            ("sudden_drop", "delta", 15000),
            ("sudden_rise", "delta", 25000),
        )
        for anomaly_type, method, value in cases:
            with self.subTest(anomaly_type=anomaly_type):
                previous = 24000
                result = make_detector_result(
                    anomaly_type=anomaly_type,
                    detector_method=method,
                    value=value,
                    previous_value=previous,
                    delta=value - previous,
                    history=[previous, value],
                    secondary_method=None,
                )
                event = AnomalyEventFormatter().build_event(
                    make_integration_result(detector_result=result)
                )
                self.assertEqual(event["anomaly_type"], anomaly_type)
                self.assertEqual(event["detector_method"], method)

    def test_reset_restores_configured_starting_identifier(self):
        formatter = AnomalyEventFormatter(starting_event_id=10)
        formatter.build_event(make_integration_result())

        formatter.reset()

        self.assertEqual(formatter.next_event_id, 10)
        self.assertEqual(
            formatter.build_event(make_integration_result())["event_id"], 10
        )

    def test_real_integration_results_emit_only_on_policy_request(self):
        integration = AnomalyIntegrationController(
            PhotoresistorAnomalyDetector(),
            AnomalyAlertPolicy(),
        )
        formatter = AnomalyEventFormatter()

        normal = formatter.build_event(integration.process(24368, 0))
        first_low = formatter.build_event(integration.process(48, 500))
        repeated_low = formatter.build_event(integration.process(40, 1000))
        cooldown_low = formatter.build_event(integration.process(45, 5500))

        self.assertIsNone(normal)
        self.assertEqual(first_low["event_id"], 1)
        self.assertEqual(first_low["anomaly_type"], "low_light")
        self.assertIsNone(repeated_low)
        self.assertEqual(cooldown_low["event_id"], 2)


class AnomalyEventFormatterSerializationTests(unittest.TestCase):
    def test_serialization_returns_compact_json_object(self):
        payload = AnomalyEventFormatter().serialize_event(
            make_integration_result()
        )

        self.assertTrue(payload.startswith("{"))
        self.assertTrue(payload.endswith("}"))
        self.assertNotIn("\n", payload)
        self.assertNotIn(": ", payload)
        self.assertNotIn(", ", payload)
        self.assertEqual(json.loads(payload)["anomaly_type"], "low_light")

    def test_serialization_returns_none_when_not_emitted(self):
        formatter = AnomalyEventFormatter()

        payload = formatter.serialize_event(
            make_integration_result(should_emit_alert=False)
        )

        self.assertIsNone(payload)
        self.assertEqual(formatter.next_event_id, 1)

    def test_serialized_identifiers_increment(self):
        formatter = AnomalyEventFormatter(starting_event_id=3)

        first = json.loads(formatter.serialize_event(make_integration_result()))
        second = json.loads(formatter.serialize_event(make_integration_result()))

        self.assertEqual(first["event_id"], 3)
        self.assertEqual(second["event_id"], 4)

    def test_compaction_preserves_spaces_inside_strings(self):
        formatter = AnomalyEventFormatter(schema_version="version 1.0 test")

        payload = formatter.serialize_event(make_integration_result())

        self.assertIn('"schema_version":"version 1.0 test"', payload)
        self.assertEqual(json.loads(payload)["schema_version"], "version 1.0 test")

    def test_compaction_preserves_escaped_string_characters(self):
        formatter = AnomalyEventFormatter(schema_version='v "1" \\ test')

        payload = formatter.serialize_event(make_integration_result())

        self.assertEqual(json.loads(payload)["schema_version"], 'v "1" \\ test')


class AnomalyEventFormatterValidationTests(unittest.TestCase):
    def test_integration_result_must_be_dictionary(self):
        for value in (None, [], "result"):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    AnomalyEventFormatter().build_event(value)

    def test_required_top_level_fields_are_enforced(self):
        for field_name in ("detector_result", "policy_decision", "alarm_triggered"):
            with self.subTest(field_name=field_name):
                result = make_integration_result()
                del result[field_name]
                with self.assertRaises(ValueError):
                    AnomalyEventFormatter().build_event(result)

    def test_nested_results_must_be_dictionaries(self):
        for field_name in ("detector_result", "policy_decision"):
            with self.subTest(field_name=field_name):
                result = make_integration_result()
                result[field_name] = []
                with self.assertRaises(TypeError):
                    AnomalyEventFormatter().build_event(result)

    def test_required_detector_fields_are_enforced(self):
        for field_name in (
            "is_anomaly",
            "anomaly_type",
            "detector_method",
            "secondary_method",
            "value",
            "previous_value",
            "delta",
            "history",
            "state_before",
            "state_after",
            "low_threshold",
            "high_threshold",
            "delta_threshold",
        ):
            with self.subTest(field_name=field_name):
                result = make_integration_result()
                del result["detector_result"][field_name]
                with self.assertRaises(ValueError):
                    AnomalyEventFormatter().build_event(result)

    def test_policy_required_fields_are_enforced(self):
        for field_name in (
            "should_emit_alert",
            "timestamp_ms",
            "cooldown_active",
        ):
            with self.subTest(field_name=field_name):
                result = make_integration_result()
                del result["policy_decision"][field_name]
                with self.assertRaises(ValueError):
                    AnomalyEventFormatter().build_event(result)

    def test_boolean_fields_are_strict(self):
        cases = (
            ("detector_result", "is_anomaly"),
            ("policy_decision", "should_emit_alert"),
            ("policy_decision", "cooldown_active"),
            (None, "alarm_triggered"),
        )
        for section, field_name in cases:
            with self.subTest(section=section, field_name=field_name):
                result = make_integration_result()
                target = result if section is None else result[section]
                target[field_name] = 1
                with self.assertRaises(TypeError):
                    AnomalyEventFormatter().build_event(result)

    def test_integer_fields_reject_boolean_and_non_integer(self):
        cases = (
            ("detector_result", "value"),
            ("detector_result", "previous_value"),
            ("detector_result", "delta"),
            ("detector_result", "low_threshold"),
            ("detector_result", "high_threshold"),
            ("detector_result", "delta_threshold"),
            ("policy_decision", "timestamp_ms"),
        )
        for section, field_name in cases:
            for invalid_value in (True, 1.5, "1"):
                with self.subTest(
                    section=section,
                    field_name=field_name,
                    invalid_value=invalid_value,
                ):
                    result = make_integration_result()
                    result[section][field_name] = invalid_value
                    with self.assertRaises(TypeError):
                        AnomalyEventFormatter().build_event(result)

    def test_unsupported_anomaly_type_is_rejected(self):
        result = make_integration_result()
        result["detector_result"]["anomaly_type"] = "unknown"
        result["detector_result"]["state_after"] = "unknown"

        with self.assertRaises(ValueError):
            AnomalyEventFormatter().build_event(result)

    def test_unsupported_detector_method_is_rejected(self):
        result = make_integration_result()
        result["detector_result"]["detector_method"] = "magic"

        with self.assertRaises(ValueError):
            AnomalyEventFormatter().build_event(result)

    def test_inconsistent_normal_result_is_rejected(self):
        result = make_normal_integration_result()
        result["detector_result"]["anomaly_type"] = "low_light"
        result["detector_result"]["state_after"] = "low_light"

        with self.assertRaises(ValueError):
            AnomalyEventFormatter().build_event(result)

    def test_emission_requires_anomalous_detector_result(self):
        result = make_normal_integration_result()
        result["policy_decision"]["should_emit_alert"] = True

        with self.assertRaises(ValueError):
            AnomalyEventFormatter().build_event(result)

    def test_previous_value_and_delta_must_be_consistent(self):
        invalid_pairs = ((None, -1), (100, None), (100, 1))
        for previous_value, delta in invalid_pairs:
            with self.subTest(previous_value=previous_value, delta=delta):
                result = make_integration_result()
                result["detector_result"]["previous_value"] = previous_value
                result["detector_result"]["delta"] = delta
                with self.assertRaises(ValueError):
                    AnomalyEventFormatter().build_event(result)

    def test_history_must_be_non_empty_list_of_adc_integers(self):
        for history in ((), [], [48.0], [True], [-1], [65536]):
            with self.subTest(history=history):
                result = make_integration_result()
                result["detector_result"]["history"] = history
                with self.assertRaises((TypeError, ValueError)):
                    AnomalyEventFormatter().build_event(result)

    def test_history_must_end_with_current_value(self):
        result = make_integration_result()
        result["detector_result"]["history"][-1] = 49

        with self.assertRaises(ValueError):
            AnomalyEventFormatter().build_event(result)

    def test_state_after_must_match_anomaly_type(self):
        result = make_integration_result()
        result["detector_result"]["state_after"] = "high_light"

        with self.assertRaises(ValueError):
            AnomalyEventFormatter().build_event(result)

    def test_threshold_configuration_is_validated(self):
        cases = (
            ("low_threshold", -1),
            ("low_threshold", 32000),
            ("delta_threshold", 0),
        )
        for field_name, value in cases:
            with self.subTest(field_name=field_name, value=value):
                result = make_integration_result()
                result["detector_result"][field_name] = value
                with self.assertRaises(ValueError):
                    AnomalyEventFormatter().build_event(result)

    def test_negative_timestamp_is_rejected(self):
        result = make_integration_result(timestamp_ms=-1)

        with self.assertRaises(ValueError):
            AnomalyEventFormatter().build_event(result)


if __name__ == "__main__":
    unittest.main()
