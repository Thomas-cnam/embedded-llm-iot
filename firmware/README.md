# Firmware

This folder contains MicroPython code for the ESP32-C6 firmware.

## Current Structure

- `tests/`: self-contained hardware test scripts verified during Week 1 bring-up.
- `peripherals/`: reusable peripheral helper modules prepared during Week 2 consolidation.
- `anomaly/`: hardware-independent detector, alert policy, and local-alarm integration logic.

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
- `firmware/anomaly/alert_policy.py` contains cooldown, suppression, state-change, and recovery decisions.
- `firmware/anomaly/local_alarm.py` maps anomaly states to injected RGB LED and buzzer objects.
- `firmware/anomaly/integration.py` coordinates detector, policy, and optional local-alarm behavior.
- The detector and alert policy have no hardware, peripheral, serial, or JSON dependency.
- Host-side tests are located in `tests/test_anomaly_detector.py` and `tests/test_anomaly_integration.py`.
- Physical ESP32-C6 integration has not started yet.
- No JSON formatter or serial event output exists yet.
- Local-alarm mappings remain provisional.
- Thresholds and timing values remain provisional pending real Week 3 tests.

Run the simulated host-side tests from the repository root:

```powershell
py -m unittest discover -s tests -p "test_*.py" -v
```
