# Anomaly Integration and Local Alarm Design

## Purpose

This layer coordinates the pure detector, alert policy, and local alarm while remaining testable without hardware. Collaborators are provided through dependency injection, so policy and orchestration can be validated on a standard Python host before any ESP32-C6 integration.

## Components

### PhotoresistorAnomalyDetector

Classifies integer photoresistor readings using provisional threshold and delta rules. Its existing behavior and structured results remain unchanged.

### AnomalyAlertPolicy

Controls event timing, active anomaly state, cooldown, repeated-event suppression, anomaly-type changes, and recovery. It does not call the detector, control hardware, serialize JSON, or emit serial output.

### LocalAlarmController

Maps supported anomaly types to the existing RGB LED and buzzer APIs. It receives peripheral objects from the caller and never creates GPIO objects. Buzzer calls always use finite durations, and `safe_off()` attempts both RGB and buzzer cleanup even if one operation fails.

### AnomalyIntegrationController

Coordinates detector evaluation, policy evaluation, and optional local-alarm actions. It preserves detector and policy results when an alarm operation fails, attempts safe cleanup, and also works with no alarm controller.

## Cooldown Policy

- The first anomaly emits immediately.
- The same anomaly is suppressed during the provisional 5000 ms cooldown.
- The same anomaly may repeat at or after 5000 ms when repeat behavior is enabled.
- An anomaly-type change emits immediately and is not blocked by the previous cooldown.
- Recovery clears the active anomaly and its last-alert timestamp.
- A new anomaly after recovery emits immediately.
- Repeated events can be disabled until recovery or anomaly-type change.
- Timestamps must be non-negative and monotonic within one policy session.

The pure detector identifies large return transitions from `low_light` as `sudden_rise` and from `high_light` as `sudden_drop`. When such a delta-only result directly exits the active threshold state, the policy treats it as recovery while preserving the raw detector result in the integration output.

Timestamp wraparound is not handled by the pure policy. A future ESP32-C6 application must normalize MicroPython ticks before calling it.

## Local Alarm Mapping

| State | RGB state | Buzzer |
|---|---|---|
| normal | green | off |
| low_light | red | 440 Hz, 200 ms |
| high_light | blue | 880 Hz, 200 ms |
| sudden_drop | red | 660 Hz, 150 ms |
| sudden_rise | white | 880 Hz, 150 ms |

These mappings remain provisional and require real hardware validation. No physical hardware test occurred in this task. Serial LEDs are not used for Week 3 local alarms.

The existing `Buzzer.tone()` API stops output after its finite duration. `show_normal()` and `safe_off()` explicitly call `buzzer.off()`.

## Integration Behavior

- The first normal result initializes the planned green state once.
- Continued normal readings do not repeatedly call the peripherals.
- An emitted alert triggers the mapped finite local alarm.
- A suppressed repeated anomaly does not replay the buzzer.
- A cooldown repeat replays the same bounded alarm.
- An anomaly-type change triggers the new mapping immediately.
- Recovery restores green and silences the buzzer.
- Reset clears detector history, policy state, visual initialization, and alarm error state, then attempts safe cleanup.

The combined result retains:

- `detector_result`
- `policy_decision`
- `alarm_action`
- `alarm_triggered`
- `alarm_error`
- `recovery_handled`

## Error Handling

- Detector validation errors are preserved and continue to raise normally.
- Local-alarm failures do not erase detector or policy results.
- A readable alarm error is returned by the integration controller.
- `safe_off()` is attempted after alarm failures.
- Both RGB and buzzer cleanup operations are attempted independently.
- Cleanup failures are retained in the reported alarm error.
- The system can operate without an alarm controller.
- Hardware validation remains pending.

## Test Execution

Execution date: 2026-07-17

Commands executed from the repository root:

```powershell
py -B -m unittest discover -s tests -p "test_anomaly_detector.py" -v
py -B -m unittest discover -s tests -p "test_anomaly_integration.py" -v
py -B -m unittest discover -s tests -p "test_*.py" -v
```

Results:

- Existing detector tests: 29 passed, 0 failed, 0 errors
- New integration tests: 48 passed, 0 failed, 0 errors
- Complete suite: 77 passed, 0 failed, 0 errors
- Final result: `OK`
- Syntax validation: passed
- Forbidden integration imports: none

The existing detector tests remain passing without weakened assertions.

## Simulated Scenarios Validated

- Policy input and timestamp validation
- First anomaly, same anomaly, cooldown boundary, cooldown repeat, and disabled repeats
- Immediate anomaly-type changes
- Normal recovery and threshold-exit delta recovery
- Normal, low-light, high-light, sudden-drop, and sudden-rise alarm mappings
- Finite buzzer frequencies and durations
- Best-effort cleanup with one or both fake peripherals failing
- First normal initialization and repeated-normal suppression
- Operation without an alarm controller
- Alarm failure while preserving detector and policy results
- Reset behavior
- Invalid sensor input propagation
- Complete normal-to-low-to-recovery-to-high-to-recovery sequence

## Limitations

- No real ADC acquisition
- No real RGB test for this integration layer
- No real buzzer test for this integration layer
- No JSON formatting
- No serial output
- No timestamp-wraparound handling
- No moving-average deviation
- No gateway or LLM
