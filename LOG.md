# Lab Notebook

## 2026-07-07

### Goal

Review the internship assignment and prepare the initial repository structure for Week 1.

### Work Done

- Reviewed the project assignment and Week 1 requirements.
- Prepared the initial repository structure.
- Added documentation placeholders for project summary, Week 1 planning, hardware bring-up, and responsible AI usage.
- Added placeholder folders for firmware, gateway, experiments, and report materials.
- Added basic MicroPython peripheral test templates.

### Observations

- The project targets a custom ESP32-C6 PCB.
- Firmware will be written in MicroPython.
- The gateway will later be written in Python 3.x.
- GPIO pin mappings are not yet documented in this repository.
- Hardware tests have not yet been performed or validated on the real board.

### Issues / Open Questions

- Confirm the official GPIO pin mapping for each peripheral.
- Confirm the exact ESP32-C6 board documentation and flashing workflow.
- Confirm which optional peripherals are available on the custom PCB.
- Confirm the local LLM runtime to evaluate after Week 1.

### Next Steps

- Read the official hardware documentation.
- Identify and document GPIO pin mappings.
- Prepare the MicroPython development environment.
- Test the ESP32-C6 peripherals with MicroPython.
- Record all hardware test results in this lab notebook.


## 2026-07-07

### Goal

Verify USB serial connection and MicroPython REPL access on the ESP32-C6 board.

### Work done

- Connected the ESP32-C6 board to the laptop using USB.
- Detected the board on COM3 as a Silicon Labs CP210x USB to UART Bridge.
- Confirmed that `mpremote` can list the board using `py -m mpremote connect list`.
- Opened the MicroPython REPL using `py -m mpremote connect COM3 repl`.
- Executed `print("Hello ESP32-C6")` in the MicroPython REPL.

### Observations

- The board is correctly detected by Windows on COM3.
- Windows identifies the USB serial bridge as Silicon Labs CP210x USB to UART Bridge.
- `mpremote` successfully lists and connects to the board on COM3.
- The MicroPython REPL is accessible through `py -m mpremote connect COM3 repl`.
- The command `print("Hello ESP32-C6")` returned the expected output: `Hello ESP32-C6`.
- Basic USB serial communication is confirmed.
- Peripheral tests are still pending until GPIO pin mappings are confirmed from official hardware documentation.

### Issues / open questions

- GPIO pin mappings are still not confirmed.
- Peripheral tests should not be executed until the official hardware documentation and pin mapping are checked.
- The photoresistor, buzzer, RGB LED, and serial LED strip have not been validated yet.

### Next steps

- Read the provided hardware documentation.
- Identify GPIO pins for the photoresistor, buzzer, RGB LED, and serial LED strip.
- Update `docs/hardware_checklist.md` with confirmed pin mappings.
- Run the first peripheral test only after confirming the correct pins.
- Record each hardware test result in `LOG.md`.

## 2026-07-07

### Goal

Document the initial team organization and prepare hardware documentation notes.

### Work done

- Updated TEAM.md with the initial division of work and collaboration rules.
- Added docs/pin_mapping.md to track confirmed GPIO pin mappings.
- Added docs/hardware_reading_notes.md to record notes from the supervisor-provided hardware documentation.
- Updated the Week 1 plan to mark the team organization step as completed.

### Observations

- The repository now separates team organization, hardware reading notes, pin mapping, and hardware test results.
- GPIO pin mappings are still not confirmed.
- Peripheral tests are still pending.

### Issues / open questions

- The supervisor-provided hardware documentation still needs to be reviewed.
- GPIO pins for the photoresistor, buzzer, RGB LED, and serial LED strip must be confirmed before running the test scripts.
- The repository still needs to be shared with GitHub user `matusformanek` if this has not been done manually yet.

### Next steps

- Share the repository with `matusformanek`.
- Read the hardware documentation.
- Fill docs/pin_mapping.md with confirmed pin mappings.
- Update firmware test scripts only after pin confirmation.
- Test each peripheral one by one and record results in LOG.md.

## 2026-07-07

### Goal

Share the GitHub repository with the supervisor and keep the Week 1 documentation up to date.

### Work done

- Shared the GitHub repository with the supervisor GitHub user `matusformanek`.
- Updated the Week 1 plan to reflect that the repository sharing step is completed.

### Observations

- The repository is now available for supervisor review.
- The repository contains the initial Week 1 structure, team organization, lab notebook, hardware checklist, pin mapping notes, and hardware reading notes.
- The project is still in the Week 1 hardware bring-up preparation phase.

### Issues / open questions

- The supervisor-provided hardware documentation still needs to be reviewed.
- GPIO pin mappings are still not confirmed.
- Peripheral tests are still pending.
- The photoresistor, buzzer, RGB LED, and serial LED strip must not be tested until their pins are confirmed.

### Next steps

