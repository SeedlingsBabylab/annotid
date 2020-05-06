import os
import platform
import re
import uuid
import sys
import argparse
from pyclan import ClanFile
import sqlite3



code_regx = re.compile('([a-zA-Z][a-z+]*)( +)(&=)([A-Za-z]{1})(_)([A-Za-z]{1})(_)([A-Z]{1}[A-Z0-9]{2})(_)?(0x[a-z0-9]{6})?', re.IGNORECASE | re.DOTALL)

def randomID():
    def generateID():
        randID = uuid.uuid4().hex[:6]
        c.execute('SELECT * FROM annotations WHERE annotid=?', (randID,))
        annotid = c.fetchall()
        num = len(annotid)
        return randID, num, annotid

    randID, num, annotid = generateID()

    while num > 0:
        # FATAL ERROR: This means duplicate annotannotid :(
        if num > 1:
            print('FATAL ERROR: This means duplicate annotids :(')
            print(annotid, num)
            sys.exit()

        # If the annotid exists (and only one exists), we spin, though this could/should be made more efficient...
        else:
            randID, num, annotid = generateID()
    
    return randID

def process_file(ifile, out_file):
    print("opening")
    in_file = ClanFile(ifile)
    in_file.annotate() # To fill the annotations

    print("done opening")
    out = []
    for line in in_file.line_map:
        if line.annotations: # if the annotations attribute is not empty
            for annotation in line.annotations:     # for each annotation
                if not annotation.annotation_id:    # if there is no id for this annot
                        id = randomID()
                        new_line = line.line.replace(repr(annotation), repr(annotation) + '_0x'+id+' ', 1)
                        c.execute('INSERT INTO annotations VALUES (?, ?, ?, ?, ?)', (id, annotation.word, annotation.speaker, annotation.present, annotation.utt_type))
                        conn.commit()
                        print("adding 0x"+id)
                        pass

                # if there is an id for this annot, check if it is duplicated in the database??
                else:   
                    c.execute('SELECT * FROM annotations WHERE annotid=?', (randID,))

                    
    out.append(new_line)
    with open(out_file, 'w') as f:
        for l in out:
            f.write(l)


if __name__ == "__main__":
    input = sys.argv[1]
    if platform.system() != "Windows":
        usedID_file = "./usedID.txt"
    else:
        usedID_file = "Z:\\Seedlings\\usedID.txt"

    # Database connection established here
    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    # If table does not exist, create it, otherwise, continue
    c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="annotations"')
    if c.fetchone():
        print("Database table was created")
    else:
        c.execute('''CREATE TABLE annotations 
            (annotid text primary key, object text, speaker text, object_present text, utterance_type text)''')

    if not input.endswith(".cha"):
        input_dir = input
        output_dir = sys.argv[2]
        usedID_file = sys.argv[3]

        files = os.listdir(input_dir)
        files.sort()
        errorFiles = []
        counter = 0
        usedID = set()
        #Load used IDs to prevent collision
        with open(usedID_file) as f:
            for line in f.readlines():
                usedID.add(line.rstrip())

        if '--fix-error' in sys.argv: #Only process files with error
            files = []
            with open('add-annotation_ID-error-file.txt') as f:
                for line in f.readlines():
                    files.append(line.rstrip().strip('\''))

        for file in files:
            if file.endswith('sparse_code.cha'):
                try:
                    in_file = os.path.join(input_dir, file)
                    out_file = os.path.join(output_dir, file)
                    process_file(in_file, out_file)
                except Exception as e:
                    print(e)
                    errorFiles.append(file)
            counter += 1
            print("Finished: {}".format(counter/float(len(files))*100))

        with open(usedID_file, 'w') as f: # not 'a' because not adding (or will introduce duplicates, and size of file+++)
            for id in usedID:
                f.write(id + '\n')

        print('Had problems processing the following files:')
        print(errorFiles)

    else:
        in_file = input
        if (len(sys.argv)>2):
            out_file = sys.argv[2]
        else:
            out_file = in_file
        print(out_file)
        process_file(in_file, out_file)

        # update used id
        with open(usedID_file, 'w') as f:
            for id in usedID:
                f.write(id + '\n')
    
    conn.commit()
    conn.close()
