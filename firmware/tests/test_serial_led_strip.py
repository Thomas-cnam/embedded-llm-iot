"""
Basic MicroPython serial LED strip test template.

TODO: Replace TODO_PIN and TODO_LED_COUNT with values confirmed from the
official board documentation before running this script on hardware.
"""

from machine import Pin
from time import sleep
import neopixel


TODO_PIN = None
TODO_LED_COUNT = None


if TODO_PIN is None or TODO_LED_COUNT is None:
    raise ValueError("Set TODO_PIN and TODO_LED_COUNT before running this test.")


strip = neopixel.NeoPixel(Pin(TODO_PIN), TODO_LED_COUNT)

colors = [
    (32, 0, 0),
    (0, 32, 0),
    (0, 0, 32),
    (0, 0, 0),
]

while True:
    for color in colors:
        for index in range(TODO_LED_COUNT):
            strip[index] = color
        strip.write()
        sleep(1)

