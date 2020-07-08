import os
import platform
import re
import uuid
import sys
import argparse
from pyclan import ClanFile
import mysql.connector
from pdb import set_trace

from settings import config

cnx = mysql.connector.connect(**config)
DB_NAME='annots' 

TABLES = {}

TABLES['annotations'] = '''CREATE TABLE IF NOT EXISTS annotations (annotid INT PRIMARY KEY, object text, speaker text, object_present text, utterance_type text)'''


code_regx = re.compile('([a-zA-Z][a-z+]*)( +)(&=)([A-Za-z]{1})(_)([A-Za-z]{1})(_)([A-Z]{1}[A-Z0-9]{2})(_)?(0x[a-z0-9]{6})?', re.IGNORECASE | re.DOTALL)

def randomID():
    def generateID():
        randID = uuid.uuid4().hex[:6]
        cursor.execute('SELECT * FROM annotations WHERE annotid={}'.format(int(randID, 16)))
        annotid = cursor.fetchall()
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
                        cursor.execute('INSERT INTO annotations VALUES (%s, %s, %s, %s, %s)', (str(int(id, 16)), annotation.word, annotation.speaker, annotation.present, annotation.utt_type))
                        cnx.commit()
                        print("adding 0x"+id)
                        #annotation.annotation_id = '0x' + id
                        line.line = line.line.replace(repr(annotation), repr(annotation) + '_0x'+id+' ', 1)

                # if there is an id for this annot, check if it is duplicated in the database??
                else:   
                    cursor.execute('SELECT * FROM annotations WHERE annotid={}'.format(int(annotation.annotation_id,16)))
                    annotid = cursor.fetchall()
                    num = len(annotid)
                    if num > 1:
                        print('FATAL ERROR: This means duplicate annotids :(')
                        print(annotid, num)
                        sys.exit()

    in_file.write_to_cha(out_file)

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)




if __name__ == "__main__":
    input = sys.argv[1]
    # Database connection established here
    cursor = cnx.cursor()
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        print("FATAL ERROR, GO FIND SARP AND TALK TO HIM. THIS IS VERY BAD. YOU CAN PANIC. YOU SHOULD PANIC.")
        print("THIS PROGRAM HAS PERFORMED AN ILLEGAL OPERATION AND THERE MIGHT BE LEGAL CONSEQUENCES FOR YOU. YOU HAVE BEEN REALLY REALL BAD. LIKE VERY BAD.")
        print("On a side note though the issue is database related.")
        exit(1)
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    # If table does not exist, create it, otherwise, continue
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name))
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            print(err.msg)



    in_file = input
    if (len(sys.argv)>2):
        out_file = sys.argv[2]
    else:
        out_file = in_file
    print(out_file)
    process_file(in_file, out_file)

    cursor.close()
    cnx.close()


    
