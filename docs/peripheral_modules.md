# Peripheral Modules

These reusable MicroPython modules provide small helpers for the confirmed ESP32-C6 custom PCB peripherals. They are prepared for Week 2 hardware consolidation, but they have not yet been independently validated on hardware.

The existing self-contained scripts in `firmware/tests/` remain the verified reference for hardware behavior.

## Confirmed Pins

| Peripheral | Module | Confirmed pin(s) |
|---|---|---|
| Photoresistor | `firmware/peripherals/photoresistor.py` | GPIO 3, PCB label `PHOTO(3)` |
| Passive buzzer | `firmware/peripherals/buzzer.py` | GPIO 5, PCB label `BUZZER(5)` |
| RGB LED | `firmware/peripherals/rgb_led.py` | Red GPIO 21, green GPIO 11, blue GPIO 10; supervisor-confirmed correction |
| Serial LEDs | `firmware/peripherals/serial_led.py` | GPIO 8, `LED_COUNT = 3` |

## `Photoresistor`

Purpose: read the analog photoresistor value through ADC.

```python
from peripherals.photoresistor import Photoresistor

sensor = Photoresistor()
value = sensor.read()
average = sensor.read_average(sample_count=10, delay_ms=20)
```

## `Buzzer`

Purpose: play finite PWM tones and provide safe shutdown.

```python
from peripherals.buzzer import Buzzer

buzzer = Buzzer()
try:
    buzzer.tone(440, 300)
finally:
    buzzer.deinit()
```

## `RgbLed`

Purpose: control the onboard RGB LED with the confirmed active-high behavior.

```python
from peripherals.rgb_led import RgbLed

led = RgbLed()
led.red()
led.off()
```

## `SerialLedStrip`

Purpose: control the three onboard serial LEDs using the MicroPython `neopixel` module.

```python
from peripherals.serial_led import SerialLedStrip

strip = SerialLedStrip()
strip.white()
strip.off()
```

## Validation Status

These modules are prepared for reuse but have not yet been independently
validated on hardware. The RGB module now uses the supervisor-confirmed
mapping, but that corrected mapping still requires a short physical repeat
test. The self-contained scripts remain the manual hardware reference:

- `firmware/tests/test_photoresistor.py`
- `firmware/tests/test_buzzer.py`
- `firmware/tests/test_rgb_led.py`
- `firmware/tests/test_serial_led_strip.py`
