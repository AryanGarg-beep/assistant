import speech_recognition as sr
import os
import psutil
import time

open_tokens = ["open", "launch", "start"]
close_tokens = ["close", "exit", "quit"]
exit_tokens = ["stop program", "exit program", "quit program"]

# ------------ Parse Intent and App ------------
def parse_command(tokens):
    intent = None
    for token in tokens:
        if token in open_tokens:
            intent = "open"
            break
        elif token in close_tokens:
            intent = "close"
            break
    tokens = [t for t in tokens if t not in open_tokens + close_tokens]
    app_name = " ".join(tokens).strip()
    return intent, app_name


# ------------ Open App ------------
def open_app(app):
    if "chrome" in app:
        os.system("start chrome")
    elif "notepad" in app:
        os.system("start notepad")
    else:
        print(f"🚫 Cannot open '{app}' — not recognized.")


# ------------ Close App ------------
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


# ------------ Main Loop ------------
recognizer = sr.Recognizer()

print("🧠Assistant is running")

while True:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            print("\n🎙️ Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except Exception:
            print("⚠️ listen() failed, falling back to record()")
            audio = recognizer.record(source, duration=5)

        try:
            text = recognizer.recognize_google(audio)
            print("📝 You said:", text.lower())

            # Check if user wants to exit
            if any(phrase in text.lower() for phrase in exit_tokens):
                print("👋 Exiting")
                break

            tokens = text.lower().split()
            intent, app = parse_command(tokens)

            if intent == "open":
                open_app(app)
            elif intent == "close":
                close_app(app)
            else:
                print("🤔 No recognizable command found.")

        except sr.UnknownValueError:
            print("❌ Couldn’t understand the audio.")
        except sr.RequestError as e:
            print(f"🚫 Google Speech Recognition error: {e}")
        except Exception as e:
            print(f"❗ Unexpected error: {e}")

    time.sleep(1)  # short delay before next listen
