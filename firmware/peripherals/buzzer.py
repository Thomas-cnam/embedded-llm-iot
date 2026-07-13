"""Passive buzzer PWM helper for the ESP32-C6 custom PCB."""

from machine import PWM, Pin
from time import sleep_ms


class Buzzer:
    """Control the passive buzzer connected to GPIO 5 by default."""

    def __init__(self, pin=5, default_duty_u16=32768, default_duty=512):
        self.pin = pin
        self.default_duty_u16 = default_duty_u16
        self.default_duty = default_duty
        self.pwm = PWM(Pin(pin))
        self.off()

    def _set_duty(self, duty):
        if hasattr(self.pwm, "duty_u16"):
            value = self.default_duty_u16 if duty is None else duty
            self.pwm.duty_u16(value)
        else:
            value = self.default_duty if duty is None else duty
            self.pwm.duty(value)

    def tone(self, frequency, duration_ms, duty=None):
        """Play one finite tone, then stop PWM output."""
        if frequency <= 0:
            raise ValueError("frequency must be greater than 0")
        if duration_ms < 0:
            raise ValueError("duration_ms must be 0 or greater")

        try:
            self.pwm.freq(frequency)
            self._set_duty(duty)
            sleep_ms(duration_ms)
        finally:
            self.off()

    def off(self):
        """Silence the buzzer without releasing the PWM object."""
        if hasattr(self.pwm, "duty_u16"):
            self.pwm.duty_u16(0)
        else:
            self.pwm.duty(0)

    def deinit(self):
        """Safely stop and release PWM resources."""
        try:
            self.off()
        finally:
            if hasattr(self.pwm, "deinit"):
                self.pwm.deinit()
