# Anomaly Detector Design

## Purpose

This document defines the initial design of the Week 3 photoresistor anomaly detector. The detector will run on the ESP32-C6 and must remain deterministic, lightweight, explainable, and independent from the future local LLM integration.

## Baseline Data Reviewed

The source reviewed for this design is `experiments/raw_data/photoresistor_baseline.csv`, containing 30 real readings for each condition.

| Condition | Minimum | Maximum | Average |
|---|---:|---:|---:|
| Covered | 16 | 80 | 47.5 |
| Ambient room light | 24293 | 24437 | 24368.7 |
| Phone flashlight | 36889 | 42010 | 39545.9 |

Absolute differences between averages:

- Covered versus ambient: 24321.3
- Covered versus flashlight: 39498.4
- Ambient versus flashlight: 15177.2

The three conditions are clearly separated in the current baseline dataset. These values describe one test environment, however, and may change with room lighting, sensor orientation, power conditions, sensor variation, or another test location. The baseline supports an initial design but does not establish final benchmark parameters.

## Detector Goals

The detector must:

- classify stable ambient light as normal
- detect very low light
- detect unusually high light
- detect sudden decreases
- detect sudden increases
- preserve a short reading history
- avoid repeated alarm flooding
- remain independent from LED and buzzer execution
- produce a structured detector result
- remain usable if the gateway or LLM is unavailable

## Initial Detector Methods

### 1. Threshold Crossing

Threshold crossing divides the ADC space into a provisional low-light region, normal range, and high-light region:

- Provisional low-light threshold: `5000`
- Provisional normal range: `5000` to `32000`, inclusive
- Provisional high-light threshold: `32000`

For the first implementation design, a reading below `5000` is `low_light`, a reading above `32000` is `high_light`, and a reading within the range is eligible to be `normal` if no sudden-change rule is active.

Covered readings between 16 and 80 are far below `5000`. Ambient readings between 24293 and 24437 are safely inside the proposed normal range. Phone-flashlight readings between 36889 and 42010 are above `32000`. The proposed values are intentionally separated from the observed baseline clusters to leave margins between the current conditions.

All threshold values are provisional. They must be adjusted, if necessary, using real Week 3 calibration tests in varied conditions before final evaluation. They are not final benchmark thresholds.

### 2. Sudden Delta Detection

The detector should calculate a signed delta:

```text
delta = current_value - previous_value
```

The provisional absolute sudden-change threshold is `8000` ADC units:

- `delta <= -8000` proposes `sudden_drop`
- `delta >= 8000` proposes `sudden_rise`

The ambient baseline variation is small relative to `8000`, while transitions from ambient to covered or flashlight conditions produce changes much larger than `8000` in the recorded data. The threshold is provisional and must be validated using controlled Week 3 transitions. Both direction and magnitude should be retained for diagnostics.

The first reading has no previous value, so it cannot produce a delta result. Its `previous_value` and `delta` should be `null` in a structured result.

### 3. Moving-Average Deviation

Moving-average deviation is optional for the first implementation:

- Provisional history size: 5 readings
- Compare a new value with the recent mean
- Preserve the history for diagnostics
- Do not implement this method initially
- Investigate it only if threshold and delta detection produce unstable results

Initial filtering and hysteresis are not required for the first threshold-and-delta trial. Multi-sample persistence, moving-average filtering, or separate entry and exit thresholds should be considered only if real tests show unstable state changes. Alert cooldown is required outside the pure detector logic.

## Proposed Anomaly Types

| Type | Meaning | Initial detection method |
|---|---|---|
| normal | Reading is inside the expected range and no sudden transition is detected | Threshold and delta |
| low_light | Reading is below the provisional low threshold | Threshold |
| high_light | Reading is above the provisional high threshold | Threshold |
| sudden_drop | Current reading decreased sharply compared with the previous reading | Delta |
| sudden_rise | Current reading increased sharply compared with the previous reading | Delta |

## Detector Priority Rules

Proposed evaluation order:

1. Read the current sensor value.
2. Calculate the signed delta from the previous value.
3. Determine low-light or high-light threshold state.
4. Determine sudden-rise or sudden-drop state.
5. Return one primary anomaly result.
6. Preserve secondary diagnostic information in the result.
7. Update history.
8. Apply cooldown outside the pure detector logic.

Proposed priority:

- `low_light` or `high_light` is the primary state when a threshold is crossed.
- `sudden_drop` or `sudden_rise` is retained as an additional trigger or method when relevant.
- `sudden_drop` or `sudden_rise` may be the primary state when the current value remains within the normal threshold range.
- `normal` is returned only when no threshold or delta rule is active.

