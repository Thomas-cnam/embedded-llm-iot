# Project Summary

The project explores embedded anomaly detection with local LLM assistance.

The planned system has the following high-level behavior:

- The ESP32-C6 reads sensor data from connected peripherals.
- Basic rule-based anomaly detection runs locally on the embedded device.
- A local alarm is triggered through LEDs or a buzzer when needed.
- A Python gateway receives alerts from the ESP32-C6.
- A local LLM later generates either a human-readable report or a structured JSON command.
- A safety whitelist validates any generated command before execution.

During Week 1, the focus is repository setup, documentation, team organization, and hardware bring-up preparation. Final anomaly detection and local LLM integration are intentionally out of scope for Week 1.

