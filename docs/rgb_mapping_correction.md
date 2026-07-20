# RGB Mapping Correction and Revalidation

## Correction

On 2026-07-20, the supervisor confirmed that the PCB red and blue silkscreen
labels are swapped.

| Channel | Previous interpretation | Correct mapping |
|---|---:|---:|
| Red | GPIO 10 | GPIO 21 |
| Green | GPIO 11 | GPIO 11 |
| Blue | GPIO 21 | GPIO 10 |

The correct configuration uses `active_low=False`.

## Impact

Source code and current documentation now use the corrected mapping. Existing
raw console captures and earlier `LOG.md` entries are preserved as historical
evidence. Previous statements assigning physical output specifically to red or
blue under the old mapping are superseded and require a repeat test.

Photoresistor acquisition, buzzer behavior, serial LEDs, detector decisions,
cooldown, cleanup, JSON formatting, and gateway-independent logic are not
affected by this correction. Green uses the same GPIO, while white and off do
not distinguish the swapped red and blue channels.

## Manual Revalidation Procedure

1. Open `firmware/tests/test_rgb_led.py` in Thonny.
2. Run the finite script on the ESP32-C6 without saving it as `main.py`.
3. Confirm the displayed sequence: red, green, blue, white, then off.
4. Confirm that the script completes without an error and leaves the LED off.
5. Record only the observed result in `LOG.md` and update the hardware
   checklist.

Test date: 2026-07-20

The operator completed the standalone test and manually confirmed red, green,
blue, white, and off. The operator also confirmed red for covered low-light
alerts and blue for flashlight high-light alerts during both guided runs.

- [x] Standalone RGB test completed
- [x] Physical red confirmed
- [x] Physical green confirmed
- [x] Physical blue confirmed
- [x] Physical white confirmed
- [x] Off state confirmed
- [x] Covered scenario produced physical red
- [x] Flashlight scenario produced physical blue
- [x] Buzzer behavior remained correct
- [x] Final cleanup completed
- [x] Corrected evidence saved

Evidence: `experiments/week3/raw_console_run_01.txt`,
`experiments/week3/raw_console_run_02.txt`, and `docs/week3_results.md`.
Codex did not operate the ESP32-C6; these conclusions use the operator's manual
observations.

## Host-Side Verification

The complete automated suite passed after the correction: 129 tests, 0
failures, and 0 errors. These tests verify the corrected defaults and script
constants as well as the existing detector, alert-policy, integration, and JSON
behavior. They do not replace the pending physical color observation.
