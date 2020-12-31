"""
# Imports
import pyaudio
import wave
import cv2


# Record Audio
def record_audio(filename):
    # Set Chunk size
    chunk = 1024

    # Sample Format
    FORMAT = pyaudio.paInt16

    # Channels = 2 for Stereo
    channels = 2

    # Sample Rates
    sample_rate = 44100

    # PyAudio Object
    p = pyaudio.PyAudio()

    # Opening Stream
    stream = p.open(format=FORMAT, channels=channels, rate=sample_rate, input=True, output=True,
                    frames_per_buffer=chunk)
    frames = []

    print("Recording Started...")

    while True:
        data = stream.read(chunk)

        frames.append(data)

        # Stop Recording Video
        if cv2.waitKey(1) == ord('q'):
            break

    print("Recording Done!")

    stream.stop_stream()
    stream.close()

    # Terminating PyAudio Object
    p.terminate()

    # Saving Audio file
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))

    wf.close()
"""