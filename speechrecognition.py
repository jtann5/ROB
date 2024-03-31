import speech_recognition as sr
from DialogEngine import DialogEngine
from rob import rob
from threading import Thread

listening = True

def run_speaking():
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()

    while listening:
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = 8000

            try:
                print("listening")
                audio = r.listen(source, timeout=None)
                print("got audio")
                word = r.recognize_google(audio)
                print(word)
                run = True
                if word.strip() == "bye":
                    run = False
                    break
                while run:
                    output = d.analyze(word.strip())
                    rob.say(output)
                    print(output)
                    print("listening")
                    audio = r.listen(source)
                    print("got audio")
                    word = r.recognize_google(audio)
                    if word.strip() != "bye":
                        run = False
            except sr.UnknownValueError:
                print("Don't know that word")


if __name__ == "__main__":
    speaking_thread = Thread(target=run_speaking)
    face_thread = Thread(target=rob.start_face)

    speaking_thread.start()
    face_thread.start()
    speaking_thread.join()
    face_thread.join()


