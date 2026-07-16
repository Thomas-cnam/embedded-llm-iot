"""Host-side tests for the pure photoresistor anomaly detector."""

import os
import sys
import unittest


REPOSITORY_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPOSITORY_ROOT not in sys.path:
    sys.path.insert(0, REPOSITORY_ROOT)

from firmware.anomaly.config import (  # noqa: E402
    HIGH_LIGHT_THRESHOLD,
    HISTORY_SIZE,
    LOW_LIGHT_THRESHOLD,
    SUDDEN_CHANGE_THRESHOLD,
)
from firmware.anomaly.detector import PhotoresistorAnomalyDetector  # noqa: E402


class PhotoresistorAnomalyDetectorTests(unittest.TestCase):
    def test_default_configuration_is_accepted(self):
        detector = PhotoresistorAnomalyDetector()

        self.assertEqual(detector.low_threshold, LOW_LIGHT_THRESHOLD)
        self.assertEqual(detector.high_threshold, HIGH_LIGHT_THRESHOLD)
        self.assertEqual(detector.delta_threshold, SUDDEN_CHANGE_THRESHOLD)
        self.assertEqual(detector.history_size, HISTORY_SIZE)

    def test_invalid_threshold_order_is_rejected(self):
        cases = ((5000, 5000), (6000, 5000))

        for low_threshold, high_threshold in cases:
            with self.subTest(low=low_threshold, high=high_threshold):
                with self.assertRaises(ValueError):
                    PhotoresistorAnomalyDetector(
                        low_threshold=low_threshold,
                        high_threshold=high_threshold,
                    )

    def test_negative_thresholds_are_rejected(self):
        with self.assertRaises(ValueError):
            PhotoresistorAnomalyDetector(low_threshold=-1)
        with self.assertRaises(ValueError):
            PhotoresistorAnomalyDetector(high_threshold=-1)

    def test_non_positive_delta_threshold_is_rejected(self):
        for value in (0, -1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    PhotoresistorAnomalyDetector(delta_threshold=value)

    def test_non_positive_history_size_is_rejected(self):
        for value in (0, -1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    PhotoresistorAnomalyDetector(history_size=value)

    def test_boolean_configuration_values_are_rejected(self):
        parameter_names = (
            "low_threshold",
            "high_threshold",
            "delta_threshold",
            "history_size",
        )

        for parameter_name in parameter_names:
            with self.subTest(parameter=parameter_name):
                with self.assertRaises(TypeError):
                    PhotoresistorAnomalyDetector(**{parameter_name: True})

    def test_non_integer_configuration_values_are_rejected(self):
        cases = (
            ("low_threshold", 10.5),
            ("high_threshold", "32000"),
            ("delta_threshold", None),
            ("history_size", 5.0),
        )

        for parameter_name, value in cases:
            with self.subTest(parameter=parameter_name, value=value):
                with self.assertRaises(TypeError):
                    PhotoresistorAnomalyDetector(**{parameter_name: value})

    def test_readings_outside_adc_range_are_rejected(self):
        detector = PhotoresistorAnomalyDetector()

        for value in (-1, 65536):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    detector.evaluate(value)

    def test_non_integer_readings_are_rejected(self):
        detector = PhotoresistorAnomalyDetector()

        for value in (1.5, "24368", True):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    detector.evaluate(value)

    def test_adc_boundary_values_are_accepted(self):
        detector = PhotoresistorAnomalyDetector()

        low_result = detector.evaluate(0)
        high_result = detector.evaluate(65535)

        self.assertEqual(low_result["value"], 0)
        self.assertEqual(low_result["anomaly_type"], "low_light")
        self.assertEqual(high_result["value"], 65535)
        self.assertEqual(high_result["anomaly_type"], "high_light")

    def test_ambient_baseline_values_are_normal_independently(self):
        for value in (24293, 24368, 24437):
            with self.subTest(value=value):
                result = PhotoresistorAnomalyDetector().evaluate(value)
                self.assertFalse(result["is_anomaly"])
                self.assertEqual(result["anomaly_type"], "normal")
                self.assertEqual(result["detector_method"], "none")
                self.assertIsNone(result["secondary_method"])

    def test_stable_ambient_sequence_remains_normal(self):
        detector = PhotoresistorAnomalyDetector()
        values = (24293, 24368, 24437, 24320, 24389, 24405)

        results = [detector.evaluate(value) for value in values]

        self.assertTrue(all(not result["is_anomaly"] for result in results))
        self.assertTrue(
            all(result["anomaly_type"] == "normal" for result in results)
        )
        self.assertTrue(
            all(result["detector_method"] == "none" for result in results)
        )
        self.assertEqual(detector.get_history(), list(values[-HISTORY_SIZE:]))

    def test_low_light_values_use_threshold_detection(self):
        for value in (16, 47, 80, 4999):
            with self.subTest(value=value):
                result = PhotoresistorAnomalyDetector().evaluate(value)
                self.assertTrue(result["is_anomaly"])
                self.assertEqual(result["anomaly_type"], "low_light")
                self.assertEqual(result["detector_method"], "threshold")

    def test_low_threshold_boundary_is_normal(self):
        result = PhotoresistorAnomalyDetector().evaluate(5000)

        self.assertFalse(result["is_anomaly"])
        self.assertEqual(result["anomaly_type"], "normal")
        self.assertEqual(result["detector_method"], "none")

    def test_high_light_values_use_threshold_detection(self):
        for value in (32001, 36889, 39546, 42010, 65535):
            with self.subTest(value=value):
                result = PhotoresistorAnomalyDetector().evaluate(value)
                self.assertTrue(result["is_anomaly"])
                self.assertEqual(result["anomaly_type"], "high_light")
                self.assertEqual(result["detector_method"], "threshold")

    def test_high_threshold_boundary_is_normal(self):
        result = PhotoresistorAnomalyDetector().evaluate(32000)

        self.assertFalse(result["is_anomaly"])
        self.assertEqual(result["anomaly_type"], "normal")
        self.assertEqual(result["detector_method"], "none")

    def test_sudden_drop_without_threshold_crossing(self):
        detector = PhotoresistorAnomalyDetector()
        detector.evaluate(24368)

        result = detector.evaluate(15000)

        self.assertTrue(result["is_anomaly"])
        self.assertEqual(result["anomaly_type"], "sudden_drop")
        self.assertEqual(result["detector_method"], "delta")
        self.assertIsNone(result["secondary_method"])
        self.assertEqual(result["delta"], -9368)

    def test_sudden_rise_without_threshold_crossing(self):
        detector = PhotoresistorAnomalyDetector()
        detector.evaluate(15000)

        result = detector.evaluate(24000)

        self.assertTrue(result["is_anomaly"])
        self.assertEqual(result["anomaly_type"], "sudden_rise")
        self.assertEqual(result["detector_method"], "delta")
        self.assertIsNone(result["secondary_method"])
        self.assertEqual(result["delta"], 9000)

    def test_combined_low_light_and_sudden_drop(self):
        detector = PhotoresistorAnomalyDetector()
        detector.evaluate(24368)

        result = detector.evaluate(50)

        self.assertEqual(result["anomaly_type"], "low_light")
        self.assertEqual(result["detector_method"], "threshold")
        self.assertEqual(result["secondary_method"], "sudden_drop")
        self.assertEqual(result["delta"], -24318)

    def test_combined_high_light_and_sudden_rise(self):
        detector = PhotoresistorAnomalyDetector()
        detector.evaluate(24368)

        result = detector.evaluate(39546)

        self.assertEqual(result["anomaly_type"], "high_light")
        self.assertEqual(result["detector_method"], "threshold")
        self.assertEqual(result["secondary_method"], "sudden_rise")
        self.assertEqual(result["delta"], 15178)

    def test_exact_delta_boundaries_are_sudden_changes(self):
        drop_detector = PhotoresistorAnomalyDetector()
        drop_detector.evaluate(20000)
        drop_result = drop_detector.evaluate(12000)

        rise_detector = PhotoresistorAnomalyDetector()
        rise_detector.evaluate(12000)
        rise_result = rise_detector.evaluate(20000)

        self.assertEqual(drop_result["delta"], -8000)
        self.assertEqual(drop_result["anomaly_type"], "sudden_drop")
        self.assertEqual(rise_result["delta"], 8000)
        self.assertEqual(rise_result["anomaly_type"], "sudden_rise")

    def test_first_normal_reading_has_no_previous_state(self):
        result = PhotoresistorAnomalyDetector().evaluate(24368)

        self.assertIsNone(result["previous_value"])
        self.assertIsNone(result["delta"])
        self.assertIsNone(result["state_before"])
        self.assertEqual(result["state_after"], "normal")

    def test_first_reading_still_uses_threshold_detection(self):
        result = PhotoresistorAnomalyDetector().evaluate(50)

        self.assertIsNone(result["previous_value"])
        self.assertIsNone(result["delta"])
        self.assertEqual(result["anomaly_type"], "low_light")
        self.assertEqual(result["detector_method"], "threshold")
        self.assertIsNone(result["secondary_method"])

    def test_history_includes_current_value_and_is_limited(self):
        detector = PhotoresistorAnomalyDetector()
        values = (10000, 11000, 12000, 13000, 14000, 15000, 16000)

        for value in values:
            result = detector.evaluate(value)

        self.assertEqual(result["history"], list(values[-5:]))
        self.assertEqual(detector.get_history(), list(values[-5:]))

    def test_returned_history_cannot_modify_internal_history(self):
        detector = PhotoresistorAnomalyDetector()
        result = detector.evaluate(24368)

        result["history"].append(1)
        direct_history = detector.get_history()
        direct_history.append(2)

        self.assertEqual(detector.get_history(), [24368])

    def test_state_transitions_are_reported(self):
        detector = PhotoresistorAnomalyDetector()

        normal = detector.evaluate(24368)
        low = detector.evaluate(50)
        normal_after_low = detector.evaluate(5000)
        high = detector.evaluate(32001)
        normal_after_high = detector.evaluate(32000)

        self.assertEqual((normal["state_before"], normal["state_after"]), (None, "normal"))
        self.assertEqual((low["state_before"], low["state_after"]), ("normal", "low_light"))
        self.assertEqual(
            (normal_after_low["state_before"], normal_after_low["state_after"]),
            ("low_light", "normal"),
        )
        self.assertEqual((high["state_before"], high["state_after"]), ("normal", "high_light"))
        self.assertEqual(
            (normal_after_high["state_before"], normal_after_high["state_after"]),
            ("high_light", "normal"),
        )

    def test_reset_clears_previous_value_history_and_state(self):
        detector = PhotoresistorAnomalyDetector()
        detector.evaluate(24368)
        detector.evaluate(50)

        detector.reset()
        result = detector.evaluate(24368)

        self.assertIsNone(result["previous_value"])
        self.assertIsNone(result["delta"])
        self.assertIsNone(result["state_before"])
        self.assertEqual(result["history"], [24368])

    def test_custom_configuration_is_used_and_returned(self):
        detector = PhotoresistorAnomalyDetector(
            low_threshold=100,
            high_threshold=1000,
            delta_threshold=50,
            history_size=2,
        )

        result = detector.evaluate(500)

        self.assertEqual(result["low_threshold"], 100)
        self.assertEqual(result["high_threshold"], 1000)
        self.assertEqual(result["delta_threshold"], 50)
        self.assertEqual(detector.history_size, 2)

    def test_result_contains_all_required_fields(self):
        result = PhotoresistorAnomalyDetector().evaluate(24368)
        expected_fields = {
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
        }

        self.assertEqual(set(result), expected_fields)


if __name__ == "__main__":
    unittest.main()
