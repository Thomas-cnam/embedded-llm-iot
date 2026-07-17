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

- [ ] Integrate the configurable sample interval
- [ ] Investigate optional moving-average deviation if hardware tests require it
- [ ] Connect real GPIO 3 sensor acquisition to the integration controller
- [x] Create finite or safely stoppable hardware integration test code
- [ ] Integrate deterministic RGB LED and buzzer alarm behavior
- [ ] Ensure local detection and alarm operation do not depend on a laptop connection
- [ ] Define a versioned structured JSON alert format
- [ ] Include sufficient alert fields for traceability, such as detector version, sensor value, state, and device uptime
- [ ] Ensure normal sensor output cannot accidentally produce malformed protocol messages
- [ ] Implement JSON serialization and one-event-per-line serial output
- [ ] Add concise firmware documentation and usage instructions

The alert policy and local-alarm integration passed host-side simulated tests. Physical ESP32-C6 integration, JSON formatting, and serial output remain pending. The pure detector and simulated local-alarm layers are implemented, but their thresholds, timing, RGB states, and buzzer behavior still require real hardware validation.

A finite guided hardware-integration script is now prepared and documented.
It has not been executed, so real sensor acquisition, RGB and buzzer behavior,
cooldown, recovery, and continued acquisition remain unchecked until the
manual Thonny test is completed.

### Verification

- [ ] Test normal ambient-light behavior on the real board
- [ ] Test covered-sensor events on the real board
- [ ] Test strong-light events on the real board
- [ ] Test transitions between conditions and detector reset behavior
- [ ] Confirm RGB LED and buzzer responses are finite and deterministic
- [ ] Confirm sensor acquisition continues after a physical alarm
- [ ] Capture structured alerts from the MicroPython console
- [ ] Record test conditions, observations, and unresolved issues in `LOG.md`
- [ ] Save labeled Week 3 test evidence without overwriting Week 2 raw data

## Deliverables

- Rule-based detector module and controlled test/application entry point
- Documented detector behavior and selected parameters
- Versioned structured JSON alert specification
- Real-board test evidence for normal and anomalous scenarios
- Updated firmware documentation and `LOG.md`

## Definition of Done

- [ ] The detector runs on the ESP32-C6 using the confirmed GPIO 3 sensor input
- [ ] Local RGB LED and buzzer alarms work without the gateway or local LLM
- [ ] Normal and anomalous scenarios produce reproducible, documented behavior
- [ ] Each detected event emits parseable structured JSON with the required fields
- [ ] Detector limitations and calibration decisions are documented
- [ ] No gateway or LLM dependency has been introduced into the detector

## Adjustment Notes

Prefer the simplest detector supported by measured data. If Week 3 evidence shows that the initial method is unstable, adjust filtering or persistence rules and record the reason in `LOG.md`. Do not expand to optional sensors until the required photoresistor path is reliable.

## Out of Scope

- Python gateway implementation
- Local LLM installation or prompting
- Model-generated actuation
- Optional sensor integration
- Final benchmarking claims
