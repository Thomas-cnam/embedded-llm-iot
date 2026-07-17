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

The combined smoke test was run manually in Thonny on 2026-07-13. All tested
peripherals completed their sequence successfully, all expected visual and
audible outputs were observed, and the safety cleanup turned all outputs off.

## Week 3 anomaly hardware integration test

`test_anomaly_hardware_integration.py` is a finite guided test for the real
photoresistor, anomaly detector, alert policy, RGB LED, and buzzer integration.
It requires the existing `/anomaly` and `/peripherals` packages to be uploaded
to the device root before the script is opened and run manually in Thonny.

The script covers ambient, covered, recovery, flashlight, and final recovery
phases. It prints human-readable diagnostics only, never writes files on the
board, and always attempts to turn the RGB LED and buzzer off. Do not save it as
`main.py`. Preparation and expected observations are documented in
`docs/week3_hardware_integration_test.md`.

The test was run manually in Thonny on 2026-07-17. Real GPIO 3 acquisition,
normal and anomalous states, RGB LED behavior, bounded buzzer tones, cooldown,
recovery, continued acquisition, and final cleanup were confirmed. Detailed
results are recorded in `docs/week3_hardware_integration_test.md`.
