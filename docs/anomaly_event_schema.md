# Anomaly Event Schema

## Purpose

This document defines the planned JSON event format emitted by the ESP32-C6 anomaly detector over USB serial. The format is designed for the future Week 4 Python gateway.

Schema version 1.0 is implemented by the pure
`AnomalyEventFormatter` and validated with host-side tests. The finite guided
hardware script now conditionally prints formatted events one object per line,
but this update has not been run on MicroPython. Real JSON capture and the
gateway parser are not implemented or validated yet.

## Transport Rule

- One JSON object per serial line
- UTF-8 text
- No explanatory text on the same line as an event
- Diagnostic text, if retained during development, must be clearly separated from JSON event lines
- The gateway must later ignore non-JSON lines safely

The formatter returns compact JSON without a newline. The guided hardware
script prints that string only when an alert is emitted; `print()` adds one line
ending. Diagnostic lines begin with `DIAG`, while JSON event lines contain only
the object. Pretty-printed multi-line JSON must not be used.

## Proposed Event Types

- `anomaly`
- `recovery`
- `status`
- `error`

Only `anomaly` is implemented by the current formatter. The other event types
remain optional until their behavior is justified and documented.

## Proposed Anomaly Types

- `low_light`
- `high_light`
- `sudden_drop`
- `sudden_rise`

## Schema 1.0 Fields

| Field | Type | Description |
|---|---|---|
| schema_version | string | Version of the event schema |
| event_id | integer | Incrementing event identifier |
| event_type | string | Event category, initially `anomaly` |
| sensor | string | Sensor identifier, initially `photoresistor` |
| anomaly_type | string | Main anomaly classification |
| detector_method | string | Main rule that triggered the event |
| value | integer | Current sensor value |
| previous_value | integer or null | Previous sensor value |
| delta | integer or null | Signed difference from previous value |
| history | array of integers | Recent sensor readings |
| timestamp_ms | integer | Monotonic time from the ESP32 |
| local_alarm | boolean | Whether the local alarm was triggered |

The formatter also includes these detector and policy context fields in every
emitted event:

| Field | Type | Description |
|---|---|---|
| low_threshold | integer | Active low-light threshold |
| high_threshold | integer | Active high-light threshold |
| delta_threshold | integer | Active sudden-change threshold |
| secondary_method | string or null | Additional rule that also matched |
| state_before | string or null | Previous detector state |
| state_after | string | New detector state |
| cooldown_active | boolean | Whether alert cooldown is active |

## Example Low-Light Event

The following object is a representative host-test example. It is not captured
output from the ESP32-C6:

```json
{
  "schema_version": "1.0",
  "event_id": 1,
  "event_type": "anomaly",
  "sensor": "photoresistor",
  "anomaly_type": "low_light",
  "detector_method": "threshold",
  "value": 48,
  "previous_value": 24320,
  "delta": -24272,
  "history": [24310, 24290, 24340, 24320, 48],
  "timestamp_ms": 18250,
  "local_alarm": true,
  "low_threshold": 5000,
  "high_threshold": 32000,
  "delta_threshold": 8000,
  "secondary_method": "sudden_drop",
  "state_before": "normal",
  "state_after": "low_light",
  "cooldown_active": false
}
```

## Field Semantics

- `schema_version` begins at the provisional value `1.0` and changes when compatibility changes.
- `event_id` increments only for emitted events. It starts at 1 by default and
  restarts at the configured starting identifier for a new or reset formatter.
- `timestamp_ms` is monotonic device time, not wall-clock time.
- `detector_method` identifies the primary rule, such as `threshold` or `delta`.
- `secondary_method` preserves an additional matching rule without replacing the primary anomaly type.
- `history` contains no more than the configured recent-history size.
- `local_alarm` reports whether the separate alarm controller was triggered for this event.
- Threshold fields report the active provisional configuration used for the decision.

## Future Validation Rules

The Week 4 gateway should later:

- parse each event as JSON data, never executable code
- require all mandatory fields and expected types
- reject unsupported schema versions safely
- accept only documented event and anomaly values
- reject invalid numerical types and malformed history arrays
- retain signed `delta` values
- log the original line and validation outcome
- ignore or record diagnostic non-JSON lines without crashing
- avoid assuming that `timestamp_ms` is a wall-clock timestamp
- tolerate device restart or monotonic timer wrap according to a documented policy

These are future gateway requirements only. No parser is implemented by this design task.

## Versioning and Compatibility

- Schema version `1.0` is provisional until the first real Week 3 event is implemented and reviewed.
- New optional fields may be added without changing existing field meaning.
- Renaming, removing, or changing the type of a required field requires a schema-version change.
- The selected Week 3 schema should be frozen before Week 4 gateway implementation.
- Major changes and their reasons must be recorded in `LOG.md`.

## Current Decisions and Open Questions

- Only `anomaly` events are emitted by the first implementation; recovery
  events remain optional.
- `event_id` starts at 1 by default and restarts with a new formatter instance.
- Detector configuration is included in every schema version 1.0 anomaly event.
- One primary method and one optional `secondary_method` are retained by schema
  version 1.0.
- How should timer wrap and device restart be represented for gateway traceability?

The schema and end-to-end pipeline passed host-side tests. Four real schema
version 1.0 events were captured from MicroPython on 2026-07-19 and parsed
successfully. They contained separator spaces because of the device's `ujson`
behavior, so a compatibility correction was added to the formatter. A repeat
capture produced four parseable compact events with no separator spaces.
Compact schema version 1.0 hardware output is therefore validated for the
finite guided test.
