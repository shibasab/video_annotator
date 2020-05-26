import os
import cv2


def resize_video(vid_path, out_dir, out_size=(224, 224)):
    filename = vid_path.split('/')[-1]

    cap = cv2.VideoCapture(vid_path)
    fourcc = cv2.VideoWriter_fourcc("m", "p", "4", "v")
    out_vid = cv2.VideoWriter(
        os.path.join(out_dir, filename),
        fourcc,
        cap.get(
            cv2.CAP_PROP_FPS),
        out_size)

    while True:
        ret, frame = cap.read()

        if ret:
            frame = cv2.resize(frame, out_size)
            out_vid.write(frame)
        else:
            break


if __name__ == "__main__":
    vid_dir = "./video/"
    out_dir = "./resized_video/"
    videos = os.listdir(vid_dir)
    out_size = (224, 224)

    for vid in videos:
        if vid == "speedup":
            continue
        resize_video(os.path.join(vid_dir, vid), out_dir, out_size)
