import sys
import csv
import subprocess
from sets import Set


add_id_script = "/Volumes/pn-opus/Seedlings/Scripts_and_Apps/Github/seedlings/annotid/audio/add-annotation_ID-audio.py"

if __name__ == "__main__":

    error = sys.argv[1]
    cha_f = Set([])

    with open(error, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            if line[-1] == 'missing ID': #error type
                cha_f.add(line[0])   #file path

    for cha in cha_f:
        subprocess.call(["python", add_id_script, cha])
