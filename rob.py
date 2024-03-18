import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import time
from threading import Thread
from multiprocessing import Process
import face

import os

rob_instance = None

import platform

def is_raspberry_pi():
    """Check if the current system is a Raspberry Pi."""
    return os.uname()[1] == 'raspberrypi'

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
    def __init__(self, queue=None):
        self.controller = Controller()
        self.voice = pyttsx3.init()
        self.queue = queue
        self.voice.setProperty('volume', 1.0)
        self.voice.setProperty('rate', 150)
        #self.voice.setProperty('voice', 'english-us')
        if not hasattr(self, 'face'):
            self.face = face.RobotFace(queue)
        pygame.mixer.init()
        # self.face.animate_eyes()

    def set_queue(self, queue):
        self.queue = queue

    def defaults(self):
        pygame.mixer.music.stop()
        for i in range(17):
            self.controller.setTarget(i, 6000)

    def say(self, text):
        if self.queue is not None:
            self.queue.put("talking")
        if (self.voice._inLoop):
            self.voice.endLoop()
        self.voice.say(text)
        self.voice.runAndWait()
        if self.queue is not None:
            self.queue.put("idle")

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

    def get_robot_face(self):
        return self.face


def get_rob_instance(queue=None):
    global rob_instance
    if rob_instance is None:
        rob_instance = ROB(queue)
    else:
        rob_instance.queue = queue
    return rob_instance


if __name__ == "__main__":
    rob = ROB()
