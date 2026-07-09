# Hardware Bring-Up Checklist

Use this checklist during manual hardware bring-up. Do not mark an item as completed until it has been tested on the real ESP32-C6 hardware.

| Item | Status | Pin mapping | Test file | Observations |
|---|---|---|---|---|
| Board USB connection | Confirmed | COM3 | N/A | Detected as Silicon Labs CP210x USB to UART Bridge |
| MicroPython REPL access | Confirmed | COM3 | N/A | `print("Hello ESP32-C6")` worked through mpremote |
| Photoresistor ADC reading | Tested / Working | GPIO 3 | `firmware/tests/test_photoresistor.py` | Successful Thonny repeat test: exposed average 28041.2; covered average 1225.6; difference 26815.6. Clear response to light changes observed. |
| Buzzer PWM output | Tested / Working | GPIO 5 | `firmware/tests/test_buzzer.py` | Manual Thonny test successful: three short tones played at 440 Hz, 660 Hz, and 880 Hz; PWM stopped correctly; no error observed. |
| RGB LED control | Pending test | GPIO 10 / GPIO 11 / GPIO 21 | `firmware/tests/test_rgb_led.py` | Pins identified from PCB labels R(10), G(11), B(21); active high/low still to test |
| Serial LED strip control | Pending test | GPIO 8 | `firmware/tests/test_serial_led_strip.py` | Pin identified from PCB label SERIAL_LED(8); 3 onboard LEDs visible; protocol still to test |
| HC-SR04 ultrasonic sensor | Optional / not tested | GPIO 15 trigger / GPIO 23 echo | TODO | Pins identified from PCB labels TR(15), EC(23); optional sensor not tested yet |
| MPU6050 accelerometer/gyroscope | Optional / not tested | GPIO 6 SDA / GPIO 7 SCL | TODO | I2C pins identified from PCB labels SDA(6), SCL(7); optional sensor not tested yet |
