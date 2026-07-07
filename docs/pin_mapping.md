# Pin Mapping Notes

This file summarizes the pin mapping information extracted from supervisor-provided material and PCB silkscreen inspection.

Do not guess GPIO numbers. Only fill this table after the pin mapping has been confirmed from official material, provided lab documentation, PCB labels, or direct confirmation from the supervisor.

## Current status

The main Week 1 peripheral pin mappings have been identified from PCB silkscreen labels. Functional tests are still required.

## Pin mapping table

| Peripheral | GPIO / Pin | Interface | Status | Notes |
|---|---:|---|---|---|
| Photoresistor | GPIO 3 | ADC | Confirmed | PCB label: PHOTO(3) |
| Passive buzzer | GPIO 5 | PWM | Confirmed | PCB label: BUZZER(5) |
| RGB LED - Red | GPIO 10 | GPIO/PWM | Confirmed | PCB label: R(10); active high/low still to test |
| RGB LED - Green | GPIO 11 | GPIO/PWM | Confirmed | PCB label: G(11); active high/low still to test |
| RGB LED - Blue | GPIO 21 | GPIO/PWM | Confirmed | PCB label: B(21); active high/low still to test |
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

These mappings were identified from PCB silkscreen labels during manual board inspection. Functional tests are still required.

The firmware test scripts must not be executed until the relevant TODO pins are replaced with confirmed values.
