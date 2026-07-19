# Week 3 Evidence

This folder is reserved for labeled evidence from repeated Week 3 anomaly and
JSON-event tests. No physical result is stored here yet.

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
folder. The first JSON-enabled hardware run remains pending.
