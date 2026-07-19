# Anomaly Event Formatter

## Purpose

`firmware/anomaly/event_formatter.py` transforms the combined dictionary from
`AnomalyIntegrationController.process()` into a schema version 1.0 anomaly
event. It is pure formatting logic: it does not read hardware, control alarms,
print output, or perform serial transport.

The formatter is compatible with MicroPython and standard Python. It prefers
`ujson` when available and otherwise uses the standard `json` module.

## Public API

### Construction

```python
from anomaly.event_formatter import AnomalyEventFormatter

formatter = AnomalyEventFormatter(
    schema_version="1.0",
    starting_event_id=1,
)
```

The schema version must be a non-empty string. The starting identifier must be
a non-negative integer; boolean values are rejected.

### Build an event dictionary

```python
event = formatter.build_event(integration_result)
```

An event is returned only when
`policy_decision["should_emit_alert"]` is `True`. Normal readings, recovery
results, and repeated anomalies suppressed by cooldown return `None` and do not
consume an event identifier.

### Serialize an event

```python
event_text = formatter.serialize_event(integration_result)
```

This returns one compact JSON object string or `None`. The string contains no
line break. A future transport layer may print the returned string followed by
one newline, but that transport behavior is intentionally not implemented in
the formatter.

### Reset identifiers

```python
formatter.reset()
```

Reset restores the next identifier to the constructor's
`starting_event_id`. With the default configuration, a new formatter instance
or a reset starts again at event identifier 1. A future gateway must therefore
not assume that identifiers remain unique across device restarts.

## Event Contents

Every emitted event contains:

- schema version, event identifier, event type, and sensor name;
- anomaly type and detector method;
- current value, previous value, signed delta, and copied history;
- monotonic device timestamp;
- whether the local alarm was successfully triggered;
- active low, high, and delta thresholds;
- secondary method and detector states;
- cooldown state from the policy decision.

The formatter does not modify the supplied integration result. In particular,
the history array is copied into the event.

## Validation

Malformed integration results are rejected with `TypeError` or `ValueError`.
Validation includes:

- required top-level, detector, and policy fields;
- strict booleans and integers, excluding booleans from integer fields;
- supported anomaly types and detector methods;
- ADC value and history ranges;
- consistency between current value, previous value, and delta;
- detector-state consistency;
- valid threshold ordering;
- non-negative monotonic timestamp values;
- consistency between an emission request and an anomalous detector result.

The formatter does not silently supply, coerce, or repair malformed values.

## Host Validation

Validation date: 2026-07-19

```powershell
py -B -m unittest discover -s tests -p "test_anomaly_event_formatter.py" -v
py -B -m unittest discover -s tests -p "test_*.py"
```

Results:

- Event-formatter tests: 38 passed, 0 failed, 0 errors
- Previous detector and integration tests: 77 still passed
- Event-pipeline tests: 11 passed, 0 failed, 0 errors
- Complete suite: 126 passed, 0 failed, 0 errors

Covered scenarios include constructor validation, complete schema fields,
incrementing identifiers, reset behavior, normal and suppressed results,
compact JSON, real integration-controller results, copied history, and
malformed nested data.

## MicroPython Compatibility Finding

The first real JSON-enabled run on 2026-07-19 showed that the available
MicroPython `ujson.dumps()` inserted spaces after separators. The output was
valid JSON but did not satisfy the intended compact representation.

The formatter now removes whitespace only while outside JSON strings after
serialization. Spaces and escaped characters inside strings remain unchanged.
This keeps compatibility with `ujson` variants that do not provide a
`separators` argument. The correction passes host tests but still requires a
repeat MicroPython capture.

## Scope and Limitations

- No ESP32-C6, COM3, Thonny, or `mpremote` access occurred.
- One MicroPython console capture exists, but it predates the compact-output
  compatibility correction.
- One-event-per-line printing is implemented by the finite guided script, not
  by this pure formatter.
- No gateway, LLM, or whitelist code is present.
- Recovery events are not emitted; only requested anomaly alerts are formatted.
- Schema version 1.0 remains provisional until real MicroPython JSON output is
  captured and reviewed.
