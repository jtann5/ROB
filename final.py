from openai import OpenAI
from rob import rob
from threading import Thread
import time
from DialogEngine import DialogEngine
import RPi.GPIO as GPIO
import speech_recognition as sr

import numpy as np
import serial
import math


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

    heading = Headings()
    
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
                  gotoQuadrant(heading, 3)
                  rob.say("We have arrived. Goodbye human")
                  # Goto A0
                  gotoQuadrant(heading, 0)
                  charging = True
                  break
                elif words.strip() == "take me to Hunter's office":
                  rob.say("Follow me to Hunter's Office")
                  # Goto A2
                  gotoQuadrant(heading, 2)
                  rob.say("We have arrived. Goodbye human")
                  # Goto A0
                  gotoQuadrant(heading, 0)
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
           # Goto A1
           gotoQuadrant(heading, 1)
           rob.say("charging activated")
           break
        time.sleep(0.1)

def run_speaking2():
    charging = False
    
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()

    heading = Headings()

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
                    gotoQuadrant(heading, 3)
                    rob.say("We have arrived. Goodbye human")
                    # Goto A0
                    gotoQuadrant(heading, 0)
                    charging = True
                    break
                  elif words.strip() == "take me to Hunter's office":
                    rob.say("Follow me to Hunter's Office")
                    # Goto A2
                    gotoQuadrant(heading, 2)
                    rob.say("We have arrived. Goodbye human")
                    # Goto A0
                    gotoQuadrant(heading, 0)
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
           # Goto A1
           gotoQuadrant(heading, 1)
           rob.say("charging activated")
           break
        time.sleep(0.1)



distance = 3

anchor0 = [0, 3]
anchor1 = [3, 3]
anchor2 = [3, 0]
anchor3 = [0, 0]

anchor0c = [0.75, 2.25]
anchor1c = [2.25, 2.25]
anchor2c = [2.25, 0.75]
anchor3c = [0.75, 0.75]

anchors = [anchor0, anchor1, anchor2, anchor3]
anchorsc = [anchor0c, anchor1c, anchor2c, anchor3c]

def readSerial():
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    ser.readline()  # example mc 00 000001ab 00000d7f 0000124c 00000d31 2996 97 000f9bda t7:0 1a38
    response = ser.readline()  # example $KT7,0.45,3.43,4.70,3.36,LO=[no solution]
    while response.decode().strip().split(',')[0] != "$KT7":
        response = ser.readline()
    print(response)
    # print(response.decode().strip())  # Decode bytes to string and remove newline characters
    arr = response.decode().strip().split(',')
    try:
        float_array = [float(x) for x in arr[1:5]]
        #print("A0: " + str(float_array[0]) + "m")
        #print("A1: " + str(float_array[1]) + "m")
        #print("A2: " + str(float_array[2]) + "m")
        #print("A3: " + str(float_array[3]) + "m")
        #print("Quad: " + str(float_array.index(min(float_array))))
        #print("")
        ser.close()
        print("FLOAT ARR: " + str(float_array))
        return float_array
    except:
        return readSerial()

def calcPosition(anchors, distances):
    # Convert input lists to NumPy arrays for easier computation
    anchors = np.array(anchors)
    distances = np.array(distances)

    # Number of dimensions (2 for 2D space, 3 for 3D space)
    num_dimensions = anchors.shape[1]

    # Ensure at least as many anchors as dimensions
    if len(anchors) < num_dimensions:
        raise ValueError("Number of anchors must be at least as many as dimensions")

    # Number of anchors
    num_anchors = len(anchors)

    # Calculate distances squared
    distances_squared = distances ** 2

    # Initialize A matrix and b vector
    A = np.zeros((num_anchors - 1, num_dimensions))
    b = np.zeros((num_anchors - 1,))

    # Iterate over pairs of anchors
    for i in range(num_anchors - 1):
        A[i] = 2 * (anchors[i] - anchors[-1])
        b[i] = np.linalg.norm(anchors[i]) ** 2 - np.linalg.norm(anchors[-1]) ** 2 - distances_squared[i] + \
               distances_squared[-1]

    # Calculate least squares solution
    position = np.linalg.lstsq(A, b, rcond=None)[0]

    # Add the position of the reference anchor
    position += anchors[-1]

    return position

def vectorDetector(initalx, initaly, finalx, finaly):
    return finalx - initalx, finaly - initaly

