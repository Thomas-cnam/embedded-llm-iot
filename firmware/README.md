# Firmware

This folder contains MicroPython code for the ESP32-C6 firmware.

## Current Structure

- `tests/`: self-contained hardware test scripts verified during Week 1 bring-up.
- `peripherals/`: reusable peripheral helper modules prepared during Week 2 consolidation.
- `anomaly/`: hardware-independent anomaly-detector configuration and pure logic.

## Confirmed Components

- Photoresistor on GPIO 3
- Passive buzzer on GPIO 5
- RGB LED on GPIO 10, GPIO 11, and GPIO 21 with `ACTIVE_LOW = False`
- Serial LEDs on GPIO 8 with `LED_COUNT = 3`
- Optional HC-SR04 ultrasonic sensor
- Optional MPU6050 motion sensor

The reusable modules are prepared for firmware consolidation but have not yet been independently validated on hardware. The self-contained scripts in `firmware/tests/` remain the verified hardware reference.

## Anomaly Detection

- `firmware/anomaly/config.py` contains the provisional detector configuration.
- `firmware/anomaly/detector.py` contains pure threshold and delta detector logic.
- The detector has no hardware, peripheral, timing, serial, or JSON dependency.
- Host-side tests are located in `tests/test_anomaly_detector.py`.
- Hardware integration has not started yet.
- Thresholds and timing values remain provisional pending real Week 3 tests.

Run the simulated host-side tests from the repository root:

```powershell
py -m unittest discover -s tests -p "test_anomaly_detector.py" -v
```
