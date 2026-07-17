"""Host-side tests for alert policy and local anomaly integration."""

import os
import sys
import unittest


REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from firmware.anomaly.alert_policy import AnomalyAlertPolicy  # noqa: E402
from firmware.anomaly.detector import PhotoresistorAnomalyDetector  # noqa: E402
from firmware.anomaly.integration import AnomalyIntegrationController  # noqa: E402
from firmware.anomaly.local_alarm import LocalAlarmController  # noqa: E402


def detector_result(is_anomaly, anomaly_type, **extra_fields):
    result = {
        "is_anomaly": is_anomaly,
        "anomaly_type": anomaly_type,
    }
    result.update(extra_fields)
    return result


class FakeRgbLed:
    def __init__(self, fail_on=None):
        self.calls = []
        self.fail_on = fail_on

    def _record(self, method_name):
        self.calls.append(method_name)
        if self.fail_on == method_name:
            raise RuntimeError("RGB " + method_name + " failed")

    def green(self):
        self._record("green")

    def red(self):
        self._record("red")

    def blue(self):
        self._record("blue")

    def white(self):
        self._record("white")

    def off(self):
        self._record("off")


class FakeBuzzer:
    def __init__(self, fail_on=None):
        self.calls = []
        self.fail_on = fail_on

    def tone(self, frequency, duration_ms, duty=None):
        self.calls.append(("tone", frequency, duration_ms, duty))
        if self.fail_on == "tone":
            raise RuntimeError("buzzer tone failed")

    def off(self):
        self.calls.append(("off",))
        if self.fail_on == "off":
            raise RuntimeError("buzzer off failed")


