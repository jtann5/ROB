import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import time
from face import RobotFace
import os
import threading
import random
import math

def is_raspberry_pi():
    try:
        return os.uname()[1] == 'raspberrypi'
    except AttributeError:
        return False

if is_raspberry_pi():
    from maestro import Controller
else:
    class Controller():
        def setTarget(self, motor, value):
            print("Set motor " + str(motor) + " to value " + str(value))

LEFTMOTOR = 0
RIGHTMOTOR = 1
WAIST = 2
HEADTILT = 3
HEADTURN = 4
RIGHTSHOULDER = 5
RIGHTBICEP = 6
RIGHTELBOW = 7
RIGHTFOREARM = 8
RIGHTWRIST = 9
RIGHTCLAW = 10
LEFTSHOULDER = 11
LEFTBICEP = 12
LEFTELBOW = 13
LEFTFOREARM = 14
LEFTWRIST = 15
LEFTCLAW = 16


class ROB:
    def __init__(self):
        self.controller = Controller()
        self.speaking_process = None
        pygame.mixer.init()
        self.face = RobotFace()
        self.motor_value = [None] * 17
        self.speech_lock = False
        #self.movements = [self.raiseLeftArm, self.raiseRightArm, self.lowerLeftArm, self.lowerRightArm, self.claspHands, self.lectureFinger, self.handWaive, self.pointingToHand, self.bigPicture, self.sweeping, self.nodding, self.shakinghead, self.lookleft, self.lookright, self.lookup, self.lookdown, self.lookintotheabyss]
        self.movements = [self.raiseLeftArm, self.raiseRightArm, self.lowerLeftArm, self.lowerRightArm, self.claspHands, self.lectureFinger, self.handWaive, self.pointingToHand, self.bigPicture, self.sweeping, self.lookleft, self.lookright, self.lookup, self.lookdown, self.lookintotheabyss]
        # self.face.animate_eyes()
        # self.face.animate_eyes()
        self.defaults()

    def defaults(self):
        pygame.mixer.music.stop()
        for i in range(17):
            self.setMotor(i, 6000)

    def smoothDefaults(self):
        pygame.mixer.music.stop()
        threads = []
        for i in range(17):
            thread = threading.Thread(target=rob.setMotorTime, args=(i, 6000, 0.3))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    
    def sayThread(self, text):
        if not self.speech_lock:
            self.speech_lock = True
            thread = threading.Thread(target=rob.say, args=(text,))
            thread.start()

    def randomMovement(self):
        random_movement = random.choice(self.movements)
        random_movement()


    def say(self, text):
        self.face.set_robot_state("talking")
        voice = pyttsx3.init()
        voice.setProperty('volume', 1.0)
        voice.setProperty('rate', 150)
        voice.setProperty('voice', 'english-us')
        voice.say(text)
        voice.runAndWait()
        self.face.set_robot_state("idle")
        self.speech_lock = False

    def gsay(self, text):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
            tts = gTTS(text=text, lang="en", slow=False)
            tts.write_to_fp(temp_file)
            temp_file.flush()
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

    def setMotor(self, motor, value):
        self.controller.setTarget(motor, value)
        self.motor_value[motor] = value

    def setMotorTime(self, motor, value, seconds):
        resolution = 0.001
        curr_value = self.motor_value[motor] # get the current value
        steps = seconds/resolution # number of steps
        amount = (value - curr_value)/steps # amount for each step
        for i in range(int(steps)):
            self.setMotor(motor, int(curr_value+(amount*i)))
            time.sleep(resolution)
        self.setMotor(motor, value)
        

    def start_face(self):
        rob.face.initialize_pygame()
        rob.face.animate_eyes()

    def alexMode(self):
        for i in range(15):
            self.setMotor(i+2, 4000)
        self.smoothDefaults()


    # For Project 10 Dynamic Personality Engine
    # Should have 10 different arm gestures and 5 different head movements
    # These animations should be smooth and natural looking

    # These can change but they are just placeholders

    # Arm Gestures
    def raiseLeftArm(self):
        # shoulder down to the minimum
        # elbow to the max
        thread1 = threading.Thread(target=rob.setMotorTime, args=(11, 4000, 1))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(13, 8000, 1))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

    def raiseRightArm(self):
        # should up to the max
        # elbow to the max
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 8000, 1))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(7, 8000, 1))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

    def lowerLeftArm(self):
        # shoulder down to the max
        # elbow to the min
        thread1 = threading.Thread(target=rob.setMotorTime, args=(11, 8000, 1))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(13, 4000, 1))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

    def lowerRightArm(self):
        # should up to the min
        # elbow to the min
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 4000, 1))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(7, 4000, 1))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

    def claspHands(self):
        # puts hands close together but out in front
        # left should min
        # right shoulder max
        # left bicep max
        # right bicep min
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 8000, 1))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(11, 4000, 1))
        thread3 = threading.Thread(target=rob.setMotorTime, args=(6, 4000, 1))
        thread4 = threading.Thread(target=rob.setMotorTime, args=(12, 8000, 1))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()


    def lectureFinger(self):
        # one arm elbow is bent and the robot moves the elbow up and down as if it is lecturing you
        # right shoulder goes slightly down like 10%
        # right elbow goes down blow default
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 8000, 0.5))
        thread1.start()
        thread1.join()
        for i in range(3):
            thread2 = threading.Thread(target=rob.setMotorTime, args=(7, 4000, 0.5))
            thread2.start()
            thread2.join()
            thread2 = threading.Thread(target=rob.setMotorTime, args=(7, 6000, 0.5))
            thread2.start()
            thread2.join()

    def handWaive(self):
        #robot waves
        # right shoulder up
        # right bicep left and right
        # right elbow up
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 8000, 0.5))
        thread1.start()
        thread2 = threading.Thread(target=rob.setMotorTime, args=(7, 8000, 0.5))
        thread2.start()
        thread1.join()
        thread2.join()
        for i in range(3):
            thread3 = threading.Thread(target=rob.setMotorTime, args=(6, 4000, 0.5))
            thread3.start()
            thread3.join()
            thread3 = threading.Thread(target=rob.setMotorTime, args=(6, 8000, 0.5))
            thread3.start()
            thread3.join()

    def pointingToHand(self):
        # robot takes one hand and points towards the other hand to convey something
        # left elbow up and down
        # left shoulder %60 to the min
        # left bicep to the max
        # right should 20% up
        # right bicep down
        # right elbow 20% down
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 6400, 0.5))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(11, 4800, 0.5))
        thread3 = threading.Thread(target=rob.setMotorTime, args=(6, 4000, 0.5))
        thread4 = threading.Thread(target=rob.setMotorTime, args=(12, 8000, 0.5))
        thread5 = threading.Thread(target=rob.setMotorTime, args=(7, 5600, 0.5))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        for i in range(3):
            self.setMotorTime(13, 4000, 0.5)
            self.setMotorTime(13, 8000, 0.5)



    def bigPicture(self):
        #arms are together and get bigger to convey a bigger picture
        # left shoulder min
        # right shoulder max
        # left bicep max to min
        # right bicep min to max
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 8000, 0.5))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(11, 4000, 0.5))
        thread3 = threading.Thread(target=rob.setMotorTime, args=(6, 4000, 0.5))
        thread4 = threading.Thread(target=rob.setMotorTime, args=(12, 8000, 0.5))
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5 = threading.Thread(target=rob.setMotorTime, args=(6, 8000, 1))
        thread6 = threading.Thread(target=rob.setMotorTime, args=(12, 4000, 1))
        thread5.start()
        thread6.start()
        thread5.join()
        thread6.join()   

    def sweeping(self):
        # one hand
        #right shoulder max up
        #right bicep from mix to max
        thread1 = threading.Thread(target=rob.setMotorTime, args=(5, 8000, 0.5))
        thread2 = threading.Thread(target=rob.setMotorTime, args=(6, 4000, 0.5))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        self.setMotorTime(6, 8000, 1)

    # Face Gestures
    def nodding(self):
        # robot face goes up and down to indicate yes
        for i in range(3):
            self.setMotorTime(3, 4000, 0.5)
            self.setMotorTime(3, 8000, 0.5)
        self.setMotorTime(3, 6000, 0.25)

    def shakinghead(self):
        # robot face goes left and right to indicate no
        for i in range(3):
            self.setMotorTime(4, 4000, 0.5)
            self.setMotorTime(4, 8000, 0.5)
        self.setMotorTime(4, 6000, 0.25)

    def lookleft(self):
        # robot face looks left needs to be smooth cant just go to value
        self.setMotorTime(4, 8000, 0.5)

    def lookright(self):
        # robot face looks right needs to be smooth cant just go to value
        self.setMotorTime(4, 4000, 0.5)

    def lookup(self):
        self.setMotorTime(3, 8000, 0.5)

    def lookdown(self):
        self.setMotorTime(3, 4000, 0.5)

    def lookintotheabyss(self):
        val = random.randint(0, 4000)
        self.setMotorTime(4, 4000+val, 0.5)
        time.sleep(0.5)


    def secondstocentimetersforwardbackward(self, centimeters, speed, direction):
        ## conversion factor is seconds/centimeters this can change to a function if we graph the amount of power
        ft = int(centimeters/2.54)/12
        ##print(ft)
        ##conversionFactor = -0.00501636 * (math.log(ft - 0.948925) / 1) + math.exp(-3.77479)
        conversionFactor = 0.0175
        if centimeters < 35:
            conversionFactor = 0.0175
        elif centimeters > 34 and centimeters < 60:
            conversionFactor = 0.0145
        elif centimeters > 59 and centimeters < 90:
            conversionFactor = 0.0129
        elif centimeters > 89 and centimeters < 120:
            conversionFactor = 0.0126
        elif centimeters > 119 and centimeters < 150:
            conversionFactor = 0.0123
        elif centimeters > 149 and centimeters < 180:
            conversionFactor = 0.01215
        elif centimeters > 179 and centimeters < 210:
            conversionFactor = 0.0119
        elif centimeters > 209 and centimeters < 240:
            conversionFactor = 0.01165
        elif centimeters > 239 and centimeters < 270:
            conversionFactor = 0.01152
        else:
            conversionFactor = 0.01152
        print(conversionFactor)
        amt_time = centimeters * conversionFactor

        if direction == "forward":
            rob.setMotor(0,  6000 - int(speed * 19.37))
            rob.setMotor(1, 6000 + (speed * 20))
            time.sleep(amt_time)
        else:
            rob.setMotor(0, 6000 + int(speed * 20))
            rob.setMotor(1, 6000 - (speed * 20))
            time.sleep(amt_time)
        rob.setMotor(0, 6000)
        rob.setMotor(1, 6000)


    def secondstodegreesturn(self, seconds, direction):
        factor = 778
        if direction == "right":
            rob.setMotor(0, 6000 - factor)
            rob.setMotor(1, 6000 - factor)
            time.sleep(seconds)
        else:
            factor = 830
            rob.setMotor(0, 6000 + factor)
            rob.setMotor(1, 6000 + factor)
            time.sleep(seconds)
        rob.setMotor(0, 6000)
        rob.setMotor(1, 6000)

    def turnDegrees(self, degrees):
        speed = 1500
        if (degrees <= 180):
            if degrees <= 45:
                factor = 0.0069
            elif degrees >= 135:
                factor = 0.0049
            else:
                factor = 0.0052
            
            rob.setMotor(0, 6000 - speed)
            rob.setMotor(1, 6000 - speed)
            time.sleep(degrees * factor)
        else:
            if degrees <= 45:
                factor = 0.0071
            elif degrees >= 135:
                factor = 0.0051
            else:
                factor = 0.0056

            rob.setMotor(0, 6000 + speed)
            rob.setMotor(1, 6000 + speed)
            time.sleep((360 - degrees) * factor)
        rob.setMotor(0, 6000)
        rob.setMotor(1, 6000)

rob = ROB()


if __name__ == "__main__":
    rob = ROB()
    rob.turnDegrees(172)
    #rob.sayThread("Hello")
    #for i in range(4):
    #    rob.sayThread("You get the joke")
    #    rob.alexMode()


