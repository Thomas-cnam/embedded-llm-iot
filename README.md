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

GPIO pin mappings are not defined yet in this repository. They must be filled in only after checking the official board documentation.

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

Week 1 focuses on repository preparation, documentation, team organization, and manual hardware bring-up planning. Hardware tests are not marked as completed until they are performed on the real ESP32-C6 board and recorded in `LOG.md`.

## Supervisor Sharing Note

The repository should be shared with GitHub user: `matusformanek`.

