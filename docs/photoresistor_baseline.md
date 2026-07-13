# Photoresistor Baseline Measurement

## Purpose

Baseline data is collected to characterize the normal ADC response of the
onboard photoresistor under repeatable lighting conditions. These measurements
will provide factual sensor data for later project work without defining an
anomaly detector or calculating thresholds during Week 2.

## Confirmed hardware

- Sensor: onboard photoresistor
- PCB label: `PHOTO(3)`
- GPIO: 3
- ADC attenuation: attempted safely with `ATTN_11DB`

## Procedure

1. Open `firmware/tests/measure_photoresistor_baseline.py` in Thonny.
2. Connect Thonny to the ESP32-C6 board.
3. Run the script and follow each printed instruction.
4. Cover the sensor completely for the `covered` condition.
5. Expose the sensor to normal room light for the `ambient_room_light` condition.
6. Direct a phone flashlight steadily at the sensor for the `phone_flashlight` condition.
7. Keep each setup stable while its readings are collected.
8. Transfer the CSV-compatible output into a copy of the raw-data template.

The script waits five seconds before every condition and collects 30 readings
per condition with a fixed delay between readings. It prints every value, then
prints the minimum, maximum, and average for each condition. It also reports
the pairwise absolute differences between condition averages.

## Data handling

All readings remain in memory while the script runs. The script does not write
to the ESP32 filesystem. Raw results will be added to
`experiments/raw_data/` only after the manual test is completed.

The CSV template uses the columns `condition`, `reading_index`, and `value`.
The script labels the same numeric reading position as `index` in its console
output.

## Project boundary

The collected results prepare sensor characterization work for Week 3. No
anomaly detector, alarm, classification rule, or threshold is implemented as
part of this experiment.
