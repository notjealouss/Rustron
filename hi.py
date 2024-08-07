import speech_recognition as sr
import openai
import pyttsx3
import pyfirmata
import time

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

# Specify the port where your Arduino is connected
board = pyfirmata.Arduino('COM3')

# Start an iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(board)
it.start()

# Define a pin
led_pin = board.get_pin('d:13:o')

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
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def blink_led():
    for _ in range(3):
        led_pin.write(1)
        time.sleep(1)
        led_pin.write(0)
        time.sleep(1)

def main():
    while True:
        text = listen()
        if text:
            if "blink LED" in text:
                print("Special command recognized: Blinking LED")
                blink_led()
            else:
                response = get_response(text)
                print(f"AI: {response}")
                speak(response)

if __name__ == "__main__":
    main()
