import sys
import os
import re

if __name__ == "__main__":


    cha_folder = sys.argv[1]

    error = []
    pattern = '.*&=[^\s]*0x[0-9a-z]{6}.*'
    print bool(re.match(pattern, '&= 0x5fdc48 .'))
    for dirpath, dirnames, filenames in os.walk(cha_folder):
        for fname in filenames:
            if fname.endswith('.cha'):
                with open(opf_paths, 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    if '&=' in line:
                        if not re.match(pattern, line):
                            error.append([fname, line]) # timestamp and word
