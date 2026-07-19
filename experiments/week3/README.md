# Week 3 Evidence

This folder contains labeled evidence from repeated Week 3 anomaly and
JSON-event tests.

## Recorded Runs

### 2026-07-19 run 1

- Raw console output: `console_output_2026-07-19_run1.txt`
- Parsed sample data: `labeled_results_2026-07-19_run1.csv`
- Samples: 60, with 12 samples in each guided phase
- JSON events: 4, with event identifiers 1 through 4
- Raw-output SHA-256:
  `57F70C028B2A0D082C27331F7C549780187501C319231C7FDC023AD7B39A855E`

The events were valid JSON and appeared only for emitted low-light and
high-light alerts. The MicroPython `ujson` representation contained separator
spaces, so it did not meet the intended compact-output requirement. The
formatter was corrected after this run. A repeat capture with the corrected
formatter remains pending.

Physical RGB and buzzer observation columns are intentionally blank because
the console capture alone does not prove what the operator saw or heard.

## Capture Procedure

1. Run `firmware/tests/test_anomaly_hardware_integration.py` manually in Thonny.
2. Preserve the complete console output without editing values or JSON lines.
3. Save it with a dated run identifier, for example
   `console_output_2026-07-19_run1.txt`.
4. Copy `labeled_results_template.csv` to a dated results file.
5. Add one row per measured sample using only observed values and actions.
6. Record physical RGB and buzzer observations manually.
7. Keep each repeated run separate; do not overwrite earlier evidence.

Diagnostic lines begin with `DIAG`. A JSON event line begins with `{` and ends
with `}`. Normal, recovery, and cooldown-suppressed readings should have no JSON
event line.

Do not add invented output or copy Week 2 baseline measurements into this
folder.
