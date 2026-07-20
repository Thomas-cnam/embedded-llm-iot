# Week 3 Results

## Objective

Week 3 validated rule-based photoresistor anomaly detection on the ESP32-C6, a
deterministic local RGB LED and buzzer response, and compact schema version 1.0
JSON anomaly events without a gateway or local LLM dependency.

## Configuration

- Photoresistor: GPIO 3
- Buzzer: GPIO 5
- RGB red: GPIO 21
- RGB green: GPIO 11
- RGB blue: GPIO 10
- Low threshold: 5000
- High threshold: 32000
- Delta threshold: 8000
- History size: 5
- Sample interval: 500 ms
- Cooldown: 5000 ms
- Schema version: 1.0

These values are the tested Week 3 configuration, not final Week 7 benchmark
or accuracy claims.

## Raw Evidence

- `experiments/week3/raw_console_run_01.txt`
- `experiments/week3/raw_console_run_02.txt`
- `experiments/week3/labeled_results.csv`

The executed script did not print the planned `TEST_START` and `TEST_END`
markers. Both unedited captures instead have an unambiguous `DIAG` start line,
five complete phases, 60 readings, a completion line, and final cleanup. This
is a minor output-format difference, not a JSON protocol failure.

## Corrected RGB Revalidation

The operator confirmed the standalone corrected RGB sequence: red, green,
blue, white, and off all worked without a console error. During both guided
runs, normal and recovery displayed green, `low_light` displayed red, and
`high_light` displayed blue. Short bounded buzzer tones occurred for low- and
high-light alerts, and final cleanup turned all outputs off.

This physically revalidates red GPIO 21, green GPIO 11, and blue GPIO 10.

## Run 1

- Readings: 60
- Ambient: 20581 to 20677
- Covered: 3440 to 4177
- Ambient recovery: 20004 to 20180
- Phone flashlight: 36985 to 37321
- Final ambient recovery: 19412 to 20068
- JSON events: 4
- Event IDs: 1, 2, 3, 4
- Anomaly types: low light, low light, high light, high light

The first covered and flashlight readings entered their anomalies. Sample 11
in each anomalous phase emitted a controlled cooldown repeat. Other repeated
anomalies were suppressed. Recovery emitted no JSON, acquisition continued,
cleanup completed, and no unhandled error appeared.

## Run 2

- Readings: 60
- Ambient: 16147 to 16868
- Covered: 1760 to 3232
- Ambient recovery: 16564 to 16660
- Phone flashlight: 36312 to 41594
- Final ambient recovery: 16820 to 16980
- JSON events: 4
- Event IDs: 1, 2, 3, 4
- Anomaly types: low light, low light, high light, high light

Run 2 repeated the same entry, suppression, cooldown-repeat, and recovery
pattern. Cleanup completed and no unhandled error appeared.

## JSON Validation

- Total JSON event lines: 8
- Successfully parsed: 8
- Parse failures: 0
- Schema version: all events use `1.0`
- Event IDs: strictly increasing from 1 through 4 in each run
- One event per line: confirmed
- Ambient and recovery JSON suppression: confirmed
- Same-anomaly suppression: confirmed
- Cooldown repeats: one low-light and one high-light repeat per run

An event is associated with a reading only when its JSON line immediately
follows that `DIAG Sample` line. Normal and suppressed readings do not consume
event identifiers.

## Reproducibility

Both runs produced the same detector-state sequence, four-event pattern,
cooldown and recovery behavior, local alarm colors and tones, and cleanup.
Absolute ADC ranges varied between manually changed lighting conditions while
remaining on the intended side of the tested thresholds.

## Limitations

- Only two complete guided runs were recorded.
- Lighting conditions were changed manually.
- Thresholds are tied to the current environment.
- Thonny was used; no Python gateway exists yet.
- Events contain device uptime rather than PC wall-clock time.
- Schema version 1.0 does not emit recovery events.
- The executed script omitted the planned start and end markers.
- No TPR, FPR, precision, recall, F1-score, or final benchmark claim is made.

## Conclusion

The Week 3 detector, corrected local RGB and buzzer response, cooldown policy,
recovery behavior, and compact JSON pipeline are validated by two complete
real runs and host-side tests. Week 3 is satisfied. Week 4 was not started.

## Host-Side Verification

- Evidence-validator tests: 13 passed
- Complete automated suite: 142 passed, 0 failed, 0 errors
