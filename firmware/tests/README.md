# Firmware Test Scripts

This folder contains finite MicroPython diagnostics for the confirmed ESP32-C6 peripherals.

The individual scripts remain the verified reference for testing one peripheral at a time.

Each script should be tested manually on the ESP32-C6 board, and the result should be recorded in `LOG.md`.

## Combined smoke test

Open `test_all_peripherals.py` directly in Thonny and run it manually on the
ESP32-C6. The script is self-contained and does not require the reusable
modules from `firmware/peripherals/` to be uploaded to the board.

The finite sequence reads five photoresistor values, plays three short buzzer
tones, and tests the RGB LED and three serial LEDs in red, green, blue, white,
and off states. It always attempts to stop PWM and turn all LEDs off before
exiting.

The combined smoke test has been prepared but has not yet been executed. Record
the manual observations in `LOG.md` after running it in Thonny.
