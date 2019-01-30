import sys
import mmap
import os
import re
import pandas


def get_codes(filepath):
   fn = filepath
   size = os.stat(fn).st_size
   # data = open(fn, "r").read()
   f= open(fn)
   data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)

   # m.extend(re.findall(r"_0x[0-9a-f]{6}", data))

   return re.findall(r"_0x[0-9a-f]{6}", data)

if __name__ == "__main__":

    # file with all cha files
    cha_files = sys.argv[1]
    audio_codes = []

    with open(cha_files, 'r') as f:
        cha_list = f.readlines()
        f.close()

    for l in cha_list:
        print(l)
        audio_codes.extend(get_codes(l.strip()))

    with open("usedID_audio.txt", 'w') as fo:
       for l in audio_codes:
           fo.write(l[1:]+"\n")

    # file with all video_sparse_code files
    video_files = sys.argv[2]
    video_codes = []

    with open(video_files, 'r') as g:
        csv_list = g.readlines()
        g.close()

    for l in csv_list:
        print(l)
        l = l.strip()
        df = pandas.read_csv(l)
        video_codes.extend(list(df["labeled_object.id"]))

    with open("usedID_video.txt", 'w') as fo:
       for l in video_codes:
           fo.write(l[1:]+"\n")

   #
   #  filepath = sys.argv[1]
   #  m = []
   #
   #  m = get_codes(filepath, m)
   #
   # with open("out.txt", 'w') as fo:
   #     for l in m:
   #         fo.write(l[1:]+"\n")
