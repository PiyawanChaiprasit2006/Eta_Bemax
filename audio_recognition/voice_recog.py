# import pvporcupine
# import pyaudio
# import struct
# import os

# # Set the path to your custom wake word model
# custom_wake_word_path = os.path.join("Final_Engineering_Project\audio_recognition\Help_me_raspi.ppn", "Help_me_raspi.ppn")  # Replace with your actual path

# porcupine = pvporcupine.create(
#     keyword_paths=[custom_wake_word_path],  # Use your custom wake word model path
#     sensitivities=[0.5]  # Adjust sensitivity (0.0 to 1.0) as needed
# )

# pa = pyaudio.PyAudio()
# audio_stream = pa.open(
#     rate=porcupine.sample_rate,
#     channels=1,
#     format=pyaudio.paInt16,
#     input=True,
#     frames_per_buffer=porcupine.frame_length
# )

# print("Listening for the wake word...")

# try:
#     while True:
#         pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
#         pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
#         result = porcupine.process(pcm)

#         if result >= 0:
#             print("Wake word detected!")
#             # Trigger your robot's action here
# finally:
#     audio_stream.close()
#     pa.terminate()
#     porcupine.delete()

import pvporcupine
import pyaudio
import struct
import os

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
    sensitivities=[0.5]  # Adjust sensitivity as needed
)

# Function to get the default microphone device index
def get_default_microphone_index(pa):
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if "microphone" in info["name"].lower():
            return i
    print("No microphone detected. Please ensure your microphone is enabled.")
    exit()

pa = pyaudio.PyAudio()

# Get the default microphone
device_index = get_default_microphone_index(pa)

# Open audio stream
try:
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=porcupine.frame_length
    )
except Exception as e:
    print(f"Failed to open audio stream: {e}")
    pa.terminate()
    exit()

print("Listening for the wake word... Press Ctrl+C to stop.")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)

        if result >= 0:
            print("Wake word detected! Recognized text: 'help me'")
            # Trigger your robot's action here

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
