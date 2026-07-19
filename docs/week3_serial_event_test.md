# Week 3 Serial Event Test

## Purpose

The JSON-enabled version of
`firmware/tests/test_anomaly_hardware_integration.py` connects the existing
photoresistor, detector, alert policy, local alarm, integration controller, and
schema version 1.0 event formatter.

This version is prepared for a later manual Thonny run. It has not been run on
the ESP32-C6, and this document contains no invented MicroPython output.

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

- New end-to-end event-pipeline tests: 11 passed
- Previous tests: 113 still passed
- Complete suite: 124 passed, 0 failed, 0 errors

The host tests confirm event emission, normal and suppressed silence, cooldown
repeat identifiers, recovery silence, compact JSON, local-alarm reporting, and
a representative normal-to-low-to-recovery-to-high sequence.

## Pending Validation

- Run the JSON-enabled script manually in Thonny.
- Capture real compact JSON lines from MicroPython.
- Validate repeated physical scenarios.
- Save labeled raw Week 3 evidence.
- Review results before closing Week 3.

Gateway, LLM, whitelist, and gateway-to-board command work remain out of scope.
