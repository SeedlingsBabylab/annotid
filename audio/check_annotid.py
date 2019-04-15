import sys
import os
import re
import csv
from sets import Set

usedID_file = "/Volumes/pn-opus/Seedlings/usedID.txt"

if __name__ == "__main__":

    usedID = Set([])
    with open(usedID_file) as f:
        for line in f.readlines():
            usedID.add(line.rstrip())

    cha_folder = sys.argv[1]

    error = []
    pattern = '[0-9a-zA-Z+]+\s&=[^\s]*0x[0-9a-z]{6}'
    pattern_word = '[0-9a-zA-Z+]+\s&=[^\s]+'
    for dirpath, dirnames, filenames in os.walk(cha_folder):
        for fname in filenames:
            if fname.endswith('.cha'):
                with open(os.path.join(cha_folder, fname), 'r') as f:
                    lines = f.readlines()
                for line in lines:
                    match = re.findall(pattern_word, line)
                    if len(match):
                        for m in match:
                            if not re.match(pattern, m):
                                error.append([os.path.join(cha_folder, fname), m, line.split(' ')[-1].strip(), 'missing ID'])
                            elif m[len(m)-8:] not in usedID:
                                error.append([os.path.join(cha_folder, fname), m, line.split(' ')[-1].strip(), 'ID not in usedID'])

    with open(os.path.join(cha_folder, "error_summary.csv"), 'w') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(["file name", "line", "timestamp", 'error type'])
        for e in error:
            writer.writerow(e)
