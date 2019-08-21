import sys
import os
from shutil import move


if __name__ == "__main__":

    home_visit_paths = sys.argv[1]
    mode = sys.argv[2] # = audio or video

    with open(home_visit_paths, 'r') as f:
        lines = f.readlines()



    for line in lines:
        line = line.strip()
        if mode == 'audio':
            old_path = line+"/Analysis/Audio_Analysis/"
        elif mode == 'video':
            old_path = line+"/Analysis/Video_Analysis/"
        else:
            print("Wrong mode: audio or video\n")
            exit()
        for csv_file in os.listdir(old_path):
            if csv_file.endswith("no_id.csv"):
                move(os.path.join(old_path, csv_file), \
                     os.path.join(old_path+"/old_files/", csv_file))
