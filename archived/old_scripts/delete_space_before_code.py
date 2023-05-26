import sys
import mmap
import os


def correct_codes(filepath):
    fn = filepath
    size = os.stat(fn).st_size
    # data = open(fn, "r").read()
    f= open(fn)
    # data = mmap.mmap(f.fileno(), size, access=mmap.ACCESS_READ)

    return f.read().replace(" 0x", "0x")


if __name__ == "__main__":

    list_cha_sparse_path = sys.argv[1]
    list_cha_sparse = open(list_cha_sparse_path).readlines()
    list_cha_sparse = [l.strip() for l in list_cha_sparse]

    for cha_sparse in list_cha_sparse:
        output = correct_codes(cha_sparse)
        open(cha_sparse, 'w').write(output)
