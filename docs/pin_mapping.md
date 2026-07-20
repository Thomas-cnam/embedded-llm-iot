# Pin Mapping Notes

This file summarizes the pin mapping information extracted from supervisor-provided material and PCB silkscreen inspection.

Do not guess GPIO numbers. Only fill this table after the pin mapping has been confirmed from official material, provided lab documentation, PCB labels, or direct confirmation from the supervisor.

## Current status

The main peripheral mappings are confirmed. The supervisor clarified on
2026-07-20 that the PCB silkscreen swaps the red and blue RGB labels.

## Pin mapping table

| Peripheral | GPIO / Pin | Interface | Status | Notes |
|---|---:|---|---|---|
| Photoresistor | GPIO 3 | ADC | Confirmed | PCB label: PHOTO(3) |
| Passive buzzer | GPIO 5 | PWM | Confirmed | PCB label: BUZZER(5) |
| RGB LED - Red | GPIO 21 | GPIO/PWM | Supervisor-confirmed | PCB red/blue silkscreen labels are swapped; `active_low=False` |
| RGB LED - Green | GPIO 11 | GPIO/PWM | Supervisor-confirmed | PCB label `G(11)` is correct; `active_low=False` |
| RGB LED - Blue | GPIO 10 | GPIO/PWM | Supervisor-confirmed | PCB red/blue silkscreen labels are swapped; `active_low=False` |
| Serial LED strip | GPIO 8 | One-wire / NeoPixel-compatible to confirm | Confirmed | PCB label: SERIAL_LED(8); 3 onboard LEDs visible; protocol to confirm by test |
| Button | GPIO 2 | GPIO input | Confirmed | PCB label: BUTTON(2) |
| HC-SR04 trigger | GPIO 15 | GPIO | Optional / confirmed from PCB | PCB label: TR(15) |
| HC-SR04 echo | GPIO 23 | GPIO | Optional / confirmed from PCB | PCB label: EC(23) |
| I2C SDA | GPIO 6 | I2C | Confirmed | PCB label: SDA(6) |
| I2C SCL | GPIO 7 | I2C | Confirmed | PCB label: SCL(7) |
| MPU6050 SDA | GPIO 6 | I2C | Optional / confirmed from PCB | PCB label: MPU6050 area uses SDA(6) |
| MPU6050 SCL | GPIO 7 | I2C | Optional / confirmed from PCB | PCB label: MPU6050 area uses SCL(7) |
| APDS9960 SDA | GPIO 6 | I2C | Optional / confirmed from PCB | PCB label: APDS9960 area uses SDA(6) |
| APDS9960 SCL | GPIO 7 | I2C | Optional / confirmed from PCB | PCB label: APDS9960 area uses SCL(7) |

## Reading checklist

- [ ] Identify board revision or PCB name
- [ ] Confirm MicroPython version
- [x] Confirm photoresistor ADC pin
- [x] Confirm buzzer PWM pin
- [x] Confirm RGB LED pins
- [x] Confirm serial LED strip data pin
- [ ] Confirm serial LED strip protocol
- [x] Confirm number of serial LEDs from visual inspection
- [x] Confirm optional HC-SR04 pins from PCB labels
- [x] Confirm optional MPU6050 I2C pins from PCB labels

## Notes

Most mappings were initially identified from PCB silkscreen labels. The RGB
mapping above supersedes the original red GPIO 10 / blue GPIO 21 interpretation
after direct supervisor clarification. A short physical RGB repeat test is
required before the corrected red and blue mapping is marked validated.

The firmware test scripts must not be executed until the relevant TODO pins are replaced with confirmed values.
