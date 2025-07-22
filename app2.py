import speech_recognition as sr
import os

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
        app = recognizer.recognize_google(audio)
        print("📝 You said:", app)
        
        # Call the function to open the app
        def open_app(app):
            if "chrome" in app.lower():
                os.system("start chrome")
            elif "notepad" in app.lower():
                os.system("start notepad")
            else:
                print(f"🚫 Application not recognized or not supported.")

        open_app(app)

    except sr.UnknownValueError:
        print("❌ Sorry, I didn't catch that.")
    except sr.RequestError as e:
        print("🚫 Error from Google Speech Recognition:", e)
