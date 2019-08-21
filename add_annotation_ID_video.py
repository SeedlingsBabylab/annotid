import argparse
import zipfile
import re
from sets import Set
import tempfile
import os
import uuid
import shutil

# For now, usedIDs are loaded into a global variable (a set), then written out from there. 
usedID = Set([])

# Same with the path to the usedID file. 
usedID_file = ''

#Load used IDs to prevent collision
def load_ID():
    with open(usedID_file) as f:
        for line in f.readlines():
            usedID.add(line.strip())


#Write IDs to usedID_file. Opening with 'w' truncates the file, so we are in effect regenerating
# the whole file each time we use it. 
def write_ID():
    with open(usedID_file, 'w') as f:
        for id in usedID:
            f.write(id)

# Method to generate random ID and check it against the usedID set (which is the set generated 
# by reading through the usedID file. Need to come up with a better way to manage these. 
def randomID():
    randID = uuid.uuid4().hex[:6]
    while '0x'+randID in usedID:
        randID = uuid.uuid4().hex[:6]
    randID = '0x' + randID
    usedID.add(randID)
    return randID
    
# Method that returns a line with annotid added! 
def add_annotid_to_line(line):
    l_list = line.split(',')
    l_list[-1] = randomID() + l_list[-1]
    return ','.join(l_list)

    
   
if __name__ == "__main__":
    # Code for argparse!
    parser = argparse.ArgumentParser(description='Add annotation ids to video (opf) files')
    parser.add_argument('opf_file', help='Full path the the opf file you want to add annotids to')
    parser.add_argument('id_file', help='Full path to the usedID file that you would like to use!')
    args = parser.parse_args()

    # Setting the usedID_file variable!
    usedID_file = args.id_file

    # Loading the used ID file for usage
    load_ID()

    #regex for hex. If there is hex, we skip that line. 
    code_hex = re.compile('0[xX][0-9a-fA-F]{6}')

    #regex for timestamp (onset), so that we know there might be an annotation on this line
    code_time = re.compile("\d{2}\:\d{2}\:\d{2}\:\d{3}")

    # Try to open the opf file as a zip file
    if not args.opf_file.endswith('.opf'):
        print("Supplied file does not have an .opf extension! Are you sure it is an opf file?")
        exit()
    
    # Making a temporary directory to extract the opf and then create it back again! 
    tempdir = tempfile.mkdtemp()
    print('listing temporary directory')
    print(os.listdir(tempdir))

    try:
        with zipfile.ZipFile(args.opf_file) as zf:
            print(zf.filename)
            zf.extractall(tempdir)
            print('listing temp directory')
            print(os.listdir(tempdir))

        with open(os.path.join(tempdir, 'tmpfile'), 'w') as tmpfile:
            with open(os.path.join(tempdir, 'db')) as dbf:
                never = True
                # Iterate through each line of db file, modify if necessary, and write it out!
                for line in dbf.readlines():
                    # there is time onset data here! which means annotation!
                    match = code_time.search(line)
                    if match:
                        annotid = code_hex.search(line)
                        # We check if there is already an annotid!
                        if not annotid:
                            never = False
                            line = add_annotid_to_line(line)
                            print('annotid was added to the line below. It looks like this:')
                            print(line)
                    tmpfile.write(line)
                if never:
                    print("No annotation IDs were added! Make sure this is what you expected!")
                    
        shutil.move(os.path.join(tempdir, 'tmpfile'), os.path.join(tempdir, 'db'))

        # Collecting everything in the temporary directory into a new opf file. 
        with zipfile.ZipFile(args.opf_file, 'w') as zf:
            for item in os.listdir(tempdir):
                zf.write(os.path.join(tempdir,item), item)

        shutil.rmtree(tempdir)
    except(zipfile.BadZipfile):
        print("Bad zip file! The file does not look to be a zip file!")
        exit()
