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
