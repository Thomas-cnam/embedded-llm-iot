from machine import Pin, ADC
import time
import sys

from anomaly.alert_policy import AnomalyAlertPolicy
from anomaly.detector import PhotoresistorAnomalyDetector
from anomaly.event_formatter import AnomalyEventFormatter
from anomaly.integration import AnomalyIntegrationController
from anomaly.local_alarm import LocalAlarmController
from peripherals.buzzer import Buzzer
from peripherals.photoresistor import Photoresistor
from peripherals.rgb_led import RgbLed

PHOTORESISTOR_PIN = 3
BUZZER_PIN = 5
RGB_RED_PIN = 21
RGB_GREEN_PIN = 11
RGB_BLUE_PIN = 10
RGB_ACTIVE_LOW = False

photoresistor = None
rgb_led = None
buzzer = None
alarm_controller = None
integration = None
event_formatter = None

def lire_luminosite():
    return Photoresistor.read();

while True:
    photoresistor = Photoresistor(pin=PHOTORESISTOR_PIN)
    rgb_led = RgbLed(
        red_pin=RGB_RED_PIN,
        green_pin=RGB_GREEN_PIN,
        blue_pin=RGB_BLUE_PIN,
        active_low=RGB_ACTIVE_LOW,
    )
    buzzer = Buzzer(pin=BUZZER_PIN)
    
    lum = lire_luminosite()

    # Envoi des données sur le port série au format simple
    print("DATA;{};{}".format(lum))

    # Attente d'une réponse du serveur (bloquant avec timeout simple)
    start = time.ticks_ms()
    reponse = ""
    while time.ticks_diff(time.ticks_ms(), start) < 3000:
        if sys.stdin.any():
            reponse = sys.stdin.readline().strip()
            break

    if reponse.startswith("ANOMALIE:1"):
        led_alerte.value(1)
    elif reponse.startswith("ANOMALIE:0"):
        led_alerte.value(0)

    time.sleep(10)