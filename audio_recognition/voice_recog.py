import pvporcupine
import pyaudio
import struct

porcupine = pvporcupine.create(
    keyword_paths=[pvporcupine.HELP]  # Replace with another pre-built word if needed
)

pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

print("Listening for the wake word...")

try:
    while True:
        pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)

        if result >= 0:
            print("Wake word detected!")
            # Trigger your robot's action here
finally:
    audio_stream.close()
    pa.terminate()
    porcupine.delete()