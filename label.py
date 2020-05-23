import os


def save_label(filepath, label):
    filename, ext = os.path.splitext(filepath.split('/')[-1])
    with open(os.path.join("./labels", filename + ".txt"), mode="w") as f:
        f.write(filename + ext + "\n")
        for v in label.values():
            f.write(str(v) + " ")
        f.write("\n")

    print("saved")
