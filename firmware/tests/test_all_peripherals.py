"""Finite, self-contained ESP32-C6 peripheral smoke test.

Run this script manually in Thonny. It tests the confirmed Week 1 hardware
without writing files to the board or requiring local project modules.
"""

from machine import ADC, Pin, PWM
from time import sleep

try:
    import neopixel
except ImportError:
    print("ERROR: neopixel is unavailable in this MicroPython firmware.")
    raise


PHOTORESISTOR_PIN = 3
BUZZER_PIN = 5
RGB_RED_PIN = 10
RGB_GREEN_PIN = 11
RGB_BLUE_PIN = 21
RGB_ACTIVE_LOW = False
SERIAL_LED_PIN = 8
SERIAL_LED_COUNT = 3

PHOTORESISTOR_READ_COUNT = 5
PHOTORESISTOR_DELAY_SECONDS = 0.2
TONE_DURATION_SECONDS = 0.25
TONE_SILENCE_SECONDS = 0.15
LED_DURATION_SECONDS = 0.75
TONES_HZ = (440, 660, 880)


def set_pwm_duty(pwm, duty_u16_value, duty_value):
    if hasattr(pwm, "duty_u16"):
        pwm.duty_u16(duty_u16_value)
    else:
        pwm.duty(duty_value)


def read_adc(adc):
    if hasattr(adc, "read_u16"):
        return adc.read_u16()
    return adc.read()


def rgb_output_value(is_on):
    if RGB_ACTIVE_LOW:
        return 0 if is_on else 1
    return 1 if is_on else 0


def set_rgb(red, green, blue, red_on, green_on, blue_on):
    red.value(rgb_output_value(red_on))
    green.value(rgb_output_value(green_on))
    blue.value(rgb_output_value(blue_on))


def set_serial_leds(pixels, color):
    for index in range(SERIAL_LED_COUNT):
        pixels[index] = color
    pixels.write()


def main():
    buzzer = None
    red = Pin(RGB_RED_PIN, Pin.OUT)
    green = Pin(RGB_GREEN_PIN, Pin.OUT)
    blue = Pin(RGB_BLUE_PIN, Pin.OUT)
    pixels = neopixel.NeoPixel(
        Pin(SERIAL_LED_PIN, Pin.OUT), SERIAL_LED_COUNT
    )

    print("ESP32-C6 combined peripheral smoke test")
    print("Photoresistor: GPIO", PHOTORESISTOR_PIN)
    print("Buzzer: GPIO", BUZZER_PIN)
    print("RGB LED: GPIO", RGB_RED_PIN, RGB_GREEN_PIN, RGB_BLUE_PIN)
    print("RGB ACTIVE_LOW =", RGB_ACTIVE_LOW)
    print("Serial LEDs: GPIO", SERIAL_LED_PIN, "count", SERIAL_LED_COUNT)

    try:
        set_rgb(red, green, blue, False, False, False)
        set_serial_leds(pixels, (0, 0, 0))

        print("\n1. Reading photoresistor ADC values...")
        adc = ADC(Pin(PHOTORESISTOR_PIN))
        try:
            adc.atten(ADC.ATTN_11DB)
            print("ADC attenuation configured to ATTN_11DB.")
        except Exception:
            print("ADC attenuation configuration unavailable; continuing.")

        for index in range(PHOTORESISTOR_READ_COUNT):
            print("Photoresistor reading", index + 1, ":", read_adc(adc))
            sleep(PHOTORESISTOR_DELAY_SECONDS)

        print("Waiting briefly before the buzzer test...")
        sleep(0.5)

        print("\n2. Testing passive buzzer...")
        buzzer = PWM(Pin(BUZZER_PIN))
        for frequency in TONES_HZ:
            print("Playing tone:", frequency, "Hz")
            buzzer.freq(frequency)
            set_pwm_duty(buzzer, 32768, 512)
            sleep(TONE_DURATION_SECONDS)
            set_pwm_duty(buzzer, 0, 0)
            sleep(TONE_SILENCE_SECONDS)
        print("Buzzer test finished.")

        print("\n3. Testing RGB LED...")
        rgb_colors = (
            ("red", True, False, False),
            ("green", False, True, False),
            ("blue", False, False, True),
            ("white", True, True, True),
        )
        for name, red_on, green_on, blue_on in rgb_colors:
            print("RGB LED:", name)
            set_rgb(red, green, blue, red_on, green_on, blue_on)
            sleep(LED_DURATION_SECONDS)
        set_rgb(red, green, blue, False, False, False)
        print("RGB LED: off")

        print("\n4. Testing serial LEDs...")
        serial_colors = (
            ("red", (255, 0, 0)),
            ("green", (0, 255, 0)),
            ("blue", (0, 0, 255)),
            ("white", (255, 255, 255)),
        )
        for name, color in serial_colors:
            print("Serial LEDs:", name)
            set_serial_leds(pixels, color)
            sleep(LED_DURATION_SECONDS)
        set_serial_leds(pixels, (0, 0, 0))
        print("Serial LEDs: off")

        print("\nCombined peripheral smoke test completed.")
    finally:
        if buzzer is not None:
            try:
                set_pwm_duty(buzzer, 0, 0)
            finally:
                if hasattr(buzzer, "deinit"):
                    buzzer.deinit()
        set_rgb(red, green, blue, False, False, False)
        set_serial_leds(pixels, (0, 0, 0))
        print("Safety cleanup complete: all outputs are off.")


main()