class AlertPolicyTests(unittest.TestCase):
    def test_valid_default_policy(self):
        policy = AnomalyAlertPolicy()

        self.assertEqual(policy.cooldown_ms, 5000)
        self.assertTrue(policy.repeat_after_cooldown)
        self.assertIsNone(policy.active_anomaly_type)
        self.assertIsNone(policy.last_alert_timestamp_ms)

    def test_negative_cooldown_is_rejected(self):
        with self.assertRaises(ValueError):
            AnomalyAlertPolicy(cooldown_ms=-1)

    def test_boolean_cooldown_is_rejected(self):
        with self.assertRaises(TypeError):
            AnomalyAlertPolicy(cooldown_ms=True)

    def test_non_integer_cooldown_is_rejected(self):
        for value in (1.5, "5000", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    AnomalyAlertPolicy(cooldown_ms=value)

    def test_invalid_repeat_after_cooldown_is_rejected(self):
        for value in (1, 0, "yes", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    AnomalyAlertPolicy(repeat_after_cooldown=value)

    def test_invalid_detector_result_type_is_rejected(self):
        policy = AnomalyAlertPolicy()

        for value in (None, [], "normal"):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    policy.evaluate(value, 0)

    def test_detector_result_missing_required_fields_is_rejected(self):
        policy = AnomalyAlertPolicy()

        for value in ({}, {"is_anomaly": False}, {"anomaly_type": "normal"}):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    policy.evaluate(value, 0)

    def test_invalid_is_anomaly_type_is_rejected(self):
        policy = AnomalyAlertPolicy()

        with self.assertRaises(TypeError):
            policy.evaluate(detector_result(1, "low_light"), 0)

    def test_invalid_anomaly_type_type_is_rejected(self):
        policy = AnomalyAlertPolicy()

        with self.assertRaises(TypeError):
            policy.evaluate(detector_result(True, None), 0)

    def test_inconsistent_detector_result_is_rejected(self):
        policy = AnomalyAlertPolicy()

        cases = (
            detector_result(True, "normal"),
            detector_result(False, "low_light"),
        )
        for value in cases:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    policy.evaluate(value, 0)

    def test_negative_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            AnomalyAlertPolicy().evaluate(detector_result(False, "normal"), -1)

    def test_boolean_timestamp_is_rejected(self):
        with self.assertRaises(TypeError):
            AnomalyAlertPolicy().evaluate(detector_result(False, "normal"), True)

    def test_non_integer_timestamp_is_rejected(self):
        for value in (1.5, "0", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    AnomalyAlertPolicy().evaluate(
                        detector_result(False, "normal"), value
                    )

    def test_timestamp_moving_backwards_is_rejected(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(False, "normal"), 100)

        with self.assertRaises(ValueError):
            policy.evaluate(detector_result(False, "normal"), 99)

    def test_first_normal_result_does_not_emit(self):
        decision = AnomalyAlertPolicy().evaluate(
            detector_result(False, "normal"), 0
        )

        self.assertFalse(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "normal")
        self.assertIsNone(decision["active_anomaly_type"])
        self.assertFalse(decision["recovered"])

    def test_first_anomaly_emits_immediately(self):
        decision = AnomalyAlertPolicy().evaluate(
            detector_result(True, "low_light"), 100
        )

        self.assertTrue(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "entered_anomaly")
        self.assertEqual(decision["active_anomaly_type"], "low_light")
        self.assertIsNone(decision["previous_anomaly_type"])

    def test_same_anomaly_is_suppressed_before_cooldown(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "low_light"), 1000)

        decision = policy.evaluate(detector_result(True, "low_light"), 1500)

        self.assertFalse(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "suppressed_same_anomaly")
        self.assertTrue(decision["cooldown_active"])
        self.assertEqual(decision["cooldown_remaining_ms"], 4500)

    def test_same_anomaly_repeats_at_cooldown_boundary(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "low_light"), 1000)

        decision = policy.evaluate(detector_result(True, "low_light"), 6000)

        self.assertTrue(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "cooldown_repeat")
        self.assertEqual(decision["cooldown_remaining_ms"], 0)

    def test_same_anomaly_repeats_after_cooldown(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "high_light"), 0)

        decision = policy.evaluate(detector_result(True, "high_light"), 6000)

        self.assertTrue(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "cooldown_repeat")
        self.assertEqual(policy.last_alert_timestamp_ms, 6000)

    def test_repeat_can_remain_disabled_after_cooldown(self):
        policy = AnomalyAlertPolicy(repeat_after_cooldown=False)
        policy.evaluate(detector_result(True, "low_light"), 0)

        decision = policy.evaluate(detector_result(True, "low_light"), 10000)

        self.assertFalse(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "suppressed_same_anomaly")
        self.assertFalse(decision["cooldown_active"])
        self.assertEqual(decision["cooldown_remaining_ms"], 0)

    def test_anomaly_type_change_emits_and_ignores_cooldown(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "low_light"), 1000)

        decision = policy.evaluate(detector_result(True, "high_light"), 1001)

        self.assertTrue(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "anomaly_changed")
        self.assertEqual(decision["previous_anomaly_type"], "low_light")
        self.assertEqual(decision["active_anomaly_type"], "high_light")

    def test_recovery_is_detected(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "low_light"), 0)

        decision = policy.evaluate(detector_result(False, "normal"), 500)

        self.assertFalse(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "recovered")
        self.assertTrue(decision["recovered"])
        self.assertIsNone(decision["active_anomaly_type"])
        self.assertIsNone(policy.last_alert_timestamp_ms)

    def test_threshold_exit_delta_is_treated_as_recovery(self):
        detector = PhotoresistorAnomalyDetector()
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector.evaluate(50), 0)

        raw_result = detector.evaluate(24300)
        decision = policy.evaluate(raw_result, 500)

        self.assertEqual(raw_result["anomaly_type"], "sudden_rise")
        self.assertEqual(decision["decision_reason"], "recovered")
        self.assertTrue(decision["recovered"])

    def test_continued_normal_after_recovery_is_normal(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "low_light"), 0)
        policy.evaluate(detector_result(False, "normal"), 100)

        decision = policy.evaluate(detector_result(False, "normal"), 200)

        self.assertEqual(decision["decision_reason"], "normal")
        self.assertFalse(decision["recovered"])

    def test_same_anomaly_after_recovery_emits_immediately(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "low_light"), 0)
        policy.evaluate(detector_result(False, "normal"), 100)

        decision = policy.evaluate(detector_result(True, "low_light"), 200)

        self.assertTrue(decision["should_emit_alert"])
        self.assertEqual(decision["decision_reason"], "entered_anomaly")

    def test_policy_reset_clears_state(self):
        policy = AnomalyAlertPolicy()
        policy.evaluate(detector_result(True, "low_light"), 500)

        policy.reset()

        self.assertIsNone(policy.active_anomaly_type)
        self.assertIsNone(policy.last_alert_timestamp_ms)
        self.assertIsNone(policy.previous_detector_state)
        decision = policy.evaluate(detector_result(True, "low_light"), 0)
        self.assertEqual(decision["decision_reason"], "entered_anomaly")


