import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import time
from face import RobotFace
import os
import threading

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
        # self.face.animate_eyes()

    def defaults(self):
        pygame.mixer.music.stop()
        for i in range(17):
            self.setMotor(i, 6000)

    def say(self, text):
        self.face.set_robot_state("talking")
        voice = pyttsx3.init()
        voice.setProperty('volume', 1.0)
        voice.setProperty('rate', 150)
        voice.setProperty('voice', 'english-us')
        voice.say(text)
        voice.runAndWait()
        self.face.set_robot_state("idle")

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
        resolution = 0.01
        curr_value = self.motor_value[motor] # get the current value
        steps = seconds/resolution # number of steps
        amount = (value - curr_value)/steps # amount for each step
        for i in range(int(steps)):
            self.setMotor(motor, int(curr_value+(amount*i)))
            time.sleep(resolution)
            print(i, " ", int(curr_value+(amount*i)))
        self.setMotor(motor, value)
        print("Finish: ", value)
        

    def start_face(self):
        rob.face.initialize_pygame()
        rob.face.animate_eyes()


    # For Project 10 Dynamic Personality Engine
    # Should have 10 different arm gestures and 5 different head movements
    # These animations should be smooth and natural looking

    # These can change but they are just placeholders

    # Arm Gestures
    def raiseLeftArm(self):
        # shoulder down to the minimum
        # elbow to the max
        pass

    def raiseRightArm(self):
        # should up to the max
        # elbow to the max
        pass

    def claspHands(self):
        # puts hands close together but out in front
        # left should min
        # right shoulder max
        # left bicep max
        # right bicep min
        pass


    def lectureFinger(self):
        # one arm elbow is bent and the robot moves the elbow up and down as if it is lecturing you
        # right shoulder goes slightly down like 10%
        # right elbow goes down blow default
        pass

    def handWaive(self):
        #robot waves
        # right shoulder up
        # right bicep left and right
        # right elbow up
        pass

    def pointingToHand(self):
        # robot takes one hand and points towards the other hand to convey something
        # left elbow up and down
        # left shoulder %60 to the min
        # left bicep to the max
        # right should 20% up
        # right bicep down
        # right elbow 20% down
        pass


    def bigPicture(self):
        #arms are together and get bigger to convey a bigger picture
        # left shoulder min
        # right shoulder max
        # left bicep max to min
        # right bicep min to max
        pass

    def sitdownGesture(self):
        # arms are slightly wider and motion to sit down by going up and down or sort of settle down gesture?
        #
        pass

    def sweeping(self):
        # one hand
        #right shoulder max up
        #right bicep from mix to max
        pass

    # Face Gestures
    def nodding(self):
        # robot face goes up and down to indicate yes
        pass

    def shakinghead(self):
        # robot face goes left and right to indicate no
        pass

    def lookleft(self):
        # robot face looks left needs to be smooth cant just go to value
        pass

    def lookright(self):
        # robot face looks right needs to be smooth cant just go to value
        pass

    def lookup(self):
        pass

    def lookdown(self):
        pass

    def lookintotheabyss(self):
        pass


rob = ROB()


if __name__ == "__main__":
    rob = ROB()
    rob.defaults()
    time.sleep(1)
    rob.setMotorTime(4, 4000, 1)
    rob.setMotorTime(4, 8000, 3)

