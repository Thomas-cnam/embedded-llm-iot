"""Finite MicroPython NeoPixel diagnostic for the ESP32-C6 serial LEDs.

Confirmed pin: GPIO 8 from PCB label SERIAL_LED(8).
Confirmed count: 3 onboard serial LEDs.
"""

from machine import Pin
from time import sleep

try:
    import neopixel
except ImportError:
    print("ERROR: neopixel module is not available in this MicroPython firmware.")
    raise


PIN_SERIAL_LED = 8
LED_COUNT = 3
COLOR_DURATION_SECONDS = 1.5


pixels = neopixel.NeoPixel(Pin(PIN_SERIAL_LED, Pin.OUT), LED_COUNT)


def set_all(color):
    for index in range(LED_COUNT):
        pixels[index] = color
    pixels.write()


def show_color(name, color):
    print("Testing serial LEDs:", name)
    set_all(color)
    sleep(COLOR_DURATION_SECONDS)


def main():
    print("ESP32-C6 serial LED strip test")
    print("Using GPIO", PIN_SERIAL_LED, "from PCB label SERIAL_LED(8).")
    print("LED_COUNT =", LED_COUNT)

    try:
        show_color("red", (255, 0, 0))
        show_color("green", (0, 255, 0))
        show_color("blue", (0, 0, 255))
        show_color("white", (255, 255, 255))
    finally:
        print("Turning serial LEDs off.")
        set_all((0, 0, 0))
        print("Serial LED test finished.")


main()