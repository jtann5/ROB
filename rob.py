from maestro import Controller
import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import time

MOTORMAIN = 0
MOTORTURN = 1
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

        pygame.mixer.init()

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
        time.sleep(7)
        self.controller.setTarget(HEADTURN, 6000)
        self.controller.setTarget(HEADTILT, 6000)
        time.sleep(5)
        self.controller.setTarget(RIGHTBICEP, 7500)
        time.sleep(1)
        self.contoller.setTarget(RIGHTSHOULDER, 7500)
        self.controller.setTarget(RIGHTBICEP, 4000)
        while pygame.mixer.music.get_busy():
                continue

rob = ROB()
rob.defaults()
rob.say("Rizz mode activated")
rob.rizz()