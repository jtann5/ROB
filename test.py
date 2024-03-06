import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(f"Voice ID: {voice.id}, Name: {voice.name}")

engine.setProperty('volume', 1.0)
engine.setProperty('rate', 150)
engine.setProperty('voice', 'english-us')
def fuck():
    engine.say("FUCK SHIT")
    engine.runAndWait()


for i in range(10):
       fuck()