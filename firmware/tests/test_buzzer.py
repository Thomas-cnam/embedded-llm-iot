"""Finite MicroPython PWM diagnostic for the ESP32-C6 passive buzzer.

Confirmed pin: GPIO 5 from PCB label BUZZER(5).
The script plays three short tones and always stops PWM before exiting.
"""

from machine import Pin, PWM
from time import sleep


BUZZER_PIN = 5
DUTY_U16_VALUE = 32768
DUTY_VALUE = 512
TONE_DURATION_SECONDS = 0.3
SILENCE_SECONDS = 0.2
TONES_HZ = (440, 660, 880)


def set_duty(pwm, value_u16, value_legacy):
    if hasattr(pwm, "duty_u16"):
        pwm.duty_u16(value_u16)
    else:
        pwm.duty(value_legacy)


def stop_pwm(pwm):
    try:
        set_duty(pwm, 0, 0)
    finally:
        if hasattr(pwm, "deinit"):
            pwm.deinit()


def main():
    buzzer = PWM(Pin(BUZZER_PIN))

    print("ESP32-C6 passive buzzer PWM test")
    print("Using GPIO", BUZZER_PIN, "from PCB label BUZZER(5).")
    print("This test plays three short tones and then stops PWM.")

    try:
        for frequency in TONES_HZ:
            print("Playing tone:", frequency, "Hz")
            buzzer.freq(frequency)
            set_duty(buzzer, DUTY_U16_VALUE, DUTY_VALUE)
            sleep(TONE_DURATION_SECONDS)
            set_duty(buzzer, 0, 0)
            sleep(SILENCE_SECONDS)
    finally:
        stop_pwm(buzzer)
        print("Buzzer PWM stopped.")


main()