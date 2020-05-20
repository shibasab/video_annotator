from load_image import VideoLoader
import os

import cv2
import tkinter as tk
from tkinter import filedialog


class ImageFrame(tk.Frame):
    def __init__(self, video_loader, master=None):
        super().__init__(master)
        self.master = master
        self.video_loader = video_loader

        self.canvas = tk.Canvas(
            self.master,
            width=self.video_loader.shape[1],
            height=self.video_loader.shape[0])
        self.canvas.pack()
        self.show_img()
        self.next1 = tk.Button(
            self,
            text="next1",
            command=lambda: self.change_img(1, "next"))
        self.next1.pack(padx=5, pady=5, side=tk.LEFT)

        self.next5 = tk.Button(
            self,
            text="next5",
            command=lambda: self.change_img(5, "next"))
        self.next5.pack(padx=5, pady=5, side=tk.LEFT)

        self.back1 = tk.Button(
            self,
            text="back1",
            command=lambda: self.change_img(1, "back")
        )
        self.back1.pack(padx=5, pady=5, side=tk.LEFT)

        self.back5 = tk.Button(
            self,
            text="back5",
            command=lambda: self.change_img(5, "back")
        )
        self.back5.pack(padx=5, pady=5, side=tk.LEFT)

        self.innum = tk.Entry(self, width=5)
        self.innum.pack(padx=5, pady=5, side=tk.LEFT)

        self.spec = tk.Button(
            self,
            text="spec",
            command=lambda: self.change_img(self.innum.get(), "spec")
        )
        self.spec.pack(padx=5, pady=5, side=tk.LEFT)

    def show_img(self):
        # self.imgの形にしないと画像がメモリに残らない
        self.img = self.video_loader.get_tkframe()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def change_img(self, n=1, direction="next"):
        if direction == "next":
            self.video_loader.count(n)
        elif direction == "spec":
            self.video_loader.change(n)
        else:
            self.video_loader.back(n)
        self.show_img()


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.initialdir = "./video"

        self.filebtn = tk.Button(
            self, text="ファイルを開く", command=self.load_video
        )
        self.filebtn.pack()

    def create_widgets(self):
        self.startbtn = tk.Button(
            self, text="start", command=lambda: self.set_splitplace("start"))
        self.startbtn.pack(padx=5, side=tk.LEFT)

        self.endbtn = tk.Button(
            self, text="end", command=lambda: self.set_splitplace("end"))
        self.endbtn.pack(padx=5, side=tk.LEFT)

        self.split_btn = tk.Button(
            self,
            text="split",
            command=lambda: self.save_video())
        self.split_btn.pack(padx=15, pady=10, side=tk.TOP)

    def load_video(self):
        self.splitplace = []
        filetypes = [("mp4", "*.mp4")]
        filepath = filedialog.askopenfilename(
            filetypes=filetypes, initialdir=self.initialdir)

        if filepath == "":
            return

        if self.pack_slaves() != []:
            for i, p in enumerate(self.pack_slaves()):
                if i == 0:
                    continue
                p.destroy()

        self.video_loader = VideoLoader(filepath)

        self.video_frame = ImageFrame(self.video_loader, self)
        self.video_frame.pack()
        self.create_widgets()

    def set_splitplace(self, t):
        idx = self.video_loader.idx
        if t == "start":
            self.splitplace.append([idx, idx])
        else:
            self.splitplace[-1][1] = idx
        print(self.splitplace)

    def save_video(self):
        save_dir = "./video"
        fps = self.video_loader.fps,
        filepath = self.video_loader.vid_path,
        places = self.splitplace

        filename = os.path.splitext(filepath.split('/')[-1])[0]
        height, width, _ = self.video_loader.imgs[0].shape
        fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")

        # ファイル名の添え字(今後もっと良い設定方法を考える)
        i = 11

        for p in places:
            writer = cv2.VideoWriter(
                os.path.join(
                    save_dir,
                    filename + "-{}.mp4".format(i)),
                fourcc,
                fps,
                (width,
                 height))
            for i in range(p[0], p[1] + 1):
                frame = cv2.cvtColor(
                    self.video_loader.imgs[i], cv2.COLOR_RGB2BGR)
                writer.write(frame)

            writer.release()
            i += 1

        self.splitplace = []


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(600, 400)
    app = App(master=root)
    app.pack(expand=1)

    root.mainloop()
