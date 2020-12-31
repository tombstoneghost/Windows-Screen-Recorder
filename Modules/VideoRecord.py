"""
# Imports
import pyautogui
import numpy as np
import cv2


# Function to start video recording
def record_video(resolution_width, resolution_height, filename):
    # Video Resolution
    resolution = (resolution_width, resolution_height)

    # Specifying Video Codec
    codec = cv2.VideoWriter_fourcc(*"XVID")

    fps = 60.0

    # Creating Video Writer Object
    out = cv2.VideoWriter(filename, codec, fps, resolution)

    # Creating an Empty Window
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)

    # Resizing the Window
    cv2.resizeWindow("Live", 480, 270)

    while True:
        img = pyautogui.screenshot()

        # Converting image to numpy array
        frame = np.array(img)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        out.write(frame)

        cv2.imshow('Live', frame)

        # Stop Recording Video
        if cv2.waitKey(1) == ord('q'):
            break

    # Release the Video Writer
    out.release()

    # Destroy all windows
    cv2.destroyAllWindows()
"""