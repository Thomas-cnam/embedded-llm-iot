# Hardware Bring-Up Checklist

Use this checklist during manual hardware bring-up. Do not mark an item as completed until it has been tested on the real ESP32-C6 hardware.

| Item | Status | Pin mapping | Test file | Observations |
|---|---|---|---|---|
| Board USB connection | Confirmed | COM3 | N/A | Detected as Silicon Labs CP210x USB to UART Bridge |
| MicroPython REPL access | Confirmed | COM3 | N/A | `print("Hello ESP32-C6")` worked through mpremote |
| Photoresistor ADC reading | Pending | TODO | `firmware/tests/test_photoresistor.py` | Waiting for official pin mapping |
| Buzzer PWM output | Pending | TODO | `firmware/tests/test_buzzer.py` | Waiting for official pin mapping |
| RGB LED control | Pending | TODO | `firmware/tests/test_rgb_led.py` | Waiting for official pin mapping |
| Serial LED strip control | Pending | TODO | `firmware/tests/test_serial_led_strip.py` | Waiting for official pin mapping |
| HC-SR04 ultrasonic sensor | Optional / not tested | TODO | TODO | Optional sensor, not connected yet |
| MPU6050 accelerometer/gyroscope | Optional / not tested | TODO | TODO | Optional sensor, not connected yet |
