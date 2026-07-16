"""Provisional configuration for the photoresistor anomaly detector."""

# These values come from the Week 2 baseline design analysis. They remain
# provisional until they are validated with real Week 3 hardware tests.
LOW_LIGHT_THRESHOLD = 5000
HIGH_LIGHT_THRESHOLD = 32000
SUDDEN_CHANGE_THRESHOLD = 8000
HISTORY_SIZE = 5

# The pure detector does not use timing. A later integration layer will apply
# the sample interval and keep cooldown separate from classification logic.
SAMPLE_INTERVAL_MS = 500
ALERT_COOLDOWN_MS = 5000
