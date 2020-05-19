import cv2
from PIL import Image, ImageTk


class VideoLoader:
    def __init__(self, vid_path):
        self.idx = 0
        self.vid_path = vid_path
        self.imgs = self.load(vid_path)
        self.shape = self.imgs[0].shape

    def get_tkframe(self):
        img = self.imgs[self.idx]
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(img_pil)
        return img_tk

    def count(self, n):
        self.idx += n
        if self.idx >= len(self.imgs):
            self.idx = len(self.imgs) - 1

    def back(self, n):
        self.idx -= n
        if self.idx < 0:
            self.idx = 0

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
