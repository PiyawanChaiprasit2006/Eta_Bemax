import pvporcupine
import pyaudio
import struct
import os

# Set your Picovoice Access Key here
ACCESS_KEY = "QtGnKUx41QZ8hcXd9C5a3cmx2zaPxdzqKWMKzpDlYnw4sztbnUWMRQ=="  # Replace with your actual access key

# Set the path to your custom wake word model
CUSTOM_WAKE_WORD_PATH = "/home/piyawan/Final_Engineering_Project/audio_recognition/help_me_en_windows.ppn"

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

pa = pyaudio.PyAudio()

# Automatically select the default microphone on the laptop
device_index = None
for i in range(pa.get_device_count()):
    info = pa.get_device_info_by_index(i)
    if info.get("maxInputChannels", 0) > 0 and "microphone" in info["name"].lower():
        device_index = i
        break

if device_index is None:
    print("No microphone detected. Please ensure your laptop microphone is enabled.")
    exit()

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

except KeyboardInterrupt:
    print("\nStopped by user.")

finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()
