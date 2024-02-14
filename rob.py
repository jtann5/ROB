from maestro import Controller
import pyttsx3
from gtts import gTTS
import pygame
import tempfile

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
        rob.setProperty('volume', 1.0)
        rob.setProperty('rate', 150)
        rob.setProperty('voice', 'english-us')

        pygame.mixer.init()

    def setDefaults(self):
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
        pygame.mixer.music.load(rizz.mp3)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
                continue

rob = ROB()
rob.setDefaults()
rob.say("Kill mode activated")