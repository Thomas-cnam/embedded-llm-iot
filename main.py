from machine import Pin, ADC
import time
import sys
import select

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
    return photoresistor.read();

# Prépare le poller une seule fois, en dehors de la boucle
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

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
    print("DATA;" + "0" + ";" + str(lum)) 

    response = ""
    if poller.poll(6000):  # attend jusqu'à 3000ms qu'il y ait des données
        response = sys.stdin.readline().strip()
    print(response)
    
    if response.startswith("ANOMALIE:1"):
        rgb_led.red()
    elif response.startswith("ANOMALIE:0"):
        rgb_led.green()

    time.sleep(10)
