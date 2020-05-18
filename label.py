import os


def save_label(file_path, label):
    file_name = os.path.splitext(file_path.split('/')[-1])[0]
    with open(os.path.join("./labels", file_name + ".txt"), mode="w") as f:
        f.write(file_path + "\n")
        for v in label.values():
            f.write(str(v) + " ")
        f.write("\n")

    print("saved")
