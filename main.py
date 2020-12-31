# Import Custom API
from Modules.Recorder import Recording
# Import Built-in Libraries
from multiprocessing import Process
import os
import subprocess
# Import GUI API
import tkinter as tk
from tkinter import *
from tkinter import messagebox
# Import Merge API
import moviepy.editor as mpe


# Start Recording
def start_recording():
    duration = float(var.get())
    print("Duration: ", type(duration), duration)
    recorder = Recording(1920, 1080, "video.avi", "audio.wav", duration=duration)

    process_video_recording = Process(target=recorder.record_video)
    process_audio_recording = Process(target=recorder.record_audio)
    process_remaining_time = Process(target=recorder.remaining_time)

    process_video_recording.start()
    process_audio_recording.start()
    process_remaining_time.start()

    process_video_recording.join()
    process_audio_recording.join()
    process_remaining_time.join()

    # Merging Files
    merge_files()


# Merging Audio/Video
def merge_files():
    if not os.path.exists("out"):
        os.mkdir("out")

    messagebox.showinfo("Merging", "The audio and video is being merged. Please Wait")

    clip = mpe.VideoFileClip('video.avi')
    audio_bg = mpe.AudioFileClip('audio.wav')

    final_file = clip.set_audio(audio_bg)
    final_file.write_videofile("out/Recording.avi", codec="png")

    location = "Recorded file is saved in: " + str(os.path.abspath("out/Recording.avi"))
    messagebox.showinfo("Success", location)
    subprocess.Popen(f'explorer {os.path.realpath("out")}')

    # Deleting Unwanted files
    os.remove('video.avi')
    os.remove('audio.wav')


# Main
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Screen Recorder")
    root.configure(bg="#1ad1ff")

    # Get Recording Duration
    Label(root, text="Enter Record Duration(In Minutes)", bg="#1ad1ff", fg="#000000", font="bold")\
        .grid(row=0, padx=(20, 20), pady=(30, 30))
    var = StringVar()
    var.set("0.0")
    val = Entry(root, textvariable=var, bd=5, width=25, font=14)
    val.grid(row=0, column=1, padx=(20, 20), pady=(20, 20))

    start_btn = Button(root, text="Start Recording", command=start_recording, activebackground="#0080ff",
                       activeforeground="#000000", font="bold", bd=10)
    start_btn.grid(row=1, column=0, padx=(40, 40), pady=(10, 10), columnspan=2)

    root.mainloop()
