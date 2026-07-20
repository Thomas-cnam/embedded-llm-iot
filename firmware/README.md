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
- RGB LED: red GPIO 21, green GPIO 11, blue GPIO 10 with `ACTIVE_LOW = False`
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
- Physical ESP32-C6 detector and local-alarm integration completed its first
  guided test on 2026-07-17. A later supervisor correction swapped the red and
  blue pin interpretation, so the corrected RGB colors require revalidation.
- The pure formatter passed host-side tests on 2026-07-19.
- One-event-per-line serial output and real MicroPython JSON capture remain
  pending.
- Detector thresholds, timing, buzzer behavior, and sensor acquisition have
  real-board evidence. Corrected RGB color mapping remains pending physical
  revalidation.

Run the simulated host-side tests from the repository root:

```powershell
py -m unittest discover -s tests -p "test_*.py" -v
```
