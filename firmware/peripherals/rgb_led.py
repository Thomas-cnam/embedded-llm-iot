"""RGB LED GPIO helper for the ESP32-C6 custom PCB."""

from machine import Pin


class RgbLed:
    """Control the RGB LED on red 21, green 11, and blue 10 by default."""

    def __init__(self, red_pin=21, green_pin=11, blue_pin=10, active_low=False):
        self.active_low = active_low
        self.red_pin = Pin(red_pin, Pin.OUT)
        self.green_pin = Pin(green_pin, Pin.OUT)
        self.blue_pin = Pin(blue_pin, Pin.OUT)
        self.off()

    def _value(self, is_on):
        if self.active_low:
            return 0 if is_on else 1
        return 1 if is_on else 0

    def set(self, red_on, green_on, blue_on):
        """Set RGB channel states."""
        self.red_pin.value(self._value(red_on))
        self.green_pin.value(self._value(green_on))
        self.blue_pin.value(self._value(blue_on))

    def red(self):
        self.set(True, False, False)

    def green(self):
        self.set(False, True, False)

    def blue(self):
        self.set(False, False, True)

    def white(self):
        self.set(True, True, True)

    def off(self):
        self.set(False, False, False)
