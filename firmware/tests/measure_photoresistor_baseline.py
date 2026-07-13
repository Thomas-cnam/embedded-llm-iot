"""Collect repeatable ESP32-C6 photoresistor baseline measurements.

Run this finite script manually in Thonny. Measurements remain in memory and
are printed as CSV-compatible lines for manual transfer after the experiment.
"""

from machine import ADC, Pin
from time import sleep


PHOTORESISTOR_PIN = 3
READING_COUNT = 30
SETUP_DELAY_SECONDS = 5
READING_DELAY_SECONDS = 0.2


def configure_adc():
    adc = ADC(Pin(PHOTORESISTOR_PIN))
    try:
        adc.atten(ADC.ATTN_11DB)
        print("ADC attenuation configured to ATTN_11DB.")
    except Exception:
        print("ADC attenuation configuration unavailable; continuing.")
    return adc


def read_adc(adc):
    if hasattr(adc, "read_u16"):
        return adc.read_u16()
    return adc.read()


def average(values):
    return sum(values) / len(values)


def collect_condition(adc, condition, instruction):
    print("\nCondition:", condition)
    print(instruction)
    print("Keep the setup steady during all readings.")
    print("Measurements start in", SETUP_DELAY_SECONDS, "seconds...")
    sleep(SETUP_DELAY_SECONDS)

    values = []
    print("condition,index,value")
    for index in range(1, READING_COUNT + 1):
        value = read_adc(adc)
        values.append(value)
        print("{},{},{}".format(condition, index, value))
        sleep(READING_DELAY_SECONDS)

    condition_average = average(values)
    print("Summary for", condition)
    print("Minimum:", min(values))
    print("Maximum:", max(values))
    print("Average:", condition_average)
    return values, condition_average


def main():
    print("ESP32-C6 photoresistor baseline measurement")
    print("Using GPIO", PHOTORESISTOR_PIN, "from PCB label PHOTO(3).")
    print("Each condition collects", READING_COUNT, "readings.")
    print("No values are written to the ESP32 filesystem.")

    adc = configure_adc()

    covered_values, covered_average = collect_condition(
        adc,
        "covered",
        "Cover the photoresistor completely with an opaque object.",
    )
    ambient_values, ambient_average = collect_condition(
        adc,
        "ambient_room_light",
        "Uncover the sensor and leave it exposed to normal room light.",
    )
    flashlight_values, flashlight_average = collect_condition(
        adc,
        "phone_flashlight",
        "Direct a phone flashlight steadily at the photoresistor.",
    )

    print("\nBaseline measurement summary")
    print("Covered average:", covered_average)
    print("Ambient room light average:", ambient_average)
    print("Phone flashlight average:", flashlight_average)
    print(
        "Absolute difference covered/ambient:",
        abs(covered_average - ambient_average),
    )
    print(
        "Absolute difference covered/phone_flashlight:",
        abs(covered_average - flashlight_average),
    )
    print(
        "Absolute difference ambient/phone_flashlight:",
        abs(ambient_average - flashlight_average),
    )
    print("Baseline measurement sequence completed.")

    # Keep references explicit until the final summary has been printed.
    _ = covered_values, ambient_values, flashlight_values


main()