- Read the supervisor-provided hardware documentation.
- Fill `docs/pin_mapping.md` with confirmed pin mappings.
- Update firmware test scripts only after pin confirmation.
- Test each peripheral one by one.
- Record each hardware test result in `LOG.md`.

## 2026-07-07

### Goal

Identify Week 1 peripheral pin mappings from the ESP32-C6 PCB silkscreen.

### Work done

- Visually inspected the ESP32-C6 custom PCB.
- Identified the main Week 1 peripheral pins from the printed PCB labels.
- Updated `docs/pin_mapping.md` with confirmed pin mappings.
- Updated `docs/hardware_reading_notes.md` with PCB silkscreen inspection notes.
- Updated `docs/hardware_checklist.md` with confirmed pins and pending test status.
- Updated the Week 1 plan to mark pin mapping identification as completed.

### Observations

- Photoresistor is labeled `PHOTO(3)`.
- Passive buzzer is labeled `BUZZER(5)`.
- RGB LED channels are labeled `R(10)`, `G(11)`, and `B(21)`.
- Serial LED is labeled `SERIAL_LED(8)`.
- The serial LED area contains 3 visible onboard LEDs.
- HC-SR04 labels are `TR(15)` and `EC(23)`.
- I2C labels are `SDA(6)` and `SCL(7)`.

### Issues / open questions

- RGB LED active high or active low behavior still needs to be tested.
- Serial LED protocol still needs to be confirmed by test.
- No peripheral test has been run yet.

### Next steps

- Update firmware test scripts with the confirmed pins.
- Test the photoresistor first.
- Then test RGB LED, buzzer, and serial LED one by one.
- Record each test result in `LOG.md`.

## 2026-07-07

### Goal

Test the onboard photoresistor using MicroPython ADC.

### Work done

- Updated `firmware/tests/test_photoresistor.py` to use GPIO 3 based on PCB label `PHOTO(3)`.
- Ran the photoresistor test on the ESP32-C6 through `mpremote`.
- Collected readings with the photoresistor exposed to room light.
- Collected readings with the photoresistor covered.

### Observations

- Exposed readings: 6065, 6081, 6081, 6049, 6081, 6081, 6049, 6065, 6065, 6065.
- Covered readings: 6065, 6081, 6081, 6049, 6049, 6097, 6049, 6065, 6033, 6033.
- Average exposed reading: 6068.2.
- Average covered reading: 6060.2.
- Absolute difference: 8.0.
- The photoresistor did not show a clear response to the covered versus exposed condition during this run, so the test is documented as inconclusive.

### Issues / open questions

- The ADC readings changed only slightly between exposed and covered conditions.
- It may be necessary to repeat the test with stronger light contrast or verify the photoresistor circuit behavior.

### Next steps

- Repeat or investigate the photoresistor ADC test before marking it as working.
- Test the RGB LED, buzzer, and serial LED strip one by one.
- Record each result in `LOG.md`.

## 2026-07-07

### Goal

Repeat the onboard photoresistor ADC test using Thonny.

### Work done

- Opened `firmware/tests/test_photoresistor.py` in Thonny.
- Ran the script on the ESP32-C6 board.
- Used GPIO 3 based on PCB label `PHOTO(3)`.
- Collected readings with the photoresistor exposed to room light.
- Collected readings with the photoresistor covered.

### Observations

- Exposed average reading: 6543.4
- Covered average reading: 6546.6
- Absolute difference: 3.2
- The exposed and covered readings are almost identical.
- The photoresistor response is still inconclusive.

### Issues / open questions

- The measured difference is too small to validate the photoresistor.
- Possible causes:
  - GPIO 3 may need confirmation.
  - ADC configuration may need adjustment.
  - The wrong physical component may have been covered.
  - The photoresistor circuit may require supervisor confirmation.
  - A hardware issue is possible.

### Next steps

- Leave the photoresistor test marked as inconclusive.
- Continue Week 1 hardware bring-up with the other peripherals.
- Test RGB LED, buzzer, and serial LED strip one by one.
- Ask the supervisor for confirmation if the photoresistor continues to show no clear response.

## 2026-07-07

### Goal

Validate the onboard photoresistor ADC test after repeating it with better sensor coverage.

### Work done

- Reran `firmware/tests/test_photoresistor.py` in Thonny.
- Used GPIO 3 based on PCB label `PHOTO(3)`.
- Collected readings with the photoresistor exposed to room light.
- Collected readings with the photoresistor properly covered.

### Observations

- Exposed average reading: 28041.2
- Covered average reading: 1225.6
- Absolute difference: 26815.6
- The readings changed clearly when the photoresistor was covered.
- The photoresistor responds correctly to light changes.

### Issues / open questions

- The previous inconclusive result was likely caused by insufficient sensor coverage or incorrect manual handling.
- No issue observed during this successful repeat test.

### Next steps

- Continue Week 1 hardware bring-up with RGB LED, buzzer, and serial LED strip tests one by one.
- Record each hardware test result in `LOG.md`.
