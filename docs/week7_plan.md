# Week 7 Plan

## Period

August 12–18, 2026

## Objective

Freeze a reproducible experimental version and measure detector quality, system latency, local-model behavior, structured-output reliability, and safety validation without changing the system during final data collection.

## Checklist

### Experimental freeze

- [ ] Select and record firmware, gateway, prompt, parser, runtime, and model versions
- [ ] Record hardware, operating system, Python, MicroPython, and serial settings
- [ ] Define labeled scenarios and trial counts before collecting final results
- [ ] Separate calibration evidence from final evaluation evidence
- [ ] Define raw-data files and column schemas
- [ ] Create a run identifier and notes field for every trial
- [ ] Document deviations or failed runs without deleting them silently

### Detector evaluation

- [ ] Collect labeled normal and anomalous trials under controlled conditions
- [ ] Record true positives, false positives, true negatives, and false negatives
- [ ] Calculate accuracy, precision, recall, specificity, F1 score, and false-positive rate where defined
- [ ] Measure detection delay and local alarm delay
- [ ] Record false alarms during a longer normal-operation observation
- [ ] Document environmental limitations and calibration sensitivity

### Gateway and model evaluation

- [ ] Measure serial alert-to-gateway latency
- [ ] Measure model time to first response and total response latency
- [ ] Measure end-to-end latency for passive and approved active modes
- [ ] Record model response success, timeout, and failure rates
- [ ] Measure structured JSON validity before parser correction
- [ ] Compare only the feasible model or prompt candidates needed for the research question

### Safety evaluation

- [ ] Run the complete valid-command test set
- [ ] Run malformed, unknown, out-of-range, extra-field, stale, and duplicate-command cases
- [ ] Run prompt-injection-like and natural-language-output cases
- [ ] Record parser acceptance, rejection, fallback, and reason
- [ ] Confirm every rejected case produces no hardware action
- [ ] Measure safe-fallback behavior during serial and model interruption

### Analysis and evidence

- [ ] Preserve raw data separately from processed summaries
- [ ] Create tables and figures using traceable scripts or documented calculations
- [ ] Report sample counts and missing data with every metric
- [ ] Avoid claims that are not supported by the collected evidence
- [ ] Update `LOG.md` with experiment dates, versions, issues, and decisions
- [ ] Prepare results material for the final report

## Deliverables

- Frozen experimental version and reproducibility record
- Raw benchmark datasets and processed summaries
- Detector confusion matrix and timing results
- Gateway/model latency and structured-output reliability results
- Safety validation and fallback results
- Report-ready figures, tables, and limitations

## Definition of Done

- [ ] All required metrics in `experimental_metrics_plan.md` are measured or explicitly marked unavailable with a reason
- [ ] Raw data, processing method, sample count, and configuration are traceable
- [ ] Detector, latency, model, JSON, and safety results are documented
- [ ] No result was removed solely because it was unfavorable
- [ ] Final report claims can be traced to stored evidence
- [ ] Experimental code and configuration are frozen for Week 8 writing

## Adjustment Notes

Reduce optional model comparisons before reducing detector, latency, reliability, or safety measurements. If a test cannot be completed, record the limitation and its effect on the research question rather than inventing or extrapolating results.

## Out of Scope

- New required features after the experimental freeze
- Unplanned optional hardware integration
- Performance claims without stored evidence
- Final submission changes unrelated to measured findings
