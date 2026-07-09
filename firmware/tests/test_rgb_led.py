"""
ESP32-C6 RGB LED test.

PCB labels:
- Red   = R(10)
- Green = G(11)
- Blue  = B(21)

This test is finite:
- red
- green
- blue
- white
- off

If the LED behaves inverted, change ACTIVE_LOW to True.
"""

from machine import Pin
from time import sleep


PIN_RED = 10
PIN_GREEN = 11
PIN_BLUE = 21

# Start with False.
# If the LED stays on when it should be off, or colors behave inverted,
# set this to True and run the test again.
ACTIVE_LOW = False


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


def show_color(name, red_on, green_on, blue_on, duration=1.5):
    print("Testing color:", name)
    set_rgb(red_on, green_on, blue_on)
    sleep(duration)


print("ESP32-C6 RGB LED test")
print("Using PCB labels: R(10), G(11), B(21)")
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
