from openai import OpenAI
from rob import rob
from threading import Thread
import time
from DialogEngine import DialogEngine
import RPi.GPIO as GPIO


# You need to export environment variable OPENAI_API_KEY
client = OpenAI()

# Create a thread
thread = client.beta.threads.create()

def get_response(text):
  # Add message to a thread
  message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=text,
  )

  # Create a run
  run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id='asst_hGCh7jVelUJcFQFOuZHZ9nB1',
  )
    
  # Check for status of run
  while run.status in ['queued', 'in_progress', 'cancelling']:
    time.sleep(1) # Wait for 1 second
    run = client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
    )

  # return message
  if run.status == 'completed': 
    message_response = client.beta.threads.messages.list(
      thread_id=thread.id
    )
    messages = message_response.data
    latest_message = messages[0]

    return latest_message.content[0].text.value
  else:
    return run.status
  
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

def run_speaking():
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()

    while True:
        if get_distance() <= 75: # if user approaches
            while True:
                print("Enter text: ")
                words = input(">>> ")
                if words.strip() == "bye":
                    break
                output = d.analyze(words.strip())
                if output == "I don't understand! ":
                   output = get_response(words.strip())
                rob.say(output)
                print("Robot: " + str(output))
        time.sleep(0.1)


if __name__ == "__main__":
    speaking_thread = Thread(target=run_speaking)
    face_thread = Thread(target=rob.start_face)

    speaking_thread.start()
    face_thread.start()
    speaking_thread.join()
    face_thread.join()