When no rule remains active, the next pure detector result returns to `normal`. Whether that recovery should produce a serial event is a separate event-policy decision.

## Proposed Detector Result Structure

The pure detector should return data rather than control hardware. The initial result should contain:

| Field | Type | Purpose |
|---|---|---|
| state | string | Primary result: `normal`, `low_light`, `high_light`, `sudden_drop`, or `sudden_rise` |
| is_anomaly | boolean | Whether the primary state is not `normal` |
| detector_method | string or null | Primary matching rule, such as `threshold` or `delta` |
| secondary_method | string or null | Additional matching rule, if any |
| value | integer | Current ADC reading |
| previous_value | integer or null | Previous ADC reading |
| delta | integer or null | Signed difference from the previous reading |
| history | array of integers | Most recent readings, limited to the configured size |
| state_before | string or null | Previous primary detector state |
| state_after | string | Current primary detector state |

The event formatter may later combine this detector result with event identifiers, timestamps, alarm status, and active configuration. Those transport fields do not belong to the pure classification responsibility.

## Proposed Configuration

| Parameter | Provisional value | Status |
|---|---:|---|
| Sample interval | 500 ms | To validate |
| Low-light threshold | 5000 | Provisional |
| High-light threshold | 32000 | Provisional |
| Sudden-change threshold | 8000 | Provisional |
| History size | 5 readings | Provisional |
| Alert cooldown | 5000 ms | Provisional |
| Buzzer pattern duration | Must remain short and bounded | To define during integration |

Thresholds and timing values must be configuration values rather than embedded throughout detector logic.

## Cooldown and Anti-Repeat Design

The detector may continue classifying every reading, but alert emission must have a separate cooldown. Remaining covered must not emit a JSON alert every sample.

A new event may be emitted when:

- the anomaly type changes
- the system returns to normal and becomes anomalous again
- the cooldown expires and a repeated-event policy allows another alert

Initial simple strategy:

- Emit an event when entering a new anomaly state.
- Do not repeatedly emit while the same anomaly remains active.
- Emit a normal or recovery event only if later considered useful.
- Keep a provisional five-second fallback cooldown for explicitly allowed repeated events.

The cooldown belongs to the alert-emission policy, not to pure detector classification. This separation allows every reading to be classified without flooding serial output or local alarms.

## Separation of Responsibilities

### Sensor acquisition

Reads GPIO 3 and returns numerical values.

### Detector

Receives values and returns structured results. It must not directly control hardware.

### Local alarm controller

Uses detector results to control RGB LED and buzzer. Alarm patterns must remain deterministic, short, bounded, and independently testable.

### Event formatter

Transforms detector results and event-policy context into JSON serial events that follow `docs/anomaly_event_schema.md`.

### Future gateway

Reads JSON events in Week 4. The detector and local alarm must continue to function when the gateway is absent.

## Initial Local-State Proposal

| Detector state | RGB LED proposal | Buzzer proposal |
|---|---|---|
| normal | Green | Off |
| low_light | Red | Short bounded alert |
| high_light | Blue | Short bounded alert |
| sudden_drop | Red or amber-like combination | Short bounded alert |
| sudden_rise | Blue or white | Short bounded alert |

Exact visual behavior will be validated during future hardware integration. This table is a proposal only and does not claim that application-level alarm logic has been implemented or tested.

## Assumptions

- GPIO 3 remains the confirmed photoresistor input.
- Baseline readings are representative of the current test environment.
- Ambient light may change in another room.
- Thresholds are configuration values, not hard-coded detector logic.
- The detector must function without a PC or LLM.
- The local alarm must remain deterministic.
- No final metric result can be claimed from the baseline alone.

## Open Questions

- Should a recovery-to-normal event be emitted?
- Should threshold anomalies take priority over delta anomalies?
- Should one event contain multiple detector methods?
- Is five seconds an appropriate alert cooldown?
- Is a 500 ms sample interval sufficient?
- Is moving-average deviation useful after initial testing?
- Should thresholds later be calibrated dynamically?

## Week 3 Validation Requirements

- [ ] Stable ambient readings remain normal
- [ ] Covered sensor produces `low_light`
- [ ] Flashlight produces `high_light`
- [ ] Ambient-to-covered transition identifies `sudden_drop`
- [ ] Ambient-to-flashlight transition identifies `sudden_rise`
- [ ] Repeated stable readings do not flood alerts
- [ ] Alert cooldown behaves predictably
- [ ] Detector results remain explainable

No validation item is complete yet. These requirements need future implementation and real-board testing.