class LocalAlarmControllerTests(unittest.TestCase):
    def setUp(self):
        self.rgb_led = FakeRgbLed()
        self.buzzer = FakeBuzzer()
        self.controller = LocalAlarmController(self.rgb_led, self.buzzer)

    def test_show_normal_selects_green_and_silences_buzzer(self):
        self.controller.show_normal()

        self.assertEqual(self.rgb_led.calls, ["green"])
        self.assertEqual(self.buzzer.calls, [("off",)])

    def test_low_light_mapping(self):
        self.controller.trigger("low_light")

        self.assertEqual(self.rgb_led.calls, ["red"])
        self.assertEqual(self.buzzer.calls, [("tone", 440, 200, None)])

    def test_high_light_mapping(self):
        self.controller.trigger("high_light")

        self.assertEqual(self.rgb_led.calls, ["blue"])
        self.assertEqual(self.buzzer.calls, [("tone", 880, 200, None)])

    def test_sudden_drop_mapping(self):
        self.controller.trigger("sudden_drop")

        self.assertEqual(self.rgb_led.calls, ["red"])
        self.assertEqual(self.buzzer.calls, [("tone", 660, 150, None)])

    def test_sudden_rise_mapping(self):
        self.controller.trigger("sudden_rise")

        self.assertEqual(self.rgb_led.calls, ["white"])
        self.assertEqual(self.buzzer.calls, [("tone", 880, 150, None)])

    def test_unsupported_anomaly_is_rejected(self):
        with self.assertRaises(ValueError):
            self.controller.trigger("unknown")

    def test_safe_off_turns_both_peripherals_off(self):
        result = self.controller.safe_off()

        self.assertEqual(self.rgb_led.calls, ["off"])
        self.assertEqual(self.buzzer.calls, [("off",)])
        self.assertTrue(result["successful"])

    def test_safe_off_attempts_buzzer_when_rgb_cleanup_fails(self):
        rgb_led = FakeRgbLed(fail_on="off")
        buzzer = FakeBuzzer()

        result = LocalAlarmController(rgb_led, buzzer).safe_off()

        self.assertEqual(rgb_led.calls, ["off"])
        self.assertEqual(buzzer.calls, [("off",)])
        self.assertFalse(result["successful"])
        self.assertIn("RGB off failed", result["rgb_error"])

    def test_safe_off_reports_both_cleanup_failures(self):
        rgb_led = FakeRgbLed(fail_on="off")
        buzzer = FakeBuzzer(fail_on="off")

        result = LocalAlarmController(rgb_led, buzzer).safe_off()

        self.assertEqual(rgb_led.calls, ["off"])
        self.assertEqual(buzzer.calls, [("off",)])
        self.assertFalse(result["successful"])
        self.assertIsNotNone(result["rgb_error"])
        self.assertIsNotNone(result["buzzer_error"])


