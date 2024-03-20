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
        self.voice = pyttsx3.init()
        self.voice.setProperty('volume', 1.0)
        self.voice.setProperty('rate', 150)
        self.voice.setProperty('voice', 'english-us')
        self.speaking_process = None
        pygame.mixer.init()
        self.face = RobotFace()
        # self.face.animate_eyes()

    def defaults(self):
        pygame.mixer.music.stop()
        for i in range(17):
            self.controller.setTarget(i, 6000)

    def say(self, text):
        self.face.set_robot_state("talking")
        if (self.voice._inLoop):
            self.voice.endLoop()
        self.voice.say(text)
        self.voice.runAndWait()
        #subprocess.call(['espeak', text])
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

    def start_face(self):
        rob.face.initialize_pygame()
        rob.face.animate_eyes()

rob = ROB()


if __name__ == "__main__":
    rob = ROB()

