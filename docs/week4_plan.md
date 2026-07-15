# Week 4 Plan

## Period

July 22–28, 2026

## Objective

Create a reliable Python serial gateway and obtain the first passive response from a carefully selected local LLM runtime and model. No model output may control hardware during this week.

## Checklist

### Serial protocol and gateway

- [ ] Review and freeze the Week 3 alert schema version used by the gateway
- [ ] Document supported serial settings and connection procedure
- [ ] Create a Python environment and dependency record for the gateway
- [ ] Implement serial connection, line framing, timeout, and reconnection behavior
- [ ] Parse incoming JSON without trusting missing or extra fields
- [ ] Preserve the original alert and gateway timestamp in logs
- [ ] Separate serial input, validation, logging, and model-client responsibilities
- [ ] Add a mock-input path for development without the board
- [ ] Add automated tests for valid, malformed, partial, and unrelated serial lines

### Local runtime and model selection

- [ ] Record laptop operating system, CPU, RAM, and available storage relevant to local inference
- [ ] Compare feasible local runtime candidates and document the selection rationale
- [ ] Treat Ollama as the preferred candidate, not a preselected final decision
- [ ] Select one or more small local model candidates based on hardware limits and licensing
- [ ] Record runtime version, model name, model size, source, and configuration
- [ ] Install only the selected runtime and models after documenting the decision
- [ ] Verify that local inference works without a cloud API

### First passive response

- [ ] Convert a validated ESP32 alert into a clearly delimited model input
- [ ] Request a passive diagnostic or reporting response only
- [ ] Log prompt version, input alert, model identity, response, and timing
- [ ] Process at least one real ESP32 alert through the complete passive path
- [ ] Confirm that model failure or timeout does not affect local detector operation
- [ ] Document setup, test evidence, limitations, and unresolved issues

## Deliverables

- Python serial gateway with reproducible setup instructions
- Versioned alert-ingestion and logging behavior
- Runtime/model selection record
- Log showing one real ESP32 alert processed by a local model
- Tests for serial framing and invalid input handling

## Definition of Done

- [ ] The gateway reconnects or exits safely after serial interruption
- [ ] Valid alerts are parsed and logged; malformed input is rejected and recorded
- [ ] A selected local model produces a passive response to a real alert
- [ ] Runtime, model, prompt version, and timing are traceable in the log
- [ ] No model response can trigger ESP32 actuation
- [ ] Setup can be repeated from repository documentation

## Adjustment Notes

If local inference performance is insufficient, preserve the working serial gateway and reduce model size or prompt complexity. Record any runtime or model change in `LOG.md`. Do not delay the required passive pipeline for broad model exploration.

## Out of Scope

- Active model-generated hardware commands
- Final prompt optimization
- Final safety parser and whitelist
- Full benchmarking campaign
- Optional network transport
