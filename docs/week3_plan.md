# Week 3 Plan

## Period

July 15–21, 2026

## Objective

Build and validate a simple rule-based photoresistor anomaly detector on the ESP32-C6. The detector must remain independent of the future gateway and local LLM, provide a deterministic local response, and emit a documented structured alert.

## Checklist

### Detector design

- [x] Review the Week 2 baseline dataset and document its measurement conditions
- [x] Define normal and anomalous test scenarios before implementation
- [x] Define the detector input, state, output, and reset behavior
- [x] Select and justify a simple rule-based detection method
- [x] Define how candidate parameters will be calibrated without using final evaluation trials
- [x] Decide whether filtering, persistence, hysteresis, or cooldown behavior is required
- [x] Document all selected detector parameters and assumptions

Design decisions and all provisional values are documented in `anomaly_detector_design.md`. The planned serial event contract is documented separately in `anomaly_event_schema.md`. No implementation or hardware-verification item is complete yet.

### Firmware implementation

- [x] Create a reusable anomaly detector module without changing verified peripheral behavior
- [x] Implement threshold crossing
- [x] Implement low-light detection
- [x] Implement high-light detection
- [x] Implement sudden delta detection
- [x] Maintain recent-reading history
- [x] Add configurable low-light and high-light thresholds
- [x] Add a configurable sudden-change limit
- [x] Add clear structured detector result types
- [x] Keep the pure detector compatible with MicroPython and standard Python

#### Simulated alert policy and local-alarm logic

- [x] Implement cooldown or anti-repeat behavior outside the pure detector
- [x] Define the provisional normal RGB state
- [x] Define the provisional low-light alarm state
- [x] Define the provisional high-light alarm state
- [x] Define the provisional sudden-change alarm states
- [x] Add short bounded buzzer patterns through the existing `tone()` API
- [x] Bound every proposed buzzer duration
- [x] Ensure buzzer shutdown through finite tones, normal state, and cleanup
- [x] Restore the expected normal LED and buzzer state during recovery
- [x] Keep local-alarm logic independent from the PC and LLM
- [x] Add deterministic best-effort cleanup
- [x] Document cooldown behavior
- [x] Document provisional local-alarm behavior

#### Pending hardware and event integration

- [x] Integrate the configurable sample interval
- [ ] Investigate optional moving-average deviation if hardware tests require it
- [x] Connect real GPIO 3 sensor acquisition to the integration controller
- [x] Create finite or safely stoppable hardware integration test code
- [x] Integrate deterministic RGB LED and buzzer alarm behavior
- [ ] Ensure local detection and alarm operation do not depend on a laptop connection
- [x] Define a versioned structured JSON alert format
- [x] Include sufficient alert fields for traceability, such as detector version, sensor value, state, and device uptime
- [x] Ensure normal sensor output cannot accidentally produce malformed protocol messages
- [x] Implement JSON serialization and one-event-per-line serial output
- [x] Add concise firmware documentation and usage instructions

The alert policy and local-alarm integration passed host-side simulated tests,
and the first physical ESP32-C6 integration test ran on 2026-07-17. Detector,
sensor, buzzer, cooldown, and cleanup behavior have real-board evidence. The
supervisor later corrected the RGB red/blue mapping, so the corrected named RGB
states required a short physical repeat. That repeat was completed manually on
2026-07-20 with the corrected mapping.

The finite guided hardware-integration script was run manually on 2026-07-17.
Real sensor acquisition, buzzer behavior, cooldown, recovery, continued
acquisition, and final cleanup were confirmed. The historical RGB observations
used the old red/blue interpretation and are preserved, but corrected color
validation was subsequently completed. JSON formatting and serial output were
validated in the two complete captures documented in `week3_results.md`.

#### Pure anomaly-event formatting

- [x] Create a MicroPython-compatible schema version 1.0 event formatter
- [x] Build events only when the alert policy requests emission
- [x] Return no event for normal and suppressed readings
- [x] Assign incrementing event identifiers only to emitted events
- [x] Serialize events as compact single-object JSON strings
- [x] Keep formatting independent from hardware and serial transport
- [x] Reject malformed integration results without silently repairing them
- [x] Add host-side formatter tests
- [x] Document formatter behavior and restart limitations

