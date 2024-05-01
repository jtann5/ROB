from openai import OpenAI
from rob import rob
from threading import Thread
import time
from DialogEngine import DialogEngine
import RPi.GPIO as GPIO
import speech_recognition as sr


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
    charging = False
    
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()

    while True:
        if get_distance() <= 75: # if user approaches
            rob.say("Hello human")
            while True:
                print("Enter text: ")
                words = input(">>> ")

                if words.strip() == "bye":
                    break
                elif words.strip() == "take me to the bathroom":
                  rob.say("Follow me to the bathroom")
                  # Goto A3
                  rob.say("We have arrived. Goodbye human")
                  # Goto A0
                  charging = True
                  break
                elif words.strip() == "take me to Hunter's office":
                  rob.say("Follow me to Hunter's Office")
                  # Goto A2
                  rob.say("We have arrived. Goodbye human")
                  # Goto A0
                  charging = True
                  break
                elif words.strip() == "charge":
                  charging = True
                  break
                else:
                    output = d.analyze(words.strip())
                    if output.strip() == "I don't understand!":
                      output = get_response(words.strip())
                    rob.say(output)
                    print("Robot: " + str(output))

        if charging:
           rob.say("charging activated")
           # Goto A1
           break
        time.sleep(0.1)

def run_speaking2():
    charging = False
    
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()

    while True:
        if get_distance() <= 75: # if user approaches
          rob.say("Hello human")
          while True:
            with sr.Microphone(device_index=1) as source:
              r = sr.Recognizer()
              r.adjust_for_ambient_noise(source)
              r.dynamic_energy_threshold = 5000

              try:
                  print("listening")
                  rob.face.set_robot_state('listening')
                  audio = r.listen(source, timeout=None)
                  rob.face.set_robot_state('idle')
                  print("got audio")
                  words = r.recognize_google(audio)
                  print(words)

                  if words.strip() == "bye":
                      break
                  elif words.strip() == "take me to the bathroom":
                    rob.say("Follow me to the bathroom")
                    # Goto A3
                    rob.say("We have arrived. Goodbye human")
                    # Goto A0
                    charging = True
                    break
                  elif words.strip() == "take me to Hunter's office":
                    rob.say("Follow me to Hunter's Office")
                    # Goto A2
                    rob.say("We have arrived. Goodbye human")
                    # Goto A0
                    charging = True
                    break
                  elif words.strip() == "charge":
                    charging = True
                    break
                  else:
                      output = d.analyze(words.strip())
                      if output.strip() == "I don't understand!":
                        output = get_response(words.strip())
                      rob.say(output)
                      print("Robot: " + str(output))

              except sr.UnknownValueError:
                  rob.say("Do not know that word human!")
                  print("Don't know that word")
        if charging:
           rob.say("charging activated")
           # Goto A1
        time.sleep(0.1)


if __name__ == "__main__":
    speaking_thread = Thread(target=run_speaking2)
    face_thread = Thread(target=rob.start_face)

    speaking_thread.start()
    face_thread.start()
    speaking_thread.join()
    face_thread.join()