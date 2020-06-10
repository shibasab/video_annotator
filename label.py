import os

import numpy as np


def save_label(filepath, label, num_frames):
    filename, ext = os.path.splitext(filepath.split('/')[-1])
    with open(os.path.join("./labels", filename + ".txt"), mode="w") as f:
        f.write(filename + ext + "\n")
        for v in label.values():
            f.write(str(v) + " ")
        f.write("\n")

        events = [label[x] for x in label]
        events = [0] + events + [num_frames - 1]
        print(events)
        labels = np.zeros(num_frames)

        for i, e in enumerate(events):
            if i == len(events) - 1:
                if events[i] == events[i - 1]:
                    break
                labels[e] = i

            else:
                if i == 0 and events[i] == events[i + 1]:
                    labels[i] = 1
                    continue

                sub = 1 / max(events[i + 1] - events[i], 1)
                for j in range(events[i], events[i + 1]):
                    labels[j + 1] = labels[j] + sub

        labels = labels.astype(str)
        f.write(" ".join(labels) + " \n")

    print("saved")
