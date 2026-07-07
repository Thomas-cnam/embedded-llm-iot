"""
Basic MicroPython photoresistor ADC test template.

TODO: Replace TODO_PIN with the confirmed ADC-capable GPIO pin from the
official board documentation before running this script on hardware.
"""

from machine import ADC, Pin
from time import sleep


TODO_PIN = None


if TODO_PIN is None:
    raise ValueError("Set TODO_PIN to the confirmed photoresistor ADC pin.")


adc = ADC(Pin(TODO_PIN))

# TODO: Configure attenuation or width if required by the ESP32-C6 MicroPython port.

while True:
    value = adc.read()
    print("Photoresistor ADC value:", value)
    sleep(1)

