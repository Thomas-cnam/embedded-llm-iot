# Week 2 Peripheral Test Script Audit

This audit reviews the existing Week 1 peripheral test scripts as preparation for Week 2 hardware consolidation. Codex did not run any hardware scripts during this audit.

## Summary

The peripheral test scripts have now been cleaned and standardized while preserving the confirmed GPIO mappings and known-working behavior. They remain finite manual diagnostics and do not implement anomaly detection, gateway communication, or local LLM integration.

## `firmware/tests/test_photoresistor.py`

- Confirmed GPIO pins: GPIO 3, PCB label `PHOTO(3)`.
- Execution is finite: Yes. The script collects a fixed number of exposed and covered readings.
- Cleanup is implemented: Not applicable. The script only reads ADC and does not drive outputs.
- TODO values remain: No.
- Third-party dependencies are used: No. It uses MicroPython `machine.ADC`, `machine.Pin`, and `time.sleep`.
- Cleaned status: Standardized module docstring, `main()` entry point, ADC configuration helper, and explicit summary output.
- Potential improvements: Add a separate baseline collection mode for Week 2 measurements.
- Ready for continued use: Yes.

## `firmware/tests/test_buzzer.py`

- Confirmed GPIO pins: GPIO 5, PCB label `BUZZER(5)`.
- Execution is finite: Yes. The script plays three short tones and stops.
- Cleanup is implemented: Yes. Duty is set to 0 and `deinit()` is called when available through `finally`.
- TODO values remain: No.
- Third-party dependencies are used: No. It uses MicroPython `machine.PWM`, `machine.Pin`, and `time.sleep`.
- Cleaned status: Standardized module docstring, `main()` entry point, explicit PWM helper functions, and guaranteed PWM cleanup.
- Potential improvements: Move tone playback into a reusable buzzer module during the reusable-module step.
- Ready for continued use: Yes.

## `firmware/tests/test_rgb_led.py`

- Confirmed GPIO pins: GPIO 21 for red, GPIO 11 for green, GPIO 10 for blue. The supervisor confirmed that the PCB red and blue silkscreen labels are swapped.
- Execution is finite: Yes. The script shows red, green, blue, white, then turns the LED off.
- Cleanup is implemented: Yes. The `finally` block turns the RGB LED off.
- TODO values remain: No.
- Third-party dependencies are used: No. It uses MicroPython `machine.Pin` and `time.sleep`.
- Cleaned status: Standardized module docstring, confirmed `ACTIVE_LOW = False`, shared color duration constant, and `main()` entry point.
- Potential improvements: Extract active-low handling and color setting into a reusable RGB LED module.
- Ready for continued use: Yes for manual revalidation with the corrected mapping; the corrected red and blue channels have not yet been physically revalidated.

## `firmware/tests/test_serial_led_strip.py`

- Confirmed GPIO pins: GPIO 8, PCB label `SERIAL_LED(8)`; `LED_COUNT = 3`.
- Execution is finite: Yes. The script shows red, green, blue, white, then turns the LEDs off.
- Cleanup is implemented: Yes. The `finally` block sets all serial LEDs to off.
- TODO values remain: No.
- Third-party dependencies are used: It uses the MicroPython firmware-provided `neopixel` module. No repository dependency was added.
- Cleaned status: Standardized module docstring, confirmed pin/count constants, explicit color duration constant, `main()` entry point, and retained `neopixel` availability check.
- Potential improvements: Extract serial LED initialization and color fill into a reusable serial LED module.
- Ready for continued use: Yes.

## Week 2 Recommendations

- Preserve the cleaned scripts as reference manual diagnostics.
- Create small reusable modules for photoresistor, buzzer, RGB LED, and serial LEDs next.
- Build a combined hardware smoke test only after the reusable modules are created.
- Keep anomaly detection, gateway communication, local LLM setup, whitelist parsing, and benchmarking out of scope for Week 2 hardware consolidation.
