# Week 3 Hardware Integration Test

## Purpose

`firmware/tests/test_anomaly_hardware_integration.py` is a finite, guided
MicroPython test that connects the real photoresistor to the existing detector,
alert policy, integration controller, RGB LED, and buzzer modules.

The script was run manually on the ESP32-C6 in Thonny on 2026-07-17. The
operator confirmed the expected physical RGB LED states and buzzer tones.

## Confirmed Hardware

| Component | Configuration |
|---|---|
| Photoresistor | GPIO 3 |
| Passive buzzer | GPIO 5 |
| RGB red channel | GPIO 10 |
| RGB green channel | GPIO 11 |
| RGB blue channel | GPIO 21 |
| RGB polarity | `active_low=False` |

The serial LED strip is intentionally not used.

## Files Required on the Device

Upload these existing package directories to the ESP32-C6 device root:

- `/anomaly`
- `/peripherals`

Then open `firmware/tests/test_anomaly_hardware_integration.py` in Thonny and
run it manually. Do not rename it to `main.py`.

## Guided Sequence

The script guides the operator through these phases:

1. Ambient room light
2. Fully covered sensor
3. Ambient-light recovery
4. Phone flashlight
5. Final ambient-light recovery

Each phase starts with a five-second setup countdown and collects 12 readings
at a provisional 500 ms interval. This duration allows the provisional
five-second alert cooldown to be observed without creating an infinite test.

For every reading, the console prints the ADC value, detector state, policy
decision, and local-alarm action as human-readable text. It does not generate
or print structured JSON events.

## Expected Provisional Behavior

- Ambient light should show the normal green state with the buzzer off.
- Covering the sensor should normally produce a red low-light alert and a short
  440 Hz tone.
- Returning to ambient light should restore the normal green state.
- A strong flashlight should normally produce a blue high-light alert and a
  short 880 Hz tone.
- Final recovery should restore green and silence the buzzer.
- Repeated readings of the same anomaly should be suppressed during cooldown.

These provisional behaviors were checked during the manual test described
below.

## Manual Test Results

Test date: 2026-07-17

| Phase | ADC observations | Detector and policy result | Physical observation |
|---|---|---|---|
| Ambient | 24005 to 24053 | Normal; normal state initialized once | Green RGB LED; buzzer off |
| Covered | 1440 to 12098 | Initial sudden drop, then low light from sample 7 | Expected red alerts and short tones observed |
| Ambient recovery | 23957 to 24053 | Sudden rise handled as recovery, then normal | Green RGB LED restored; buzzer off |
| Phone flashlight | 38713 to 39417 | High light on all samples | Blue RGB LED and expected 880 Hz tones observed |
| Final recovery | 23669 to 24117 | Sudden drop handled as recovery, then normal | Green RGB LED restored; buzzer off |

The covered phase included intermediate readings while the sensor was being
covered. It first produced a `sudden_drop` alert at 6705, briefly returned to a
normal classification, and entered stable `low_light` at 4129 and below. This
reflects the real manual transition and is not recorded as a script failure.

During the flashlight phase, repeated `high_light` readings were suppressed
during cooldown. A bounded repeat alert occurred at sample 11 after the
provisional five-second cooldown. Acquisition continued after every tone.

Both ambient-recovery phases restored the normal state. The sequence completed
without an exception, and the final safety cleanup turned the RGB LED and
buzzer off. The operator confirmed that the displayed LED colors and audible
tones matched the planned mappings.

## Timestamp Handling

MicroPython `ticks_ms()` wraps around. The script uses `ticks_diff()` and a
cumulative elapsed time so that the integration policy receives non-negative,
monotonic timestamps during the finite test.

## Safety

The complete sequence is finite. A `finally` block resets the integration,
turns the RGB LED and buzzer off, and deinitializes the buzzer PWM even when an
error occurs. Nothing is written to the ESP32-C6 filesystem.

## Recorded Validation

- Real GPIO 3 acquisition: confirmed
- Normal, low-light, high-light, and transition detection: confirmed
- Physical RGB LED behavior: confirmed
- Physical buzzer behavior: confirmed
- Cooldown suppression and repeat during high light: confirmed
- Recovery to the normal local state: confirmed
- Continued acquisition after alarms: confirmed
- Final output cleanup: confirmed
- Console or cleanup error: none observed

JSON formatting and serial event output were not part of this test and remain
pending.
