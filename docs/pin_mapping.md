# Pin Mapping Notes

This file summarizes the pin mapping information extracted from the supervisor-provided hardware and MicroPython lab documentation.

Do not guess GPIO numbers. Only fill this table after the pin mapping has been confirmed from official material, provided lab documentation, PCB labels, or direct confirmation from the supervisor.

## Current status

No GPIO pin mapping has been confirmed yet.

## Pin mapping table

| Peripheral | GPIO / Pin | Interface | Status | Notes |
|---|---:|---|---|---|
| Photoresistor | TODO | ADC | To confirm | Analog light intensity input |
| Passive buzzer | TODO | PWM | To confirm | PWM-controlled acoustic output |
| RGB LED - Red | TODO | GPIO/PWM | To confirm | Need to verify active high or active low behavior |
| RGB LED - Green | TODO | GPIO/PWM | To confirm | Need to verify active high or active low behavior |
| RGB LED - Blue | TODO | GPIO/PWM | To confirm | Need to verify active high or active low behavior |
| Serial LED strip | TODO | One-wire / NeoPixel-compatible | To confirm | Need to confirm protocol and number of LEDs |
| HC-SR04 trigger | TODO | GPIO | Optional / to confirm | Optional distance sensor |
| HC-SR04 echo | TODO | GPIO | Optional / to confirm | Optional distance sensor |
| MPU6050 SDA | TODO | I2C | Optional / to confirm | Optional accelerometer/gyroscope |
| MPU6050 SCL | TODO | I2C | Optional / to confirm | Optional accelerometer/gyroscope |

## Reading checklist

- [ ] Identify board revision or PCB name
- [ ] Confirm MicroPython version
- [ ] Confirm photoresistor ADC pin
- [ ] Confirm buzzer PWM pin
- [ ] Confirm RGB LED pins
- [ ] Confirm serial LED strip data pin
- [ ] Confirm serial LED strip protocol
- [ ] Confirm number of serial LEDs
- [ ] Confirm optional HC-SR04 pins
- [ ] Confirm optional MPU6050 I2C pins

## Notes

The firmware test scripts must not be executed until the relevant TODO pins are replaced with confirmed values.
