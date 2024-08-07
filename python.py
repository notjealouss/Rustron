import speech_recognition as sr
import copilot
import pyttsx3
import pyaudio
# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set your OpenAI API key
copilot.api_key = '237e13d22d9642c3831a18939252ec9f.a4910c4893f716b3'

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

def get_response(text):
    response = copilot.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        text = listen()
        if text:
            if "special command" in text:
                print("Special command recognized!")
                # Add your unique signal handling code here
            else:
                response = get_response(text)
                print(f"AI: {response}")
                speak(response)