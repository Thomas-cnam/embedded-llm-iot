"""
MicroPython photoresistor ADC test for the ESP32-C6 custom PCB.

Pin source: PCB silkscreen label PHOTO(3).
This script reads only GPIO 3 through ADC and does not drive any output pins.
"""

from machine import ADC, Pin
from time import sleep


PHOTORESISTOR_PIN = 3
READ_COUNT = 10
READ_DELAY_SECONDS = 0.5
SETUP_DELAY_SECONDS = 5
COVER_DELAY_SECONDS = 10


adc = ADC(Pin(PHOTORESISTOR_PIN))

try:
    adc.atten(ADC.ATTN_11DB)
    print("ADC attenuation configured to ATTN_11DB.")
except Exception:
    print("ADC attenuation configuration not supported on this firmware; continuing.")


def read_adc_value():
    if hasattr(adc, "read_u16"):
        return adc.read_u16()
    return adc.read()


def collect_readings(label):
    readings = []
    print("Collecting", READ_COUNT, label, "readings...")
    for index in range(READ_COUNT):
        value = read_adc_value()
        readings.append(value)
        print(label, "reading", index + 1, ":", value)
        sleep(READ_DELAY_SECONDS)
    return readings


def average(values):
    return sum(values) / len(values)


print("ESP32-C6 photoresistor ADC test")
print("Using GPIO", PHOTORESISTOR_PIN, "from PCB label PHOTO(3).")
print("Leave the photoresistor exposed to normal room light.")
print("Starting exposed readings in", SETUP_DELAY_SECONDS, "seconds...")
sleep(SETUP_DELAY_SECONDS)

exposed_readings = collect_readings("exposed")

print("Now cover the photoresistor with a finger or an object.")
print("Covered readings will start in", COVER_DELAY_SECONDS, "seconds...")
sleep(COVER_DELAY_SECONDS)

covered_readings = collect_readings("covered")

exposed_average = average(exposed_readings)
covered_average = average(covered_readings)
difference = abs(exposed_average - covered_average)

print("Photoresistor test summary")
print("Exposed readings:", exposed_readings)
print("Covered readings:", covered_readings)
print("Average exposed reading:", exposed_average)
print("Average covered reading:", covered_average)
print("Absolute difference:", difference)
print("A clear difference indicates that the photoresistor responds to light changes.")
