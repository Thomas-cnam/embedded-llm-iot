# Week 2 Plan

## Objective

Consolidate the ESP32-C6 hardware bring-up and prepare a clean, reusable firmware foundation without implementing anomaly detection.

## Checklist

- [x] Audit existing peripheral test scripts
- [x] Clean and standardize peripheral test scripts
- [x] Create reusable peripheral modules
- [x] Create a combined hardware smoke test
- [x] Run and document the combined hardware smoke test
- [x] Collect photoresistor baseline measurements
- [x] Save baseline measurements in the experiments folder
- [x] Update LOG.md and hardware documentation
- [x] Complete Week 2 hardware consolidation

## Out of scope

- Edge anomaly detection
- Gateway communication
- Local LLM setup
- Prompt engineering
- Whitelist parser
- LLM benchmarking

## Baseline status

The repeatable photoresistor baseline experiment was run manually in Thonny on
2026-07-13. All 90 raw readings are saved in the experiments folder and the
descriptive results are documented. Week 2 hardware consolidation was reviewed
and completed on 2026-07-15 without starting Week 3 implementation.

## Later RGB correction

The Week 2 completion record is preserved. A supervisor correction received on
2026-07-20 established the functional RGB mapping as red GPIO 21, green GPIO
11, and blue GPIO 10 because the PCB red/blue labels are swapped. The scripts
have been corrected, but named red/blue physical behavior requires a repeat
test. Photoresistor, buzzer, serial LED, baseline, and cleanup results are
unaffected.
