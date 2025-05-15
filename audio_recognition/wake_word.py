import pvporcupine
import pyaudio
import struct
import os
import speech_recognition as sr
import time

# Set your Picovoice Access Key here
ACCESS_KEY = "gaoJG0yVsQvUN1+vpsZGVNb7Fid1gpCgBuEPUb385ZD2Sx9CFi32+g=="  # Replace with your actual access key

# Set the path to your custom wake word model
CUSTOM_WAKE_WORD_PATH = os.path.join("Final_Engineering_Project", "audio_recognition", "helpme_window.ppn")

# Check if the wake word model file exists
if not os.path.exists(CUSTOM_WAKE_WORD_PATH):
    print(f"Wake word model file not found at {CUSTOM_WAKE_WORD_PATH}")
    exit()

# Initialize Porcupine with custom wake word
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keyword_paths=[CUSTOM_WAKE_WORD_PATH],
    sensitivities=[0.5]
)

pa = pyaudio.PyAudio()

# Open audio stream
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

recognizer = sr.Recognizer()
microphone = sr.Microphone()

print("Listening for the wake word... Press Ctrl+C to stop.")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)

        if result >= 0:
            print("Wake word detected! Recognized text: 'Help me'")
            print("Listening for the command...")
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)

            try:
                command = recognizer.recognize_google(audio).lower()
                print(f"Recognized command: {command}")

                if "come to me" in command:
                    print("[ACTION] Moving towards the person.")
                elif "open" in command:
                    print("[ACTION] Opening compartment.")
                else:
                    print("[WARNING] Command not recognized.")

            except sr.UnknownValueError:
                print("[ERROR] Could not understand the command.")
            except sr.RequestError as e:
                print(f"[ERROR] Could not request results: {e}")

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
