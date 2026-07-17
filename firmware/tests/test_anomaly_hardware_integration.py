"""Finite guided ESP32-C6 anomaly and local-alarm hardware test."""

from time import sleep_ms, ticks_diff, ticks_ms

from anomaly.alert_policy import AnomalyAlertPolicy
from anomaly.detector import PhotoresistorAnomalyDetector
from anomaly.integration import AnomalyIntegrationController
from anomaly.local_alarm import LocalAlarmController
from peripherals.buzzer import Buzzer
from peripherals.photoresistor import Photoresistor
from peripherals.rgb_led import RgbLed


PHOTORESISTOR_PIN = 3
BUZZER_PIN = 5
RGB_RED_PIN = 10
RGB_GREEN_PIN = 11
RGB_BLUE_PIN = 21
RGB_ACTIVE_LOW = False

SAMPLE_INTERVAL_MS = 500
SAMPLES_PER_PHASE = 12
SETUP_DELAY_SECONDS = 5

PHASES = (
    (
        "ambient",
        "Leave the photoresistor exposed to normal room light.",
    ),
    (
        "covered",
        "Cover the photoresistor completely with an opaque object.",
    ),
    (
        "ambient recovery",
        "Uncover the photoresistor and restore normal room light.",
    ),
    (
        "phone flashlight",
        "Direct a phone flashlight steadily at the photoresistor.",
    ),
    (
        "final ambient recovery",
        "Remove the flashlight and restore normal room light.",
    ),
)


def wait_for_setup():
    """Give the operator a finite preparation countdown."""
    for seconds_left in range(SETUP_DELAY_SECONDS, 0, -1):
        print("Starting in", seconds_left, "second(s)...")
        sleep_ms(1000)


def print_result(index, value, result):
    """Print one human-readable result without serializing an event."""
    detector_result = result["detector_result"]
    policy_decision = result["policy_decision"]
    print(
        "Sample",
        index,
        "of",
        SAMPLES_PER_PHASE,
        "value=",
        value,
        "state=",
        detector_result["anomaly_type"],
        "decision=",
        policy_decision["decision_reason"],
        "alarm=",
        result["alarm_action"],
    )
    if result["alarm_error"] is not None:
        print("Local alarm error:", result["alarm_error"])


def run_test():
    """Run the complete finite guided sequence and always clean up outputs."""
    photoresistor = None
    rgb_led = None
    buzzer = None
    alarm_controller = None
    integration = None

    print("ESP32-C6 anomaly hardware integration test")
    print("Photoresistor: GPIO", PHOTORESISTOR_PIN)
    print("Buzzer: GPIO", BUZZER_PIN)
    print(
        "RGB LED: GPIO",
        RGB_RED_PIN,
        RGB_GREEN_PIN,
        RGB_BLUE_PIN,
    )
    print("RGB ACTIVE_LOW =", RGB_ACTIVE_LOW)
    print("Sample interval:", SAMPLE_INTERVAL_MS, "ms")
    print("Samples per phase:", SAMPLES_PER_PHASE)
    print("This test is finite and does not produce JSON events.")

    try:
        photoresistor = Photoresistor(pin=PHOTORESISTOR_PIN)
        rgb_led = RgbLed(
            red_pin=RGB_RED_PIN,
            green_pin=RGB_GREEN_PIN,
            blue_pin=RGB_BLUE_PIN,
            active_low=RGB_ACTIVE_LOW,
        )
        buzzer = Buzzer(pin=BUZZER_PIN)

        detector = PhotoresistorAnomalyDetector()
        alert_policy = AnomalyAlertPolicy()
        alarm_controller = LocalAlarmController(rgb_led, buzzer)
        integration = AnomalyIntegrationController(
            detector,
            alert_policy,
            alarm_controller,
        )

        last_tick = ticks_ms()
        elapsed_ms = 0

        for phase_number, phase in enumerate(PHASES, 1):
            phase_name, instruction = phase
            print()
            print("Phase", phase_number, "of", len(PHASES), ":", phase_name)
            print(instruction)
            print("Keep the setup steady while readings are collected.")
            wait_for_setup()

            for index in range(1, SAMPLES_PER_PHASE + 1):
                current_tick = ticks_ms()
                tick_delta = ticks_diff(current_tick, last_tick)
                if tick_delta < 0:
                    raise RuntimeError("monotonic clock moved backwards")
                elapsed_ms += tick_delta
                last_tick = current_tick

                value = photoresistor.read()
                result = integration.process(value, elapsed_ms)
                print_result(index, value, result)

                if index < SAMPLES_PER_PHASE:
                    sleep_ms(SAMPLE_INTERVAL_MS)

        print()
        print("Guided anomaly hardware integration sequence completed.")
        print("Review the physical LED and buzzer behavior before validation.")
    except Exception as error:
        print("Hardware integration test stopped with error:", error)
        raise
    finally:
        if integration is not None:
            integration.reset()
            if integration.last_alarm_error is not None:
                print("Integration cleanup error:", integration.last_alarm_error)
        elif alarm_controller is not None:
            cleanup_result = alarm_controller.safe_off()
            if not cleanup_result["successful"]:
                print("Local alarm cleanup result:", cleanup_result)
        else:
            if rgb_led is not None:
                try:
                    rgb_led.off()
                except Exception as error:
                    print("RGB cleanup error:", error)
            if buzzer is not None:
                try:
                    buzzer.off()
                except Exception as error:
                    print("Buzzer cleanup error:", error)

        if buzzer is not None:
            try:
                buzzer.deinit()
            except Exception as error:
                print("Buzzer deinitialization error:", error)

        print("Safety cleanup complete: RGB LED and buzzer are off.")


run_test()
