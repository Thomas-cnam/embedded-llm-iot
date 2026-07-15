# Week 5 Plan

## Period

July 29–August 4, 2026

## Objective

Create stable, versioned prompt designs and a strict safety-validation layer for any structured local-model output. Passive reporting remains the default, and unvalidated output must never reach the ESP32-C6.

## Checklist

### Prompt design

- [ ] Define separate prompt goals for passive reporting and structured command proposals
- [ ] Create version identifiers and a change log for prompt revisions
- [ ] Clearly delimit untrusted sensor and alert content
- [ ] Instruct the model to return only the requested response format
- [ ] Define a safe fallback response for uncertainty or insufficient context
- [ ] Build a representative prompt test set from real alerts and controlled malformed inputs
- [ ] Compare prompt variants using the metrics in `experimental_metrics_plan.md`
- [ ] Select and document a stable prompt version for Week 6

### Command schema and whitelist

- [ ] Define the smallest command schema required for the demonstration
- [ ] Define an explicit whitelist of allowed command names and parameters
- [ ] Define types, ranges, duration limits, and required fields
- [ ] Reject unknown fields, unknown commands, invalid types, and out-of-range values
- [ ] Define passive-only and active-command operating modes
- [ ] Document which component has authority to enable active mode

### Safety parser

- [ ] Parse model output as data rather than executable code
- [ ] Reject natural-language text when structured JSON is required
- [ ] Reject malformed JSON, duplicate or missing fields, and nested unexpected content
- [ ] Apply schema validation before whitelist validation
- [ ] Produce explicit accepted, rejected, and safe-fallback outcomes
- [ ] Log validation reason without storing secrets
- [ ] Add automated tests for every accepted command form
- [ ] Add automated rejection tests for malformed, adversarial, and prompt-injection-like outputs
- [ ] Confirm rejected output cannot be forwarded to the board

## Deliverables

- Versioned prompt specification and evaluation set
- Minimal structured command schema
- Explicit whitelist and parameter constraints
- Strict parser/validator with automated positive and negative tests
- Safety behavior documentation and Week 5 evidence in `LOG.md`

## Definition of Done

- [ ] A stable prompt version is selected using documented evidence
- [ ] Every allowed command and parameter is explicitly listed
- [ ] Valid output is parsed deterministically
- [ ] Invalid, ambiguous, or unexpected output is rejected with a safe fallback
- [ ] Automated tests cover accepted and rejected classes
- [ ] No active command has been sent to the ESP32-C6 during parser development

## Adjustment Notes

Keep the command surface deliberately small. If structured output remains unreliable, retain passive reporting as the required deliverable and treat active command generation as optional. Safety validation must not be weakened to improve acceptance rate.

## Out of Scope

- Unrestricted natural-language actuation
- Dynamic code execution
- Commands outside the documented whitelist
- Full end-to-end actuation experiments
- Final benchmark conclusions
