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

GPIO pin mappings from supervisor-provided documents are not confirmed yet. PCB silkscreen labels have been recorded below.

## PCB silkscreen inspection

The ESP32-C6 custom PCB was visually inspected, and the labels printed on the PCB were used to identify the main Week 1 peripheral pins.

Observed PCB labels:

- Photoresistor: PHOTO(3)
- Passive buzzer: BUZZER(5)
- RGB LED: R(10), G(11), B(21)
- Serial LED: SERIAL_LED(8)
- Button: BUTTON(2)
- HC-SR04: TR(15), EC(23)
- I2C: SDA(6), SCL(7)

Additional observations:

- The serial LED area contains 3 visible onboard LEDs.
- RGB active high/low behavior still needs to be verified by test.
- Serial LED protocol still needs to be verified by test.
- No peripheral test has been run yet.
