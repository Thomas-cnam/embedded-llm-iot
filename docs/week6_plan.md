# Week 6 Plan

## Period

August 5–11, 2026

## Objective

Integrate the verified detector, serial gateway, local model, and safety validator into a controlled end-to-end pipeline. Passive mode remains the default; active actuation is enabled only for explicitly authorized, validated experiments.

## Checklist

### Integration design

- [ ] Document the end-to-end message sequence and component ownership
- [ ] Freeze compatible versions of the detector alert and command schemas
- [ ] Define passive, controlled-active, degraded, and offline operating modes
- [ ] Define timeouts, retry limits, duplicate-event handling, and cooldown behavior
- [ ] Ensure local detection and alarm remain independent of gateway or model availability
- [ ] Define an operator-controlled method for enabling and disabling active mode

### End-to-end pipeline

- [ ] Connect real ESP32 alerts to the Python gateway
- [ ] Connect validated gateway input to the selected local model
- [ ] Pass structured model output through schema and whitelist validation
- [ ] Log each pipeline stage with a shared event identifier
- [ ] Implement safe fallback for timeout, runtime failure, malformed output, and validation rejection
- [ ] Prevent duplicate or stale commands from being applied
- [ ] Keep passive reporting fully usable when active mode is disabled

### Controlled actuation

- [ ] Define a minimal set of safe demonstration commands
- [ ] Review commands, parameter limits, and test procedure before enabling active mode
- [ ] Test one validated command at a time under direct supervision
- [ ] Confirm invalid and rejected commands produce no hardware action
- [ ] Confirm the operator can stop actuation immediately
- [ ] Confirm LED and buzzer outputs return to a safe off state
- [ ] Record accepted, rejected, fallback, timeout, and disconnect scenarios

### Documentation and tests

- [ ] Add automated integration tests using mocked serial and model responses
- [ ] Run a real-board passive end-to-end test
- [ ] Run approved controlled-active tests only after passive validation
- [ ] Document setup, operating modes, shutdown, and recovery procedures
- [ ] Record evidence and remaining limitations in `LOG.md`

## Deliverables

- Integrated required pipeline with passive mode as the default
- Traceable end-to-end event logs
- Safe fallback and recovery behavior
- Controlled actuation evidence for the minimal whitelist, if approved
- Operator and demonstration instructions

## Definition of Done

- [ ] A real sensor event travels through the complete passive pipeline
- [ ] Every stage is traceable through a shared event identifier
- [ ] Invalid, late, duplicate, or unavailable model output causes no unsafe action
- [ ] Local detector and alarm continue when the gateway or model is unavailable
- [ ] Any active test uses only validated whitelisted commands and documented limits
- [ ] Safe shutdown and recovery are demonstrated and documented

## Adjustment Notes

If controlled actuation cannot be demonstrated safely, complete Week 6 with the passive end-to-end pipeline and documented validator decisions. Active actuation is subordinate to safety and must not delay benchmarking or final delivery.

## Out of Scope

- Unrestricted model control
- Optional sensors or wireless transport before the required pipeline is stable
- New model exploration without a clear Week 7 measurement need
- Final report formatting
