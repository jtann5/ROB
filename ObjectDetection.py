import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set GPIO pins
TRIG_PIN = 23
ECHO_PIN = 24

# Set TRIG as output and ECHO as input
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # Set TRIG to LOW for a short time to ensure clean signal
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)

    # Send a 10us pulse to trigger
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Measure the time it takes for the echo to return
    timeout = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        if (time.time() - timeout) > 3: # Timeout after 1 second
            print("Timeout occurred while waiting for echo signal")
            return None
    pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        if (time.time() - timeout) >  3: # Timeout after 1 second
            print("Timeout occurred while receiving echo signal")
            return None
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Speed of sound is 343m/s. The distance is half of the total time multiplied by the speed of sound
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance


while True:
    print(get_distance(), "cm")
    time.sleep(1)