# Video and Audio Annotation ID (annotid) Processing Scripts
This repository contains scripts that perform the following tasks:
1. Addition of ID to each cell in the video (.opf) files
2. Additon of ID to each annotated cell in the audio (.cha) files.

Unverified tasks that previous README contained, but I (Sarp) am not fully sure of:
1. Link the Pho references of the video cells based on onset offset times
2. Addition of ID to %pho, %xcom, and annotations of the format [a-zA-Z]\_[a-zA-Z]\_[a-zA-Z]{3}
3. Addition of ID references between pho and chi, as well as detecting audio annotation file errors along the way
4. Check whether Annotation IDs are added to all words that are annotated. 

Please file issues if you encounter any bugs with as much detail as possible. 


## Current Instructions

### add_annotation_id_video.py
This script will add annotation IDs to opf files. You must have a settings.py file with configuration info 
to connect to the database. Contact the lab tech if you are missing that file. More detailed instructions
to run the script are [on gitbook](https://app.gitbook.com/@bergelsonlab/s/blab/data-pipeline/video/video-annotation-checks#1-run-add_annotation_id_video-py). 

`python add_annotation_id_video.py /path/to/opf_file.opf

### add-annotation_ID_audio.py
This script will add annotation IDs to cha files. The instructions to run this script can be
found in the gitbook, under the page "Audio Add Annotation IDs"

## Past Instructions for past scripts

All the scripts mentioned below have been moved into the old_scripts subdirectory for clean up.
These instructions are for them. 

### add_annotation_ID_video.py
This script will add annotation IDs to opf files. It creates temporary directories/files to unzip
then zip back the annotation IDs. The script takes two arguments: path to the opf file, and the
path to the used ID file. Usage:

`python add_annotation_ID_video.py /path/to/opf_file.opf /path/to/usedID.txt`

### retrieve_codes.py usage

$ python retrieve_codes.py ../scatter/path_files/cha_sparse_code_paths.txt ../scatter/video_sparse_code_paths.txt batch


### delete_space_before_code.py

Correct mistake made when using script from one_time_scripts/replace_used_id.py (additional space inserted)

### check_fixme.py

One time script -- retrieves files that have FIXME in wrong column, example of output in fixme_errors_audio.txt

### merge_bl_new_id

One time script to add annotid column to basic level

### move_no_id

One time script that moved files with no_id in name to folder named old_files
 
### undo_id

Removes all annotid from file.
