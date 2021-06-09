import os
import platform
import re
import sys
import argparse
from datetime import date

from pyclan import ClanFile
import mysql.connector

from settings import config
from annotid_models import *



# Ugly code, but for now this is how we get the file name and month.
FILE = ''
MONTH = ''

code_regx = re.compile('([a-zA-Z][a-z+]*)( +)(&=)([A-Za-z]{1})(_)([A-Za-z]{1})(_)([A-Z]{1}[A-Z0-9]{2})(_)?(0x[a-z0-9]{6})?', re.IGNORECASE | re.DOTALL)


def insert_annotation():
    return


def process_file(ifile, out_file):
    global FILE, MONTH
    FILE = os.path.basename(ifile).split('_')[0]
    MONTH = os.path.basename(ifile).split('_')[1]
    sys.stdout.write("File: {} \t Month: {} \n".format(FILE, MONTH))
    print("opening")
    sys.stdout.write('Handling {}\n'.format(ifile))
    in_file = ClanFile(ifile)
    in_file.annotate() # To fill the annotations

    print("done opening")
    out = []
    for line in in_file.line_map:
        if line.annotations: # if the annotations attribute is not empty
            for annotation in line.annotations:     # for each annotation
                if not annotation.annotation_id:    # if there is no id for this annot
                        try:
                            ann = Annotation.create(
                                    file_name = FILE,
                                    month = MONTH,
                                    object_name = annotation.word,
                                    object_present = annotation.present,
                                    speaker = annotation.speaker,
                                    utterance_type = annotation.utt_type,
                                    date_added = date.today(),
                                    audio_video = 'audio',
                                    )
                            
                        else:
                            sys.stdout.write("adding {}\n".format(hex(ann.annotid))
                            line.line = line.line.replace(
                                    repr(annotation) + ' ', 
                                    repr(annotation) + '_'+ hex(ann.annotid) +' ', 
                                    1
                                    )

                # if there is an id for this annot, check if it is duplicated in the database??
                else:   
                    query = Annotation.select().where(Annotation.annotid == annotation.annotation_id)
                    num = len(query)

                    # If there is nothing, that means this annotation is not in the database, so insert it!
                    if num == 0:
                            ann = Annotation.create(
                                    annotid = annotation.annotation_id,
                                    file_name = FILE,
                                    month = MONTH,
                                    object_name = annotation.word,
                                    object_present = annotation.present,
                                    speaker = annotation.speaker,
                                    utterance_type = annotation.utt_type,
                                    date_added = date.today(),
                                    audio_video = 'audio',
                                    )

                    elif num > 1:
                        print('FATAL ERROR: This means duplicate annotids :(')
                        print(annotid, num)
                        sys.exit()

    in_file.write_to_cha(out_file)

if __name__ == "__main__":
    database.connect()
    process_file(sys.argv[1], sys.argv[1])
    database.close()


    
