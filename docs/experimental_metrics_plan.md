# Experimental Metrics Plan

## Purpose

This document defines the evidence that should be collected during Week 7. It is a plan, not a result report. Trial counts may be adjusted for justified practical constraints, but changes must be recorded in `LOG.md` before final analysis.

## Measurement Principles

- [ ] Freeze firmware, gateway, parser, prompt, runtime, and model versions before final collection
- [ ] Record configuration and environment metadata with every experiment group
- [ ] Keep calibration data separate from final evaluation data
- [ ] Preserve raw observations and failed trials
- [ ] Use explicit labels assigned from the physical test condition, not detector output
- [ ] Use consistent units and clocks for comparable timing measurements
- [ ] Report sample counts and missing values beside every summary
- [ ] Store processing formulas or scripts with the results
- [ ] Avoid selecting detector parameters from final evaluation outcomes

## Experiment Metadata

Record at minimum:

- Experiment and run identifier
- Date and local time
- Operator
- PCB and sensor identification
- Firmware revision and detector version
- Gateway revision and Python version
- Prompt and parser versions
- Runtime and model identity
- Serial port settings
- Physical lighting condition and setup notes
- Expected label and observed outcome
- Errors, interruptions, retries, and exclusions with reasons

## Detector Metrics

### Required counts

- True positive (`TP`): anomalous trial correctly detected
- False positive (`FP`): normal trial incorrectly detected
- True negative (`TN`): normal trial correctly left normal
- False negative (`FN`): anomalous trial not detected

### Required derived metrics

| Metric | Formula | Reporting note |
|---|---|---|
| Accuracy | `(TP + TN) / (TP + TN + FP + FN)` | Report only with all four counts |
| Precision | `TP / (TP + FP)` | Mark undefined if denominator is zero |
| Recall / sensitivity | `TP / (TP + FN)` | Report per anomaly scenario and overall |
| Specificity | `TN / (TN + FP)` | Report for defined normal scenarios |
| False-positive rate | `FP / (FP + TN)` | Include normal-observation duration |
| F1 score | `2 * precision * recall / (precision + recall)` | Mark undefined when required terms are undefined |
| Detection delay | Detection time minus physical-event start time | Report unit, mean, median, range, and high percentile |
| False alarms per hour | False alarms divided by normal observation hours | State observation duration |

### Planned trials

- [ ] Define at least one normal ambient scenario and each required anomaly scenario
- [ ] Target at least 30 labeled trials per required scenario where practical
- [ ] Include repeated normal-to-anomaly and anomaly-to-normal transitions
- [ ] Include a longer normal-operation observation for false alarms
- [ ] Record manual setup variability and environmental limitations

The detector threshold and acceptance targets are not defined in this planning document. They must be justified from calibration evidence and fixed before final evaluation.

## Latency Metrics

Measure timestamps at the closest practical boundaries:

1. Physical event begins
2. Sensor sample is acquired
3. Detector event is declared
4. Local alarm starts
5. Serial alert is emitted
6. Gateway receives a complete alert
7. Local-model request starts
8. First model output is available
9. Complete model output is available
10. Parser decision is available
11. Optional validated command is applied

Required latency summaries:

- Detector delay
- Local alarm delay
- Serial transport and gateway ingestion latency
- Model time to first output
- Model total response latency
- Parser validation latency
- End-to-end passive latency
- End-to-end controlled-active latency, if active mode is approved

Target at least 30 runs for each required latency path where practical. Report count, mean, median, minimum, maximum, and a high percentile such as p95. State clock resolution and whether timestamps come from one or multiple devices.

## Local Model and Prompt Metrics

For each feasible model and selected prompt version, record:

- Request count
- Successful response count
- Timeout and runtime failure count
- Time to first output and total latency
- Raw structured-output validity rate
- Required-field completeness rate
- Parser acceptance, rejection, and fallback counts
- Response consistency across repeated equivalent alerts
- Approximate model size and relevant runtime settings
- Host resource observations when available and measured consistently

Use a fixed evaluation set. Target at least 20 responses per selected model/prompt combination, increasing the count only if time permits. Optional broad model comparison must not delay required safety and detector measurements.

## Structured Output and Safety Metrics

Test classes should include:

- Valid whitelisted command
- Valid passive response
- Malformed JSON
- Missing required field
- Unknown or extra field
- Unknown command
- Invalid type
- Out-of-range parameter
- Excessive duration
- Natural-language text instead of JSON
- Prompt-injection-like content
- Duplicate event or command
- Stale command
- Model timeout or unavailable runtime
- Serial interruption

Record for each case:

- Expected validator outcome
- Actual validator outcome
- Acceptance, rejection, or fallback reason
- Whether any command reached the board
- Whether any physical action occurred
- Recovery behavior

Required safety reporting includes invalid-output rejection rate, valid-output acceptance rate, false acceptance count, false rejection count, and confirmation that rejected cases caused no hardware actuation.

## Raw Data Layout

Keep separate files for detector trials, latency runs, model responses, and safety cases. Recommended common columns:

```text
experiment_id,run_id,timestamp,version,scenario,expected_label,observed_outcome,value,unit,valid,notes
```

Store original model responses and serial alerts without silently repairing them. Processed tables and figures must reference their source files.

## Analysis Checklist

- [ ] Validate row counts and required fields before calculation
- [ ] Verify labels against experiment notes
- [ ] Calculate metrics from raw data using documented formulas
- [ ] Check edge cases such as zero denominators
- [ ] Compare candidates using identical evaluation inputs
- [ ] Include uncertainty, spread, and sample size rather than averages alone
- [ ] Explain exclusions and failed runs
- [ ] Separate measured facts from interpretation
- [ ] Record limitations and threats to validity

## Definition of Done

- [ ] Detector quality, latency, model behavior, JSON reliability, and safety are measured
- [ ] Configurations and sample counts are traceable
- [ ] Raw and processed data are stored separately
- [ ] Calculations can be reproduced
- [ ] Negative and failed results are retained and discussed
- [ ] Report figures and claims link back to recorded evidence
