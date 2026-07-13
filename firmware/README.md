# Firmware

This folder contains MicroPython code for the ESP32-C6 firmware.

## Current Structure

- `tests/`: self-contained hardware test scripts verified during Week 1 bring-up.
- `peripherals/`: reusable peripheral helper modules prepared during Week 2 consolidation.

## Confirmed Components

- Photoresistor on GPIO 3
- Passive buzzer on GPIO 5
- RGB LED on GPIO 10, GPIO 11, and GPIO 21 with `ACTIVE_LOW = False`
- Serial LEDs on GPIO 8 with `LED_COUNT = 3`
- Optional HC-SR04 ultrasonic sensor
- Optional MPU6050 motion sensor

The reusable modules are prepared for firmware consolidation but have not yet been independently validated on hardware. The self-contained scripts in `firmware/tests/` remain the verified hardware reference.