class AnomalyIntegrationControllerTests(unittest.TestCase):
    def make_controller(self, rgb_led=None, buzzer=None, alarm=True):
        detector = PhotoresistorAnomalyDetector()
        policy = AnomalyAlertPolicy()
        if not alarm:
            return AnomalyIntegrationController(detector, policy), None, None

        rgb_led = rgb_led or FakeRgbLed()
        buzzer = buzzer or FakeBuzzer()
        local_alarm = LocalAlarmController(rgb_led, buzzer)
        return (
            AnomalyIntegrationController(detector, policy, local_alarm),
            rgb_led,
            buzzer,
        )

    def test_first_normal_initializes_green_only_once(self):
        controller, rgb_led, buzzer = self.make_controller()

        first = controller.process(24368, 0)
        second = controller.process(24320, 500)

        self.assertEqual(first["alarm_action"], "show_normal")
        self.assertEqual(second["alarm_action"], "none")
        self.assertEqual(rgb_led.calls, ["green"])
        self.assertEqual(buzzer.calls, [("off",)])

    def test_low_light_entry_triggers_one_alarm(self):
        controller, rgb_led, buzzer = self.make_controller()

        result = controller.process(50, 0)

        self.assertEqual(result["policy_decision"]["decision_reason"], "entered_anomaly")
        self.assertEqual(result["alarm_action"], "trigger_low_light")
        self.assertTrue(result["alarm_triggered"])
        self.assertEqual(rgb_led.calls, ["red"])
        self.assertEqual(buzzer.calls, [("tone", 440, 200, None)])

    def test_same_low_light_before_cooldown_does_not_retrigger(self):
        controller, rgb_led, buzzer = self.make_controller()
        controller.process(50, 0)

        result = controller.process(40, 500)

        self.assertEqual(result["alarm_action"], "none")
        self.assertFalse(result["alarm_triggered"])
        self.assertEqual(rgb_led.calls, ["red"])
        self.assertEqual(buzzer.calls, [("tone", 440, 200, None)])

    def test_same_low_light_after_cooldown_retriggers(self):
        controller, rgb_led, buzzer = self.make_controller()
        controller.process(50, 0)

        result = controller.process(40, 5000)

        self.assertEqual(result["policy_decision"]["decision_reason"], "cooldown_repeat")
        self.assertEqual(result["alarm_action"], "trigger_low_light")
        self.assertEqual(rgb_led.calls, ["red", "red"])
        self.assertEqual(
            buzzer.calls,
            [("tone", 440, 200, None), ("tone", 440, 200, None)],
        )

    def test_high_light_entry_triggers_blue_alarm(self):
        controller, rgb_led, buzzer = self.make_controller()

        result = controller.process(39546, 0)

        self.assertEqual(result["alarm_action"], "trigger_high_light")
        self.assertEqual(rgb_led.calls, ["blue"])
        self.assertEqual(buzzer.calls, [("tone", 880, 200, None)])

    def test_anomaly_type_change_triggers_immediately(self):
        controller, rgb_led, buzzer = self.make_controller()
        controller.process(50, 0)

        result = controller.process(39546, 100)

        self.assertEqual(result["policy_decision"]["decision_reason"], "anomaly_changed")
        self.assertEqual(result["alarm_action"], "trigger_high_light")
        self.assertEqual(rgb_led.calls, ["red", "blue"])
        self.assertEqual(len(buzzer.calls), 2)

    def test_recovery_restores_normal_state(self):
        controller, rgb_led, buzzer = self.make_controller()
        controller.process(50, 0)

        result = controller.process(24300, 500)

        self.assertEqual(result["policy_decision"]["decision_reason"], "recovered")
        self.assertEqual(result["alarm_action"], "show_normal")
        self.assertTrue(result["recovery_handled"])
        self.assertEqual(rgb_led.calls, ["red", "green"])
        self.assertEqual(buzzer.calls[-1], ("off",))

    def test_anomaly_after_recovery_triggers_again(self):
        controller, rgb_led, buzzer = self.make_controller()
        controller.process(50, 0)
        controller.process(24300, 500)

        result = controller.process(39546, 1000)

        self.assertEqual(result["policy_decision"]["decision_reason"], "entered_anomaly")
        self.assertEqual(result["alarm_action"], "trigger_high_light")
        self.assertEqual(rgb_led.calls, ["red", "green", "blue"])

    def test_operation_without_alarm_controller(self):
        controller, _, _ = self.make_controller(alarm=False)

        result = controller.process(50, 0)

        self.assertEqual(result["detector_result"]["anomaly_type"], "low_light")
        self.assertEqual(result["policy_decision"]["decision_reason"], "entered_anomaly")
        self.assertEqual(result["alarm_action"], "none")
        self.assertFalse(result["alarm_triggered"])
        self.assertIsNone(result["alarm_error"])

    def test_alarm_failure_preserves_results_and_attempts_safe_off(self):
        rgb_led = FakeRgbLed()
        buzzer = FakeBuzzer(fail_on="tone")
        controller, _, _ = self.make_controller(rgb_led, buzzer)

        result = controller.process(50, 0)

        self.assertEqual(result["detector_result"]["anomaly_type"], "low_light")
        self.assertEqual(result["policy_decision"]["decision_reason"], "entered_anomaly")
        self.assertEqual(result["alarm_action"], "trigger_low_light")
        self.assertFalse(result["alarm_triggered"])
        self.assertIn("buzzer tone failed", result["alarm_error"])
        self.assertEqual(rgb_led.calls, ["red", "off"])
        self.assertEqual(
            buzzer.calls,
            [("tone", 440, 200, None), ("off",)],
        )

    def test_reset_clears_state_and_allows_normal_initialization_again(self):
        controller, rgb_led, _ = self.make_controller()
        controller.process(24368, 100)
        controller.process(50, 200)

        controller.reset()

        self.assertEqual(controller.detector.get_history(), [])
        self.assertIsNone(controller.alert_policy.active_anomaly_type)
        self.assertIsNone(controller.last_alarm_error)
        result = controller.process(24368, 0)
        self.assertEqual(result["alarm_action"], "show_normal")
        self.assertEqual(rgb_led.calls.count("green"), 2)

    def test_invalid_sensor_reading_preserves_detector_error(self):
        controller, _, _ = self.make_controller()

        with self.assertRaises(TypeError):
            controller.process("invalid", 0)

    def test_representative_complete_sequence(self):
        controller, rgb_led, buzzer = self.make_controller()
        sequence = (
            (24368, 0),
            (24320, 500),
            (50, 1000),
            (40, 1500),
            (45, 6000),
            (24300, 6500),
            (39546, 7000),
            (24350, 7500),
        )

        results = [controller.process(value, timestamp) for value, timestamp in sequence]

        self.assertEqual(
            [result["detector_result"]["anomaly_type"] for result in results],
            [
                "normal",
                "normal",
                "low_light",
                "low_light",
                "low_light",
                "sudden_rise",
                "high_light",
                "sudden_drop",
            ],
        )
        self.assertEqual(
            [result["policy_decision"]["decision_reason"] for result in results],
            [
                "normal",
                "normal",
                "entered_anomaly",
                "suppressed_same_anomaly",
                "cooldown_repeat",
                "recovered",
                "entered_anomaly",
                "recovered",
            ],
        )
        self.assertEqual(
            rgb_led.calls,
            ["green", "red", "red", "green", "blue", "green"],
        )
        self.assertEqual(
            buzzer.calls,
            [
                ("off",),
                ("tone", 440, 200, None),
                ("tone", 440, 200, None),
                ("off",),
                ("tone", 880, 200, None),
                ("off",),
            ],
        )


if __name__ == "__main__":
    unittest.main()
