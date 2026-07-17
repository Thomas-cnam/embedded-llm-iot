"""Dependency-injected local RGB LED and buzzer alarm controller."""


class LocalAlarmController:
    """Map anomaly states to provisional bounded local alarm behavior."""

    # These mappings are provisional and require real hardware validation.
    _MAPPINGS = {
        "low_light": ("red", 440, 200),
        "high_light": ("blue", 880, 200),
        "sudden_drop": ("red", 660, 150),
        "sudden_rise": ("white", 880, 150),
    }

    def __init__(self, rgb_led, buzzer):
        self._validate_methods(
            "rgb_led", rgb_led, ("green", "red", "blue", "white", "off")
        )
        self._validate_methods("buzzer", buzzer, ("tone", "off"))
        self.rgb_led = rgb_led
        self.buzzer = buzzer

    @staticmethod
    def _validate_methods(name, collaborator, method_names):
        if collaborator is None:
            raise TypeError(name + " must not be None")
        for method_name in method_names:
            if not callable(getattr(collaborator, method_name, None)):
                raise TypeError(name + " must provide " + method_name + "()")

    def show_normal(self):
        """Display the provisional normal state and silence the buzzer."""
        self.rgb_led.green()
        self.buzzer.off()

    def trigger(self, anomaly_type):
        """Display one anomaly state and play one short bounded tone."""
        if anomaly_type not in self._MAPPINGS:
            raise ValueError("unsupported anomaly type: " + str(anomaly_type))

        rgb_method_name, frequency, duration_ms = self._MAPPINGS[anomaly_type]
        getattr(self.rgb_led, rgb_method_name)()
        self.buzzer.tone(frequency, duration_ms)

    def safe_off(self):
        """Attempt both cleanup operations and report any failures."""
        rgb_error = None
        buzzer_error = None

        try:
            self.rgb_led.off()
        except Exception as error:
            rgb_error = str(error)

        try:
            self.buzzer.off()
        except Exception as error:
            buzzer_error = str(error)

        return {
            "successful": rgb_error is None and buzzer_error is None,
            "rgb_error": rgb_error,
            "buzzer_error": buzzer_error,
        }
