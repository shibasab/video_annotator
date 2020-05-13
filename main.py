from PIL import Image, ImageTk

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk


class VideoFrame:
    def __init__(self, vid_path):
        self.idx = 0
        self.imgs = self.load(vid_path)
        self.shape = self.imgs[0].shape

    def get_tkframe(self):
        img = self.imgs[self.idx]
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img_pil)
        return img_tk

    def count(self):
        self.idx += 1

    def load(self, vid_path):
        imgs = []

        cap = cv2.VideoCapture(vid_path)
        if not cap.isOpened():
            print("Could not open video.")
            return

        while True:
            ret, frame = cap.read()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                imgs.append(frame)

            else:
                break

        return imgs


root = tk.Tk()
root.title("test")
root.geometry('640x320')
root.resizable(width=10, height=10)

video_frame = VideoFrame("./video/0.mp4")

frame1 = ttk.Frame(root, padding=5)
# frame1.grid()

button1 = ttk.Button(
    frame1,
    text="next",
    command=video_frame.count()
)
# button1.grid(row=2, column=1, columnspan=2)

canvas = tk.Canvas(
    root, width=video_frame.shape[0], height=video_frame.shape[1])
canvas.pack()
img = video_frame.get_tkframe()
canvas.create_image(0, 0, anchor="nw", image=img)

root.mainloop()
