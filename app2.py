import speech_recognition as sr
import os

open_tokens = ["open", "launch", "start"]
close_tokens = ["close", "exit", "quit"]

# Create recognizer object
recognizer = sr.Recognizer()

# Use the default microphone
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
    print("🎙️ Say something:")
    try:
        audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
    except Exception:
        print("listen() failed, falling back to record()")
        audio = recognizer.record(source, duration=3)


    try:
        text = recognizer.recognize_google(audio)
        print("📝 You said:", text)

        tokens = text.lower().split()
        print("Tokens:", tokens)
        def parse_command(tokens):
            intent = None
            for token in tokens:
                if token in open_tokens:
                    intent = "open"
                    break
                elif token in close_tokens:
                    intent = "close"
                    break
            print("Intent:", intent)
            return intent
            
        parse_command(tokens)
           

        # Define the function to open the app
        def open_app(app):
            if "chrome" in app.lower():
                os.system("start chrome")
            elif "notepad" in app.lower():
                os.system("start notepad")
            else:
                print(f"🚫 Application not recognized or not supported.")

        # Find the app name from tokens and call open_app
        for token in tokens:
            if token in ["chrome", "notepad"]:
                open_app(token)
                break


    except sr.UnknownValueError:
        print("❌ Sorry, I didn't catch that.")
    except sr.RequestError as e:
        print("🚫 Error from Google Speech Recognition:", e)
