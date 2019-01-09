import sys
import mmap
import os
import re


def get_codes(filepath, m):
   fn = filepath
   size = os.stat(fn).st_size
   # data = open(fn, "r").read()
   f= open(fn)
   data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)

   m.extend(re.findall(r"_0x[0-9a-f]{6}", data))

   return m

if __name__ == "__main__":

    filepath = sys.argv[1]
    m = []

    m = get_codes(filepath, m)

   with open("out.txt", 'w') as fo:
       for l in m:
           fo.write(l[1:]+"\n")
