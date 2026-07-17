"""Coordinate pure detection, alert policy, and optional local alarms."""


class AnomalyIntegrationController:
    """Process readings while preserving detector and policy results."""

    def __init__(self, detector, alert_policy, alarm_controller=None):
        self._validate_methods("detector", detector, ("evaluate", "reset"))
        self._validate_methods(
            "alert_policy", alert_policy, ("evaluate", "reset")
        )
        if alarm_controller is not None:
            self._validate_methods(
                "alarm_controller",
                alarm_controller,
                ("show_normal", "trigger", "safe_off"),
            )

        self.detector = detector
        self.alert_policy = alert_policy
        self.alarm_controller = alarm_controller
        self._normal_visual_initialized = False
        self.last_alarm_error = None

    @staticmethod
    def _validate_methods(name, collaborator, method_names):
        if collaborator is None:
            raise TypeError(name + " must not be None")
        for method_name in method_names:
            if not callable(getattr(collaborator, method_name, None)):
                raise TypeError(name + " must provide " + method_name + "()")

    @staticmethod
    def _format_cleanup_error(cleanup_result):
        if not isinstance(cleanup_result, dict):
            return None
        if cleanup_result.get("successful", True):
            return None

        parts = []
        if cleanup_result.get("rgb_error"):
            parts.append("RGB cleanup: " + cleanup_result["rgb_error"])
        if cleanup_result.get("buzzer_error"):
            parts.append("buzzer cleanup: " + cleanup_result["buzzer_error"])
        if not parts:
            parts.append("cleanup was not fully successful")
        return "; ".join(parts)

    def _attempt_safe_off(self):
        if self.alarm_controller is None:
            return None
        try:
            return self._format_cleanup_error(self.alarm_controller.safe_off())
        except Exception as error:
            return "safe_off failed: " + str(error)

    def process(self, value, timestamp_ms):
        """Evaluate one reading and coordinate any required local action."""
        detector_result = self.detector.evaluate(value)
        policy_decision = self.alert_policy.evaluate(
            detector_result, timestamp_ms
        )

        alarm_action = "none"
        alarm_triggered = False
        alarm_error = None
        recovery_handled = False

        if self.alarm_controller is not None:
            try:
                if policy_decision["recovered"]:
                    alarm_action = "show_normal"
                    self.alarm_controller.show_normal()
                    self._normal_visual_initialized = True
                    recovery_handled = True
                elif policy_decision["should_emit_alert"]:
                    anomaly_type = detector_result["anomaly_type"]
                    alarm_action = "trigger_" + anomaly_type
                    self.alarm_controller.trigger(anomaly_type)
                    self._normal_visual_initialized = False
                    alarm_triggered = True
                elif (
                    not detector_result["is_anomaly"]
                    and not self._normal_visual_initialized
                ):
                    alarm_action = "show_normal"
                    self.alarm_controller.show_normal()
                    self._normal_visual_initialized = True
            except Exception as error:
                alarm_error = str(error)
                alarm_triggered = False
                self._normal_visual_initialized = False
                cleanup_error = self._attempt_safe_off()
                if cleanup_error:
                    alarm_error = alarm_error + "; " + cleanup_error

        self.last_alarm_error = alarm_error

        return {
            "detector_result": detector_result,
            "policy_decision": policy_decision,
            "alarm_action": alarm_action,
            "alarm_triggered": alarm_triggered,
            "alarm_error": alarm_error,
            "recovery_handled": recovery_handled,
        }

    def reset(self):
        """Reset detector, policy, visual initialization, and alarm state."""
        self.detector.reset()
        self.alert_policy.reset()
        self._normal_visual_initialized = False
        self.last_alarm_error = None

        cleanup_error = self._attempt_safe_off()
        if cleanup_error:
            self.last_alarm_error = cleanup_error
