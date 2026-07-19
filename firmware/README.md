# Firmware

This folder contains MicroPython code for the ESP32-C6 firmware.

## Current Structure

- `tests/`: self-contained hardware test scripts verified during Week 1 bring-up.
- `peripherals/`: reusable peripheral helper modules prepared during Week 2 consolidation.
- `anomaly/`: hardware-independent detector, alert policy, local-alarm
  integration, and event-formatting logic.

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
- `firmware/anomaly/event_formatter.py` validates integration results and builds
  compact schema version 1.0 anomaly JSON.
- The detector, alert policy, integration, and formatter remain independent
  from serial transport, the gateway, and the local LLM.
- Host-side tests are located in `tests/test_anomaly_detector.py`,
  `tests/test_anomaly_integration.py`, and
  `tests/test_anomaly_event_formatter.py`.
- Physical ESP32-C6 detector and local-alarm integration passed its first
  guided test on 2026-07-17.
- The pure formatter passed host-side tests on 2026-07-19.
- One-event-per-line serial output and real MicroPython JSON capture remain
  pending.
- Local-alarm mappings, thresholds, and timing values have one successful
  hardware validation but remain provisional until repeated trials.

Run the simulated host-side tests from the repository root:

```powershell
py -m unittest discover -s tests -p "test_*.py" -v
```
