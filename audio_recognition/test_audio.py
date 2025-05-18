import pvporcupine
import pyaudio
import struct
import numpy as np
from scipy.signal import resample
import os

ACCESS_KEY = "kZvkhgCgIlxxRieDyhRW+gI4G0tm7UibG6tYqnip1zpAJOIbXmASJA=="

# Initialize Porcupine with built-in keyword "porcupine"
porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=["porcupine"])

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
