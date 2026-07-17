"""Hardware-independent alert cooldown and state-transition policy."""

from .config import ALERT_COOLDOWN_MS


class AnomalyAlertPolicy:
    """Decide when detector results should produce a new alert."""

    def __init__(self, cooldown_ms=ALERT_COOLDOWN_MS, repeat_after_cooldown=True):
        self._validate_integer("cooldown_ms", cooldown_ms)
        if cooldown_ms < 0:
            raise ValueError("cooldown_ms must be zero or greater")
        if not isinstance(repeat_after_cooldown, bool):
            raise TypeError("repeat_after_cooldown must be a boolean")

        self.cooldown_ms = cooldown_ms
        self.repeat_after_cooldown = repeat_after_cooldown
        self.reset()

    @staticmethod
    def _validate_integer(name, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(name + " must be an integer")

    @staticmethod
    def _validate_detector_result(detector_result):
        if not isinstance(detector_result, dict):
            raise TypeError("detector_result must be a dictionary")
        if "is_anomaly" not in detector_result:
            raise ValueError("detector_result must contain is_anomaly")
        if "anomaly_type" not in detector_result:
            raise ValueError("detector_result must contain anomaly_type")
        if not isinstance(detector_result["is_anomaly"], bool):
            raise TypeError("detector_result is_anomaly must be a boolean")
        if not isinstance(detector_result["anomaly_type"], str):
            raise TypeError("detector_result anomaly_type must be a string")
        if detector_result["is_anomaly"]:
            if detector_result["anomaly_type"] == "normal":
                raise ValueError("an anomalous result cannot use anomaly_type normal")
        elif detector_result["anomaly_type"] != "normal":
            raise ValueError("a normal result must use anomaly_type normal")

    def _validate_timestamp(self, timestamp_ms):
        self._validate_integer("timestamp_ms", timestamp_ms)
        if timestamp_ms < 0:
            raise ValueError("timestamp_ms must be zero or greater")
        if (
            self._last_timestamp_ms is not None
            and timestamp_ms < self._last_timestamp_ms
        ):
            raise ValueError("timestamp_ms must not move backwards")

    def _is_threshold_recovery_transition(self, detector_result):
        if detector_result.get("detector_method") != "delta":
            return False
        if detector_result.get("state_before") != self.active_anomaly_type:
            return False
        return (
            self.active_anomaly_type == "low_light"
            and detector_result["anomaly_type"] == "sudden_rise"
        ) or (
            self.active_anomaly_type == "high_light"
            and detector_result["anomaly_type"] == "sudden_drop"
        )

    def evaluate(self, detector_result, timestamp_ms):
        """Return a new alert decision for one detector result."""
        self._validate_detector_result(detector_result)
        self._validate_timestamp(timestamp_ms)

        previous_anomaly_type = self.active_anomaly_type
        anomaly_type = detector_result["anomaly_type"]
        should_emit_alert = False
        recovered = False
        cooldown_active = False
        cooldown_remaining_ms = 0

        reports_recovery = not detector_result["is_anomaly"]
        if self._is_threshold_recovery_transition(detector_result):
            reports_recovery = True

        if reports_recovery:
            if self.active_anomaly_type is not None:
                decision_reason = "recovered"
                recovered = True
                self.active_anomaly_type = None
                self.last_alert_timestamp_ms = None
            else:
                decision_reason = "normal"
        elif self.active_anomaly_type is None:
            decision_reason = "entered_anomaly"
            should_emit_alert = True
            self.active_anomaly_type = anomaly_type
            self.last_alert_timestamp_ms = timestamp_ms
        elif anomaly_type != self.active_anomaly_type:
            decision_reason = "anomaly_changed"
            should_emit_alert = True
            self.active_anomaly_type = anomaly_type
            self.last_alert_timestamp_ms = timestamp_ms
        else:
            elapsed_ms = timestamp_ms - self.last_alert_timestamp_ms
            cooldown_remaining_ms = self.cooldown_ms - elapsed_ms
            if cooldown_remaining_ms < 0:
                cooldown_remaining_ms = 0

            if self.repeat_after_cooldown and elapsed_ms >= self.cooldown_ms:
                decision_reason = "cooldown_repeat"
                should_emit_alert = True
                self.last_alert_timestamp_ms = timestamp_ms
            else:
                decision_reason = "suppressed_same_anomaly"
                cooldown_active = elapsed_ms < self.cooldown_ms

        self.previous_detector_state = anomaly_type
        self._last_timestamp_ms = timestamp_ms

        return {
            "should_emit_alert": should_emit_alert,
            "decision_reason": decision_reason,
            "active_anomaly_type": self.active_anomaly_type,
            "previous_anomaly_type": previous_anomaly_type,
            "recovered": recovered,
            "cooldown_active": cooldown_active,
            "cooldown_remaining_ms": cooldown_remaining_ms,
            "timestamp_ms": timestamp_ms,
        }

    def reset(self):
        """Clear active anomaly, alert timestamp, and detector-state history."""
        self.active_anomaly_type = None
        self.last_alert_timestamp_ms = None
        self.previous_detector_state = None
        self._last_timestamp_ms = None
