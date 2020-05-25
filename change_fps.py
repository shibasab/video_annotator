import os

import numpy as np
import cv2


def change_fps(vid_path):
    filename = vid_path.split("/")[-1]
    cap = cv2.VideoCapture(vid_path)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    out = cv2.VideoWriter(
        os.path.join("./video/speedup",
                     filename),
        fourcc,
        cap.get(cv2.CAP_PROP_FPS),
        (int(width),
         int(height)))

    ret, pre_frame = cap.read()

    while True:
        ret, frame = cap.read()
        if ret:
            im_diff = np.abs(frame.astype(int) - pre_frame.astype(int))
            print(im_diff.max())
            if im_diff.max() > 50:
                out.write(frame)
                pre_frame = frame

        else:
            break

    out.release()


if __name__ == "__main__":
    vid_path = "./video/"
    files = os.listdir(vid_path)
    for file in files:
        if file in ["8.mp4", "speedup"]:
            continue
        print(file)
        change_fps(os.path.join(vid_path, file))

    print("done")
