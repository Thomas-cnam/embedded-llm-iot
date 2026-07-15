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

## 2026-07-07

### Goal

Prepare the passive buzzer PWM test script for manual execution.

### Work done

- Updated `firmware/tests/test_buzzer.py` to use GPIO 5 based on PCB label `BUZZER(5)`.
- Prepared a finite MicroPython PWM test with short tones at 440 Hz, 660 Hz, and 880 Hz.
- Added PWM cleanup so duty is set to 0 and PWM is deinitialized at the end.

### Observations

- The buzzer test script is ready for manual execution in Thonny.
- The buzzer has not been tested yet.

### Issues / open questions

- No buzzer result is available yet because the script was only prepared, not executed.

### Next steps

- Run `firmware/tests/test_buzzer.py` manually in Thonny on the ESP32-C6 board.
- Confirm whether the buzzer produces the expected short tones.
- Record the buzzer test result in `LOG.md`.

## 2026-07-07

### Goal

Test the onboard passive buzzer using MicroPython PWM.

### Work done

- Opened `firmware/tests/test_buzzer.py` in Thonny.
- Ran the script on the ESP32-C6 board.
- Used GPIO 5 based on PCB label `BUZZER(5)`.
- Played three short tones at 440 Hz, 660 Hz, and 880 Hz.
- Confirmed that PWM stopped at the end of the script.

### Observations

- The buzzer produced the expected short tones.
- The script completed without errors.
- PWM was stopped at the end.

### Issues / open questions

- No issue observed during this test.

### Next steps

- Continue Week 1 hardware bring-up with RGB LED and serial LED strip tests.
- Record each hardware test result in `LOG.md`.

## 2026-07-07

### Goal

Test the onboard RGB LED using MicroPython GPIO output.

### Work done

- Opened `firmware/tests/test_rgb_led.py` in Thonny.
- Ran the script on the ESP32-C6 board.
- Used GPIO 10, GPIO 11, and GPIO 21 based on PCB labels `R(10)`, `G(11)`, and `B(21)`.
- Tested red, green, blue, white, and off states.

### Observations

- The RGB LED displayed red correctly.
- The RGB LED displayed green correctly.
- The RGB LED displayed blue correctly.
- The RGB LED displayed white correctly.
- The RGB LED turned off correctly at the end.
- The script completed without errors.
- `ACTIVE_LOW = False` worked correctly.

### Issues / open questions

- No issue observed during this test.

### Next steps

- Continue Week 1 hardware bring-up with the serial LED strip test.
- Record each hardware test result in `LOG.md`.

## 2026-07-07

### Goal

Document successful Week 1 hardware peripheral tests.

### Work done

- Confirmed the passive buzzer test on GPIO 5.
- Confirmed the RGB LED test using GPIO 10, GPIO 11, and GPIO 21.
- Confirmed the serial LED strip test using GPIO 8 and 3 onboard LEDs.
- Verified that each test script completed without errors.
- Updated the hardware checklist and Week 1 plan.

### Observations

- The passive buzzer produced the expected short tones at 440 Hz, 660 Hz, and 880 Hz.
- The RGB LED displayed red, green, blue, white, and turned off correctly.
- The serial LED strip displayed red, green, blue, white, and turned off correctly.
- The serial LED test used LED_COUNT = 3.
- No error occurred during these tests.

### Issues / open questions

- No issue observed during the buzzer, RGB LED, or serial LED tests.
- The photoresistor was successfully validated after repeating the test with better sensor coverage.

### Next steps

- Keep the Week 1 hardware bring-up results documented.
- Prepare for the next project phase only after Week 1 documentation is reviewed.

## 2026-07-13

### Goal

Start Week 2 hardware consolidation planning and audit the existing peripheral test scripts.

### Work done

- Created `docs/week2_plan.md` for Week 2 hardware consolidation.
- Audited the existing peripheral test scripts without modifying their implementation.
- Created `docs/week2_audit.md` with script-level findings and improvement notes.
- Marked only the Week 2 audit checklist item as completed.

### Observations

- The Week 1 peripheral test scripts use the confirmed PCB pin mappings.
- The scripts are finite and suitable for continued manual use.
- Output cleanup is implemented for buzzer, RGB LED, and serial LEDs.
- No new hardware test was executed during this audit.
- Edge anomaly detection remains out of scope.

### Issues / open questions

- Reusable peripheral modules still need to be designed and created during Week 2.
- A combined hardware smoke test still needs to be created and run later.

### Next steps

- Clean and standardize the peripheral test scripts only where useful.
- Create reusable peripheral modules while preserving the known-working behavior.
- Prepare a combined hardware smoke test after reusable modules exist.

## 2026-07-13

### Goal

Clean and standardize the existing Week 1 peripheral test scripts for Week 2 consolidation.

### Work done

