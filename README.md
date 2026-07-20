# Embedded Anomaly Detection with Local LLM Assistance

## Overview

This repository contains the initial structure for a summer internship project at the University of Zilina. The project explores how an ESP32-C6-based embedded system can detect anomalies in sensor data and cooperate with a local gateway that later uses local LLM assistance.

## Research Question

How can a low-power embedded device detect basic sensor anomalies locally and interact safely with a local LLM-assisted gateway for reporting or command generation?

## Hardware Platform

The target hardware is a custom PCB based on an ESP32-C6 microcontroller.

Planned peripherals include:

- Photoresistor
- Buzzer
- RGB LED
- Serial LED strip
- Optional HC-SR04 ultrasonic sensor
- Optional MPU6050 motion sensor

Confirmed GPIO mappings are documented in `docs/pin_mapping.md` and the hardware checklist.

## Planned Software Stack

- Firmware: MicroPython on ESP32-C6
- Gateway: Python 3.x
- Future local LLM runtime: to be selected and configured after Week 1
- Documentation and reporting: Markdown and final English report

## Repository Structure

```text
embedded-llm-iot/
├── README.md
├── TEAM.md
├── LOG.md
├── .gitignore
├── docs/
├── firmware/
├── gateway/
├── experiments/
└── report/
```

## Week 1 Status

Week 1 is completed. Repository setup, team documentation, MicroPython access, pin identification, and the main peripheral tests are recorded in `LOG.md` and the Week 1 documentation.

## Supervisor Sharing Note

The repository should be shared with GitHub user: `matusformanek`.

## Current Status

- Week 1: completed
- Week 2 hardware consolidation: completed
- Main peripherals verified in MicroPython
- Photoresistor baseline measurements recorded
- Week 3 edge anomaly detector: implemented and host-tested
- Corrected RGB mapping: red GPIO 21, green GPIO 11, blue GPIO 10
- Corrected RGB color revalidation on the ESP32-C6: pending
- Gateway and local LLM work: not started

## Project Planning

The remaining work is organized as an adjustable plan through the August 29, 2026 deadline:

- [Project roadmap](docs/project_roadmap.md)
- [Week 3: edge anomaly detector](docs/week3_plan.md)
- [Week 4: Python gateway and first local LLM response](docs/week4_plan.md)
- [Week 5: prompt engineering and safety parser](docs/week5_plan.md)
- [Week 6: safe end-to-end integration](docs/week6_plan.md)
- [Week 7: experimental benchmarking](docs/week7_plan.md)
- [Week 8: report, cleanup, presentation, and submission](docs/week8_plan.md)
- [Experimental metrics plan](docs/experimental_metrics_plan.md)
- [Final report outline](docs/final_report_outline.md)
- [Final submission checklist](docs/final_submission_checklist.md)

Required deliverables are planned for completion by August 25. August 26–29 is reserved for corrections, verification, backups, and final submission rather than new required features.
