import pyttsx3
from summerizer import summerizer


# initialize Text-to-speech engine
engine = pyttsx3.init()



def text_to_speech():
    # convert this text to speech
    text = summerizer()

    voices = engine.getProperty("voices")

    # for different voice type
    engine.setProperty("voice", voices[1].id)

    # from slower speaking rate
    engine.setProperty("rate", 150)

    engine.say(text)
    # play the speech
    engine.runAndWait()

while True:
    if __name__ == '__main__':
        text_to_speech()