- Standardized the photoresistor, buzzer, RGB LED, and serial LED test scripts.
- Preserved all confirmed GPIO mappings and known-working test sequences.
- Kept each script finite and suitable for manual execution.
- Updated `docs/week2_audit.md` with the final cleaned script status.
- Updated `docs/week2_plan.md` to mark script cleaning and standardization as completed.

### Observations

- No hardware scripts were run during this task.
- The cleaned scripts still target the confirmed ESP32-C6 PCB pins.
- Output cleanup remains implemented for buzzer, RGB LED, and serial LEDs.
- Anomaly detection, gateway communication, and local LLM integration remain out of scope.

### Issues / open questions

- Reusable peripheral modules still need to be created in a later Week 2 step.
- A combined hardware smoke test still needs to be created after the modules exist.

### Next steps

- Create reusable peripheral modules for the confirmed hardware components.
- Keep the cleaned scripts as reference manual diagnostics.

## 2026-07-13

### Goal

Create reusable MicroPython peripheral modules for Week 2 hardware consolidation.

### Work done

- Created `firmware/peripherals/` with reusable helper modules for the photoresistor, buzzer, RGB LED, and serial LEDs.
- Preserved the confirmed GPIO mappings from Week 1 hardware bring-up.
- Added `docs/peripheral_modules.md` to describe module purpose, pins, and usage examples.
- Updated `firmware/README.md` with the current firmware structure.
- Updated `docs/week2_plan.md` to mark reusable peripheral module creation as completed.

### Observations

- The new modules are MicroPython-compatible helper classes.
- The existing self-contained test scripts remain the verified hardware reference.
- No hardware script was run or uploaded during this task.
- The reusable modules have not yet been independently validated on hardware.

### Issues / open questions

- The reusable modules still need hardware validation in a later Week 2 step.
- A combined hardware smoke test still needs to be created after module validation planning.

### Next steps

- Create a combined hardware smoke test using the reusable modules.
- Run and document that smoke test only when explicitly requested.

## 2026-07-13

### Goal

Prepare a finite, self-contained combined hardware smoke test for manual Thonny execution.

### Work done

- Created `firmware/tests/test_all_peripherals.py` using the confirmed ESP32-C6 GPIO mappings.
- Added a finite sequence for the photoresistor, buzzer, RGB LED, and serial LEDs.
- Added safety cleanup for PWM, the RGB LED, and the serial LEDs.
- Updated `firmware/tests/README.md` with manual execution instructions.
- Marked only creation of the combined hardware smoke test as completed in `docs/week2_plan.md`.

### Observations

- The smoke test is self-contained and does not require reusable peripheral modules on the board.
- Only built-in MicroPython modules are used.
- The script was prepared but was not executed or uploaded during this task.
- No new hardware result is claimed.

### Issues / open questions

- The combined hardware smoke test still needs to be run manually in Thonny.
- Its observed results must be documented after manual execution.

### Next steps

- Run `firmware/tests/test_all_peripherals.py` manually in Thonny.
- Observe each peripheral and record the results in `LOG.md`.

## 2026-07-13

### Goal

Run and validate the combined ESP32-C6 peripheral smoke test in Thonny.

### Work done

- Ran `firmware/tests/test_all_peripherals.py` manually on the ESP32-C6 board in Thonny.
- Read five photoresistor ADC values on GPIO 3.
- Played buzzer tones at 440 Hz, 660 Hz, and 880 Hz on GPIO 5.
- Tested red, green, blue, white, and off states on the RGB LED.
- Tested red, green, blue, white, and off states on the three serial LEDs.
- Confirmed the visual and audible outputs manually.

### Observations

- Photoresistor readings: 4513, 4513, 4513, 4513, and 4497.
- Average photoresistor reading: 4509.8.
- The three buzzer tones were heard as expected.
- The RGB LED displayed red, green, blue, and white, then turned off.
- The serial LEDs displayed red, green, blue, and white, then turned off.
- The complete sequence finished without errors.
- Safety cleanup completed and all outputs were turned off.

### Issues / open questions

- No issue was observed during the combined smoke test.
- Dedicated photoresistor baseline measurements still need to be collected separately.

### Next steps

- Collect and save the planned photoresistor baseline measurements.
- Continue the remaining Week 2 hardware consolidation documentation.

## 2026-07-13

### Goal

Prepare a repeatable photoresistor baseline measurement experiment.

### Work done

- Created `firmware/tests/measure_photoresistor_baseline.py` for GPIO 3.
- Prepared three measurement conditions: covered, ambient room light, and phone flashlight.
- Configured the finite experiment to collect 30 readings per condition after a five-second setup delay.
- Added CSV-compatible console output and in-memory summary calculations.
- Created the raw-data folder, an empty CSV template, and the experiment procedure documentation.

### Observations

