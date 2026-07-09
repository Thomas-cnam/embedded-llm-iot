"""
MicroPython passive buzzer PWM test for the ESP32-C6 custom PCB.

Pin source: PCB silkscreen label BUZZER(5).
This script is finite and intended for manual execution in Thonny.
"""

from machine import Pin, PWM
from time import sleep


BUZZER_PIN = 5
DUTY_U16_VALUE = 32768
DUTY_VALUE = 512
TONE_DURATION_SECONDS = 0.3
SILENCE_SECONDS = 0.2
TONES_HZ = (440, 660, 880)


buzzer = PWM(Pin(BUZZER_PIN))


def set_duty(value_u16, value_legacy):
    if hasattr(buzzer, "duty_u16"):
        buzzer.duty_u16(value_u16)
    else:
        buzzer.duty(value_legacy)


def stop_pwm():
    try:
        set_duty(0, 0)
    finally:
        if hasattr(buzzer, "deinit"):
            buzzer.deinit()


print("ESP32-C6 passive buzzer PWM test")
print("Using GPIO", BUZZER_PIN, "from PCB label BUZZER(5).")
print("This test plays three short tones and then stops PWM.")

try:
    for frequency in TONES_HZ:
        print("Playing tone:", frequency, "Hz")
        buzzer.freq(frequency)
        set_duty(DUTY_U16_VALUE, DUTY_VALUE)
        sleep(TONE_DURATION_SECONDS)
        set_duty(0, 0)
        sleep(SILENCE_SECONDS)
finally:
    stop_pwm()
    print("Buzzer PWM stopped.")
