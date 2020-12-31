# Imports
import pyautogui
import numpy as np
import cv2
import pyaudio
import wave
import time
import tkinter as tk
from tkinter import *


# Recording Class
class Recording:
    def __init__(self, resolution_width, resolution_height, filename_video, filename_audio, duration):
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height
        self.filename_video = filename_video
        self.filename_audio = filename_audio
        self.duration = duration
        self.window = ""

    # Remaining Time Counter
    def remaining_time(self):
        self.window = tk.Tk()

        Label(self.window, text="Time Remaining", justify="center", font=("Arial", 15, "bold"))\
            .grid(row=0, padx=(25, 25), pady=(35, 35), column=1)

        hour = StringVar()
        minute = StringVar()
        seconds = StringVar()

        hour.set("00")
        minute.set("00")
        seconds.set("00")

        hourEntry = Entry(self.window, width=8, font=20, textvariable=hour)
        hourEntry.grid(row=1, column=0)
        minuteEntry = Entry(self.window, width=8, font=20, textvariable=minute)
        minuteEntry.grid(row=1, column=1)
        secondEntry = Entry(self.window, width=8, font=20, textvariable=seconds)
        secondEntry.grid(row=1, column=2)

        timer = time.time()
        endTime = timer + self.duration * 60
        endTimeStrings = time.strftime('%H:%M:%S', time.localtime(endTime)).split(":")
        print(endTimeStrings)

        while timer <= endTime:

            currentTime = time.strftime('%H:%M:%S', time.localtime(timer))

            timeStrings = currentTime.split(":")
            print(timeStrings)

            hour.set(str(abs(int(endTimeStrings[0]) - int(timeStrings[0]))))
            minute.set(str(abs(int(endTimeStrings[1]) - int(timeStrings[1]))))
            seconds.set(str(abs(int(endTimeStrings[2]) - int(timeStrings[2]))))

            self.window.update()

            time.sleep(1)

            timer = time.time()

            if timer > endTime:
                self.window.destroy()

        self.window.mainloop()

    # Record Video
    def record_video(self):
        # Video Resolution
        resolution = (self.resolution_width, self.resolution_height)

        # Specifying Video Codec
        codec = cv2.VideoWriter_fourcc(*"XVID")

        fps = 15.0

        # Creating Video Writer Object
        out = cv2.VideoWriter(self.filename_video, codec, fps, resolution)

        # Creating an Empty Window
        # cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

        # Resizing the Window
        # cv2.resizeWindow("Live", 480, 270)

        # Set End Time
        time_end = time.time() + self.duration * 60  # Converts given duration in minutes to seconds.

        print("Video Recording Started...")

        while time.time() < time_end:
            img = pyautogui.screenshot()

            # Converting image to numpy array
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            # cv2.imshow('Live', frame)

        # Release the Video Writer
        out.release()

        print("Video Recording Done.")

        # Destroy all windows
        cv2.destroyAllWindows()

    # Record Audio
    def record_audio(self):
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

        print("Audio Recording Started...")

        # Set End Time
        time_end = time.time() + self.duration * 60  # Converts given duration in minutes to seconds.

        while time.time() < time_end:
            # Audio Recording
            data = stream.read(chunk)
            frames.append(data)

        # Terminating Recording
        print("Audio Recording Done!")

        stream.stop_stream()
        stream.close()

        # Terminating PyAudio Object
        p.terminate()

        # Saving Audio file
        wf = wave.open(self.filename_audio, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))

        wf.close()
