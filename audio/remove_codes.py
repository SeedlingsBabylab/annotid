import sys
import mmap
import os
import re

if __name__ == "__main__":

   fn = sys.argv[1]
   size = os.stat(fn).st_size
   # data = open(fn, "r").read()
   f= open(fn)
   data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)

   m = re.sub(r"_0x[0-9a-f]{6}", '', data)

   with open(fn, 'w') as f:
       f.write(m)
