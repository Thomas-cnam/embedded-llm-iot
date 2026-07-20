# Week 3 Serial Event Test

## Purpose

The JSON-enabled version of
`firmware/tests/test_anomaly_hardware_integration.py` connects the existing
photoresistor, detector, alert policy, local alarm, integration controller, and
schema version 1.0 event formatter.

The first JSON-enabled run was performed manually on 2026-07-19. Its complete
console output and mechanically parsed sample data are stored under
`experiments/week3/`. A compact-output compatibility correction was prepared
after that run and validated by the second capture documented below.

## Output Separation

The console uses two unambiguous line types:

- diagnostic lines begin with `DIAG`;
- emitted anomaly events are compact JSON objects printed alone on lines that
  begin with `{` and end with `}`.

Blank separator lines may appear between phases. No JSON line is printed for a
normal reading, a recovery, or an anomaly suppressed by cooldown.

The pure formatter returns JSON without a newline. The script's `print()` call
adds exactly one line ending, keeping one event per line. No serial library or
transport abstraction is used.

## Required Device Files

The current supervisor-confirmed RGB mapping is red GPIO 21, green GPIO 11,
and blue GPIO 10. The PCB red and blue silkscreen labels are swapped.

Before the manual test, upload the current package directories to the device
root:

- `/anomaly`, including `event_formatter.py`;
- `/peripherals`.

Open the test script from the local repository in Thonny. Do not save it as
`main.py` and do not configure automatic execution at boot.

## Guided Test Procedure

The existing finite five-phase sequence is unchanged:

1. ambient room light;
2. fully covered sensor;
3. ambient-light recovery;
4. phone flashlight;
5. final ambient-light recovery.

Each phase collects 12 readings at a provisional 500 ms interval after a
five-second setup countdown. Follow every instruction and keep each condition
steady during acquisition.

## Expected Logical Checks

During the run, verify that:

- ambient and recovery samples print diagnostics but no JSON event;
- the first emitted anomaly alert prints one JSON object;
- repeated samples suppressed during cooldown print no JSON event;
- a cooldown repeat prints a new event with the next identifier;
- a change to a different anomaly can emit immediately;
- every JSON line parses as one object and contains the schema version 1.0
  fields;
- RGB LED and buzzer behavior remains bounded and correct;
- acquisition continues after local alarms;
- Ctrl+C, completion, or an exception still reaches safety cleanup.

The exact number and types of events depend on real sensor transitions. They
must be recorded from the actual run rather than predicted as evidence.

## Evidence Capture

1. Preserve the complete Thonny console output without editing it.
2. Save it under `experiments/week3/` using a dated run identifier.
3. Copy `experiments/week3/labeled_results_template.csv` to a dated results
   file.
4. Record every sample and whether a JSON event appeared immediately after it.
5. Record observed RGB colors and buzzer sounds.
6. Keep failed or interrupted attempts as separate runs when they contain
   useful evidence.
7. Never overwrite Week 2 baseline data or an earlier Week 3 run.

## Host-Side Preparation Result

Preparation date: 2026-07-19

- Event-pipeline tests: 11 passed
- Event-formatter tests after the compatibility correction: 38 passed
- Detector and integration tests: 77 passed
- Complete suite: 126 passed, 0 failed, 0 errors

The host tests confirm event emission, normal and suppressed silence, cooldown
repeat identifiers, recovery silence, compact JSON, local-alarm reporting, and
a representative normal-to-low-to-recovery-to-high sequence.

## First Real Capture

Run date: 2026-07-19

| Phase | Samples | Minimum | Maximum | Average | JSON events |
|---|---:|---:|---:|---:|---:|
| Ambient | 12 | 25942 | 26070 | 25992.7 | 0 |
| Covered | 12 | 4305 | 4817 | 4529.0 | 2 |
| Ambient recovery | 12 | 25286 | 25398 | 25339.3 | 0 |
| Phone flashlight | 12 | 38105 | 38473 | 38274.3 | 2 |
| Final ambient recovery | 12 | 25110 | 25318 | 25208.7 | 0 |

Observed event sequence:

1. `low_light`, entered anomaly, value 4817, timestamp 15547 ms;
2. `low_light`, cooldown repeat, value 4497, timestamp 20815 ms;
3. `high_light`, entered anomaly, value 38105, timestamp 37117 ms;
4. `high_light`, cooldown repeat, value 38137, timestamp 42389 ms.

All four event lines parsed as schema version 1.0 JSON and reported
`local_alarm: true`. Normal, recovery, and suppressed readings produced no JSON
line. Event identifiers were continuous from 1 through 4, acquisition continued
after each event, and final cleanup completed without a console error.

The capture exposed one compatibility issue: MicroPython `ujson.dumps()` used
spaces after commas and colons by default. The events were valid one-line JSON,
but not maximally compact. `AnomalyEventFormatter` now removes JSON whitespace
outside string values in a MicroPython-compatible way. Two additional tests
verify that spaces and escaped characters inside strings remain unchanged.

The operator has not yet confirmed the physical LED colors and buzzer sounds
for this specific run, so those evidence fields remain empty.

## Corrected Repeat Capture

Run date: 2026-07-19, run 2

| Phase | Samples | Minimum | Maximum | Average | JSON events |
|---|---:|---:|---:|---:|---:|
| Ambient | 12 | 10610 | 10962 | 10879.3 | 0 |
| Covered | 12 | 704 | 1392 | 790.7 | 2 |
| Ambient recovery | 12 | 10834 | 10914 | 10867.3 | 0 |
| Phone flashlight | 12 | 38969 | 41546 | 39995.9 | 2 |
| Final ambient recovery | 12 | 10546 | 10706 | 10656.7 | 0 |

Observed event sequence:

1. `low_light`, entered anomaly, value 1392, timestamp 15547 ms;
2. `low_light`, cooldown repeat, value 736, timestamp 20815 ms;
3. `high_light`, entered anomaly, value 38969, timestamp 37127 ms;
4. `high_light`, cooldown repeat, value 40553, timestamp 42396 ms.

All four events parsed successfully, contained the required schema version 1.0
fields, used continuous identifiers 1 through 4, and contained no spaces after
JSON separators. No JSON was emitted for normal, recovery, or suppressed
readings. Acquisition continued after every event and cleanup completed without
a console error.

The lower ambient values compared with run 1 show that room-light conditions
can vary substantially. Despite that variation, all ambient values remained
between the provisional low and high thresholds, covered values remained below
the low threshold, and flashlight values remained above the high threshold in
both runs.

Physical RGB and buzzer observations for run 2 still require explicit operator
confirmation.

The preserved raw captures print the old RGB order `GPIO 10 11 21` because
they were produced before the supervisor correction. This historical line must
not be edited. It does not affect the captured ADC values, detector decisions,
cooldown behavior, buzzer actions, or JSON events.

## Pending Validation

- Repeat and confirm physical RGB LED colors with red GPIO 21, green GPIO 11,
  and blue GPIO 10; confirm buzzer sounds during that run.
- Review results before closing Week 3.

Gateway, LLM, whitelist, and gateway-to-board command work remain out of scope.
