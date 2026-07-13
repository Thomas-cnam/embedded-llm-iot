"""Finite MicroPython ADC diagnostic for the ESP32-C6 photoresistor.

Confirmed pin: GPIO 3 from PCB label PHOTO(3).
The script reads ADC values only and does not drive output pins.
"""

from machine import ADC, Pin
from time import sleep


PHOTORESISTOR_PIN = 3
READ_COUNT = 10
READ_DELAY_SECONDS = 0.5
SETUP_DELAY_SECONDS = 5
COVER_DELAY_SECONDS = 10


def configure_adc(pin_number):
    adc = ADC(Pin(pin_number))
    try:
        adc.atten(ADC.ATTN_11DB)
        print("ADC attenuation configured to ATTN_11DB.")
    except Exception:
        print("ADC attenuation configuration not supported; continuing.")
    return adc


def read_adc_value(adc):
    if hasattr(adc, "read_u16"):
        return adc.read_u16()
    return adc.read()


def collect_readings(adc, label):
    readings = []
    print("Collecting", READ_COUNT, label, "readings...")
    for index in range(READ_COUNT):
        value = read_adc_value(adc)
        readings.append(value)
        print(label, "reading", index + 1, ":", value)
        sleep(READ_DELAY_SECONDS)
    return readings


def average(values):
    return sum(values) / len(values)


def main():
    adc = configure_adc(PHOTORESISTOR_PIN)

    print("ESP32-C6 photoresistor ADC test")
    print("Using GPIO", PHOTORESISTOR_PIN, "from PCB label PHOTO(3).")
    print("Leave the photoresistor exposed to normal room light.")
    print("Starting exposed readings in", SETUP_DELAY_SECONDS, "seconds...")
    sleep(SETUP_DELAY_SECONDS)

    exposed_readings = collect_readings(adc, "exposed")

    print("Now cover the photoresistor with a finger or an object.")
    print("Covered readings will start in", COVER_DELAY_SECONDS, "seconds...")
    sleep(COVER_DELAY_SECONDS)

    covered_readings = collect_readings(adc, "covered")

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


main()