- The script prefers `read_u16()` and falls back to `read()`.
- ADC attenuation is attempted safely.
- The script does not write to the ESP32 filesystem.
- The baseline script was prepared but was not run during this task.
- No baseline results, anomaly conclusion, or threshold were produced.

### Issues / open questions

- The three lighting conditions still need to be measured manually in Thonny.
- Raw measurement output still needs to be transferred to the experiments folder after testing.

### Next steps

- Run `firmware/tests/measure_photoresistor_baseline.py` manually in Thonny.
- Save the captured CSV-compatible readings without changing the raw values.

## 2026-07-13

### Goal

Collect and document repeatable photoresistor baseline measurements.

### Work done

- Ran `firmware/tests/measure_photoresistor_baseline.py` manually in Thonny on the ESP32-C6 board.
- Collected 30 readings with the photoresistor covered.
- Collected 30 readings in ambient room light.
- Collected 30 readings with a phone flashlight directed at the sensor.
- Saved all 90 raw readings unchanged in `experiments/raw_data/photoresistor_baseline_2026-07-13.csv`.
- Updated the baseline procedure and Week 2 documentation with descriptive results.

### Observations

- Covered: minimum 16, maximum 80, average 47.5.
- Ambient room light: minimum 24293, maximum 24437, average 24368.7.
- Phone flashlight: minimum 36889, maximum 42010, average 39545.9.
- Absolute average difference between covered and ambient room light: 24321.3.
- Absolute average difference between covered and phone flashlight: 39498.4.
- Absolute average difference between ambient room light and phone flashlight: 15177.2.
- The finite sequence completed without errors.

### Issues / open questions

- No execution issue was observed during data collection.
- No anomaly threshold or detector was defined from these measurements.

### Next steps

- Review the completed Week 2 hardware consolidation records.
- Keep anomaly detection work out of scope until the planned project phase.

## 2026-07-15

### Goal

Review the baseline experiment records and close Week 2 hardware consolidation.

### Work done

- Verified that the baseline dataset contains 90 real measurements: 30 covered, 30 in ambient room light, and 30 with a phone flashlight.
- Saved the unchanged measurements in `experiments/raw_data/photoresistor_baseline.csv`.
- Reviewed the numerical summary and documented the observed sensor behavior.
- Marked the Week 2 hardware consolidation checklist as completed.
- Added the current project status to `README.md`.

### Observations

- Covered: minimum 16, maximum 80, average 47.5.
- Ambient room light: minimum 24293, maximum 24437, average 24368.7.
- Phone flashlight: minimum 36889, maximum 42010, average 39545.9.
- Absolute average difference between covered and ambient room light: 24321.3.
- Absolute average difference between covered and phone flashlight: 39498.4.
- Absolute average difference between ambient room light and phone flashlight: 15177.2.
- Covered and ambient readings were stable within their respective conditions.
- Flashlight readings were higher and increased during the manual measurement series.
- The sensor showed a clear response across the three lighting conditions.

### Issues / open questions

- No hardware or data-recording issue remains open for Week 2.
- No anomaly threshold has been selected yet.

### Week 2 conclusion

- Week 2 hardware consolidation is completed.
- The main peripherals are verified in MicroPython.
- Photoresistor baseline measurements are recorded and documented.
- Week 3 implementation has not started.

## 2026-07-15

### Goal

Create an adjustable roadmap and detailed plan for the remaining internship work through the August 29 deadline.

### Work done

- Created `docs/project_roadmap.md` with the current status, milestones, target architecture, dependencies, and safety buffer.
- Created detailed pending checklists for Weeks 3 through 8.
- Created `docs/experimental_metrics_plan.md` for detector, latency, model, structured-output, and safety measurements.
- Created `docs/final_report_outline.md` for the English final report.
- Created `docs/final_submission_checklist.md` for repository, report, presentation, demonstration, backup, and submission verification.
- Added planning links and the remaining schedule to `README.md`.

### Observations

- The roadmap is a working plan and may be adjusted when technical evidence justifies a change.
- Required pipeline work has priority over optional sensors, model comparisons, and additional features.
- Required deliverables are planned for completion by August 25.
- August 26–29 is reserved as a safety buffer for corrections and submission verification.
- Week 1 and Week 2 remain completed; all future checklist items remain pending.

### Issues / open questions

- Runtime and local-model selection remain planned for Week 4.
- Detector parameters and experimental acceptance criteria must be selected from future measured evidence, not assumed during planning.
- Final university formatting and submission requirements must be confirmed with the supervisor.

### Next steps

- Review the roadmap with the supervisor and record any major adjustment in `LOG.md`.
- Begin Week 3 one checklist item at a time without starting later-week optional work early.

### Scope confirmation

- No source code was modified.
- No Week 3 implementation was started.
- No runtime or model was installed.
- No experiment was run and no result was invented.
