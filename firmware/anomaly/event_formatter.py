"""Pure anomaly-event construction and compact JSON formatting."""

try:
    import ujson as _json

    _USING_UJSON = True
except ImportError:
    import json as _json

    _USING_UJSON = False


class AnomalyEventFormatter:
    """Build schema 1.0 anomaly events from integration results."""

    _ANOMALY_TYPES = (
        "low_light",
        "high_light",
        "sudden_drop",
        "sudden_rise",
    )
    _DETECTOR_METHODS = ("none", "threshold", "delta")

    def __init__(self, schema_version="1.0", starting_event_id=1):
        self._validate_non_empty_string("schema_version", schema_version)
        self._validate_integer("starting_event_id", starting_event_id)
        if starting_event_id < 0:
            raise ValueError("starting_event_id must be zero or greater")

        self.schema_version = schema_version
        self.starting_event_id = starting_event_id
        self.next_event_id = starting_event_id

    @staticmethod
    def _validate_non_empty_string(name, value):
        if not isinstance(value, str):
            raise TypeError(name + " must be a string")
        if not value.strip():
            raise ValueError(name + " must not be empty")

    @staticmethod
    def _validate_integer(name, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(name + " must be an integer")

    @classmethod
    def _validate_optional_integer(cls, name, value):
        if value is not None:
            cls._validate_integer(name, value)

    @staticmethod
    def _require_key(container, key, container_name):
        if key not in container:
            raise ValueError(container_name + " must contain " + key)
        return container[key]

    @classmethod
    def _require_dictionary(cls, container, key, container_name):
        value = cls._require_key(container, key, container_name)
        if not isinstance(value, dict):
            raise TypeError(container_name + " " + key + " must be a dictionary")
        return value

    @classmethod
    def _validate_history(cls, history):
        if not isinstance(history, list):
            raise TypeError("detector_result history must be a list")
        if not history:
            raise ValueError("detector_result history must not be empty")
        for value in history:
            cls._validate_integer("detector_result history value", value)
            if value < 0 or value > 65535:
                raise ValueError(
                    "detector_result history values must be between 0 and 65535"
                )

    @classmethod
    def _validate_detector_result(cls, detector_result):
        required_fields = (
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
        )
        for field_name in required_fields:
            cls._require_key(detector_result, field_name, "detector_result")

        is_anomaly = detector_result["is_anomaly"]
        if not isinstance(is_anomaly, bool):
            raise TypeError("detector_result is_anomaly must be a boolean")

        anomaly_type = detector_result["anomaly_type"]
        cls._validate_non_empty_string(
            "detector_result anomaly_type", anomaly_type
        )
        if is_anomaly:
            if anomaly_type not in cls._ANOMALY_TYPES:
                raise ValueError("unsupported anomaly_type: " + anomaly_type)
        elif anomaly_type != "normal":
            raise ValueError("a normal detector result must use anomaly_type normal")

        detector_method = detector_result["detector_method"]
        cls._validate_non_empty_string(
            "detector_result detector_method", detector_method
        )
        if detector_method not in cls._DETECTOR_METHODS:
            raise ValueError("unsupported detector_method: " + detector_method)
        if is_anomaly and detector_method == "none":
            raise ValueError("an anomalous result cannot use detector_method none")
        if not is_anomaly and detector_method != "none":
            raise ValueError("a normal result must use detector_method none")

        secondary_method = detector_result["secondary_method"]
        if secondary_method is not None:
            cls._validate_non_empty_string(
                "detector_result secondary_method", secondary_method
            )
            if secondary_method not in ("sudden_drop", "sudden_rise"):
                raise ValueError(
                    "unsupported secondary_method: " + secondary_method
                )

        value = detector_result["value"]
        cls._validate_integer("detector_result value", value)
        if value < 0 or value > 65535:
            raise ValueError("detector_result value must be between 0 and 65535")

        previous_value = detector_result["previous_value"]
        delta = detector_result["delta"]
        cls._validate_optional_integer(
            "detector_result previous_value", previous_value
        )
        cls._validate_optional_integer("detector_result delta", delta)
        if previous_value is None and delta is not None:
            raise ValueError("delta must be None when previous_value is None")
        if previous_value is not None:
            if previous_value < 0 or previous_value > 65535:
                raise ValueError(
                    "detector_result previous_value must be between 0 and 65535"
                )
            if delta is None:
                raise ValueError("delta must be present when previous_value is present")
            if delta != value - previous_value:
                raise ValueError("delta must equal value minus previous_value")

        cls._validate_history(detector_result["history"])
        if detector_result["history"][-1] != value:
            raise ValueError("detector_result history must end with value")

        state_before = detector_result["state_before"]
        if state_before is not None:
            cls._validate_non_empty_string(
                "detector_result state_before", state_before
            )
        state_after = detector_result["state_after"]
        cls._validate_non_empty_string(
            "detector_result state_after", state_after
        )
        if state_after != anomaly_type:
            raise ValueError("state_after must match anomaly_type")

        low_threshold = detector_result["low_threshold"]
        high_threshold = detector_result["high_threshold"]
        delta_threshold = detector_result["delta_threshold"]
        cls._validate_integer("detector_result low_threshold", low_threshold)
        cls._validate_integer("detector_result high_threshold", high_threshold)
        cls._validate_integer("detector_result delta_threshold", delta_threshold)
        if low_threshold < 0 or high_threshold < 0:
            raise ValueError("detector thresholds must be zero or greater")
        if low_threshold >= high_threshold:
            raise ValueError("low_threshold must be lower than high_threshold")
        if delta_threshold <= 0:
            raise ValueError("delta_threshold must be greater than zero")

    @classmethod
    def _validate_policy_decision(cls, policy_decision):
        should_emit = cls._require_key(
            policy_decision, "should_emit_alert", "policy_decision"
        )
        timestamp_ms = cls._require_key(
            policy_decision, "timestamp_ms", "policy_decision"
        )
        cooldown_active = cls._require_key(
            policy_decision, "cooldown_active", "policy_decision"
        )

        if not isinstance(should_emit, bool):
            raise TypeError(
                "policy_decision should_emit_alert must be a boolean"
            )
        cls._validate_integer("policy_decision timestamp_ms", timestamp_ms)
        if timestamp_ms < 0:
            raise ValueError("policy_decision timestamp_ms must be zero or greater")
        if not isinstance(cooldown_active, bool):
            raise TypeError("policy_decision cooldown_active must be a boolean")

    @classmethod
    def _validate_integration_result(cls, integration_result):
        if not isinstance(integration_result, dict):
            raise TypeError("integration_result must be a dictionary")

        detector_result = cls._require_dictionary(
            integration_result, "detector_result", "integration_result"
        )
        policy_decision = cls._require_dictionary(
            integration_result, "policy_decision", "integration_result"
        )
        alarm_triggered = cls._require_key(
            integration_result, "alarm_triggered", "integration_result"
        )
        if not isinstance(alarm_triggered, bool):
            raise TypeError("integration_result alarm_triggered must be a boolean")

        cls._validate_detector_result(detector_result)
        cls._validate_policy_decision(policy_decision)

        if policy_decision["should_emit_alert"] and not detector_result["is_anomaly"]:
            raise ValueError("an emitted alert requires an anomalous detector result")

        return detector_result, policy_decision, alarm_triggered

    def build_event(self, integration_result):
        """Build one new event dictionary, or return None when suppressed."""
        detector_result, policy_decision, alarm_triggered = (
            self._validate_integration_result(integration_result)
        )

        if not policy_decision["should_emit_alert"]:
            return None

        event = {
            "schema_version": self.schema_version,
            "event_id": self.next_event_id,
            "event_type": "anomaly",
            "sensor": "photoresistor",
            "anomaly_type": detector_result["anomaly_type"],
            "detector_method": detector_result["detector_method"],
            "value": detector_result["value"],
            "previous_value": detector_result["previous_value"],
            "delta": detector_result["delta"],
            "history": list(detector_result["history"]),
            "timestamp_ms": policy_decision["timestamp_ms"],
            "local_alarm": alarm_triggered,
            "low_threshold": detector_result["low_threshold"],
            "high_threshold": detector_result["high_threshold"],
            "delta_threshold": detector_result["delta_threshold"],
            "secondary_method": detector_result["secondary_method"],
            "state_before": detector_result["state_before"],
            "state_after": detector_result["state_after"],
            "cooldown_active": policy_decision["cooldown_active"],
        }
        self.next_event_id += 1
        return event

    def serialize_event(self, integration_result):
        """Return one compact JSON object string, or None when suppressed."""
        event = self.build_event(integration_result)
        if event is None:
            return None
        if _USING_UJSON:
            return _json.dumps(event)
        return _json.dumps(event, separators=(",", ":"))

    def reset(self):
        """Reset the next event identifier to its configured starting value."""
        self.next_event_id = self.starting_event_id
