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
access_key = "gaoJG0yVsQvUN1+vpsZGVNb7Fid1gpCgBuEPUb385ZD2Sx9CFi32+g=="  # Replace with your actual access key

# Set the path to your custom wake word model
custom_wake_word_path = os.path.join("Final_Engineering_Project/audio_recognition", "helpme_window.ppn")  # Replace with your actual path

porcupine = pvporcupine.create(
    access_key=access_key,                # Added the required access key
    keyword_paths=[custom_wake_word_path],  # Use your custom wake word model path
    sensitivities=[0.5]  # Adjust sensitivity (0.0 to 1.0) as needed
)

pa = pyaudio.PyAudio()

# Use your laptop's default microphone (device_index=0). Adjust if necessary.
device_index = None  # Default microphone (None)
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if "microphone" in info["name"].lower():
        device_index = i
        break

if device_index is None:
    print("No microphone detected. Please ensure your laptop microphone is enabled.")
    exit()

audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    input_device_index=device_index,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for the wake word...")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)

        if result >= 0:
            print("Wake word detected! Recognized text: 'help me'")
            # our robot's action here
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
