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
        height, width = self.video_loader.shape[0], self.video_loader.shape[1]
        self.coords = [
            width // 4,
            height // 4,
            width // 2 + width // 4,
            height // 2 + height // 4]

        self.canvas = tk.Canvas(
            self.master,
            width=width,
            height=height)
        self.canvas.pack()
        self.show_img()

        self.next30 = tk.Button(
            self,
            text="next30",
            command=lambda: self.change_img(30, "next"))
        self.next30.pack(padx=5, pady=5, side=tk.LEFT)

        self.back5 = tk.Button(
            self,
            text="back5",
            command=lambda: self.change_img(5, "back")
        )
        self.back5.pack(padx=5, pady=5, side=tk.LEFT)

        self.leftp = tk.Button(
            self,
            text="left+",
            command=lambda: self.change_rectangle("left+")
        )
        self.leftp.pack(padx=5, pady=5, side=tk.LEFT)

        self.leftm = tk.Button(
            self,
            text="left-",
            command=lambda: self.change_rectangle("left-")
        )
        self.leftm.pack(padx=5, pady=5, side=tk.LEFT)

        self.rightp = tk.Button(
            self,
            text="right+",
            command=lambda: self.change_rectangle("right+")
        )
        self.rightp.pack(padx=5, pady=5, side=tk.LEFT)

        self.rightm = tk.Button(
            self,
            text="right-",
            command=lambda: self.change_rectangle("right-")
        )
        self.rightm.pack(padx=5, pady=5, side=tk.LEFT)

        self.upp = tk.Button(
            self,
            text="up+",
            command=lambda: self.change_rectangle("up+")
        )
        self.upp.pack(padx=5, pady=5, side=tk.LEFT)

        self.upm = tk.Button(
            self,
            text="up-",
            command=lambda: self.change_rectangle("up-")
        )
        self.upm.pack(padx=5, pady=5, side=tk.LEFT)

        self.bottomp = tk.Button(
            self,
            text="bottom+",
            command=lambda: self.change_rectangle("bottom+")
        )
        self.bottomp.pack(padx=5, pady=5, side=tk.LEFT)

        self.bottomm = tk.Button(
            self,
            text="bottom-",
            command=lambda: self.change_rectangle("bottom-")
        )
        self.bottomm.pack(padx=5, pady=5, side=tk.LEFT)

    def show_img(self):
        # self.imgの形にしないと画像がメモリに残らない
        self.img = self.video_loader.get_tkframe()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        self.show_rectangle()

    def change_img(self, n=1, direction="next"):
        if direction == "next":
            self.video_loader.count(n)
        else:
            self.video_loader.back(n)
        self.show_img()

    def show_rectangle(self):
        x0, y0, x1, y1 = self.coords
        self.rec = self.canvas.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            outline="blue")

    def change_rectangle(self, direction):
        if direction == "left+":
            self.coords[0] += 1
        elif direction == "left-":
            self.coords[0] -= 1
        if direction == "right+":
            self.coords[2] += 1
        elif direction == "right-":
            self.coords[2] -= 1
        if direction == "up+":
            self.coords[1] += 1
        elif direction == "up-":
            self.coords[1] -= 1
        if direction == "bottom+":
            self.coords[3] += 1
        elif direction == "bottom-":
            self.coords[3] -= 1

        x0, y0, x1, y1 = self.coords
        self.canvas.coords(self.rec, x0, y0, x1, y1)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.k = 1
        self.initialdir = "./video"

        self.filebtn = tk.Button(
            self, text="ファイルを開く", command=self.load_video
        )
        self.filebtn.pack()

    def create_widgets(self):
        self.split_btn = tk.Button(
            self,
            text="crop",
            command=lambda: self.save_video())
        self.split_btn.pack(padx=15, pady=10, side=tk.TOP)

    def load_video(self):
        self.k = 1
        self.splitplace = []
        filetypes = [("mp4", "*.mp4")]
        filepath = filedialog.askopenfilename(
            filetypes=filetypes, initialdir=self.initialdir)

        self.vid_dir = filepath.split("/")[-2]

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

    def save_video(self):

        fps = self.video_loader.fps
        filepath = self.video_loader.vid_path
        print(filepath)
        places = self.splitplace

        filename = os.path.splitext(filepath.split('/')[-1])[0]
        height, width, _ = self.video_loader.imgs[0].shape
        fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
        # ファイル名の添え字(今後もっと良い設定方法を考える)

        for p in places:
            writer = cv2.VideoWriter(
                os.path.join(
                    self.vid_dir,
                    filename + "-{}.mp4".format(self.k)),
                fourcc,
                fps,
                (width, height))
            for i in range(p[0], p[1] + 1):
                frame = cv2.cvtColor(
                    self.video_loader.imgs[i], cv2.COLOR_RGB2BGR)
                writer.write(frame)

            writer.release()
            self.k += 1

        self.splitplace = []


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(600, 400)
    app = App(master=root)
    app.pack(expand=1)

    root.mainloop()
