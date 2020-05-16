from load_image import VideoFrame

import tkinter as tk


class App(tk.Frame):
    def __init__(self, video_frame, master=None):
        super().__init__(master)
        self.master = master
        self.video_frame = video_frame
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
            command=lambda: self.change_img(30))
        self.btn.pack(anchor=tk.NW, side="top")

    def show_img(self):
        self.img = self.video_frame.get_tkframe()
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)

    def change_img(self, n=10):
        self.video_frame.idx += n

        if self.video_frame.idx > len(self.video_frame.imgs):
            self.video_frame.idx = 0

        self.show_img()


root = tk.Tk()
root.geometry('640x320')
root.resizable(width=10, height=10)

video_frame = VideoFrame("./video/0.mp4")
app = App(video_frame, master=root)

app.mainloop()
