# Week 2 Peripheral Test Script Audit

This audit reviews the existing Week 1 peripheral test scripts as preparation for Week 2 hardware consolidation. Codex did not run any hardware scripts during this audit.

## Summary

The existing scripts are ready for continued use as manual peripheral tests. They already use the confirmed PCB pin mappings and finite execution patterns. The main Week 2 improvement opportunity is to extract reusable helper modules after preserving the known-working behavior.

## `firmware/tests/test_photoresistor.py`

- Confirmed GPIO pins: GPIO 3, PCB label `PHOTO(3)`.
- Execution is finite: Yes. The script collects a fixed number of exposed and covered readings.
- Cleanup is implemented: Not applicable. The script only reads ADC and does not drive outputs.
- TODO values remain: No.
- Third-party dependencies are used: No. It uses MicroPython `machine.ADC`, `machine.Pin`, and `time.sleep`.
- Potential improvements: Extract ADC setup, averaging, and reading collection into a reusable photoresistor module; add a baseline collection mode for Week 2 measurements.
- Ready for continued use: Yes.

## `firmware/tests/test_buzzer.py`

- Confirmed GPIO pins: GPIO 5, PCB label `BUZZER(5)`.
- Execution is finite: Yes. The script plays three short tones and stops.
- Cleanup is implemented: Yes. Duty is set to 0 and `deinit()` is called when available, including through `finally`.
- TODO values remain: No.
- Third-party dependencies are used: No. It uses MicroPython `machine.PWM`, `machine.Pin`, and `time.sleep`.
- Potential improvements: Move buzzer tone playback and PWM cleanup into a reusable buzzer helper module; centralize tone duration and duty configuration.
- Ready for continued use: Yes.

## `firmware/tests/test_rgb_led.py`

- Confirmed GPIO pins: GPIO 10 for red, GPIO 11 for green, GPIO 21 for blue; PCB labels `R(10)`, `G(11)`, and `B(21)`.
- Execution is finite: Yes. The script shows red, green, blue, white, then turns the LED off.
- Cleanup is implemented: Yes. The `finally` block turns the RGB LED off.
- TODO values remain: No.
- Third-party dependencies are used: No. It uses MicroPython `machine.Pin` and `time.sleep`.
- Potential improvements: Extract active-low handling and color setting into a reusable RGB LED module; define named color constants for future smoke tests.
- Ready for continued use: Yes.

## `firmware/tests/test_serial_led_strip.py`

- Confirmed GPIO pins: GPIO 8, PCB label `SERIAL_LED(8)`; `LED_COUNT = 3`.
- Execution is finite: Yes. The script shows red, green, blue, white, then turns the LEDs off.
- Cleanup is implemented: Yes. The `finally` block sets all serial LEDs to off.
- TODO values remain: No.
- Third-party dependencies are used: It uses the MicroPython `neopixel` module. This is firmware-provided on many MicroPython builds, not a repository dependency.
- Potential improvements: Extract serial LED initialization and color fill into a reusable module; keep the `neopixel` availability check; define a shared color sequence for the future combined smoke test.
- Ready for continued use: Yes, assuming the MicroPython firmware includes `neopixel` as already verified during manual testing.

## Week 2 Recommendations

- Preserve the existing working test scripts as reference examples.
- Create small reusable modules for photoresistor, buzzer, RGB LED, and serial LEDs.
- Build a combined hardware smoke test only after the reusable modules are created.
- Keep anomaly detection, gateway communication, local LLM setup, whitelist parsing, and benchmarking out of scope for Week 2 hardware consolidation.