# Hardware Reading Notes

## Goal

Extract the hardware information required to safely run the Week 1 MicroPython peripheral tests.

The supervisor-provided material should be used to confirm pin mappings and peripheral behavior before running the test scripts on the real ESP32-C6 board.

## Documents reviewed

| Document | Reviewed | Notes |
|---|---|---|
| Supervisor-provided ESP32-C6 PCB documentation | No | TODO |
| Supervisor-provided MicroPython lab material | No | TODO |
| Peripheral driver examples | No | TODO |

## Key information to extract

- Board revision or PCB identifier
- MicroPython version
- USB serial chip and COM port information
- Photoresistor ADC pin
- Expected photoresistor value range
- Buzzer PWM pin
- Safe buzzer frequency range
- RGB LED pins
- RGB LED active high or active low behavior
- Serial LED strip data pin
- Serial LED strip protocol
- Serial LED strip LED count
- Optional HC-SR04 wiring
- Optional MPU6050 I2C wiring

## Confirmed information so far

| Item | Value | Source |
|---|---|---|
| USB serial chip | Silicon Labs CP210x USB to UART Bridge | Windows Device Manager |
| Serial port | COM3 | `mpremote connect list` |
| MicroPython REPL access | Confirmed | `py -m mpremote connect COM3 repl` |
| Basic REPL command | `print("Hello ESP32-C6")` returned `Hello ESP32-C6` | Manual test |

## Open questions

- What GPIO pin is used by the photoresistor?
- What GPIO pin is used by the passive buzzer?
- What GPIO pins are used by the RGB LED?
- Is the RGB LED active high or active low?
- What GPIO pin is used by the serial LED strip?
- What protocol and LED count does the serial LED strip use?
- Are optional HC-SR04 and MPU6050 sensors connected or only available on request?

## Notes

No GPIO pin mapping has been confirmed yet.
