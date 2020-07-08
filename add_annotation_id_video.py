import pyvyu
import mysql.connector
import uuid

from settings import config

""" Script to add annotation IDs to opf files. The script also checks for duplicate ids,
and other issues.

"""

# This line needs to be here, otherwise gets garbage collected!
cnx = mysql.connector.connect(**config)

add_cell = ("INSERT INTO annotations "
        "(annotid, object, speaker, object_present, utterance_type) "
        "VALUES (%s, %s, %s, %s, %s)")


def read_opf(path):
    """ Read an opf file and return the chronologically sorted cells """
    opf_file = pyvyu.load_opf(path)
    labeled_object_column = opf_file.get_column('labeled_object')
    cells = labeled_object_column.sorted_cells()

    return cells


def connect_to_db():
    cursor = cnx.cursor()
    return cursor

def search_annotid(cursor, annotid):
    cursor.execute('SELECT * FROM annotations WHERE annotid={}'.format(int(annotid, 16)))
    return cursor.fetchall()

def add_annotid(cursor, cell):
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

    data_cell = (
            int(randID, 16), 
            cell.get_code('object'),
            cell.get_code('speaker'),
            cell.get_code('object_present'),
            cell.get_code('utterance_type')
            )

    cursor.execute(add_cell, data_cell)

    
    





if __name__ == '__main__':
    opf_cells = read_opf('data/test.opf')
    cursor = connect_to_db()




    
