from load_image import VideoLoader
from label import save_label

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

    def show_img(self):
        # self.imgの形にしないと画像がメモリに残らない
        self.img = self.video_loader.get_tkframe()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def change_img(self, n=1, direction="next"):
        if direction == "next":
            self.video_loader.count(n)
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
        self.make_classbtn()

        self.save_btn = tk.Button(
            self, text="save", command=lambda: save_label(
                self.video_loader.vid_path, self.classes))
        self.save_btn.pack(padx=15, pady=10, side=tk.TOP)

    def make_classbtn(self):
        self.buttons = []
        self.classes = {
            "Address": 0,
            "Take-back": 0,
            "Top": 0,
            "Tatamu": 0,
            "Impact": 0,
            "Follow-through": 0,
            "Finish": 0}

        for i, k in enumerate(self.classes):
            classbtn = tk.Button(
                self, text=k, command=lambda K=k: self.set_eventnum(
                    K, self.video_loader.idx))
            classbtn.pack(padx=5, pady=10, side=tk.LEFT, expand=1)
            self.buttons.append(classbtn)

    def set_eventnum(self, k, idx):
        self.classes[k] = idx
        print(self.classes)

    def load_video(self):
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


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(600, 400)
    app = App(master=root)
    app.pack(expand=1)

    root.mainloop()
