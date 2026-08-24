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
├── .gitignore
├── tests/
├── server/
├── firmware/
├── experiments/
└── ESP/
```

## how to use the project

the "firmware" files regroup every test and peripherals that was developped for the first few week of the project.
the "tests" files regroup test to show to the professor the functionnality of the ESP32 
In those files the "preripherals" regroup every python class for different functionnality of the given ESP32.

"ESP" files contain script for the ESP32
"server" files are to run locally on the PC

the LLM that was use come from ollama, this part must be installed seperatly, the models used was **phi4-mini** (worked) and **llama3.2:1b** (didnt worked)

for additionnal information on how each script worked read the "README.md" in each files

## result of the project

in ProjectResult.png you can see what is logged by the server script
they are two instances where i messed with the captor to make an anomaly

## first intance

value = 36776 lum.
LLM answer = Jugement AI: {'anomaly': True, 'message': 'New measurement significantly higher than recent history average.'}
ESP32 = red light turned on

it was atteigned by using the lamp function of my mobile phone

## second intance

value = 0 lum.
LLM answer = Jugement AI: {'anomaly': True, 'message': 'New luminosity value (0 lux) deviates significantly from recent history average (~25158 lux)'}
ESP32 = red light turned on

it was atteigned by using putting a black tee shirt on the captor
