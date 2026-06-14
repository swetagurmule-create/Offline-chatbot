# -----------------------------------------
# Project: Offline AI Assistant
# Developer: Sweta Gajanan Gurmule
# Description: Offline ChatGPT-like AI with Voice Support
# -----------------------------------------

import ollama
import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer
import pyttsx3

model = Model("vosk-model-small-en-in-0.4")
recognizer = KaldiRecognizer(model, 16000)

engine = pyttsx3.init()

def speak(text):
    print("AI:", text)
    engine.say(text)
    engine.runAndWait()

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

messages = []

print("Voice Chatbot Started")
print("Say 'exit' to stop")

with sd.RawInputStream(samplerate=16000, blocksize=8000,
                       dtype='int16', channels=1,
                       callback=callback):

    while True:
        data = q.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            user_input = result.get("text", "")

            print("You:", user_input)

            if user_input.lower() == "exit":
                break

            messages.append({
                "role": "user",
                "content": user_input + ". Answer in 2-3 lines only."
            })

            response = ollama.chat(
                model="mistral",
                messages=messages,
                options={"num_predict": 50}
            )

            reply = response["message"]["content"]
            messages.append({"role": "assistant", "content": reply})

            speak(reply)

            if len(messages) > 6:
                messages = []