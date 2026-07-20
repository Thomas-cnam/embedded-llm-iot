"""Finite MicroPython GPIO diagnostic for the ESP32-C6 RGB LED.

Supervisor-confirmed pins: red GPIO 21, green GPIO 11, blue GPIO 10.
Confirmed behavior: ACTIVE_LOW = False.
"""

from machine import Pin
from time import sleep


PIN_RED = 21
PIN_GREEN = 11
PIN_BLUE = 10
ACTIVE_LOW = False
COLOR_DURATION_SECONDS = 1.5


red = Pin(PIN_RED, Pin.OUT)
green = Pin(PIN_GREEN, Pin.OUT)
blue = Pin(PIN_BLUE, Pin.OUT)


def output_value(is_on):
    if ACTIVE_LOW:
        return 0 if is_on else 1
    return 1 if is_on else 0


def set_rgb(red_on, green_on, blue_on):
    red.value(output_value(red_on))
    green.value(output_value(green_on))
    blue.value(output_value(blue_on))


def show_color(name, red_on, green_on, blue_on):
    print("Testing color:", name)
    set_rgb(red_on, green_on, blue_on)
    sleep(COLOR_DURATION_SECONDS)


def main():
    print("ESP32-C6 RGB LED test")
    print("Using supervisor-confirmed mapping: red 21, green 11, blue 10")
    print("PCB red and blue silkscreen labels are swapped.")
    print("ACTIVE_LOW =", ACTIVE_LOW)

    try:
        print("Turning RGB LED off before test...")
        set_rgb(False, False, False)
        sleep(1)

        show_color("red", True, False, False)
        show_color("green", False, True, False)
        show_color("blue", False, False, True)
        show_color("white", True, True, True)
    finally:
        print("Turning RGB LED off.")
        set_rgb(False, False, False)
        print("RGB LED test finished.")


main()