The pure formatter passes 38 dedicated host tests, the 77 detector and
integration tests still pass, and the 11 event-pipeline tests pass. The complete
suite now contains 142 passing tests after adding RGB pin-mapping and Week 3
evidence-validation coverage.
The formatter now has two real MicroPython captures. The second capture
validates compact output; corrected physical RGB observations are confirmed.

#### JSON-enabled guided pipeline

- [x] Integrate `AnomalyEventFormatter` into the finite guided hardware script
- [x] Print emitted events as standalone compact JSON lines
- [x] Prefix diagnostic output so it is distinct from JSON event lines
- [x] Emit no JSON for normal, recovery, or suppressed readings
- [x] Add host-side end-to-end event-pipeline tests
- [x] Prepare a labeled Week 3 evidence folder and CSV template
- [x] Document the manual serial-event test procedure
- [x] Run the JSON-enabled script on the ESP32-C6
- [x] Capture real JSON event lines from Thonny
- [x] Complete repeated hardware sensor and JSON scenarios
- [x] Save populated labeled Week 3 evidence

The first JSON-enabled run captured 60 samples and four valid schema version
1.0 events on 2026-07-19. It also exposed default `ujson` separator spaces. A
minimal compatibility correction now passes 38 formatter tests, and the
complete suite contains 126 passing tests. The corrected compact output was
then validated in run 2.

The corrected repeat run captured another 60 samples and four events. All
events were compact and parseable, and the expected normal, low-light,
high-light, suppression, cooldown, and recovery behavior repeated. Explicit
physical LED and buzzer behavior was confirmed by the operator.

### Verification

- [x] Test normal ambient-light behavior on the real board
- [x] Test covered-sensor events on the real board
- [x] Test strong-light events on the real board
- [x] Test transitions between conditions and detector reset behavior
- [x] Confirm buzzer responses are finite and deterministic
- [x] Revalidate RGB LED colors with red GPIO 21, green GPIO 11, and blue GPIO 10
- [x] Confirm sensor acquisition continues after a physical alarm
- [x] Capture structured alerts from the MicroPython console
- [x] Record test conditions, observations, and unresolved issues in `LOG.md`
- [x] Save labeled Week 3 test evidence without overwriting Week 2 raw data

## Deliverables

- Rule-based detector module and controlled test/application entry point
- Documented detector behavior and selected parameters
- Versioned structured JSON alert specification
- Real-board test evidence for normal and anomalous scenarios
- Updated firmware documentation and `LOG.md`

## Definition of Done

- [x] The detector runs on the ESP32-C6 using the confirmed GPIO 3 sensor input
- [x] Local buzzer alarms work without the gateway or local LLM
- [x] Corrected local RGB LED colors are physically validated without the gateway or local LLM
- [x] Normal and anomalous scenarios produce reproducible, documented behavior
- [x] Each detected event emits parseable structured JSON with the required fields
- [x] Detector limitations and calibration decisions are documented
- [x] No gateway or LLM dependency has been introduced into the detector

## Adjustment Notes

Prefer the simplest detector supported by measured data. If Week 3 evidence shows that the initial method is unstable, adjust filtering or persistence rules and record the reason in `LOG.md`. Do not expand to optional sensors until the required photoresistor path is reliable.

Moving-average deviation was not implemented because threshold and delta
detection were stable during the documented Week 3 runs.

## RGB Mapping Correction

On 2026-07-20, the supervisor confirmed that the PCB red and blue silkscreen
labels are swapped. Current code uses red GPIO 21, green GPIO 11, and blue GPIO
10. Earlier raw output and journal entries remain unchanged as historical
evidence. Photoresistor, buzzer, detector, cooldown, cleanup, and JSON results
are unaffected. Corrected named RGB colors were manually revalidated on
2026-07-20.

## Completion

Week 3 is complete. Two raw 60-reading runs, 120 labeled rows, eight valid
schema version 1.0 events, corrected RGB observations, buzzer behavior,
cooldown, recovery, and cleanup are documented in `week3_results.md`.

## Out of Scope

- Python gateway implementation
- Local LLM installation or prompting
- Model-generated actuation
- Optional sensor integration
- Final benchmarking claims
