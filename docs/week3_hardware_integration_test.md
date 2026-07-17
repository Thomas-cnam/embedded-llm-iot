# Week 3 Hardware Integration Test

## Purpose

`firmware/tests/test_anomaly_hardware_integration.py` is a finite, guided
MicroPython test that connects the real photoresistor to the existing detector,
alert policy, integration controller, RGB LED, and buzzer modules.

The script has been prepared for manual execution. It has not been run on the
ESP32-C6, and no physical result is claimed in this document.

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

These are expected behaviors from the provisional configuration, not recorded
hardware observations. Actual values, colors, tones, cooldown behavior, and
recovery behavior must be checked manually.

## Timestamp Handling

MicroPython `ticks_ms()` wraps around. The script uses `ticks_diff()` and a
cumulative elapsed time so that the integration policy receives non-negative,
monotonic timestamps during the finite test.

## Safety

The complete sequence is finite. A `finally` block resets the integration,
turns the RGB LED and buzzer off, and deinitializes the buzzer PWM even when an
error occurs. Nothing is written to the ESP32-C6 filesystem.

## Results to Record Manually

After execution, record:

- representative ADC values for every phase;
- observed RGB states and buzzer tones;
- whether repeated alerts were suppressed during cooldown;
- whether recovery restored the normal state;
- whether acquisition continued after each alarm;
- any console or cleanup error.

Do not mark the physical test complete until all observations have been made.
