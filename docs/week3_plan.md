# Week 3 Plan

## Period

July 15–21, 2026

## Objective

Build and validate a simple rule-based photoresistor anomaly detector on the ESP32-C6. The detector must remain independent of the future gateway and local LLM, provide a deterministic local response, and emit a documented structured alert.

## Checklist

### Detector design

- [ ] Review the Week 2 baseline dataset and document its measurement conditions
- [ ] Define normal and anomalous test scenarios before implementation
- [ ] Define the detector input, state, output, and reset behavior
- [ ] Select and justify a simple rule-based detection method
- [ ] Define how candidate parameters will be calibrated without using final evaluation trials
- [ ] Decide whether filtering, persistence, hysteresis, or cooldown behavior is required
- [ ] Document all selected detector parameters and assumptions

### Firmware implementation

- [ ] Create a reusable detector module without changing verified peripheral behavior
- [ ] Create finite or safely stoppable detector test code
- [ ] Integrate deterministic RGB LED and buzzer alarm behavior
- [ ] Ensure local detection and alarm operation do not depend on a laptop connection
- [ ] Define a versioned structured JSON alert format
- [ ] Include sufficient alert fields for traceability, such as detector version, sensor value, state, and device uptime
- [ ] Ensure normal sensor output cannot accidentally produce malformed protocol messages
- [ ] Add concise firmware documentation and usage instructions

### Verification

- [ ] Test normal ambient-light behavior on the real board
- [ ] Test covered-sensor events on the real board
- [ ] Test strong-light events on the real board
- [ ] Test transitions between conditions and detector reset behavior
- [ ] Confirm RGB LED and buzzer responses are finite and deterministic
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
