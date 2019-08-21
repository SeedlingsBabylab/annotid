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

    if 'batch' in sys.argv:
        # file with all cha files
        cha_files = sys.argv[1]
        # audio_codes = []
        #
        # with open(cha_files, 'r') as f:
        #     cha_list = f.readlines()
        #     f.close()
        #
        # for l in cha_list:
        #     print(l)
        #     l = l.strip()
        #     audio_codes.append([l,get_codes(l.strip())])
        #
        # with open("usedID_audio.csv_TO_RENAME", 'w') as fo:
        #    for l in audio_codes:
        #        for c in l[1]:
        #            fo.write(l[0]+","+c[1:]+"\n")

        # file with all video_sparse_code files
        video_files = sys.argv[2]
        video_codes = []

        # with open(video_files, 'r') as g:
        #     csv_list = g.readlines()
        #     g.close()

        # for l in csv_list:
        for l in os.listdir(video_files):
            print(l)
            # l = l.strip()
            l = os.path.join(video_files, l)
            df = pandas.read_csv(l, error_bad_lines=False) # error bad lines: comments with a comma
            video_codes.append([l,list(df["labeled_object.id"])])

        with open("usedID_video.csv_TO_RENAME", 'w') as fo:
           for l in video_codes:
               for c in l[1]:
                   # print(c)
                   fo.write(l[0]+","+str(c)+"\n")

    elif sys.argv[1].endswith(".cha"):
        cha_file = sys.argv[1]
        codes = get_codes(cha_file)
        with open(cha_file+".idlist", 'w') as fo:
            for l in codes :
                fo.write(cha_file+","+l[1:]+"\n")

    elif sys.argv[1].endswith(".csv"):
        video_file = sys.argv[1]
        df = pandas.read_csv(video_file)
        with open(video_file+".idlist", 'w') as fo:
            for l in list(df["labeled_object.id"]):
                fo.write(video_file+","+l[1:]+"\n")

    else:
        print("Wrong usage")

   #
   #  filepath = sys.argv[1]
   #  m = []
   #
   #  m = get_codes(filepath, m)
   #
   # with open("out.txt", 'w') as fo:
   #     for l in m:
   #         fo.write(l[1:]+"\n")
