import speech_recognition as sr
from flask import render_template


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak my Lord!")
    audio = r.listen(source, timeout=100.0, phrase_time_limit=100.0)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")

        if "dog" in text:
            if "title" in text:
                pass










    except:
        print("sorry")