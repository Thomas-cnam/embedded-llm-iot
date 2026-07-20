# Project Roadmap

This roadmap translates the internship assignment into practical weekly milestones. It is a working plan rather than a rigid specification. It may evolve when experiments reveal technical limitations, unexpected results, or better implementation choices. Any major change should be documented in LOG.md.

## Current Status

- [x] Week 1 — Repository setup and initial hardware bring-up
- [x] Week 2 — Hardware consolidation and photoresistor baseline
- [x] Week 3 — Edge anomaly detector
- [ ] Week 4 — Python gateway and first local LLM response
- [ ] Week 5 — Prompt engineering and safety parser
- [ ] Week 6 — Safe end-to-end integration
- [ ] Week 7 — Experimental benchmarking
- [ ] Week 8 — Final report, cleanup, presentation, and submission
- [ ] August 26–29 — Final safety buffer and submission verification

## Milestones

| Period | Milestone | Main outcome | Status |
|---|---|---|---|
| Weeks 1–2 | M1.1 Hardware bring-up | Main peripherals verified and sensor baseline recorded | Completed |
| Week 3 | M1.2 Edge anomaly detector | Detector triggers local alarm and emits structured alert | Completed |
| Week 4 | M1.3 Gateway and local LLM setup | First ESP32 alert processed by a local model | Pending |
| Week 5 | M1.4A Prompt engineering and safety parser | Stable prompts, schema, whitelist, and validation | Pending |
| Week 6 | M1.4B Safe end-to-end integration | Complete safe pipeline and actuation experiments | Pending |
| Week 7 | M1.5 Benchmarking | Detection, latency, model, and reliability metrics | Pending |
| Week 8 | Final delivery | English report, repository, presentation, and demonstration | Pending |
| August 26–29 | Safety buffer | Corrections and final submission only | Pending |

## Target Architecture

Week 3 milestone note: the real local alarm and corrected RGB mapping were
validated, compact JSON events were captured, and two repeated raw evidence
runs were saved. Week 4 and later work remains pending.

```text
Photoresistor on ESP32-C6
        ↓
Rule-based anomaly detector
        ↓
Deterministic local RGB LED and buzzer response
        ↓
Structured JSON alert over USB serial
        ↓
Python gateway on the laptop
        ↓
Local LLM runtime
        ↓
Passive report or structured JSON command
        ↓
Whitelist and safety-validation layer
        ↓
Accepted command, rejected command, or safe fallback
        ↓
Optional validated command returned to ESP32-C6
```

## Working Schedule

| Period | Primary focus | Required deliverable |
|---|---|---|
| July 15–21 | Week 3 detector | Reproducible edge detector, local alarm behavior, structured serial alert, and tests |
| July 22–28 | Week 4 gateway and local model | Serial gateway, logged alert flow, selected local runtime/model candidates, and first passive response |
| July 29–August 4 | Week 5 prompts and safety | Versioned prompt design, command schema, whitelist, strict parser, and adversarial validation cases |
| August 5–11 | Week 6 integration | Safe end-to-end pipeline with passive mode as the default and controlled actuation tests |
| August 12–18 | Week 7 experiments | Reproducible detector, latency, model, JSON, and safety measurements |
| August 19–25 | Week 8 delivery | Final English report, cleaned repository, presentation, and demonstration package |
| August 26–29 | Safety buffer | Corrections, exports, backups, submission verification, and no new required features |

## Required Pipeline

The required project path has priority over optional extensions:

1. Detect a photoresistor anomaly locally on the ESP32-C6.
2. Provide a finite local RGB LED and buzzer response.
3. Emit a structured alert over USB serial.
4. Receive and log the alert in a Python gateway.
5. Obtain a passive response from a selected local model.
6. Validate any structured model output against a strict schema and whitelist.
7. Demonstrate safe fallback behavior for invalid, unavailable, or delayed model output.
8. Measure and report the system using a reproducible experiment protocol.

## Optional Work

Optional sensors, richer model comparisons, additional commands, wireless transport, and advanced visualizations may be explored only after the required pipeline is complete. Optional work must not delay safety validation, benchmarking, the report, the presentation, or submission.

## Milestone Dependencies

- Week 3 depends on the verified Week 2 baseline data.
- Week 4 depends on a stable structured alert format from Week 3.
- Week 5 depends on real gateway input and at least one local model candidate.
- Week 6 depends on the Week 5 schema, whitelist, parser, and safe fallback rules.
- Week 7 depends on a frozen experimental version of the required pipeline.
- Week 8 depends on traceable results, figures, limitations, and reproducibility notes from Week 7.

## Definition of Project Completion

- [ ] Required edge-to-gateway pipeline demonstrated with recorded evidence
- [ ] Local alarm works independently of the gateway and local model
- [ ] Invalid or unavailable model output cannot trigger unvalidated actuation
- [ ] Experimental datasets and metrics are reproducible and documented
- [ ] Repository contains setup, operation, safety, and demonstration instructions
- [ ] Final report and presentation are complete in English
- [ ] Supervisor-facing demonstration and submission package are verified
- [ ] Final backup and repository status are checked before August 29

## Change Control

This roadmap may be adjusted when evidence justifies a change. Record the date, reason, impact on required deliverables, and replacement plan in `LOG.md`. Do not mark a milestone complete until its definition of done and required evidence are present in the repository.
