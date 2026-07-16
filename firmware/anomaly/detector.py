"""Hardware-independent photoresistor anomaly detection logic."""

from .config import (
    HIGH_LIGHT_THRESHOLD,
    HISTORY_SIZE,
    LOW_LIGHT_THRESHOLD,
    SUDDEN_CHANGE_THRESHOLD,
)


class PhotoresistorAnomalyDetector:
    """Classify ADC readings using provisional threshold and delta rules."""

    ADC_MIN = 0
    ADC_MAX = 65535

    def __init__(
        self,
        low_threshold=LOW_LIGHT_THRESHOLD,
        high_threshold=HIGH_LIGHT_THRESHOLD,
        delta_threshold=SUDDEN_CHANGE_THRESHOLD,
        history_size=HISTORY_SIZE,
    ):
        self._validate_integer("low_threshold", low_threshold)
        self._validate_integer("high_threshold", high_threshold)
        self._validate_integer("delta_threshold", delta_threshold)
        self._validate_integer("history_size", history_size)

        if low_threshold < 0:
            raise ValueError("low_threshold must be non-negative")
        if high_threshold < 0:
            raise ValueError("high_threshold must be non-negative")
        if low_threshold >= high_threshold:
            raise ValueError("low_threshold must be lower than high_threshold")
        if delta_threshold <= 0:
            raise ValueError("delta_threshold must be greater than zero")
        if history_size <= 0:
            raise ValueError("history_size must be greater than zero")

        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
        self.delta_threshold = delta_threshold
        self.history_size = history_size
        self.reset()

    @staticmethod
    def _validate_integer(name, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(name + " must be an integer")

    def _validate_reading(self, value):
        self._validate_integer("value", value)
        if value < self.ADC_MIN or value > self.ADC_MAX:
            raise ValueError("value must be between 0 and 65535")

    def evaluate(self, value):
        """Evaluate one ADC reading and return a new result dictionary."""
        self._validate_reading(value)

        previous_value = self._previous_value
        state_before = self._state
        delta = None
        sudden_condition = None

        if previous_value is not None:
            delta = value - previous_value
            if delta <= -self.delta_threshold:
                sudden_condition = "sudden_drop"
            elif delta >= self.delta_threshold:
                sudden_condition = "sudden_rise"

        threshold_condition = None
        if value < self.low_threshold:
            threshold_condition = "low_light"
        elif value > self.high_threshold:
            threshold_condition = "high_light"

        if threshold_condition is not None:
            anomaly_type = threshold_condition
            detector_method = "threshold"
            secondary_method = sudden_condition
        elif sudden_condition is not None:
            anomaly_type = sudden_condition
            detector_method = "delta"
            secondary_method = None
        else:
            anomaly_type = "normal"
            detector_method = "none"
            secondary_method = None

        self._history.append(value)
        if len(self._history) > self.history_size:
            del self._history[0]

        self._previous_value = value
        self._state = anomaly_type

        return {
            "is_anomaly": anomaly_type != "normal",
            "anomaly_type": anomaly_type,
            "detector_method": detector_method,
            "secondary_method": secondary_method,
            "value": value,
            "previous_value": previous_value,
            "delta": delta,
            "history": self.get_history(),
            "state_before": state_before,
            "state_after": anomaly_type,
            "low_threshold": self.low_threshold,
            "high_threshold": self.high_threshold,
            "delta_threshold": self.delta_threshold,
        }

    def reset(self):
        """Clear the previous value, history, and current state."""
        self._previous_value = None
        self._history = []
        self._state = None

    def get_history(self):
        """Return a copy of the recent reading history."""
        return list(self._history)
