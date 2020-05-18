from load_image import VideoFrame
from label import save_label

import tkinter as tk


class App(tk.Frame):
    def __init__(self, video_frame, master=None):
        super().__init__(master)
        self.master = master
        self.video_frame = video_frame
        self.buttons = []
        self.classes = {
            "Address": 0,
            "Take-back": 0,
            "Top": 0,
            "Tatamu": 0,
            "Impact": 0,
            "Follow-through": 0,
            "Finish": 0}
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(
            self.master,
            width=self.video_frame.shape[0],
            height=self.video_frame.shape[1])

        self.canvas.pack()
        self.show_img()

        self.btn = tk.Button(
            self,
            text="next",
            command=lambda: self.change_img())
        self.btn.pack(anchor=tk.NW, side="top")

        self.make_classbtn()

        self.save_btn = tk.Button(
            self, text="save", command=lambda: save_label(
                self.video_frame.vid_path, self.classes))
        self.save_btn.pack(anchor=tk.NW)

    def show_img(self):
        self.img = self.video_frame.get_tkframe()
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def change_img(self, n=1):
        self.video_frame.count(n)

        if self.video_frame.idx > len(self.video_frame.imgs):
            self.video_frame.idx = 0

        self.show_img()

    def make_classbtn(self):
        for k in self.classes:
            classbtn = tk.Button(
                self,
                text=k,
                command=lambda K=k: self.set_eventnum(K, self.video_frame.idx))
            classbtn.pack()
            self.buttons.append(classbtn)

    def set_eventnum(self, k, idx):
        self.classes[k] = idx
        print(self.classes)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('640x320')
    root.resizable(width=10, height=10)

    video_frame = VideoFrame("./video/0.mp4")
    app = App(video_frame, master=root)

    app.mainloop()
