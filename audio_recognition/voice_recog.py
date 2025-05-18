

# import pvporcupine
# import pyaudio
# import struct
# import os

# # Set your Picovoice Access Key here
# ACCESS_KEY = "kZvkhgCgIlxxRieDyhRW+gI4G0tm7UibG6tYqnip1zpAJOIbXmASJA=="  # Replace with your actual access key

# # Set the path to your custom wake word model
# CUSTOM_WAKE_WORD_PATH = "/home/piyawan/Final_Engineering_Project/audio_recognition/raspberry_help_me.ppn"

# # Check if the wake word model file exists
# if not os.path.exists(CUSTOM_WAKE_WORD_PATH):
#     print(f"Wake word model file not found at {CUSTOM_WAKE_WORD_PATH}")
#     exit()

# # Initialize Porcupine with custom wake word
# porcupine = pvporcupine.create(
#     access_key=ACCESS_KEY,
#     keyword_paths=[CUSTOM_WAKE_WORD_PATH],
#     sensitivities=[0.5]  # Adjust sensitivity as needed
# )

# # Function to get the default microphone device index
# def get_default_microphone_index(pa):
#     for i in range(pa.get_device_count()):
#         info = pa.get_device_info_by_index(i)
#         if "microphone" in info["name"].lower():
#             return i
#     print("No microphone detected. Please ensure your microphone is enabled.")
#     exit()

# pa = pyaudio.PyAudio()

# # Get the default microphone
# device_index = get_default_microphone_index(pa)

# # Open audio stream
# try:
#     audio_stream = pa.open(
#         rate=porcupine.sample_rate,
#         channels=1,
#         format=pyaudio.paInt16,
#         input=True,
#         input_device_index=device_index,
#         frames_per_buffer=porcupine.frame_length
#     )
# except Exception as e:
#     print(f"Failed to open audio stream: {e}")
#     pa.terminate()
#     exit()

# print("Listening for the wake word... Press Ctrl+C to stop.")

# try:
#     while True:
#         pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
#         pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
#         result = porcupine.process(pcm)

#         if result >= 0:
#             print("Wake word detected! Recognized text: 'help me'")
#             # Trigger your robot's action here

# except KeyboardInterrupt:
#     print("\nStopped by user.")

# finally:
#     audio_stream.close()
#     pa.terminate()
#     porcupine.delete()
# import pvporcupine
# import pyaudio
# import struct
# import os

# ACCESS_KEY = "kZvkhgCgIlxxRieDyhRW+gI4G0tm7UibG6tYqnip1zpAJOIbXmASJA=="
# CUSTOM_WAKE_WORD_PATH = "/home/piyawan/Final_Engineering_Project/audio_recognition/raspberry_help_me.ppn"

# if not os.path.exists(CUSTOM_WAKE_WORD_PATH):
#     print(f"Wake word model file not found at {CUSTOM_WAKE_WORD_PATH}")
#     exit()

# # Initialize Porcupine
# porcupine = pvporcupine.create(
#     access_key=ACCESS_KEY,
#     keyword_paths=[CUSTOM_WAKE_WORD_PATH],
#     sensitivities=[0.5]
# )

# pa = pyaudio.PyAudio()
# device_index = 1  # USB Microphone index (adjust if necessary)

# # Auto-detect a compatible sample rate (44100 or 48000)
# SUPPORTED_SAMPLE_RATES = [44100, 48000, porcupine.sample_rate]
# sample_rate = None

# for rate in SUPPORTED_SAMPLE_RATES:
#     try:
#         stream = pa.open(
#             rate=rate,
#             channels=1,
#             format=pyaudio.paInt16,
#             input=True,
#             input_device_index=device_index,
#             frames_per_buffer=porcupine.frame_length
#         )
#         stream.close()
#         sample_rate = rate
#         print(f"Using compatible sample rate: {sample_rate} Hz")
#         break
#     except:
#         continue

# if sample_rate is None:
#     print("No compatible sample rate found. Exiting.")
#     pa.terminate()
#     exit()

# # Open audio stream with the detected sample rate
# audio_stream = pa.open(
#     rate=sample_rate,
#     channels=1,
#     format=pyaudio.paInt16,
#     input=True,
#     input_device_index=device_index,
#     frames_per_buffer=porcupine.frame_length
# )

# print("Listening for the wake word... Press Ctrl+C to stop.")

# try:
#     while True:
#         pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
#         pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
#         result = porcupine.process(pcm)

#         if result >= 0:
#             print("Wake word detected! Recognized text: 'help me'")
#             # Trigger your robot's action here

# except KeyboardInterrupt:
#     print("\nStopped by user.")

# finally:
#     audio_stream.close()
#     pa.terminate()
#     porcupine.delete()


# import pvporcupine
# import pyaudio
# import struct
# import os


# ACCESS_KEY = "kZvkhgCgIlxxRieDyhRW+gI4G0tm7UibG6tYqnip1zpAJOIbXmASJA=="
# KEYWORD_PATH = "/home/piyawan/Final_Engineering_Project/audio_recognition/raspberry_help_me.ppn"

# porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_PATH])

# print("Porcupine requires sample rate:", porcupine.sample_rate)

# p = pyaudio.PyAudio()
# device_index = 1  # Adjust

# stream = p.open(
#     rate=porcupine.sample_rate,
#     channels=1,
#     format=pyaudio.paInt16,
#     input=True,
#     input_device_index=device_index,
#     frames_per_buffer=porcupine.frame_length
# )

# print("Listening for wake word...")

# try:
#     while True:
#         pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
#         pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
#         result = porcupine.process(pcm)
#         if result >= 0:
#             print("Wake word detected!")
# except KeyboardInterrupt:
#     pass
# finally:
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#     porcupine.delete()

import pvporcupine
import pyaudio
import struct
import numpy as np
from scipy.signal import resample
import os

ACCESS_KEY = "kZvkhgCgIlxxRieDyhRW+gI4G0tm7UibG6tYqnip1zpAJOIbXmASJA=="
KEYWORD_PATH = "/home/piyawan/Final_Engineering_Project/audio_recognition/raspberry_help_me.ppn"

# Initialize Porcupine
porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_PATH])
print("Porcupine sample rate:", porcupine.sample_rate)  # Should be 16000

p = pyaudio.PyAudio()
device_index = 1  # Adjust to your USB mic index

# Open the microphone at 44100 Hz (or whatever it supports)
input_sample_rate = 44100
stream = p.open(
    rate=input_sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    input_device_index=device_index,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for wake word...")

try:
    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = np.frombuffer(pcm, dtype=np.int16)

        # Resample from 44100 Hz to 16000 Hz
        resampled_pcm = resample(pcm, porcupine.frame_length)

        # Convert back to int16
        resampled_pcm = resampled_pcm.astype(np.int16)

        # Pass resampled audio to Porcupine
        result = porcupine.process(resampled_pcm)

        if result >= 0:
            print("Wake word detected!")

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    porcupine.delete()
