# Team Organization

## Current division of work

### Student 1 - Firmware and hardware bring-up

Responsibilities:

- ESP32-C6 MicroPython environment
- Board connection and REPL testing
- Photoresistor ADC tests
- Buzzer PWM tests
- RGB LED tests
- Serial LED strip tests
- Firmware documentation
- Updating hardware test results in LOG.md

### Student 2 - Gateway, LLM and benchmarking

Responsibilities:

- Python gateway structure
- Future serial or Wi-Fi communication with the ESP32-C6
- Future local LLM runtime setup
- Future prompt templates
- Logging system
- Benchmarking scripts and result tables
- Safety whitelist parser documentation

## Shared responsibilities

Both students are responsible for:

- Keeping LOG.md updated after important experiments or decisions
- Reviewing each other's code and documentation
- Preparing and running experiments
- Writing the final English report
- Maintaining the GitHub repository
- Keeping the commit history clear and regular
- Documenting any reused idea or code from another team

## Collaboration rules

- Pull the latest version before starting work.
- Commit small and understandable changes.
- Use clear commit messages.
- Do not modify the same file at the same time without coordination.
- Record every important experiment, observation, issue, and decision in LOG.md.
- Do not claim that a hardware test worked until it has been tested on the real ESP32-C6 board.
- Do not invent pin mappings; only use values confirmed from official documentation or supervisor information.
- If code or ideas are reused or adapted from another team, document it clearly in the repository or final report.

## Notes

This organization may evolve during the internship depending on progress, hardware issues, or changes in the project direction.
