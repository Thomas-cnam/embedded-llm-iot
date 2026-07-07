"""
Basic MicroPython buzzer PWM test template.

TODO: Replace TODO_PIN with the confirmed buzzer GPIO pin from the
official board documentation before running this script on hardware.
"""

from machine import Pin, PWM
from time import sleep


TODO_PIN = None


if TODO_PIN is None:
    raise ValueError("Set TODO_PIN to the confirmed buzzer pin.")


buzzer = PWM(Pin(TODO_PIN))

try:
    buzzer.freq(1000)
    buzzer.duty_u16(32768)
    sleep(1)
    buzzer.duty_u16(0)
finally:
    buzzer.deinit()

