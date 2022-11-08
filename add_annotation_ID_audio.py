import os
import platform
import re
import uuid
import sys
import argparse
from pyclan import ClanFile
import mysql.connector
from pdb import set_trace

from mysql.connector import errorcode

from settings import config


ANNOTATIONS_TABLE = 'annotids'


# This line needs to be here, otherwise gets garbage collected!
sys.stdout.write('Connecting to the database\n')

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor(buffered=True)

except mysql.connector.Error as e:
    print("Error code:", e.errno)
    print("SQLSTATE value:", e.sqlstate)
    print("Error message:", e.msg)
    print("Error:", e)
    s = str(e)
    print("Error:", s)
    sys.exit()


add_cell = (f"INSERT INTO {ANNOTATIONS_TABLE} "
            "(annotid) "
            "VALUES (%s)")


# Ugly code, but for now this is how we get the file name and month.
FILE = ''
MONTH = ''

code_regx = re.compile('([a-zA-Z][a-z+]*)( +)(&=)([A-Za-z]{1})(_)([A-Za-z]{1})(_)([A-Z]{1}[A-Z0-9]{2})(_)?(0x[a-z0-9]{6})?', re.IGNORECASE | re.DOTALL)

def randomID():
    def generateID():
        randID = uuid.uuid4().hex[:6]
        annotid = search_annotid(randID)
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


def search_annotid(annotid):
    cursor.execute(f'SELECT * FROM {ANNOTATIONS_TABLE} WHERE annotid = "{annotid}"')
    return cursor.fetchall()


def insert_annotation(annotation):
    try:
        rows = search_annotid(annotation.annotation_id)
    except ValueError as e:
        sys.stderr.write(str(e) + '\n')
        sys.stderr.write(str(annotation) + '\n')

    # if the annotid exists in the database, it has to be equal to the cell we are about to add!
    # Otherwise, this might mean we have duplicates :(((
    if rows:
        if len(rows) > 1:
            sys.stderr.write('Duplicates :(((( \n')
            sys.stderr.write('The duplicated cell and the database row are:\n{}\n{}\n'.format(cell, row))

        for row in rows:
            if check_equal(annotation, row):
                break
            else:
                sys.stderr.write('Duplicates :(((( \n')
                sys.stderr.write('The duplicated cell and the database row are:\n{} from the file {}_{} and \n{}\n'.format(cell, FILE, MONTH, row))


    else:
        data_cell = (
                randID
                )
        cursor.execute(add_cell, data_cell)
        cnx.commit()


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
                        id = randomID()
                        try:
                            annot_dict = (id,)
                            cursor.execute(add_cell, annot_dict)
                            cnx.commit()
                        except mysql.connector.Error as e:
                            sys.stderr.write("Error occurred!\n")
                            sys.stderr.write("{}\n".format(annot_dict))
                        
                            
                        else:
                            sys.stdout.write("adding 0x{}\n".format(id))
                            #annotation.annotation_id = '0x' + id
                            line.line = line.line.replace(repr(annotation) + ' ', repr(annotation) + '_0x'+id+' ', 1)

                # if there is an id for this annot, check if it is duplicated in the database??
                else:
                    annotid = search_annotid(annotation.annotation_id)
                    num = len(annotid)
                    if num > 1:
                        print('FATAL ERROR: This means duplicate annotids :(')
                        print(annotid, num)
                        sys.exit()

    in_file.write_to_cha(out_file)


def close_connection():
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    process_file(sys.argv[1], sys.argv[1])
    close_connection()


    
