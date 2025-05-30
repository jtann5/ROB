import speech_recognition as sr
from DialogEngine import DialogEngine
from rob import rob
from threading import Thread

listening = True

def run_speaking():
    global listening
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()

    while listening:
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
                word = r.recognize_google(audio)
                print(word)
                if word.strip() == "bye":
                    listening = False
                else:
                    output = d.analyze(word.strip())
                    rob.say(output)
                    print(output)
            except sr.UnknownValueError:
                rob.say("Do not know that word human!")
                print("Don't know that word")


def UIlistening():
    global listening
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()
    listening = True

    while listening:
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
                word = r.recognize_google(audio)
                print(word)
                if word.strip() == "bye":
                    listening = False
                else:
                    output = d.analyze(word.strip())
                    rob.say(output)
                    print(output)
                    listening = False
            except sr.UnknownValueError:
                rob.say("Do not know that word human!")
                print("Don't know that word")


if __name__ == "__main__":
    speaking_thread = Thread(target=run_speaking)
    face_thread = Thread(target=rob.start_face)

    speaking_thread.start()
    face_thread.start()
    speaking_thread.join()
    face_thread.join()


