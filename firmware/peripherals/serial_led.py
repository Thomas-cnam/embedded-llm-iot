"""Serial LED strip helper for the ESP32-C6 custom PCB."""

from machine import Pin
import neopixel


class SerialLedStrip:
    """Control the three onboard serial LEDs connected to GPIO 8 by default."""

    def __init__(self, pin=8, count=3):
        if count <= 0:
            raise ValueError("count must be greater than 0")
        self.pin = pin
        self.count = count
        self.pixels = neopixel.NeoPixel(Pin(pin, Pin.OUT), count)
        self.off()

    def set_all(self, color):
        """Set all LEDs to an RGB tuple, then write the update."""
        if len(color) != 3:
            raise ValueError("color must be an RGB tuple")
        for index in range(self.count):
            self.pixels[index] = color
        self.pixels.write()

    def red(self):
        self.set_all((255, 0, 0))

    def green(self):
        self.set_all((0, 255, 0))

    def blue(self):
        self.set_all((0, 0, 255))

    def white(self):
        self.set_all((255, 255, 255))

    def off(self):
        self.set_all((0, 0, 0))
