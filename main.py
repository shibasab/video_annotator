from load_image import VideoLoader
from label import save_label

import tkinter as tk


class ImageFrame(tk.Frame):
    def __init__(self, video_loader, master=None):
        super().__init__(master)
        self.master = master
        self.video_loader = video_loader

        self.canvas = tk.Canvas(
            self.master,
            width=self.video_loader.shape[0] * 2 + 20,
            height=self.video_loader.shape[1])
        self.canvas.grid(row=0, column=0)
        self.show_img()
        self.btn = tk.Button(
            self,
            text="next",
            command=lambda: self.change_img())

        self.btn.grid(row=0, column=1)

    def show_img(self):
        # self.imgの形にしないと画像がメモリに残らない
        self.img = self.video_loader.get_tkframe()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def change_img(self, n=1):
        self.video_loader.count(n)
        self.show_img()


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.buttons = []
        self.classes = {
            "Address": 0,
            "Take-back": 0,
            "Top": 0,
            "Tatamu": 0,
            "Impact": 0,
            "Follow-through": 0,
            "Finish": 0}
        self.video_loader = VideoLoader("./video/0.mp4")

        self.video_frame = ImageFrame(self.video_loader, self)
        self.video_frame.grid()
        self.create_widgets()

    def create_widgets(self):
        self.make_classbtn()

        self.save_btn = tk.Button(
            self, text="save", command=lambda: save_label(
                self.video_loader.vid_path, self.classes))
        self.save_btn.grid(row=3, column=0, sticky=tk.W)

    def make_classbtn(self):
        for i, k in enumerate(self.classes):
            classbtn = tk.Button(
                self, text=k, command=lambda K=k: self.set_eventnum(
                    K, self.video_loader.idx))
            classbtn.grid(row=2, column=i, padx=5)
            self.buttons.append(classbtn)

    def set_eventnum(self, k, idx):
        self.classes[k] = idx
        print(self.classes)


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=10, height=10)
    root.geometry("640x320")
    app = App(master=root)
    app.pack()

    app.mainloop()
