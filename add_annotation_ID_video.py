import argparse
import zipfile
import re
from sets import Set
import tempfile

# For now, usedIDs are loaded into a global variable (a set), then written out from there. 
usedID = ([])

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
    usedID.add('0x'+randID)
    return randID
    
   
if __name__ == "__main__":
    # Code for argparse!
    parser = argparse.ArgumentParser(description='Add annotation ids to video (opf) files')
    parser.add_argument('opf_file', help='Full path the the opf file you want to add annotids to')
    parser.add_argument('id_file', help='Full path to the usedID file that you would like to use!')
    args = parser.parse_args()

    # Setting the usedID_file variable!
    usedID_file = args.id_file

    #regex for hex. If there is hex, we skip that line. 
    code_hex = re.compile('0[xX][0-9a-fA-F]')

    #regex for timestamp (onset), so that we know there might be an annotation on this line
    code_time = re.compile("\d{2}\:\d{2}\:\d{2}\:\d{3}")


        # Try to open the opf file as a zip file
        try:
            if not args.opf_file.endswith('.opf'):
                print("Supplied file does not have an .opf extension!")
            
            # Opening the zipfile itself (not one of the member files)
            with zipfile.ZipFile(args.opf_file, "r") as zf:
                print("A zip file was supplied")

                # Making sure that the zip file contains a file called db. That appears to be a default for opf files. 
                assert "db" in zf.namelist()

                # The db file is the cha-like file which contains our annotations (and timestamps, etc.)
                with zf.open("db") as db:
                    for line in db:

                        # Line contains a time stamp! Which means an annotation! 
                        if code_time.search(line):

                            # Check to see if the line already contains an annotid! If it does, continue
                            if code_hex.search(line):
                                print("matched")
                                print(line)
                                continue 

                            # No annotid. Adding annotid to line here! 
                            else:
                                print('unmatched')
                                print(line)


        except(zipfile.BadZipfile):
            print("Bad zip file! The file does not look to be a zip file!")
            exit()
