import pyvyu
import mysql.connector
import uuid
import sys
import os.path

from settings import config

from pdb import set_trace

""" Script to add annotation IDs to opf files. The script also checks for duplicate ids,
and other issues.

"""

# This line needs to be here, otherwise gets garbage collected!
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(buffered=True)

add_cell = ("INSERT INTO annotations "
        "(annotid, object, speaker, object_present, utterance_type, file, month) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)")

# Ugly code, but for now this is how we get the file name and month.
FILE = ''
MONTH = ''

def read_opf(path):
    """ Read an opf file and return the chronologically sorted cells """
    global FILE, MONTH
    FILE = os.path.basename(path).split('_')[0]
    MONTH = os.path.basename(path).split('_')[1]
    sys.stdout.write("File: {} \t Month: {} \n".format(FILE, MONTH))
    try:
        opf_file = pyvyu.load_opf(path)
    except FileNotFoundError as e:
        sys.stderr.write('The file {} was not found. \n'.format(path))
        sys.stderr.write(str(e) + '\n')
        sys.exit()

    try:
        col = opf_file.get_column_list()[0]
        labeled_object_column = opf_file.get_column(col)

    except KeyError as e:
        sys.stderr.write('The column in the file {} is not named labeled_object (or labeled_object_DL)? \n'.format(path))
        sys.exit()


    return opf_file

def search_annotid(annotid):
    cursor.execute('SELECT * FROM annotations WHERE annotid={}'.format(int(annotid, 16)))
    return cursor.fetchall()

def add_annotid(cell):
    def generateID():
        randID = uuid.uuid4().hex[:6]
        annotid = search_annotid(randID)
        num = 0 if not annotid else len(annotid)
        return randID, num, annotid

    randID, num, annotid = generateID()

    while num > 0:
        # FATAL ERROR: This means duplicate annotannotid :(
        if num > 1:
            sys.stderr.write('FATAL ERROR: This means duplicate annotids :( \n')
            sys.stderr.write("\n".join(annotid, num) + "\n")
            sys.exit()

        # If the annotid exists (and only one exists), we spin, though this could/should be made more efficient...
        else:
            randID, num, annotid = generateID()

    data_cell = (
            int(randID, 16), 
            cell.get_code('object'),
            cell.get_code('speaker'),
            cell.get_code('object_present'),
            cell.get_code('utterance_type'),
            FILE,
            MONTH
            )

    cursor.execute(add_cell, data_cell)
    cnx.commit()
    return randID

    
def check_equal(cell1, cell2):
    return (
            int(cell1.get_code('id'), 16) == cell2[0] and
            cell1.get_code('object') == cell2[1] and
            cell1.get_code('speaker') == cell2[2] and
            cell1.get_code('object_present') == cell2[3] and
            cell1.get_code('utterance_type') == cell2[4] and
            FILE == cell2[5] and
            MONTH == cell2[6]
            )


# Very basic function to check whether two annotations with the same ID are duplicates OR just a change from reliability
def check_change(cell, row):
    return (
            FILE == row[5] and
            MONTH == row[6]
            )

    
def insert_annotation(cell):

    try:
        rows = search_annotid(cell.get_code('id'))
    except ValueError as e:
        sys.stderr.write(str(e) + '\n')
        sys.stderr.write(str(cell) + '\n')

    # if the annotid exists in the database, it has to be equal to the cell we are about to add!
    # Otherwise, this might mean we have duplicates :(((
    if rows:
        if len(rows) > 1:
            sys.stderr.write('Duplicates :(((( \n')
            sys.stderr.write('The duplicated cell and the database row are:\n{}\n{}\n'.format(cell, row))

        for row in rows:
            if check_equal(cell, row):
                break

            # We check to see whether the cell and row are from the same file with maybe a minor difference, which more than likely indicates a change made during reliability
            elif check_change(cell, row):
                break
            else:
                sys.stderr.write('Duplicates :(((( \n')
                sys.stderr.write('The duplicated cell and the database row are:\n{} from the file {}_{} and \n{}\n'.format(cell, FILE, MONTH, row))


    else:
        data_cell = (
                int(cell.get_code('id'), 16),
                cell.get_code('object'),
                cell.get_code('speaker'),
                cell.get_code('object_present'),
                cell.get_code('utterance_type'),
                FILE,
                MONTH
                )
        cursor.execute(add_cell, data_cell)
        cnx.commit()

def main(file_path):
    opf_file = read_opf(file_path)

    col = opf_file.get_column_list()[0]
    labeled_object_column = opf_file.get_column(col)
    opf_cells = labeled_object_column.sorted_cells()

    for cell in opf_cells:

        # Skip comments and %pho
        if '%com' in cell.get_code('object') or '%pho' in cell.get_code('object'):
            continue

        # If the cell does not have an annotation id, we add one. 
        if not cell.get_code('id'):
            try:
                annotid = add_annotid(cell)
            except Exception as e:
                sys.stderr.write('An exception occurred\n')
            else:
                sys.stdout.write('Adding {}\n'.format(annotid))
                cell.change_code('id', '0x' + annotid)




        # If the cell does have an annotation id, we check/insert that into the database. 
        else:
            insert_annotation(cell)

    cursor.close()
    cnx.close()
    pyvyu.save_opf(opf_file, sys.argv[1], overwrite_project=True)

if __name__ == '__main__':
    main(sys.argv[1])

