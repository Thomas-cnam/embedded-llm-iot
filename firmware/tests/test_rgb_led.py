"""
Basic MicroPython RGB LED test template.

TODO: Replace TODO_PIN_RED, TODO_PIN_GREEN, and TODO_PIN_BLUE with the
confirmed GPIO pins from the official board documentation before running this
script on hardware.
"""

from machine import Pin
from time import sleep


TODO_PIN_RED = None
TODO_PIN_GREEN = None
TODO_PIN_BLUE = None


if None in (TODO_PIN_RED, TODO_PIN_GREEN, TODO_PIN_BLUE):
    raise ValueError("Set all RGB LED TODO pins to confirmed GPIO pins.")


red = Pin(TODO_PIN_RED, Pin.OUT)
green = Pin(TODO_PIN_GREEN, Pin.OUT)
blue = Pin(TODO_PIN_BLUE, Pin.OUT)


def set_rgb(r, g, b):
    red.value(r)
    green.value(g)
    blue.value(b)


colors = [
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
]

while True:
    for color in colors:
        set_rgb(*color)
        sleep(1)

