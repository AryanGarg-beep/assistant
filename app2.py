import speech_recognition as sr
import os
import psutil

open_tokens = ["open", "launch", "start"]
close_tokens = ["close", "exit", "quit"]

# ------------ parse command ------------
def parse_command(tokens):
    intent = None
    for token in tokens:
        if token in open_tokens:
            intent = "open"
            break
        elif token in close_tokens:
            intent = "close"
            break

    # Remove the intent token from tokens
    tokens = [t for t in tokens if t not in open_tokens + close_tokens]

    app_name = " ".join(tokens).strip()
    return intent, app_name


# ------------ Open app ------------
def open_app(app):
    if "chrome" in app:
        os.system("start chrome")
    elif "notepad" in app:
        os.system("start notepad")
    else:
        print(f"🚫 Cannot open '{app}' — not recognized.")


# ------------ Close app using psutil ------------
def close_app(app):
    targets = []

    if "chrome" in app:
        targets = ["chrome.exe"]
    elif "notepad" in app:
        targets = ["notepad.exe"]
    else:
        print(f"🚫 Cannot close '{app}' — not recognized.")
        return

    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() in targets:
            print(f"⛔ Closing {proc.info['name']} (PID {proc.info['pid']})")
            proc.terminate()
            found = True
    if not found:
        print(f"❌ No running instance of '{app}' found.")


# ------------ Voice Recognition ------------
recognizer = sr.Recognizer()

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
        intent, app = parse_command(tokens)

        if intent == "open":
            open_app(app)
        elif intent == "close":
            close_app(app)
        else:
            print("🤔 Sorry, I didn't catch an action.")

    except sr.UnknownValueError:
        print("❌ Couldn’t understand the audio.")
    except sr.RequestError as e:
        print(f"🚫 Google Speech Recognition error: {e}")
    except Exception as e:
        print(f"❗ Unexpected error: {e}")
