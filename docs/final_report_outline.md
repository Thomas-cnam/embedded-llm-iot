# Final Report Outline

## Purpose

The final report must explain the project in English as an evidence-based engineering study. Confirm the university template, formatting rules, expected length, citation style, and submission method with the supervisor before final formatting.

## Front Matter

- [ ] Title page with project title, student, internship, university, department, supervisor, and date
- [ ] Required declaration or approval pages, if applicable
- [ ] Abstract summarizing problem, method, principal measured results, safety approach, and conclusion
- [ ] Keywords
- [ ] Table of contents
- [ ] Lists of figures, tables, and abbreviations where useful

## 1. Introduction

- [ ] Internship and project context
- [ ] Motivation for edge anomaly detection and local LLM assistance
- [ ] Research question
- [ ] Objectives and required deliverables
- [ ] Scope and exclusions
- [ ] Report structure

## 2. Background and Related Work

- [ ] Embedded anomaly-detection concepts
- [ ] Rule-based detection on constrained hardware
- [ ] ESP32-C6 and MicroPython constraints relevant to the project
- [ ] Local LLM inference and gateway architecture
- [ ] Structured model output and command validation
- [ ] Safety risks of model-assisted actuation
- [ ] Properly cited related systems and sources

## 3. Requirements and System Design

- [ ] Functional and non-functional requirements
- [ ] Hardware platform and confirmed GPIO mappings
- [ ] Target architecture and data flow
- [ ] Component responsibilities and trust boundaries
- [ ] Alert and command schemas
- [ ] Passive, active, degraded, and offline modes
- [ ] Safety assumptions and threat model

## 4. Hardware Bring-Up and Sensor Characterization

- [ ] Week 1 peripheral validation method and evidence
- [ ] Reusable peripheral modules and combined smoke test
- [ ] Photoresistor baseline procedure
- [ ] Baseline dataset summary and observed stability
- [ ] Hardware limitations and measurement conditions

## 5. Edge Anomaly Detector

- [ ] Detector method and rationale
- [ ] Calibration process and separation from final evaluation
- [ ] Sampling, filtering, persistence, hysteresis, and reset behavior as applicable
- [ ] Local RGB LED and buzzer response
- [ ] Structured alert generation
- [ ] Implementation constraints and limitations

## 6. Python Gateway and Local LLM

- [ ] Serial ingestion and reconnection design
- [ ] Logging and traceability
- [ ] Runtime and model selection rationale
- [ ] Prompt design and versioning
- [ ] Passive-response workflow
- [ ] Host hardware and software configuration

## 7. Safety Validation and Integration

- [ ] Minimal command schema and whitelist
- [ ] Parser and validation order
- [ ] Rejection and safe-fallback behavior
- [ ] End-to-end operating modes
- [ ] Controlled actuation procedure, if approved
- [ ] Failure, timeout, duplicate, stale, and disconnect handling
- [ ] Boundary of local-model authority

## 8. Experimental Methodology

- [ ] Research questions or testable evaluation questions
- [ ] Frozen system versions
- [ ] Scenarios, labels, sample counts, and equipment
- [ ] Detector evaluation protocol
- [ ] Latency measurement points
- [ ] Model and prompt comparison protocol
- [ ] Structured-output and safety test protocol
- [ ] Data processing and metric formulas
- [ ] Reproducibility and threats to validity

## 9. Results

- [ ] Detector confusion matrix and quality metrics
- [ ] Detection, local alarm, gateway, model, parser, and end-to-end latency
- [ ] Local-model response and structured-output reliability
- [ ] Parser acceptance, rejection, fallback, and safety outcomes
- [ ] Resource observations where measured
- [ ] Tables and figures with units, sample counts, and captions
- [ ] Failed or inconclusive results reported honestly

## 10. Discussion

- [ ] Interpretation relative to the research question
- [ ] Trade-offs between edge simplicity and detection behavior
- [ ] Trade-offs between local-model capability, latency, and reliability
- [ ] Safety implications and residual risks
- [ ] Comparison with related work
- [ ] Generalizability and deployment constraints

## 11. Limitations and Future Work

- [ ] Sensor and environment limitations
- [ ] Dataset and sample-size limitations
- [ ] Rule-based detector limitations
- [ ] Runtime and model limitations
- [ ] Safety and actuation limitations
- [ ] Optional sensors, wireless transport, and improved methods as future work only

## 12. Conclusion

- [ ] Concise answer to the research question
- [ ] Main engineering contributions
- [ ] Principal measured findings
- [ ] Safety conclusion
- [ ] Final statement on project completion

## Back Matter

- [ ] References in the required style
- [ ] Appendices for schemas, prompts, test cases, setup details, and extended results
- [ ] Repository URL and reproducibility pointers
- [ ] AI-use disclosure where required

## Required Figures and Tables

- [ ] System architecture diagram
- [ ] Hardware and confirmed pin-mapping table
- [ ] Photoresistor baseline table or plot
- [ ] Detector state or data-flow diagram
- [ ] Alert and command schema examples
- [ ] End-to-end sequence diagram
- [ ] Detector confusion matrix
- [ ] Latency summary table or plot
- [ ] Model/prompt reliability comparison
- [ ] Safety test outcome table
- [ ] Final limitations summary

## Quality Checklist

- [ ] Every result has a source dataset or log
- [ ] Every figure has a caption, unit, and explanation
- [ ] Measured results are separated from interpretation
- [ ] Claims match sample size and experimental scope
- [ ] No credentials or private data appear in the report
- [ ] Terminology and version names are consistent
- [ ] English grammar and formatting are reviewed
- [ ] PDF export is visually inspected page by page
- [ ] Supervisor feedback is addressed before submission
