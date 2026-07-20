# Week 1 Plan

- [x] Create GitHub repository
- [x] Prepare initial repository structure
- [x] Share repository with `matusformanek`
- [x] Agree on team organization
- [x] Create `TEAM.md`
- [x] Create `LOG.md`
- [x] Confirm board detection by Windows on COM3
- [x] Confirm MicroPython REPL access
- [x] Read hardware documentation
- [x] Identify pin mappings - Main peripheral pins identified from PCB silkscreen labels; functional tests still pending.
- [x] Install or prepare MicroPython development environment (`mpremote` verified)
- [x] Test photoresistor
- [x] Test buzzer
- [x] Test RGB LED
- [x] Test serial LED strip
- [x] Record all results in `LOG.md`

## RGB mapping correction

The Week 1 RGB test remains part of the historical bring-up record. On
2026-07-20, the supervisor confirmed that the PCB red and blue silkscreen labels
are swapped. The corrected mapping is red GPIO 21, green GPIO 11, and blue GPIO
10. Named red/blue behavior must be physically revalidated with the corrected
script; this does not alter the other Week 1 test results.

- [ ] Revalidate RGB LED colors with the supervisor-confirmed mapping

## Notes

- Photoresistor test repeated in Thonny with better sensor coverage; result is now validated as working.
