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

The combined smoke test was run manually in Thonny on 2026-07-13. The run
remains valid for the photoresistor, buzzer, serial LEDs, finite sequence, and
cleanup. A later supervisor correction established that the PCB red and blue
silkscreen labels are swapped, so the corrected RGB mapping must be tested
again: red GPIO 21, green GPIO 11, blue GPIO 10.

For the short repeat, open `test_rgb_led.py` in Thonny and run it manually.
Verify red, green, blue, white, and off in order. Do not save it as `main.py`.

## Week 3 anomaly hardware integration test

`test_anomaly_hardware_integration.py` is a finite guided test for the real
photoresistor, anomaly detector, alert policy, RGB LED, and buzzer integration.
It requires the existing `/anomaly` and `/peripherals` packages to be uploaded
to the device root before the script is opened and run manually in Thonny.

The script covers ambient, covered, recovery, flashlight, and final recovery
phases. Diagnostic lines begin with `DIAG`. A requested anomaly alert is
printed as one compact JSON object on its own line; normal, recovery, and
cooldown-suppressed readings produce no JSON event. The script never writes
files on the board and always attempts to turn the RGB LED and buzzer off. Do
not save it as `main.py`.

The test was run manually in Thonny on 2026-07-17. Real GPIO 3 acquisition,
normal and anomalous states, bounded buzzer tones, cooldown, recovery,
continued acquisition, and final cleanup were confirmed. Historical RGB
observations used the old red/blue interpretation and require a corrected
physical repeat. Detailed results are recorded in
`docs/week3_hardware_integration_test.md`.

The JSON-enabled update was prepared on 2026-07-19 but has not yet been run on
the ESP32-C6. Its manual procedure and evidence-capture rules are documented in
`docs/week3_serial_event_test.md`. The earlier physical results must not be
presented as JSON-output validation.
