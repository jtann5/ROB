from maestro import Controller
import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import time
import face

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

class FakeController():
    def setTarget(self, motor, value):
        print("Set motor " + str(motor) + " to value " + str(value))


class ROB:
    def __init__(self):
        self.controller = FakeController()

        self.voice = pyttsx3.init()
        self.voice.setProperty('volume', 1.0)
        self.voice.setProperty('rate', 150)
        self.voice.setProperty('voice', 'english-us')

        pygame.mixer.init()

        #self.face = face.RobotFace()
        #self.face.mainloop()

    def defaults(self):
        for i in range(17):
            self.controller.setTarget(i, 6000)

    def say(self, text):
        self.voice.say(text)
        self.voice.runAndWait()

    def gsay(self, text):
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_file:
            tts = gTTS(text=text, lang="en", slow=False)
            tts.write_to_fp(temp_file)
            temp_file.flush()
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

    def rizz(self):
        pygame.mixer.music.load("rizz.mp3")
        pygame.mixer.music.play()
        self.controller.setTarget(HEADTILT, 4000)
        self.controller.setTarget(HEADTURN, 7500)
        time.sleep(5)
        self.controller.setTarget(HEADTURN, 6000)
        self.controller.setTarget(HEADTILT, 6000)
        time.sleep(3)
        self.controller.setTarget(LEFTBICEP, 3500)
        self.controller.setTarget(RIGHTBICEP, 8500)
        time.sleep(1)
        self.controller.setTarget(LEFTBICEP, 6000)
        self.controller.setTarget(RIGHTBICEP, 6000)
        time.sleep(1)
        self.controller.setTarget(RIGHTSHOULDER, 4000)
        self.controller.setTarget(RIGHTELBOW, 8000)
        self.controller.setTarget(LEFTSHOULDER, 4000)
        self.controller.setTarget(LEFTELBOW, 8000)
        while pygame.mixer.music.get_busy():
            continue

    def fight(self):
        self.controller.setTarget(RIGHTSHOULDER, 4000)
        self.controller.setTarget(LEFTSHOULDER, 4000)

        time.sleep(1)
        self.controller.setTarget(RIGHTSHOULDER, 4000)
        self.controller.setTarget(RIGHTSHOULDER, 4000)
        time.sleep(1)
        self.controller.setTarget(RIGHTSHOULDER, 4000)
        self.controller.setTarget(RIGHTSHOULDER, 4000)

    def setMotor(self, motor, value):
        self.controller.setTarget(motor, value)