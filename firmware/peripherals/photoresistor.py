"""Photoresistor ADC helper for the ESP32-C6 custom PCB."""

from machine import ADC, Pin
from time import sleep_ms


class Photoresistor:
    """Read the photoresistor connected to GPIO 3 by default."""

    def __init__(self, pin=3):
        self.pin = pin
        self.adc = ADC(Pin(pin))
        try:
            self.adc.atten(ADC.ATTN_11DB)
        except Exception:
            pass

    def read(self):
        """Return one ADC sample, preferring 16-bit reads when available."""
        if hasattr(self.adc, "read_u16"):
            return self.adc.read_u16()
        return self.adc.read()

    def read_average(self, sample_count=10, delay_ms=20):
        """Return the average of a finite number of ADC samples."""
        if sample_count <= 0:
            raise ValueError("sample_count must be greater than 0")
        if delay_ms < 0:
            raise ValueError("delay_ms must be 0 or greater")

        total = 0
        for _ in range(sample_count):
            total += self.read()
            if delay_ms:
                sleep_ms(delay_ms)
        return total / sample_count
