# Anomaly Detector Simulated Tests

## Purpose

These tests validate the pure photoresistor anomaly-detector logic on the PC before hardware integration. They check deterministic classification, validation, history, and state behavior using simulated integer readings.

- No ESP32-C6 hardware was used.
- No sensor was read.
- No RGB LED, serial LED, or buzzer was controlled.
- Results are simulated logic-test results, not hardware-validation results.

## Tested Configuration

| Parameter | Value |
|---|---:|
| Low-light threshold | 5000 |
| High-light threshold | 32000 |
| Sudden-change threshold | 8000 |
| History size | 5 |

All values remain provisional and require later real ESP32-C6 validation.

## Covered Scenarios

- Configuration validation
- Input type and ADC-range validation
- Stable ambient values
- Low-light values
- High-light values
- Sudden drop
- Sudden rise
- Threshold plus delta combinations
- Exact threshold boundaries
- Exact delta boundaries
- First-reading behavior
- History management and defensive copies
- State transitions
- Custom configuration
- Reset behavior
- Structured result fields

## Expected Representative Results

| Previous value | Current value | Expected primary result | Expected secondary result |
|---:|---:|---|---|
| None | 24368 | normal | None |
| None | 50 | low_light | None |
| 24368 | 50 | low_light | sudden_drop |
| 24368 | 39546 | high_light | sudden_rise |
| 24368 | 15000 | sudden_drop | None |
| 15000 | 24000 | sudden_rise | None |

## Test Execution

- Execution date: 2026-07-16
- Environment: standard Python on the Windows development PC
- Command used:

```powershell
py -m unittest discover -s tests -p "test_anomaly_detector.py" -v
```

- Tests run: 29
- Passed: 29
- Failed: 0
- Errors: 0
- Result: `OK`

A separate syntax parse also passed for the package and test files. Static inspection found no `machine`, `neopixel`, serial, JSON, time, or peripheral-module import in the pure detector.

## Limitations

- Simulated tests do not validate ADC acquisition.
- Simulated tests do not validate MicroPython execution on the ESP32-C6.
- Simulated tests do not validate timing or the configured sample interval.
- Simulated tests do not validate local alarms.
- Simulated tests do not validate serial JSON.
- Provisional thresholds still require real hardware testing.
- Cooldown and event suppression remain outside the detector module.
- Moving-average deviation is not implemented.