def dotProduct(vector1x, vector1y, vector2x, vector2y):
    return 10*(vector1x * vector2x + vector1y * vector2y)

def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def angle_between_vectors(vector1, vector2):
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    magnitude1 = math.sqrt(vector1[0]**2 + vector1[1]**2)
    magnitude2 = math.sqrt(vector2[0]**2 + vector2[1]**2)
    cos_theta = dot_product / (magnitude1 * magnitude2)
    # Ensure cos_theta is within [-1, 1] range to avoid invalid input to arccosine function
    cos_theta = max(min(cos_theta, 1), -1)
    angle_in_radians = math.acos(cos_theta)
    angle_in_degrees = math.degrees(angle_in_radians)

    # Find which side the vector is on
    cross_product = vector1[0] * vector2[1] - vector1[1] * vector2[0]
    if cross_product < 0: # right
        return angle_in_degrees
    else: #left
        return angle_in_degrees + 180

def gotoQuadrant(heading, quadrantNum):
    ## use robvectorx and robvectory
    getRobProduct(heading)
    quadrantCoords = anchorsc[quadrantNum]
    print(f'Quadrant Coords {quadrantCoords}')
    distance = distance_between_points([heading.robXm, heading.robYm], quadrantCoords) + 0.2
    driveVector = vectorDetector(heading.robXm, heading.robYm, quadrantCoords[0], quadrantCoords[1])
    print(f'This is inital values {heading.roborienx1} {heading.roborieny1}')
    print(f'This is the final values {heading.robXm} {heading.robYm}')
    print(f'This is the rob vector: {heading.robVectorX}, {heading.robVectorY}')
    print(f'This is the drive vector: {driveVector}')
    angle = angle_between_vectors([heading.robVectorX, heading.robVectorY], driveVector)
    rob.turnDegrees(angle)
    print("Angle: ", angle)
    print("Distance: ", distance*100)
    rob.secondstocentimetersforwardbackward(distance*100, 60, "forward")



def getRobProduct(type):
    #print("ROBS COORDINATES")
    rob1 = readSerial()
    time.sleep(1)
    #print("ROB P1")
    rob.setMotor(0, 7000)
    rob.setMotor(1, 5000)
    time.sleep(0.5)
    rob.setMotor(0, 6000)
    rob.setMotor(1, 6000)
    time.sleep(1)
    rob_coords = readSerial()
    rob.defaults()
    global anchors
    position = calcPosition(anchors, rob_coords)
    ##print(position)
    type.robposx = position[0]
    type.robposy = position[1]
    type.robXm = position[0]
    type.robYm = position[1]
    print(f'Robs Pos in m: {type.robXm} {type.robYm}')
    closestAnchor = rob_coords.index(min(rob_coords))
    ##if not type.said:
    ##    rob.say("Quadrant " + str(closestAnchor))
    ##    type.said = True
    type.closestAnchor = closestAnchor

    roborienx1, roborieny1 = calcPosition(anchors, rob1)
    type.roborienx1 = roborienx1
    type.roborieny1 = roborieny1
    robVectorX, robVectorY = vectorDetector(type.robXm, type.robYm, type.roborienx1, type.roborieny1)
    type.robVectorX = robVectorX * 10
    type.robVectorY = robVectorY * 10



class Headings:
    def __init__(self):
        self.robposx = 0
        self.robposy = 0
        self.closestAnchor = 0
        self.initialx = 0
        self.initialy = 0
        self.anchorVectorX = 0
        self.anchorVectorY = 0
        self.roborienx1 = 0
        self.roborieny1 = 0
        self.robVectorX = 0
        self.robVectorY = 0
        self.robProduct = 0
        self.robXm = 0
        self.robYm = 0
        self.said = False

    def printValues(self):
        print("X: {:.4f}".format(self.robposx))
        print("Y: {:.4f}".format(self.robposy))
        print("Anchor Vector <{:.4f}, {:.4f}>".format(self.anchorVectorX, self.anchorVectorY))
        print("Rob Vector <{:.4f}, {:.4f}>".format(self.robVectorX, self.robVectorY))
        print("ROB Product {:.4f}".format(self.robProduct))




if __name__ == "__main__":
    speaking_thread = Thread(target=run_speaking2)
    face_thread = Thread(target=rob.start_face)

    speaking_thread.start()
    face_thread.start()
    speaking_thread.join()
    face_thread.join()
