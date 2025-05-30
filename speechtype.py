from DialogEngine import DialogEngine
from robNoFace import rob
from threading import Thread

def run_speaking():
    d = DialogEngine()
    d.setFile('dialogInput.txt')
    d.openFile()
    running = True

    while running:
        print("Enter text: ")
        word = input(">>> ")
        if word.strip() == "bye":
            break
        output = d.analyze(word.strip())
        rob.say(output)
        print("Robot: " + str(output))



if __name__ == "__main__":
    speaking_thread = Thread(target=run_speaking)
    face_thread = Thread(target=rob.start_face)

    speaking_thread.start()
    face_thread.start()
    speaking_thread.join()
    face_thread.join()


